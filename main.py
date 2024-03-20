import random
from abc import ABC, abstractmethod

zivotyHrac1 = 0
zivotyHrac2 = 0
bozskeTokenyHrac1 = 0
bozskeTokenyHrac2 = 0
bohoviaHrac1 = [None]
bohoviaHrac2 = [None]
vybraneKocky1 = [None] * 6
vybraneKocky2 = [None] * 6
hrac1IdePrvy = random.choice([True, False])

kocky = None
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

class Boh(ABC):
    def __init__(self, meno, priorita, cena1, cena2, cena3):
        self.meno = meno
        self.priorita = priorita
        self.cena1 = cena1
        self.cena2 = cena2
        self.cena3 = cena3

    def getMeno(self):
        return self.meno

    def getPriorita(self):
        return self.priorita

    def getCena(self, level):
        if level == 1:
            return self.cena1
        elif level == 2:
            return self.cena2
        else:
            return self.cena3

    @abstractmethod
    def doStuff(self, *args, **kwargs):
        pass

    @abstractmethod
    def showStuff(self):
        pass

class Thor(Boh):
    def __init__(self, meno, priorita, cena1, cena2, cena3):
        super().__init__(meno, priorita, cena1, cena2, cena3)

    def doStuff(self, zivotyOponentHrac, bozskeTokeny, levelKuzla):
        if levelKuzla == 1:
            if self.getCena(1) <= bozskeTokeny:
                zivotyOponentHrac = zivotyOponentHrac - 2
                bozskeTokeny = bozskeTokeny - 4
                return zivotyOponentHrac, bozskeTokeny

        elif levelKuzla == 2:
            if self.getCena(2) <= bozskeTokeny:
                zivotyOponentHrac = zivotyOponentHrac - 5
                bozskeTokeny = bozskeTokeny - 8
                return zivotyOponentHrac, bozskeTokeny

        else:
            if self.getCena(3) <= bozskeTokeny:
                zivotyOponentHrac = zivotyOponentHrac - 8
                bozskeTokeny = bozskeTokeny - 12
                return zivotyOponentHrac, bozskeTokeny

    def showStuff(self):
        print("1: 2 DMG, " + str(self.getCena(1)) + " tokeny, priorita " + str(self.getPriorita()))
        print("2: 5 DMG, " + str(self.getCena(2)) + " tokeny, priorita " + str(self.getPriorita()))
        print("3: 8 DMG, " + str(self.getCena(3)) + " tokeny, priorita " + str(self.getPriorita()))

class Thrymr(Boh):
    def __init__(self, meno, priorita, cena1, cena2, cena3):
        super().__init__(meno, priorita, cena1, cena2, cena3)

    def doStuff(self, bozskeTokeny, levelKuzla, levelKuzlaOponent):
        #todo sem ak invalid akcia boha oponenta atd
        if levelKuzla == 1:
            if self.getCena(1) <= bozskeTokeny:
                levelKuzlaOponent = levelKuzlaOponent - 1
                bozskeTokeny = bozskeTokeny - 3
                return levelKuzlaOponent, bozskeTokeny

        elif levelKuzla == 2:
            if self.getCena(2) <= bozskeTokeny:
                levelKuzlaOponent = levelKuzlaOponent - 2
                bozskeTokeny = bozskeTokeny - 6
                return levelKuzlaOponent, bozskeTokeny

        else:
            if self.getCena(3) <= bozskeTokeny:
                levelKuzlaOponent = levelKuzlaOponent - 3
                bozskeTokeny = bozskeTokeny - 9
                return levelKuzlaOponent, bozskeTokeny

    def showStuff(self):
        print("1: -1 level, " + str(self.getCena(1)) + " tokeny, priorita " + str(self.getPriorita()))
        print("2: -2 level, " + str(self.getCena(2)) + " tokeny, priorita " + str(self.getPriorita()))
        print("3: -3 level, " + str(self.getCena(3)) + " tokeny, priorita " + str(self.getPriorita()))

