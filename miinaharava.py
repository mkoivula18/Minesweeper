#MIINAHARAVA
import math
import random
import haravasto as haravasto
import time as t
import timeit

skrr = {
	"HIIRI_VASEN" : "vasen",
	"HIIRI_OIKEA" : "oikea",
	"HIIRI_KESKI" : "keski"
}

tila = {
    "kentta": None,
    "kentta_nakyva": None,
    "SIIRROT": 0,
    "MIINAT": 0,
    "VOITTO": False,
    "HAVIO": False,
    "AIKA_ALKU": 0,
    "AIKA_LOPETUS": 0
}

kentta = []
kentta_nakyva = []

def laske_ninjat(x, y, huone):
    
    ninjat = 0
    korkeus = len(huone) - 1
    leveys = len(huone[0]) - 1
    if x == 0:
        xalku = x
        xloppu = x + 1
    elif x == leveys:
        xalku = x - 1
        xloppu = x
    else:
        xalku = x - 1
        xloppu = x + 1
    if y == 0:
        yalku = y
        yloppu = y + 1
    elif y == korkeus:
        yalku = y - 1
        yloppu = y
    else:
        yalku = y - 1
        yloppu = y + 1
            
    for x in range(xalku, xloppu + 1):    
        for y in range(yalku, yloppu + 1):
            if huone[y][x] == "x":
                ninjat += 1
    
    return ninjat

def tarkista_tyhjien_maara(talo):
    maara = 0
    for y in talo:
        for x in y:
            if x == " ":
                maara += 1
    #print("Tyhjiä jäljellä:", maara)
    if maara == tila["MIINAT"]:
        tila["VOITTO"] = True
        pelin_lopetus()
	
def kasittele_hiiri(x, y, nappi, modit):
	
    if nappi == 1:
        nappi = skrr["HIIRI_VASEN"]
    if nappi == 4:
        nappi = skrr["HIIRI_OIKEA"]
    if nappi == 2:
        nappi = skrr["HIIRI_KESKI"]
	
    ruutu_x = int(x / 40)
    ruutu_y = int(y / 40)

	
    if nappi == skrr["HIIRI_VASEN"]:
        tila["SIIRROT"] += 1
        tulvataytto(kentta, ruutu_x, ruutu_y)
        tarkista_tyhjien_maara(kentta_nakyva)
    if nappi == skrr["HIIRI_OIKEA"]:
        liputa(ruutu_x, ruutu_y)
    

def liputa(x, y):
    if kentta[y][x] == kentta_nakyva[y][x]:
        pass
    else:
        if kentta_nakyva[y][x] == "f":
            kentta_nakyva[y][x] = " "
        else:
            kentta_nakyva[y][x] = "f"


def miinoita(kentta, jaljella, miinoja):
    
    for miina in range(miinoja):
        x, y = random.choice(jaljella)
        jaljella.remove((x, y))
        kentta[y][x] = "x"     
    
def piirra_kentta():
    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, ruutu in enumerate(tila["kentta"]):
        for x, ruutunen in enumerate(ruutu):
            haravasto.lisaa_piirrettava_ruutu(ruutunen, x*40, y*40)
    
    haravasto.piirra_ruudut()
    

def tulvataytto(kentta, alkux, alkuy):
    lista = [(alkux, alkuy)]

    if kentta[alkuy][alkux] == "0":
        while lista:
            
            korkeus = len(kentta) - 1
            leveys = len(kentta[0]) - 1   
            piste = lista.pop()

            x = piste[0]
            y = piste[1]
            kentta_nakyva[piste[1]][piste[0]] = "0"
            if x == 0:
                xalku = x
                xloppu = x + 1
            elif x == leveys:
                xalku = x - 1
                xloppu = x
            else:
                xalku = x - 1
                xloppu = x + 1
            if y == 0:
                yalku = y
                yloppu = y + 1
            elif y == korkeus:
                yalku = y - 1
                yloppu = y
            else:
                yalku = y - 1
                yloppu = y + 1
                
            for x in range(xalku, xloppu + 1):    
                for y in range(yalku, yloppu + 1):
                    if kentta_nakyva[y][x] == kentta_nakyva[piste[1]][piste[0]]:
                        pass
                    
                    elif kentta_nakyva[y][x] == "f":
                        pass
                    
                    else:
                        if kentta[y][x] == "0":
                            lista.append((x, y))
                        elif kentta[y][x] == "1" or kentta[y][x] == "2" or kentta[y][x] == "3" or kentta[y][x] == "4"\
                        or kentta[y][x] == "5" or kentta[y][x] == "6" or kentta[y][x] == "7" or kentta[y][x] == "8":
                            kentta_nakyva[y][x] = kentta[y][x]


    
    elif kentta[alkuy][alkux] == "x":
        
        tila["HAVIO"] = True

        pelin_lopetus()
        
    elif kentta_nakyva[alkuy][alkux] == "f":
        return
        
    elif kentta[alkuy][alkux] != "0" or kentta[alkuy][alkux] != "x":
        kentta_nakyva[alkuy][alkux] = kentta[alkuy][alkux]
    

