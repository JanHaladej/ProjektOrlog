import random


class Orlog:
    def __init__(self):
        # staticke premenne globalne
        self.kocky = [self.Kocka(1, 6, 4, 7, 5, 1), self.Kocka(1, 2, 7, 4, 9, 1), self.Kocka(1, 3, 8, 5, 6, 1), self.Kocka(1, 7, 8, 1, 5, 2), self.Kocka(1, 3, 4, 6, 9, 1), self.Kocka(1, 3, 2, 8, 9, 1)]
        self.slovnik = {
            1: (0, 1),
            2: (0, 2),
            3: (0, 3),
            4: (0, 4),
            5: (0, 5),
            6: (1, 2),
            7: (1, 3),
            8: (1, 4),
            9: (1, 5)
        }
        self.vypisMaskuAkcii = False
        self.vypisHraciuPlochu = False
        self.vypisStavovyPriestor = False
        self.vypisCinnostiPodrobne = False
        self.seedForRandomGenerators = False

    # interakcie s agentom ----------------------------------------
    def getAkcieVyberKociek(self, hrac):
        pole = [0] * 7

        # skip vyber
        pole[6] = 1

        if hrac == 1:
            for i in range(6):
                if self.vybraneKocky1[i] is None:
                    pole[i] = 1
                else:
                    pole[i] = 0
        else:
            for i in range(6):
                if self.vybraneKocky2[i] is None:
                    pole[i] = 1
                else:
                    pole[i] = 0

        if self.vypisMaskuAkcii:
            print("Maska akcii:")
            for j in range(7):
                print(pole[j], end=" ")
            print()

        return pole

    def zistiHodnotyPreZnak(self, znak):
        if znak is None:
            return 0, 0
        else:
            return self.slovnik[znak]

    def getStavKockyHracov(self, vypisStavDoKonzoly):
        # x y z pre indexovanie potom
        array = [[[0 for _ in range(2)] for _ in range(6)] for _ in range(7)]  # inicializovane pre cely stavovy priestor

        for col in range(6):
            if self.vybraneKocky1[col] is None:
                zlatyBorder, riadokPreZnak = self.zistiHodnotyPreZnak(self.nevybraneKocky1[col])
                # array[0][col] = 0 #nie je potrebne lebo nainicializovane na 0
            else:
                zlatyBorder, riadokPreZnak = self.zistiHodnotyPreZnak(self.vybraneKocky1[col])
                array[0][col][0] = 1

            # aby sa neukladalo 1 ked obe maju None vsade napr pri prvom stave po spusteni
            if riadokPreZnak != 0:
                array[riadokPreZnak][col][0] = 1
                array[6][col][0] = zlatyBorder

        for col in range(6):
            if self.vybraneKocky2[col] is None:
                zlatyBorder, riadokPreZnak = self.zistiHodnotyPreZnak(self.nevybraneKocky2[col])
            else:
                zlatyBorder, riadokPreZnak = self.zistiHodnotyPreZnak(self.vybraneKocky2[col])
                array[0][col][1] = 1

            if riadokPreZnak != 0:
                array[riadokPreZnak][col][1] = 1
                array[6][col][1] = zlatyBorder

        if self.vypisStavovyPriestor and vypisStavDoKonzoly:
            for k in range(2):
                print(f"Layer z = {k}, ({'AI' if k == 0 else 'Random'})")
                for i in range(7):
                    for j in range(6):
                        print(array[i][j][k], end=" ")
                    print()
                print()
            # self.saveMatrixToFile(array, "output.txt") #todo toto asi prec ne ? :D


        return array

    def saveMatrixToFile(self, matrix, filename):
        # Open the file in write mode
        with open(filename, 'a') as file:
            # Iterate over each layer
            for k in range(2):
                # Iterate over each column (skip the first row)
                for col in range(6):
                    # Create a string for each column, skipping the first row (i.e., row 0)
                    col_string = ''.join(str(matrix[row][col][k]) for row in range(1, 7))
                    # Write the column string to the file followed by a semicolon
                    file.write(col_string + ';')
                # Add a newline after each layer (optional)
                # file.write('\n')

    def getStavZivotyHracov(self):
        pole = [0] * 2

        pole[0] = self.zivotyHrac1
        pole[1] = self.zivotyHrac2

        return pole

    def getKoloAKtoPrvy(self):
        pole = [0] * 2

        pole[0] = 1 if self.hrac1IdePrvy else 0
        pole[1] = self.kolo

        return pole

    # classky ---------------------------------------------------
    class Kocka:
        znaky = [None] * 6

        def __init__(self, znak1, znak2, znak3, znak4, znak5, znak6):
            self.znaky[0] = znak1
            self.znaky[1] = znak2
            self.znaky[2] = znak3
            self.znaky[3] = znak4
            self.znaky[4] = znak5
            self.znaky[5] = znak6

        def hodKockou(self):
            return self.znaky[random.randint(0, 5)]

    # metody pre fungovanie programu --------------------------------------------
    def onStart(self):  # definicia premmennych na zaciatku
        self.generalVypis("Zacina sa nova hra ---------------------------------")
        if self.seedForRandomGenerators:
            random.seed(42)

        self.zivotyHrac1 = 15
        self.zivotyHrac2 = 15
        self.bozskeTokenyHrac1 = 0
        self.bozskeTokenyHrac2 = 0
        self.bohoviaHrac1 = [None]
        self.bohoviaHrac2 = [None]
        self.nevybraneKocky1 = [None] * 6
        self.vybraneKocky1 = [None] * 6
        self.nevybraneKocky2 = [None] * 6
        self.vybraneKocky2 = [None] * 6
        self.hrac1IdePrvy = random.choice([True, False])  # hrac jedna je vzdy AI
        self.kolo = 0
        self.terminal = False
        self.reward = 0

        # nastavenie prveho stavu
        if not self.hrac1IdePrvy:
            self.generalVypis("Random zacina prvy")
            self.hodKockami(2)
            self.randomVyberKocky()
            # treba hodit aby aj AI vedelo z coho mam hadzat
            self.hodKockami(1)
        else:
            self.generalVypis("Ai zacina prve")
            self.hodKockami(1)

        self.vypisy()
        # bohoviaHrac1 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
        # bohoviaHrac2 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
        return self.getStavKockyHracov(False), self.getStavZivotyHracov(), self.getKoloAKtoPrvy(), self.getAkcieVyberKociek(1), self.terminal, self.reward

    def hodKockami(self, hraca):  # nech sa hodia kocky a daju sa do nevybranych aby sa z nich vyberalo
        # nech sa hodia kocky co su este neni vybrane
        if hraca == 1:
            for i in range(6):
                if self.vybraneKocky1[i] is None:
                    self.nevybraneKocky1[i] = self.kocky[i].hodKockou()
        else:
            for i in range(6):
                if self.vybraneKocky2[i] is None:
                    self.nevybraneKocky2[i] = self.kocky[i].hodKockou()

    def randomVyberKocky(self):
        self.generalVypis("Random vyber kociek")
        for i in range(6):
            if self.vybraneKocky2[i] is None and random.choice([True, False]):
                self.generalVypis("vybral si kocku na indexe: " + str(i))
                self.vybraneKocky2[i] = self.nevybraneKocky2[i]
        self.generalVypis("Random ukoncuje vyber kociek")

    def zistiStatyKociek(self, vybraneKocky):  # vrati vsetky premenne podla kociek co bolo hodene
        sekeraDMG = 0
        sipDMG = 0
        rukyDMG = 0
        helmyHP = 0
        stityHP = 0
        bozskeTokeny = 0

        for znak in vybraneKocky:
            if znak == 1:
                sekeraDMG += 1
            elif znak == 2:
                sipDMG += 1
            elif znak == 3:
                rukyDMG += 1
            elif znak == 4:
                helmyHP += 1
            elif znak == 5:
                stityHP += 1
            elif znak == 6:
                sipDMG += 1
                bozskeTokeny += 1
            elif znak == 7:
                rukyDMG += 1
                bozskeTokeny += 1
            elif znak == 8:
                helmyHP += 1
                bozskeTokeny += 1
            else:  # znak == 9
                stityHP += 1
                bozskeTokeny += 1
        return sekeraDMG, sipDMG, rukyDMG, helmyHP, stityHP, bozskeTokeny

    def vypocitajStavPodlaPremennych(self):
        sekeraDMG1, sipDMG1, rukyDMG1, helmyHP1, stityHP1, bozskeTokeny1 = self.zistiStatyKociek(self.vybraneKocky1)
        sekeraDMG2, sipDMG2, rukyDMG2, helmyHP2, stityHP2, bozskeTokeny2 = self.zistiStatyKociek(self.vybraneKocky2)

        # bozske tokeny/ruky
        self.bozskeTokenyHrac1 += bozskeTokeny1
        self.bozskeTokenyHrac2 += bozskeTokeny2

        if self.hrac1IdePrvy:
            if self.bozskeTokenyHrac2 - rukyDMG1 < 0:
                self.bozskeTokenyHrac1 += rukyDMG1 + (self.bozskeTokenyHrac2 - rukyDMG1)
                self.bozskeTokenyHrac2 = 0
            else:
                self.bozskeTokenyHrac1 += rukyDMG1
                self.bozskeTokenyHrac2 -= rukyDMG1

            if self.bozskeTokenyHrac1 - rukyDMG2 < 0:
                self.bozskeTokenyHrac2 += rukyDMG2 + (self.bozskeTokenyHrac1 - rukyDMG2)
                self.bozskeTokenyHrac1 = 0
            else:
                self.bozskeTokenyHrac2 += rukyDMG2
                self.bozskeTokenyHrac1 -= rukyDMG2
        else:
            if self.bozskeTokenyHrac1 - rukyDMG2 < 0:
                self.bozskeTokenyHrac2 += rukyDMG2 + (self.bozskeTokenyHrac1 - rukyDMG2)
                self.bozskeTokenyHrac1 = 0
            else:
                self.bozskeTokenyHrac2 += rukyDMG2
                self.bozskeTokenyHrac1 -= rukyDMG2

            if self.bozskeTokenyHrac2 - rukyDMG1 < 0:
                self.bozskeTokenyHrac1 += rukyDMG1 + (self.bozskeTokenyHrac2 - rukyDMG1)
                self.bozskeTokenyHrac2 = 0
            else:
                self.bozskeTokenyHrac1 += rukyDMG1
                self.bozskeTokenyHrac2 -= rukyDMG1

        # po vyhodnoteni tokenov sa budu prepocitavat bozske veci
        # zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2 = vyhodnotenieBohovia(hrac1IdePrvy, bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2, zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2)

        # helmy/sekery
        sekery1Helmy2Rozdiel = helmyHP2 - sekeraDMG1
        sekery2Helmy1Rozdiel = helmyHP1 - sekeraDMG2

        # stity/sipy
        sipy1Stity2Rozdiel = stityHP2 - sipDMG1
        sipy2Stity1Rozdiel = stityHP1 - sipDMG2

        if sekery1Helmy2Rozdiel < 0:
            self.zivotyHrac2 += sekery1Helmy2Rozdiel
        if sekery2Helmy1Rozdiel < 0:
            self.zivotyHrac1 += sekery2Helmy1Rozdiel

        if sipy1Stity2Rozdiel < 0:
            self.zivotyHrac2 += sipy1Stity2Rozdiel
        if sipy2Stity1Rozdiel < 0:
            self.zivotyHrac1 += sipy2Stity1Rozdiel

    def resetRound(self):
        self.generalVypis("Resetuje sa kolo")
        self.vybraneKocky1 = [None] * 6
        self.vybraneKocky2 = [None] * 6
        self.hrac1IdePrvy = not self.hrac1IdePrvy
        self.bohHrac1 = None
        self.bohHrac2 = None
        self.bozskaAkciaHrac1 = None
        self.bozskaAkciaHrac2 = None

        if not self.hrac1IdePrvy:
            self.generalVypis("Random ide prvy toto kolo")
            self.hodKockami(2)
            self.randomVyberKocky()
            # treba hodit aby aj AI vedelo z coho mam hadzat
            self.hodKockami(1)
        else:
            self.generalVypis("Ai ide prve toto kolo")
            self.hodKockami(1)  # podla toho kto zacina sa hodia kocky

        self.vypisy()

    def doplnOstatneKocky(self, vybraneKocky, nevybraneKocky):
        for i in range(6):
            if vybraneKocky[i] == None:
                vybraneKocky[i] = nevybraneKocky[i]

    def step(self, aivstup):

        if aivstup == 6:  # ak ukonci kolo vtedy sa ide dalej dovtedy opakovane vybera
            self.generalVypis("AI ukoncuje svoje kolo")
            self.kolo += 1

            # hadzanie random hodu ak ma hadzat, cize AI nejde za sebou
            if self.hrac1IdePrvy:  # ak random este nesiel a rolluje a potom aj na dlasie kolo
                self.generalVypis("Random hadze kockami a vybera si znaky")
                self.hodKockami(2)
                self.randomVyberKocky()
                if self.kolo < 2:  # toto sa vykona iba ak game stage je < ako 3 lebo potom uz nie na dlasie kolo
                    self.generalVypis("Random hadze kockami a vybera si znaky")
                    self.hodKockami(2)
                    self.randomVyberKocky()

            # hodenie pre Ai na dalsie kolo
            self.hodKockami(1)

            # ukoncenie velkeho kola a vyhodnotenie
            if self.kolo == 2:
                self.doplnOstatneKocky(self.vybraneKocky1, self.nevybraneKocky1)
                self.doplnOstatneKocky(self.vybraneKocky2, self.nevybraneKocky2)
                self.vypisy()
                self.generalVypis("Ukoncuje sa velke kolo, doplnuju sa ostatne kocky, vyhodnocuju sa znaky ----------------------------")
                self.vypocitajStavPodlaPremennych()
                self.kolo = 0
                self.vypisy()#treba pored resetom elbo tam uz moze hadzat Random
                self.resetRound()
                if self.zivotyHrac1 < 1 or self.zivotyHrac2 < 1:
                    self.terminal = True
                    self.generalVypis("Hra skoncila --------------------------------")
                    if self.zivotyHrac1 > 0 or self.zivotyHrac2 > 0:
                        if self.zivotyHrac1 > 0:
                            self.reward = 1
                            # self.reward = self.zivotyHrac1 / 15
                            self.generalVypis("AI vyhralo")
                        else:
                            self.reward = -1
                            # self.reward = -1 * self.zivotyHrac2 / 15
                            self.generalVypis("Random vyhral")
                    else:
                        self.reward = 0  # obaja prehrali lebo maju pod 0
                        self.generalVypis("Obaja prehrali")

                    self.generalVypis("Zivoty Hrac1 - AI: " + str(self.zivotyHrac1) + " Zivoty hrac2: " + str(self.zivotyHrac2))
                    self.generalVypis("Reward je teda: " + str(self.reward))

        else:
            self.generalVypis("AI si vybralo kocku: " + str(aivstup))
            self.vybraneKocky1[aivstup] = self.nevybraneKocky1[aivstup]

        self.vypisy()
        return self.getStavKockyHracov(False), self.getStavZivotyHracov(), self.getKoloAKtoPrvy(), self.getAkcieVyberKociek(1), self.terminal, self.reward

    def vypisKociek(self, vybraneKockyArray):
        kocky = "|"

        for kocka in vybraneKockyArray:
            if kocka == 1:
                kocky += "Sekera     |"
            elif kocka == 2:
                kocky += "Sip        |"
            elif kocka == 3:
                kocky += "Ruka       |"
            elif kocka == 4:
                kocky += "Helma      |"
            elif kocka == 5:
                kocky += "Stit       |"
            elif kocka == 6:
                kocky += "Zlaty Sip  |"
            elif kocka == 7:
                kocky += "Zlata Ruka |"
            elif kocka == 8:
                kocky += "Zlata helma|"
            elif kocka == 9:
                kocky += "Zlaty Stit |"
            else:
                kocky += "           |"

        return kocky

    def vypisNevybranychKociek(self, nevybraneKockyArray):
        kocky = "|"

        for kocka in nevybraneKockyArray:
            if kocka == 1:
                kocky += "Sekera     |"
            elif kocka == 2:
                kocky += "Sip        |"
            elif kocka == 3:
                kocky += "Ruka       |"
            elif kocka == 4:
                kocky += "Helma      |"
            elif kocka == 5:
                kocky += "Stit       |"
            elif kocka == 6:
                kocky += "Zlaty Sip  |"
            elif kocka == 7:
                kocky += "Zlata Ruka |"
            elif kocka == 8:
                kocky += "Zlata helma|"
            elif kocka == 9:
                kocky += "Zlaty Stit |"
            else:
                kocky += "           |"

        return kocky

    def vypisHraciaPlocha(self):
        print("--------------------------------- Hrac 1 ---------------------------------")
        print(f"Zivoty: {self.zivotyHrac1}           Bohovia: todo          BozskeTokeny: {self.bozskeTokenyHrac1}")
        print("--------------------------------------------------------------------------")

        print(f"{self.vypisKociek(self.vybraneKocky1)}")
        print(f"{self.vypisKociek(self.vybraneKocky2)}")

        print("--------------------------------- Hrac 2 ---------------------------------")
        print(f"Zivoty: {self.zivotyHrac2}           Bohovia: todo          BozskeTokeny: {self.bozskeTokenyHrac2}")
        print("--------------------------------------------------------------------------")

    def generalVypis(self, text):
        if self.vypisCinnostiPodrobne:
            print(text, end=" ")
            print()

    def vypisy(self):

        if self.vypisHraciuPlochu:
            self.vypisHraciaPlocha()

        if self.vypisStavovyPriestor:
            self.getStavKockyHracov(True)
            print(f"Vypis nevybranych kociek AI: {self.vypisNevybranychKociek(self.nevybraneKocky1)}")

    def setVypisMaskaAkcii(self, bool):
        self.vypisMaskuAkcii = bool

    def setVypisHraciaPlocha(self, bool):
        self.vypisHraciuPlochu = bool

    def setVypisStavovyPriestor(self, bool):
        self.vypisStavovyPriestor = bool

    def setVypisCinnostiPodrobne(self, bool):
        self.vypisCinnostiPodrobne = bool

    def setPredefinedSeed(self, bool):
        self.seedForRandomGenerators = bool