class Vidar(Boh):
    def __init__(self, meno, priorita, cena1, cena2, cena3):
        super().__init__(meno, priorita, cena1, cena2, cena3)

    def doStuff(self, helmyHP, bozskeTokeny, levelKuzla):
        if levelKuzla == 1:
            if self.getCena(1) <= bozskeTokeny:
                helmyHP = helmyHP - 2
                bozskeTokeny = bozskeTokeny - 2
                return helmyHP, bozskeTokeny

        elif levelKuzla == 2:
            if self.getCena(2) <= bozskeTokeny:
                helmyHP = helmyHP - 4
                bozskeTokeny = bozskeTokeny - 4
                return helmyHP, bozskeTokeny

        else:
            if self.getCena(3) <= bozskeTokeny:
                helmyHP = helmyHP - 6
                bozskeTokeny = bozskeTokeny - 6
                return helmyHP, bozskeTokeny

    def showStuff(self):
        print("1: -2 helmy, " + str(self.getCena(1)) + " tokeny, priorita " + str(self.getPriorita()))
        print("2: -4 helmy, " + str(self.getCena(2)) + " tokeny, priorita " + str(self.getPriorita()))
        print("3: -6 heliem, " + str(self.getCena(3)) + " tokeny, priorita " + str(self.getPriorita()))


def onStart():
    global zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, kocky

    kocky = [Kocka(1, 6, 4, 7, 5, 1), Kocka(1, 2, 7, 4, 9, 1), Kocka(1, 3, 8, 5, 6, 1), Kocka(1, 7, 8, 1, 5, 2), Kocka(1, 3, 4, 6, 9, 1), Kocka(1, 3, 2, 8, 9, 1)]
    zivotyHrac1 = 15
    zivotyHrac2 = 15
    #bozskeTokenyHrac1 = 0
    #bozskeTokenyHrac2 = 0
    #todo sem mozno netreba passovat meno lebo uz classka rozhodne ako sa vola a teda napriamo ulozit meno v classke
    bohoviaHrac1 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
    bohoviaHrac2 = [Thor("Thor", 6, 4, 8, 12), Thrymr("Thrymr", 1, 3, 6, 9), Vidar("Vidar", 4, 2, 4, 6)]
    #vybraneKocky1 = [None] * 6
    #vybraneKocky2 = [None] * 6
    #hrac1IdePrvy = random.choice([True, False])
    #return kocky
#definicia premmennych na zaciatku

def vypisHraciaPlocha():
    global vybraneKocky1, vybraneKocky2, zivotyHrac1, zivotyHrac2, bohoviaHrac1, bohoviaHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2

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
        bohovia = bohovia + boh.getMeno() + " | "

    return bohovia
#vypis typov bohov nemiesto cisel aby boli mena

def akciaBohov(akcia, boh, zivotyOponentHrac, bozskeTokeny, levelKuzlaOponent, helmyHPoponent):
    if isinstance(boh, Thor):
        zivotyOponentHrac, bozskeTokeny = boh.doStuff(zivotyOponentHrac, bozskeTokeny, akcia)
    elif isinstance(boh, Thrymr):
        levelKuzlaOponent, bozskeTokeny = boh.doStuff(bozskeTokeny, akcia, levelKuzlaOponent)
    elif isinstance(boh, Vidar):
        helmyHPoponent, bozskeTokeny = boh.doStuff(helmyHPoponent, bozskeTokeny, akcia)
    #todo sem to padlo predtym ze to vytahovalo none ked nie je dost penazi
    return zivotyOponentHrac, bozskeTokeny, levelKuzlaOponent, helmyHPoponent
#akcia bohov sa vykona a poslu sa spat upravene premenne