def pelin_lopetus():
    tila["AIKA_LOPETUS"] = timeit.default_timer()
    haravasto.lopeta() 

    if tila["VOITTO"] == True:
        print(" ")
        print("Voitto kotiin!")
        print(" ")
    elif tila["HAVIO"] == True:
        print(" ")
        print("Hävisit pelin!")
        print("Parempi onni ensikerralla.")
        print(" ")
    print("Tehtyjä siirtoja:", tila["SIIRROT"])
    
    laskettu_aika = round(tila["AIKA_LOPETUS"] - tila["AIKA_ALKU"], 1)
    
    print("Aika: {} sekuntia".format(laskettu_aika))
    
def piirra_kentta():
    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, ruutu in enumerate(kentta_nakyva):
        for x, ruutunen in enumerate(ruutu):
            haravasto.lisaa_piirrettava_ruutu(ruutunen, x*40, y*40)
    
    haravasto.piirra_ruudut()

def nollaa_peli():
    tila["SIIRROT"] = 0
    kentta.clear()
    kentta_nakyva.clear()
    tila["VOITTO"] = False
    tila["HAVIO"] = False
    
def laske_miinat(kentta, korkeus, leveys):
    for y in range(0, korkeus):
        for x in range(0, leveys):
            lkm = laske_ninjat(x, y, kentta)
            if kentta[y][x] != "x":
                kentta[y][x] = str(lkm)
 
def kysely_leveys():
    while True:
        try:
            leveys = int(input("Anna kentän leveys: "))
            if leveys > 1:
                return leveys
        except ValueError:
            print(" ")
            print("Eihän tuo ole edes luku!")
            print(" ")
        else:
            print(" ")
            print("Leveyden pitää olla vähintään 2!")
            print(" ")

def kysely_korkeus():
    while True:
            try:
                korkeus = int(input("Anna kentän korkeus: "))
                if korkeus > 1:
                    return korkeus
            except ValueError:
                print(" ")
                print("Eihän tuo ole edes luku!")
                print(" ")
            else:
                print(" ")
                print("Korkeuden pitää olla vähintään 2!")
                print(" ")
                
def kysely_miinojen_maara():
    while True:
        try:
            miinojen_maara = int(input("Kuinka monta miinaa haluat? "))
            if miinojen_maara > 0:
                return miinojen_maara
        except ValueError:
            print(" ")
            print("Eihän tuo ole edes luku!")
            print(" ")
        else:
            print("Vähän haastetta nyt..")

def luo_kentta(huone, korkeus, leveys):
    for rivi in range(korkeus):
        huone.append([])
        for sarake in range(leveys):
            huone[-1].append(" ")
    return huone
    
def main():
    nollaa_peli()

    jaljella = []
    leveys = kysely_leveys()
    korkeus = kysely_korkeus()
    miinojen_maara = kysely_miinojen_maara()
    tila["AIKA_ALKU"] = timeit.default_timer()
    tila["MIINAT"] = miinojen_maara
    
    print(" ")
    print("-------------------------------------------")

    luo_kentta(kentta, korkeus, leveys)
    luo_kentta(kentta_nakyva, korkeus, leveys)
    
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))

    tila["kentta"] = kentta

    miinoita(kentta, jaljella, miinojen_maara)
    laske_miinat(kentta, korkeus, leveys)
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(leveys*40, korkeus*40)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()
    
    
if __name__ == "__main__":    
    main()
    
