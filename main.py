import numpy as np
import torch

import OrlogModule
import random

import csv
import AIpackage


def randomInputy(orlog, pocetReplikacii):
    pomer = 0

    for i in range(pocetReplikacii):
        # random inputy
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()

        while not orlog.terminal:
            for i in range(6):
                if orlog.vybraneKocky1[i] is None and random.choice([True, False]):
                    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(i)

            stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(6)

        pomer = pomer + reward  # a teda malo by byt co najblizsie nule

    print(pomer)  # rozdiel vysiel 22 a teda celkom dobre ked 10 000 replikacii


def klasickaHraUserInput(orlog):
    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()

    while not orlog.terminal:
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(int(input("input: ")))


def randomInputyAdvantagePrvy(orlog, pocetReplikacii):
    start_player_wins = 0
    start_player = None

    for _ in range(pocetReplikacii):
        # Initialize game state
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()
        start_player = stavKoloAKtoPrvy[0]  # Determine the starting player

        while not terminal:
            for i in range(6):
                if orlog.vybraneKocky1[i] is None and random.choice([True, False]):
                    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(i)

            stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(6)

        # Check if the starting player won
        if start_player == 1 and reward == 1:
            start_player_wins += 1
        elif start_player == 0 and reward == -1:
            start_player_wins += 1

    print(f"The starting player won {start_player_wins} times out of {pocetReplikacii} games.") #The starting player won 3906 times out of 10000 games.


def saveOutcomes(outcomes, cumulativeOutcomes, cumulativeReward, cumulativeRewardDividedByGames):
    row = outcomes + [""] + cumulativeOutcomes + [""] + [cumulativeReward] + [""] + [cumulativeRewardDividedByGames]

    with open('combined_outcomes.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(row)


def printer(poKolkoKolachVypis, aktualneKolo, epsilon, outcomes, cumulativeOutcomes, optionsPicked):
        print(f'-----------------------------------------------------------')
        print(f'Epsilon: ', epsilon)
        print(f'Games {aktualneKolo - (poKolkoKolachVypis - 1)} to {aktualneKolo + 1}: Wins: {outcomes[0]}, Losses: {outcomes[1]}, Ties: {outcomes[2]}')
        cumulativeReward = (cumulativeOutcomes[0] + (cumulativeOutcomes[1] * (-1)))
        cumulativeRewardDividedByGames = (cumulativeOutcomes[0] + (cumulativeOutcomes[1] * (-1))) / (aktualneKolo + 1)
        print(f'Cumulative: Wins: {cumulativeOutcomes[0]}, Losses: {cumulativeOutcomes[1]}, Ties: {cumulativeOutcomes[2]} \t cumulative reward = {cumulativeReward} \t cumulative reward / gamesPlayed = {cumulativeRewardDividedByGames} \t options picked:{optionsPicked}')
        print(f'-----------------------------------------------------------')

        saveOutcomes(outcomes, cumulativeOutcomes, cumulativeReward, cumulativeRewardDividedByGames)


def AIrun(gamesCount):
    orlog = OrlogModule.Orlog()

    bufferSize = 512 #512 pri 3000
    state_dim = (88,)  # State dimension based on state construction 2*42 + 2 + 2
    stepsStorage = AIpackage.StepsStorageManager(bufferSize, state_dim)

    neuralNetwork = AIpackage.NeuralNetwork(7, 6, 2, 2, 7)

    gamma = 0.99
    actionMaskSize = 7
    lr = 0.005  # 0.0005
    updateSteps = 16384
    batchSize = 64  # 64
    epsilon = 1
    epsilonDecrement = 0.0000005  # 0.0000005 pri 50 000 #0.00001 pri 3000
    epsilonMinimum = 0.0001   # 0.0001 pri 5000
    agent = AIpackage.AgentDQN(gamma, actionMaskSize, neuralNetwork, stepsStorage, lr, updateSteps, batchSize, epsilon, epsilonDecrement, epsilonMinimum)

    # orlog.setVypisMaskaAkcii(True)
    # orlog.setVypisHraciaPlocha(True)
    # orlog.setVypisStavovyPriestor(True)
    # orlog.setVypisCinnostiPodrobne(True)
    # orlog.setPredefinedSeed(True)
    writeOutQvalues = False #pre vypis ako sa menia

    # moje custom na vysledky
    outcomes = [0, 0, 0]  # [wins, losses, ties]
    cumulativeOutcomes = [0, 0, 0]
    optionsPicked = [0, 0] #prve kolo a potom druhe kolo kolko pickol

    for i in range(gamesCount):
        # Unpack all values returned by onStart
        state, health, roundInfo, actionMask, terminal, reward = orlog.onStart()
        state = torch.from_numpy(np.concatenate((np.array(state).flatten(), health, roundInfo))).float()

        while not terminal:
            action = agent.chooseAction(state, actionMask, writeOutQvalues)

            # Unpack all values returned by step
            nextState, health, roundInfo, actionMask, terminal, reward = orlog.step(action)
            nextState = torch.from_numpy(np.concatenate((np.array(nextState).flatten(), health, roundInfo))).float()

            agent.store(state, action, reward, nextState, terminal)

            agent.learn()

            state = nextState

            # zaznamenam kolko pickol v ktorom kole
            if action != 6:
                optionsPicked[roundInfo[1]] += 1

        if reward > 0: # == 1
            outcomes[0] += 1
        elif reward < 0: # == -1
            outcomes[1] += 1
        else:
            outcomes[2] += 1

        if (i + 1) % 100 == 0:
            for j in range(3):
                cumulativeOutcomes[j] += outcomes[j]
            printer(100, i, agent.epsilon, outcomes, cumulativeOutcomes, optionsPicked)
            outcomes = [0, 0, 0]
            optionsPicked = [0, 0]

        if i == gamesCount - 2:
            orlog.setVypisMaskaAkcii(True)
            orlog.setVypisHraciaPlocha(True)
            orlog.setVypisStavovyPriestor(True)
            orlog.setVypisCinnostiPodrobne(True)
            writeOutQvalues = True


if __name__ == '__main__':

    # orlog = OrlogModule.Orlog()
    #
    # # orlog.setVypisMaskaAkcii(True)
    # # orlog.setVypisHraciaPlocha(True)
    # # orlog.setVypisStavovyPriestor(True)
    # orlog.setVypisCinnostiPodrobne(True)
    # orlog.setPredefinedSeed(True)
    #
    # # klasickaHraUserInput(orlog)
    #
    # randomInputy(orlog, 2)
    #
    # # randomInputyAdvantagePrvy(orlog, 1)

    AIrun(50000)