def vyhodnotenieBohovia(hrac1IdePrvy, bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2, zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2):
    if bohHrac1 is not None and bohHrac2 is not None:

        #mensie cislo priorita je skor
        if bohHrac1.getPriorita() < bohHrac2.getPriorita():
            zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2 = akciaBohov(bozskaAkciaHrac1, bohHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2)
            zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1 = akciaBohov(bozskaAkciaHrac2, bohHrac2, zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1)
        elif bohHrac1.getPriorita() > bohHrac2.getPriorita():
            zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1 = akciaBohov(bozskaAkciaHrac2, bohHrac2, zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1)
            zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2 = akciaBohov(bozskaAkciaHrac1, bohHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2)
        else:
            if hrac1IdePrvy:
                zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2 = akciaBohov(bozskaAkciaHrac1, bohHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2)
                zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1 = akciaBohov(bozskaAkciaHrac2, bohHrac2, zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1)
            else:
                zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1 = akciaBohov(bozskaAkciaHrac2, bohHrac2, zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1)
                zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2 = akciaBohov(bozskaAkciaHrac1, bohHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2)

        return zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2

    else:

        if bohHrac1 is not None:
            zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2 = akciaBohov(bozskaAkciaHrac1, bohHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskaAkciaHrac2, helmyHP2)
        elif bohHrac2 is not None:
            zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1 = akciaBohov(bozskaAkciaHrac2, bohHrac2, zivotyHrac1, bozskeTokenyHrac2, bozskaAkciaHrac1, helmyHP1)

    return zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2
#volanie akcii s parametrami
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

    #nech sa zobrazia na vyber iba pre volne kocky
    for i in range(6):
        if vybraneKocky[i] == None:
            temp.append(kocky[i].hodKockou())
            tempIdx.append(i)

    #ak si este moze vybrat
    while len(temp) > 0:
        #vypis moznosti
        for j in range(len(temp)):
            print("Kocka: " + str(tempIdx[j]) + " ma znak: " + str(temp[j]))

        print("Ukoncenie kola: 6")

        #vyber moznosti
        choice = int(input())
        if choice == 6:
            break
        else:
            for k in tempIdx:
                if k == choice:
                    indexVtemp = tempIdx.index(k)
                    vybraneKocky[k] = temp[indexVtemp]
                    temp.pop(indexVtemp)
                    tempIdx.remove(k)
                    break

    return vybraneKocky
#vybranie kociek ktore si chcem nechat a zahrat

def doplnOstatneKocky(kocky, vybraneKocky):
    for i in range(6):
        if vybraneKocky[i] == None:
            vybraneKocky[i] = kocky[i].hodKockou()

    return vybraneKocky
#ked uz prebehli 2 rollovania tak 3 uz nevyberam kocky ale automaticky sa daju rollnute

def vyberKociek():
    global kocky, vybraneKocky1, vybraneKocky2, hrac1IdePrvy

    for i in range(2):
        if(hrac1IdePrvy):
            print("Hrac 1 vybera kocky:")
            vyberKocky(kocky, vybraneKocky1)
            vypisHraciaPlocha()
            print("Hrac 2 vybera kocky:")
            vyberKocky(kocky, vybraneKocky2)
            vypisHraciaPlocha()
        else:
            print("Hrac 2 vybera kocky:")
            vyberKocky(kocky, vybraneKocky2)
            vypisHraciaPlocha()
            print("Hrac 1 vybera kocky:")
            vyberKocky(kocky, vybraneKocky1)
            vypisHraciaPlocha()

    doplnOstatneKocky(kocky, vybraneKocky1)
    doplnOstatneKocky(kocky, vybraneKocky2)
    vypisHraciaPlocha()
#cele vyberanie kociek

