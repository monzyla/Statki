import random


class Gra():
    def __init__(self):
        self.wiersze = 10
        self.kolumny = 10
        self.wymiary = 10
        self.plansza_ukryta = []
        self.plansza_do_gry = []
        self.statki = [5,4,3,2,1]


    def stworz_plansze(self, plansza):
        for i in range(self.wiersze):
            plansza.append([0]*self.kolumny)
        return plansza

    def wyswietl_plansze(self, plansza):
        print("   A B C D E F G H I J")
        for i in range(len(plansza)):
            if i+1 <10:
                print(i+1, end='  ')
            else:
                print(i+1, end=' ')

            for j in range(len(plansza[i])):
                print(plansza[i][j], end = ' ')
            print()
        print()

    def stworz_statek(self,dlugosc):

    	while not self.czy_mozna_postawic(wspolrzedne):
    		orientacja = random.choice(["pionowo", "poziomo"])
    		if orientacja == "poziomo":
    		    polozenie_wiersz = random.randint(0, self.wymiary-1)
    		    polozenie_kolumna = random.randint(0, self.wymiary-dlugosc)
    		    wspolrzedne = []
    		    for i in range(dlugosc):
    		        wspolrzedne.append([polozenie_wiersz, polozenie_kolumna+i])
    		elif orientacja == "pionowo":
    		    polozenie_wiersz = random.randint(0, self.wymiary-dlugosc)
    		    polozenie_kolumna = random.randint(0, self.wymiary-1)
    		    wspolrzedne = []
    		    for i in range(dlugosc):
    		        wspolrzedne.append((polozenie_wiersz+i, polozenie_kolumna))


    def czy_mozna_postawic(self,lista_wspolrzednych):
        for i in range(len(lista_wspolrzednych)):
            if self.plansza_ukryta[lista_wspolrzednych[i][0]][lista_wspolrzednych[i][1]] == 1:
                return False
            else:
                return True
        self.postaw_statek(lista_wspolrzednych)

    def postaw_statek(self, lista):
        for i in range(len(lista)):
            self.plansza_ukryta[lista[i][0]][lista[i][1]] = 1


    def podaj_wiersz(self):
        while True:
            print("Podaj wiersz.")
            wiersz = input()
            if wiersz.isdigit():
                if int(wiersz) > 0 and int(wiersz) < 11:
                    break
                else:
                    print("Nieprawidłowy znak. Podaj numer wiersza (1-10) jeszcze raz.")
            else:
                print("Nieprawidłowy znak. Podaj numer wiersza (1-10) jeszcze raz.")
        return int(wiersz) - 1

    def podaj_kolumne(self):
        kolumny = "ABCDEFGHIJabcdefghij"
        litery_na_cyfry = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
        while True:
            print("Podaj kolumnę.")
            kolumna_lit = input()
            if kolumna_lit.isalnum():
                if kolumna_lit in kolumny:
                    break
                else:
                    print("Nieprawidłowy znak. Podaj kolumnę (A-J) jeszcze raz.")
            else:
                print("Nieprawidłowy znak. Podaj kolumnę (A-J) jeszcze raz.")
        kolumna = litery_na_cyfry[kolumna_lit.capitalize()]
        return kolumna


moja_gra = Gra()
moja_gra.stworz_plansze(moja_gra.plansza_ukryta)
moja_gra.stworz_plansze(moja_gra.plansza_do_gry)

for statek in moja_gra.statki:
    dlugosc_statku = moja_gra.stworz_statek(statek)

moja_gra.wyswietl_plansze(moja_gra.plansza_ukryta)
