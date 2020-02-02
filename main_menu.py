#MAIN MENU

import miinaharava as m
import time as t
print(" ")
print("-------------------------------------------")
print("|   TERVETULOA    |     MIINAHARAVAAN     |")
print("-------------------------------------------")

def kelpaava_syote():
    while True:
        try:
            valittu_valikko = input("Anna seuraava valinta: ")
            if valittu_valikko == "1" or valittu_valikko == "2" or valittu_valikko == "3":
                return valittu_valikko
        except ValueError:
            print("Vastaukseksi käy ainoastaan 1, 2, tai 3")
            print("")
        else:
            print("Vastaukseksi käy ainoastaan 1, 2, tai 3")
            print("")

def main_menu():

    while True:
        print(" ")
        print("1. Play")
        print("2. High Scores")
        print("3. Exit")
        print(" ") 
        valittu_valikko = kelpaava_syote()
        if valittu_valikko == "1":
            m.main()
        
        elif valittu_valikko == "2":
            print(" ")
            print("Coming soon!")
            t.sleep(1)
        
        elif valittu_valikko == "3":
            break
        else:
            pass

def main():
    main_menu()
    
if __name__ == "__main__": 
    main()

