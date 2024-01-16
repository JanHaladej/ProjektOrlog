import random

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


def onStart():
    kocky = [Kocka(1, 6, 4, 7, 5, 1), Kocka(1, 2, 7, 4, 9, 1), Kocka(1, 3, 8, 5, 6, 1), Kocka(1, 7, 8, 1, 5, 2), Kocka(1, 3, 4, 6, 9, 1), Kocka(1, 3, 2, 8, 9, 1)]
    zivotyHrac1 = 15
    zivotyHrac2 = 15
    bozskeTokenyHrac1 = 0
    bozskeTokenyHrac2 = 0
    bohoviaHrac1 = [1, 2, 3]
    bohoviaHrac2 = [1, 2, 3]
    vybraneKocky1 = [None] * 6
    vybraneKocky2 = [None] * 6
    return kocky, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, vybraneKocky1, vybraneKocky2
#definicia premmennych na zaciatku

def vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2):
    print("--------------------------------- Hrac 1 ---------------------------------")
    print(f"Zivoty: {zivotyHrac1}           Bohovia: {vypisBohovia(bohoviaHrac1)}           BozskeTokeny: {bozskeTokenyHrac1}")
    print("--------------------------------------------------------------------------")

    print(f"{vypisKociek(vybraneKocky1)}")
    print(f"{vypisKociek(vybraneKocky2)}")

    print("--------------------------------- Hrac 2 ---------------------------------")
    print(f"Zivoty: {zivotyHrac2}           Bohovia: {vypisBohovia(bohoviaHrac2)}           BozskeTokeny: {bozskeTokenyHrac2}")
    print("--------------------------------------------------------------------------")
#vypisanie hracej plochy do konzoly

def vypisBohovia(bohoviaArray):
    bohovia = "| "
    for boh in bohoviaArray:
        if boh == 1:
            bohMeno = "Thor"
        elif boh == 2:
            bohMeno = "Bragi"
        elif boh == 3:
            bohMeno = "Loki"
        elif boh == 4:
            bohMeno = "Thrymr"
        elif boh == 5:
            bohMeno = "Vidar"
        elif boh == 6:
            bohMeno = "Freyr"
        elif boh == 7:
            bohMeno = "Odin"
        elif boh == 8:
            bohMeno = "Heimdall"
        elif boh == 9:
            bohMeno = "Mimir"
        elif boh == 10:
            bohMeno = "Skuld"
        else:
            bohMeno = "Error vypisBohovia switch!"
            print("Error vypisBohovia switch!")

        bohovia = bohovia + bohMeno + " "

    bohovia = bohovia + "|"
    return bohovia
#vypis typov bohov nemiesto cisel aby boli mena

def vypisKociek(vybraneKockyArray):
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
#vypis mien co je hodene na kocke

def vyberKocky(kocky, vybraneKocky):
    temp = []
    tempIdx = []

    ##print("aktualne vybrane kocky")

    ##vypis povodnych vybranych kociek
    ##for i in range(6):
        ##print(vybraneKocky[i], end=" ")

    ##print()

    #nech sa zobrazia na vyber iba pre volne kocky
    for i in range(6):
        if vybraneKocky[i] == None:
            temp.append(kocky[i].hodKockou())
            tempIdx.append(i)

    if len(temp) > 0:
        #vypis moznosti
        print("Index znaku:", end=" ")
        for i in range(len(tempIdx)):
            print(i, end=" ")
        print()
        print("Znak na kocke:", end=" ")
        for i in range(len(temp)):
            print(str(temp[i]), end=" ")
        print()

        #nech si veberie z volnych
        moznosti = input("Vyber si kocky: ").split()
        int_list = [int(num) for num in moznosti]

        #nech sa pridaju do vybranych kociek
        for cislo in int_list:
            vybraneKocky[tempIdx[cislo]] = temp[cislo]

        ##print("aktualne vybrane kocky po vybere")

        ##vypis novo vybranych kociek
        ##for i in range(6):
            ##print(vybraneKocky[i], end=" ")

        ##print()

    return vybraneKocky
#vybranie kociek ktore si chcem nechat a zahrat

def doplnOstatneKocky(kocky, vybraneKocky):
    for i in range(6):
        if vybraneKocky[i] == None:
            vybraneKocky[i] = kocky[i].hodKockou()

    return vybraneKocky
#ked uz prebehli 2 rollovania tak 3 uz nevyberam kocky ale automaticky sa daju rollnute

def vyberKociek(kocky, vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2):
    vyberKocky(kocky, vybraneKocky1)
    #print('\n' * 100)
    vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

    vyberKocky(kocky, vybraneKocky2)
    #print('\n' * 100)
    vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

    vyberKocky(kocky, vybraneKocky1)
    #print('\n' * 100)
    vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

    vyberKocky(kocky, vybraneKocky2)
    #print('\n' * 100)
    vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

    doplnOstatneKocky(kocky, vybraneKocky1)
    doplnOstatneKocky(kocky, vybraneKocky2)
    #print('\n' * 100)
    vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)
#cele vyberanie kociek

def zistiStatyKociek(vybraneKocky):
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


def resetRound():
    vybraneKocky1 = [None] * 6
    vybraneKocky2 = [None] * 6
    return vybraneKocky1, vybraneKocky2

if __name__ == '__main__':

    kocky, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, vybraneKocky1, vybraneKocky2 = onStart()

    stop = False
    while not stop:
        vyberKociek(kocky, vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

        # todo kto ide prvy a ako to ovplyvni vybery ...
        # hrac1 vyberie boha
        # hrac2 vyberie boha

        sekeraDMG1, sipDMG1, rukyDMG1, helmyHP1, stityHP1, bozskeTokeny1 = zistiStatyKociek(vybraneKocky1)
        sekeraDMG2, sipDMG2, rukyDMG2, helmyHP2, stityHP2, bozskeTokeny2 = zistiStatyKociek(vybraneKocky2)

        bozskeTokenyHrac1 = bozskeTokenyHrac1 + bozskeTokeny1 - rukyDMG2
        bozskeTokenyHrac2 = bozskeTokenyHrac2 + bozskeTokeny2 - rukyDMG1

        sekery1Helmy2Rozdiel = helmyHP2 - sekeraDMG1
        sekery2Helmy1Rozdiel = helmyHP1 - sekeraDMG2

        sipy1Stity2Rozdiel = stityHP2 - sipDMG1
        sipy2Stity1Rozdiel = stityHP1 - sipDMG2

        if sekery1Helmy2Rozdiel < 0:
            zivotyHrac2 += sekery1Helmy2Rozdiel
        if sekery2Helmy1Rozdiel < 0:
            zivotyHrac1 += sekery2Helmy1Rozdiel

        if sipy1Stity2Rozdiel < 0:
            zivotyHrac2 += sipy1Stity2Rozdiel
        if sipy2Stity1Rozdiel < 0:
            zivotyHrac1 += sipy2Stity1Rozdiel

        vybraneKocky1, vybraneKocky2 = resetRound()

        vypisHraciaPlocha(vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2)

        if zivotyHrac1 < 1 or zivotyHrac2 < 1:
            stop = True

