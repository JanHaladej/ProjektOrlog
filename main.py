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

    print(pomer)  # rozdiel vysiel 22 a teda celkom dobre


def klasickaHraUserInput(orlog):
    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()

    while not orlog.terminal:
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(int(input("input: ")))

if __name__ == '__main__':

    orlog = OrlogModule.Orlog()

    # klasickaHraUserInput(orlog)

    # randomInputy(orlog, 500)

    #todo ukecanost
    #todo pomery prveho a ci vyhral
    #todo ake znaky boli vyberane
