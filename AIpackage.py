import numpy as np  # For numerical operations
import torch  # For tensor operations
import copy  # To copy objects
import torch.optim as optim  # For optimization
import torch.nn as nn  # For neural network layers
import torch.nn.functional as F  # For neural network functions

# -----------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------

class StepsStorageManager():
    def __init__(self, bufferSize, stateDimensions):
        self.index = 0
        self.bufferSize = bufferSize
        self.stateDimensions = stateDimensions
        dim = (bufferSize,) + stateDimensions

        self.states = torch.zeros(dim)  # Store states
        self.actions = torch.zeros((self.bufferSize,), dtype=torch.int8)  # Store actions
        self.rewards = torch.zeros(self.bufferSize)  # Store rewards
        self.nextStates = torch.zeros(dim)  # Store next states
        self.terminals = torch.zeros(self.bufferSize)  # Store terminal states (true or false)
        self.bufferWasFilled = False

    def store(self, state, action, reward, nextState, terminal):
        if self.index == self.bufferSize:
            self.index = 0  # Ensure it overwrites the oldest experience when full
            if not self.bufferWasFilled:
                self.bufferWasFilled = True
                print("Buffer was filled ----------------------------------------------------")
        # prepisuje ulozene kroky od najstarsich
        # prilis maly buffer = malo variablity
        # prilis velky buffer = bude obsahovat zastarale steps
        self.states[self.index] = state
        self.actions[self.index] = action
        self.rewards[self.index] = reward
        self.nextStates[self.index] = nextState
        self.terminals[self.index] = int(terminal)  # Convert terminal flag to integer
        self.index += 1

    def sample(self, batchSize):
        if self.bufferWasFilled:  # Ensure we don't sample unfilled parts of the buffer
            length = self.bufferSize
        else:
            length = self.index

        batchIndices = np.random.choice(length, batchSize, replace=False)  # Randomly sample steps

        states = self.states[batchIndices]
        actions = self.actions[batchIndices]
        rewards = self.rewards[batchIndices]
        nextStates = self.nextStates[batchIndices]
        terminals = self.terminals[batchIndices]
        return states, actions, rewards, nextStates, terminals


# -----------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------

