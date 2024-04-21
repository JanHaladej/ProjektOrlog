import random
from abc import ABC, abstractmethod

zivotyHrac1 = 0
zivotyHrac2 = 0
bozskeTokenyHrac1 = 0
bozskeTokenyHrac2 = 0
bohoviaHrac1 = [None]
bohoviaHrac2 = [None]
nevybraneKocky1 = [None] * 6
vybraneKocky1 = [None] * 6
nevybraneKocky2 = [None] * 6
vybraneKocky2 = [None] * 6
hrac1IdePrvy = random.choice([True, False])  # hrac jedna je vzdy AI
kolo = 0
koniec = False

# staticke premenne globalne
kocky = [None]
slovnik = {
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


# interakcie s agentom ----------------------------------------
def getAkcieVyberKociek(hrac):
    global vybraneKocky1, vybraneKocky2
    # todo prepisat do metody nech to neni 2 krat to iste

    pole = [0] * 7

    # skip vyber
    pole[6] = 1

    if hrac == 1:
        for i in range(6):
            if vybraneKocky1[i] is None:
                pole[i] = 1
            else:
                pole[i] = 0
    else:
        for i in range(6):
            if vybraneKocky2[i] is None:
                pole[i] = 1
            else:
                pole[i] = 0
    return pole


def getAkcieVyberBoha():
    pole = [0] * 4
    pole[3] = 1  # todo zatial preskakujeme bohov preto 0 vsade a 1 na skip
    return pole


def getAkcieVyberBozskejAkcie():
    pole = [1] * 3
    return pole


def zistiHodnotyPreZnak(znak):
    global slovnik
    if znak is None:
        return 0, 0
    else:
        return slovnik[znak]


def setStavKockyHracov():
    global vybraneKocky1, nevybraneKocky1, vybraneKocky2, nevybraneKocky2
    # * 13 lebo nechcem prepisovat vysledky do ineho arrayu v hlavnej metode na pytanie stavu a teda posledny stlpec si dosadim veci ja
    array = [[0] * 13 for _ in range(7)]

    for col in range(6):
        if vybraneKocky1[col] is None:
            zlatyBorder, riadokPreZnak = zistiHodnotyPreZnak(nevybraneKocky1[col])
            # array[0][col] = 0 #nie je potrebne lebo nainicializovane na 0
        else:
            zlatyBorder, riadokPreZnak = zistiHodnotyPreZnak(vybraneKocky1[col])
            array[0][col] = 1

        # aby sa neukladalo 1 ked obe maju None vsade napr pri prvom stave po spusteni
        if riadokPreZnak != 0:
            array[riadokPreZnak][col] = 1
            array[6][col] = zlatyBorder

    for col in range(6):
        if vybraneKocky2[col] is None:
            zlatyBorder, riadokPreZnak = zistiHodnotyPreZnak(nevybraneKocky2[col])
        else:
            zlatyBorder, riadokPreZnak = zistiHodnotyPreZnak(vybraneKocky2[col])
            array[0][col + 6] = 1

        if riadokPreZnak != 0:
            array[riadokPreZnak][col + 6] = 1
            array[6][col + 6] = zlatyBorder

    return array


def getStavGlobalnyStav():
    global kolo, zivotyHrac1, zivotyHrac2, hrac1IdePrvy

    globalnyStav = setStavKockyHracov()
    globalnyStav[0][12] = zivotyHrac1
    globalnyStav[1][12] = zivotyHrac2
    globalnyStav[2][12] = 1 if hrac1IdePrvy else 0
    globalnyStav[3][12] = kolo

    # for row in globalnyStav:
    #     # Iterate over each element in the row
    #     for element in row:
    #         print(element, end=' ')  # Print the element followed by a space
    #     print()  # Print a newline after each row

    return globalnyStav


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
def onStart():  # definicia premmennych na zaciatku
    global zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, kocky

    kocky = [Kocka(1, 6, 4, 7, 5, 1), Kocka(1, 2, 7, 4, 9, 1), Kocka(1, 3, 8, 5, 6, 1), Kocka(1, 7, 8, 1, 5, 2), Kocka(1, 3, 4, 6, 9, 1), Kocka(1, 3, 2, 8, 9, 1)]
    zivotyHrac1 = 15
    zivotyHrac2 = 15
    # bozskeTokenyHrac1 = 0
    # bozskeTokenyHrac2 = 0
    # todo sem mozno netreba passovat meno lebo uz classka rozhodne ako sa vola a teda napriamo ulozit meno v classke
    # bohoviaHrac1 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
    # bohoviaHrac2 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
    # vybraneKocky1 = [None] * 6
    # vybraneKocky2 = [None] * 6
    # hrac1IdePrvy = random.choice([True, False])
    # return kocky


def hodKockami(hraca):  # nech sa hodia kocky a daju sa do nevybranych aby sa z nich vyberalo
    global vybraneKocky1, vybraneKocky2, nevybraneKocky1, nevybraneKocky2

    # nech sa hodia kocky co su este neni vybrane
    if hraca == 1:
        for i in range(6):
            if vybraneKocky1[i] is None:
                nevybraneKocky1[i] = kocky[i].hodKockou()
    else:
        for i in range(6):
            if vybraneKocky2[i] is None:
                nevybraneKocky2[i] = kocky[i].hodKockou()


def randomVyberKocky():
    hodKockami(2)
    for i in range(6):
        if vybraneKocky2[i] is None and random.choice([True, False]):
            vybraneKocky2[i] = kocky[i].hodKockou()


def zistiStatyKociek(vybraneKocky):  # vrati vsetky premenne podla kociek co bolo hodene
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


def vypocitajStavPodlaPremennych():  # upravi zivoty a tokeny podla vybranych kociek
    global vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, hrac1IdePrvy, bozskeTokenyHrac1, bozskeTokenyHrac2

    sekeraDMG1, sipDMG1, rukyDMG1, helmyHP1, stityHP1, bozskeTokeny1 = zistiStatyKociek(vybraneKocky1)
    sekeraDMG2, sipDMG2, rukyDMG2, helmyHP2, stityHP2, bozskeTokeny2 = zistiStatyKociek(vybraneKocky2)

    # bozske tokeny/ruky
    bozskeTokenyHrac1 = bozskeTokenyHrac1 + bozskeTokeny1
    bozskeTokenyHrac2 = bozskeTokenyHrac2 + bozskeTokeny2

    if hrac1IdePrvy:
        if bozskeTokenyHrac2 - rukyDMG1 < 0:
            bozskeTokenyHrac1 = bozskeTokenyHrac1 + rukyDMG1 + (bozskeTokenyHrac2 - rukyDMG1)
            bozskeTokenyHrac2 = 0
        else:
            bozskeTokenyHrac1 = bozskeTokenyHrac1 + rukyDMG1
            bozskeTokenyHrac2 = bozskeTokenyHrac2 - rukyDMG1

        if bozskeTokenyHrac1 - rukyDMG2 < 0:
            bozskeTokenyHrac2 = bozskeTokenyHrac2 + rukyDMG2 + (bozskeTokenyHrac1 - rukyDMG2)
            bozskeTokenyHrac1 = 0
        else:
            bozskeTokenyHrac2 = bozskeTokenyHrac2 + rukyDMG2
            bozskeTokenyHrac1 = bozskeTokenyHrac1 - rukyDMG2
    else:
        if bozskeTokenyHrac1 - rukyDMG2 < 0:
            bozskeTokenyHrac2 = bozskeTokenyHrac2 + rukyDMG2 + (bozskeTokenyHrac1 - rukyDMG2)
            bozskeTokenyHrac1 = 0
        else:
            bozskeTokenyHrac2 = bozskeTokenyHrac2 + rukyDMG2
            bozskeTokenyHrac1 = bozskeTokenyHrac1 - rukyDMG2

        if bozskeTokenyHrac2 - rukyDMG1 < 0:
            bozskeTokenyHrac1 = bozskeTokenyHrac1 + rukyDMG1 + (bozskeTokenyHrac2 - rukyDMG1)
            bozskeTokenyHrac2 = 0
        else:
            bozskeTokenyHrac1 = bozskeTokenyHrac1 + rukyDMG1
            bozskeTokenyHrac2 = bozskeTokenyHrac2 - rukyDMG1

    # po vyhodnoteni tokenov sa budu prepocitavat bozske veci
    # zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2 = vyhodnotenieBohovia(hrac1IdePrvy, bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2, zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2)

    # helmy/sekery
    sekery1Helmy2Rozdiel = helmyHP2 - sekeraDMG1
    sekery2Helmy1Rozdiel = helmyHP1 - sekeraDMG2

    # stity/sipy
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


def resetRound():
    global vybraneKocky1, vybraneKocky2, hrac1IdePrvy, kolo

    vybraneKocky1 = [None] * 6
    vybraneKocky2 = [None] * 6
    hrac1IdePrvy = not hrac1IdePrvy
    bohHrac1 = None
    bohHrac2 = None
    bozskaAkciaHrac1 = None
    bozskaAkciaHrac2 = None


def doplnOstatneKocky(kocky, vybraneKocky, nevybraneKocky):
    for i in range(6):
        if vybraneKocky[i] == None:
            vybraneKocky[i] = nevybraneKocky[i]


def step(aivstup):
    global vybraneKocky1, nevybraneKocky1, koniec, zivotyHrac1, zivotyHrac2, kolo

    if aivstup == 6:  # ak ukonci kolo vtedy sa ide dalej dovtedy opakovane vybera
        kolo += 1
        if hrac1IdePrvy:  # ak random este nesiel na rolluje a potom aj na dlasie kolo
            randomVyberKocky()
            if kolo < 3:  # toto sa vykona iba ak game stage je < ako 3 lebo potom uz nie na dlasie kolo
                randomVyberKocky()

        if kolo == 3:
            doplnOstatneKocky(kocky, vybraneKocky1, nevybraneKocky1)
            doplnOstatneKocky(kocky, vybraneKocky2, nevybraneKocky2)
            vypisHraciaPlocha()
            vypocitajStavPodlaPremennych()
            kolo = 0
            resetRound()
            if zivotyHrac1 < 1 or zivotyHrac2 < 1:
                koniec = True

    else:
        vybraneKocky1[aivstup] = nevybraneKocky1[aivstup]

    vypisHraciaPlocha()
    return getStavGlobalnyStav(), koniec


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


def vypisHraciaPlocha():
    global vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2

    print("--------------------------------- Hrac 1 ---------------------------------")
    print(f"Zivoty: {zivotyHrac1}           Bohovia: todo          BozskeTokeny: {bozskeTokenyHrac1}")
    print("--------------------------------------------------------------------------")

    print(f"{vypisKociek(vybraneKocky1)}")
    print(f"{vypisKociek(vybraneKocky2)}")

    print("--------------------------------- Hrac 2 ---------------------------------")
    print(f"Zivoty: {zivotyHrac2}           Bohovia: todo          BozskeTokeny: {bozskeTokenyHrac2}")
    print("--------------------------------------------------------------------------")


if __name__ == '__main__':

    onStart()

    # vytvorenie classy a potom set stav zaciatku hry aby sa to dalo AIcku
    if not hrac1IdePrvy:
        print("Ai nezacina prve")
        randomVyberKocky()
        vypisHraciaPlocha()

    stop = False
    while not stop:
        hodKockami(1)  # vzdy nech sa hodia kocky lebo sak ide teraz dalsi step
        var, stop = step(int(input("input: ")))
