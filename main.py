import OrlogModule

if __name__ == '__main__':

    orlog = OrlogModule.Orlog()

    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()

    while not orlog.terminal:
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(int(input("input: ")))

    print("Ended, starting new game")

    stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.onStart()

    while not orlog.terminal:
        stavKociek, stavZivotyHracov, stavKoloAKtoPrvy, maskaAkcii, terminal, reward = orlog.step(int(input("input: ")))

