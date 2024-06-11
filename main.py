import OrlogModule
import random

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


if __name__ == '__main__':

    orlog = OrlogModule.Orlog()

    # klasickaHraUserInput(orlog)

    # randomInputy(orlog, 500)

    randomInputyAdvantagePrvy(orlog, 10000)

    #todo ukecanost
    #todo pomery prveho a ci vyhral
    #todo ake znaky boli vyberane