def vyberBozskuAkciu():
    global bohoviaHrac1, bohoviaHrac2, hrac1IdePrvy

    if hrac1IdePrvy:
        #vyber boha
        print("Vybera Hrac 1")

        for i in range(len(bohoviaHrac1)):
            print("Boh " + str(i) + ": " + str(bohoviaHrac1[i].getMeno()))
        print("4. Nevybrat ziadneho")

        choiceHrac1 = int(input())

        #vyber urovne kuzla
        if choiceHrac1 != 4:
            bohHrac1 = bohoviaHrac1[choiceHrac1]
            bohHrac1.showStuff()
            choiceHrac1 = int(input())
        else:
            bohHrac1 = None

        print("Vybera Hrac 2")

        for j in range(len(bohoviaHrac2)):
            print("Boh " + str(j) + ": " + str(bohoviaHrac2[j].getMeno()))
        print("4. Nevybrat ziadneho")

        choiceHrac2 = int(input())

        if choiceHrac2 != 4:
            bohHrac2 = bohoviaHrac2[choiceHrac2]
            bohHrac2.showStuff()
            choiceHrac2 = int(input())
        else:
            bohHrac2 = None

    else:
        print("Vybera Hrac 2")

        for j in range(len(bohoviaHrac2)):
            print("Boh " + str(j) + ": " + str(bohoviaHrac2[j].getMeno()))
        print("4. Nevybrat ziadneho")

        choiceHrac2 = int(input())

        if choiceHrac2 != 4:
            bohHrac2 = bohoviaHrac2[choiceHrac2]
            bohHrac2.showStuff()
            choiceHrac2 = int(input())
        else:
            bohHrac2 = None

        print("Vybera Hrac 1")

        for i in range(len(bohoviaHrac1)):
            print("Boh " + str(i) + ": " + str(bohoviaHrac1[i].getMeno()))
        print("4. Nevybrat ziadneho")

        choiceHrac1 = int(input())

        if choiceHrac1 != 4:
            bohHrac1 = bohoviaHrac1[choiceHrac1]
            bohHrac1.showStuff()
            choiceHrac1 = int(input())
        else:
            bohHrac1 = None

    return choiceHrac1, bohHrac1, choiceHrac2, bohHrac2
#ktora akcia sa ma zahrat s akym bohom

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
#vrati vsetky premenne podla kociek co bolo hodene

def vypocitajStavPodlaPremennych(bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2):
    global vybraneKocky1, vybraneKocky2, bozskeTokenyHrac1, bozskeTokenyHrac2, zivotyHrac1, zivotyHrac2, hrac1IdePrvy

    sekeraDMG1, sipDMG1, rukyDMG1, helmyHP1, stityHP1, bozskeTokeny1 = zistiStatyKociek(vybraneKocky1)
    sekeraDMG2, sipDMG2, rukyDMG2, helmyHP2, stityHP2, bozskeTokeny2 = zistiStatyKociek(vybraneKocky2)

    #bozske tokeny/ruky
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


    #po vyhodnoteni tokenov sa budu prepocitavat bozske veci
    zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2 = vyhodnotenieBohovia(hrac1IdePrvy, bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2, zivotyHrac1, zivotyHrac2, bozskeTokenyHrac1, bozskeTokenyHrac2, helmyHP1, helmyHP2)

    #helmy/sekery
    sekery1Helmy2Rozdiel = helmyHP2 - sekeraDMG1
    sekery2Helmy1Rozdiel = helmyHP1 - sekeraDMG2

    #stity/sipy
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

    return bozskeTokenyHrac1, bozskeTokenyHrac2, zivotyHrac1, zivotyHrac2
#upravi zivoty a tokeny podla vybranych kociek

def resetRound():
    global vybraneKocky1, vybraneKocky2, hrac1IdePrvy

    vybraneKocky1 = [None] * 6
    vybraneKocky2 = [None] * 6
    hrac1IdePrvy = not hrac1IdePrvy
    bohHrac1 = None
    bohHrac2 = None
    bozskaAkciaHrac1 = None
    bozskaAkciaHrac2 = None
    return bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2
#vyprazdni kocky

if __name__ == '__main__':

    onStart()

    vypisHraciaPlocha()

    stop = False
    while not stop:
        #hraci vyberu kocky
        vyberKociek()

        # hraci vyberu akciu boha
        bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2 = vyberBozskuAkciu()

        #vypocita sa stav podla vybranych kociek hracov
        vypocitajStavPodlaPremennych(bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2)

        #resetovanie kola
        bozskaAkciaHrac1, bohHrac1, bozskaAkciaHrac2, bohHrac2 = resetRound()

        vypisHraciaPlocha()

        if zivotyHrac1 < 1 or zivotyHrac2 < 1:
            stop = True