class AgentDQN:
    def __init__(self, gamma, actions_count, model, stepsStorageManager, lr, updateSteps, batchSize, epsilon,
                 epsilonDecrement, epsilonMinimum):

        self.gamma = gamma
        self.actions_count = actions_count
        self.onlineModel = model
        self.targetModel = copy.deepcopy(model)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print('Using device: ', self.device)
        self.onlineModel.to(self.device)
        self.targetModel.to(self.device)

        for param in self.targetModel.parameters():
            param.requires_grad = False
        self.mse = nn.MSELoss()
        self.stepsStorageManager = stepsStorageManager
        self.optimizer = optim.Adam(self.onlineModel.parameters(), lr=lr)
        self.updateSteps = updateSteps
        self.current_steps = 0
        self.batchSize = batchSize
        self.epsilon = epsilon
        self.epsilonMinimum = epsilonMinimum
        self.epsilonDecrement = epsilonDecrement

    def chooseAction(self, state, actionMask, writeOutQvalues):
        r = np.random.random()

        if r < self.epsilon:
            # return random choice
            availableActions = np.where(np.array(actionMask) == 1)[0]
            action = np.random.choice(availableActions)
            return action
        else:
            # #skusim ukoncovat kolo
            # r = np.random.random()
            # if r < 0.3 and sum(actionMask) != 7:
            #     return 6
            # else:
                # return best q value choice
                state = state.unsqueeze(0).to(self.device).float()
                with torch.no_grad():
                    actions = self.onlineModel(state)

                # Convert actionMask to a tensor and find valid actions
                actionMaskTensor = torch.tensor(actionMask, dtype=torch.bool, device=self.device)
                availableActions = torch.where(actionMaskTensor)[0]  # Indices of valid actions

                # Select the valid action with the highest Q-value
                validActionsQValues = actions[0, availableActions]  # Q-values of valid actions

                if writeOutQvalues: #pridane aby sa vypisovali q hodnoty
                    print("Q-values of valid actions:", validActionsQValues.cpu().numpy())

                bestValidActionIdx = torch.argmax(validActionsQValues).item()  # Index of the best valid action in availableActions
                action = availableActions[bestValidActionIdx].item()  # Map back to original action space

                return action

    def store(self, state, action, reward, state_, terminal):
        self.stepsStorageManager.store(state, action, reward, state_, terminal)

    def learn(self):
        if not self.stepsStorageManager.bufferWasFilled:
            return

        self.optimizer.zero_grad()
        states, actions, rewards, nextStates, terminals = self.stepsStorageManager.sample(self.batchSize)

        computeCurrentQvalues = self.onlineModel(states.to(self.device))
        computeNextStateQvaluesTarget = computeCurrentQvalues.detach().cpu()
        computeNextStateQvalues = self.targetModel(nextStates.to(self.device)).cpu()

        for i in range(0, len(states)):
            computeNextStateQvaluesTarget[i, actions[i]] = rewards[i] + self.gamma * torch.max(
                computeNextStateQvalues[i]) * (1 - terminals[i])

        MeanSquaredErrorLoss = self.mse(computeCurrentQvalues, computeNextStateQvaluesTarget.to(self.device))
        MeanSquaredErrorLoss.backward()
        self.optimizer.step()

        self.current_steps += 1
        if self.current_steps == self.updateSteps:
            print("Updating model")
            self.targetModel.load_state_dict(self.onlineModel.state_dict())
            self.current_steps = 0

        if self.epsilon > self.epsilonMinimum:
            self.epsilon = max(self.epsilon - self.epsilonDecrement, self.epsilonMinimum)


# -----------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------

class NeuralNetwork(nn.Module):
    def __init__(self, tableStatesHeight, tableStatesWidth, bothPlayerLivesStateSize, playerOrderAndRoundStates,
                 actionMaskSize):  # 7,6,2,2,7
        super(NeuralNetwork, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=2, out_channels=16, kernel_size=3, stride=1,
                               padding=1)  # 2 channels for player 1 and player 2 table states
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)

        self.fc1 = nn.Linear(
            in_features=64 * tableStatesHeight * tableStatesWidth + bothPlayerLivesStateSize + playerOrderAndRoundStates,
            out_features=128)  # output of conv3 is transformed from 2*7*6 to 64*7*6 - table states
        self.fc2 = nn.Linear(in_features=128, out_features=64)
        self.fc3 = nn.Linear(in_features=64, out_features=actionMaskSize)

        self.flatten = nn.Flatten()  # change to 1D vector

    # def encode_state(self, tables, lives, shared_state): #todo maybe remove
    #     return np.concatenate((tables.flatten(), lives.flatten(), shared_state.flatten()))

    def decode_state(self, state):
        return state[:84].reshape((1, 2, 7, 6)), state[84:86].reshape((1, 2)), state[86:88].reshape((1,
                                                                                                     2))  # batch 1, 2 channels - layer z, 7 height, 6 width, # array 2 player lives, #array 2 miniround values

    def forward(self, states):
        decodedStates = [self.decode_state(state) for state in states]

        tableTensors = torch.cat([state[0] for state in decodedStates], dim=0)
        livesTensors = torch.cat([state[1] for state in decodedStates], dim=0)
        playerOrderAndRoundTensors = torch.cat([state[2] for state in decodedStates], dim=0)

        x = F.relu(self.conv1(tableTensors))  # table state sent through convolutionl layers
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.flatten(x)  # flattened to 1d vector

        x = torch.cat((x, livesTensors, playerOrderAndRoundTensors), dim=1)  # adds player lives and round state info

        x = F.relu(self.fc1(x))  # passing through fully connected layers
        x = F.relu(self.fc2(x))
        x = self.fc3(x)  # returned Q-values for action mask

        return x