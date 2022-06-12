import random
import time
import os
import termcolor


class Gra():
    def __init__(self):
        self.wiersze = 10
        self.kolumny = 10
        self.wymiary = 10
        self.plansza_ukryta_komputer = []
        self.stworz_plansze_dwa(self.plansza_ukryta_komputer)
        self.plansza_zgadywanie_uzytkownik = []
        self.stworz_plansze(self.plansza_zgadywanie_uzytkownik)
        self.plansza_ukryta_uzytkownik = []
        self.stworz_plansze(self.plansza_ukryta_uzytkownik)
        self.plansza_zgadywanie_komputer = []
        self.stworz_plansze_dwa(self.plansza_zgadywanie_komputer)
        self.statki = [5,4,4,3,3,3,2,2,2,2,1,1,1,1,1]
        self.wykorzystane_komputer = [] 
        self.wykorzystane_uzytkownik = []
        self.cele = []
        self.statki_komputer = [] 
        self.statki_uzytkownik = []

    def stworz_plansze(self, plansza):
        for i in range(self.wiersze):
            plansza.append([termcolor.colored("0", "blue")]*self.kolumny)
        return plansza
                         
    def stworz_plansze_dwa(self, plansza):
        for i in range(self.wiersze):
            plansza.append([termcolor.colored("0", "cyan")]*self.kolumny)
        return plansza

    def wyswietl_plansze(self, plansza):
        print("   A B C D E F G H I J")
        for i in range(len(plansza)):
            if i < 9:
                print(i+1, end='  ')
            else:
                print(i+1, end=' ')

            for j in range(len(plansza[i])):
                print(plansza[i][j], end = ' ')
            print()
        print()

    def rozloz_statki_dla_komputera(self):
        """Dla każdej długości statku podanego na liście wywołuje funkcje
        naloz_na_plansze_losowo"""
        jakie_statki = self.statki
        plansza = self.plansza_ukryta_komputer
        for statek in jakie_statki:
            self.naloz_na_plansze_losowo(statek, plansza)

    def naloz_na_plansze_losowo(self,statek,plansza):
        """Dopóki nie da się położyć statku, losuje orientację statku
        i pozycję jego lewego górnego rogu"""
        da_sie_polozyc = False
        orientacja = None
        wiersz = None
        kolumna = None
        tablica = self.statki_komputer

        while da_sie_polozyc == False:
            orientacja = random.choice(["0","1"])
            wiersz = random.randint(0,len(plansza))
            kolumna = random.randint(0,len(plansza[0]))
            da_sie_polozyc = self.sprawdz(plansza,wiersz,kolumna,orientacja,statek)

        self.poloz_statek(plansza,tablica,wiersz,kolumna,orientacja,statek)


    def generuj(self,wiersz,kolumna,orientacja,dlugosc):
        """Na podstawie orientacji statku i współrzędnych jego lewego górnego rogu
        generuje listę wszystkich współrzędnych statku o przekazanej długości"""
        wspolrzedne = []
        if orientacja == "1":
            for i in range(dlugosc):
                wspolrzedne.append((wiersz, kolumna+i))
        else:
            for i in range(dlugosc):
                wspolrzedne.append((wiersz+i, kolumna))
        return wspolrzedne

    def wystaje(self,plansza,wiersz,kolumna):
        """Zwraca True, jeśli (wiersz,kolumna) jest poza planszą"""
        return wiersz<0 or kolumna<0 or wiersz>= len(plansza) or kolumna>=len(plansza[0])

    def zly_sasiad(self,plansza,wiersz,kolumna):
        """Zwraca True, jeśli pole nie nadaje się nie sąsiada statku"""
        if not self.wystaje(plansza,wiersz,kolumna):
            return plansza[wiersz][kolumna] == 1
        else:
            return False

    def sprawdz(self,plansza,wiersz,kolumna,orientacja,statek):
        """Zwraca True, kiedy żadna ze współrzędnych statku nie znajduje się
        poza planszą oraz kiedy sąsiadem nie jest pole zajęte przez inny statek"""
        wspolrzedne_statku = self.generuj(wiersz,kolumna,orientacja,statek)
        for wiersz_s, kolumna_s in wspolrzedne_statku:
            if self.wystaje(plansza, wiersz_s, kolumna_s):
                return False
            else:
                if plansza[wiersz_s][kolumna_s]==1:
                    return False
                if self.zly_sasiad(plansza, wiersz_s+1,kolumna_s):
                    return False
                if self.zly_sasiad(plansza, wiersz_s-1,kolumna_s):
                    return False
                if self.zly_sasiad(plansza, wiersz_s,kolumna_s+1):
                    return False
                if self.zly_sasiad(plansza, wiersz_s,kolumna_s-1):
                    return False
        return True

    def poloz_statek(self,plansza,tablica,wiersz,kolumna,orientacja,dlugosc):
        """Kładzie statek"""
        gdzie = self.generuj(wiersz,kolumna,orientacja,dlugosc)
        for wiersz,kolumna in gdzie:
            plansza[wiersz][kolumna] = 1
            tablica.append((wiersz,kolumna))

    def poloz_uzytkownik(self):
                            
        for statek in self.statki:
            while True:
                print(f"Czas położyć statek {statek}-masztowy")
                while True:
                    if statek == 1:
                        print("Proszę podaj współrzędne statku.")
                        break
                    else:
                        print("Proszę wpisz orientację: 0 [pionowo], 1 [poziomo]")
                        orientacja = input()
                        if orientacja == "0" or orientacja == "1":
                            if orientacja == "0":
                                print("Proszę podaj współrzędne górnej części statku.")
                            elif orientacja == "1":
                                print("Proszę podaj współrzędne lewego brzegu statku.")
                            break
                wiersz = self.podaj_wiersz()
                kolumna = self.podaj_kolumne()
                plansza = self.plansza_ukryta_uzytkownik
                czy_mozna_postawic = self.sprawdz(plansza,wiersz,kolumna,orientacja,statek)
                if not czy_mozna_postawic:
                    print("Ups! Tam nie można postawić statku")
                    time.sleep(1)
                    os.system("cls")
                    self.wyswietl_plansze(self.plansza_ukryta_uzytkownik)
                else:
                    self.poloz_statek(plansza,wiersz,kolumna,orientacja,statek)
                    os.system("cls")
                    self.wyswietl_plansze(self.plansza_ukryta_uzytkownik)
                    break
        time.sleep(0.5)
        os.system("cls")
        print("Koniec ustawiania statków! Czas zacząć grę")


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

    def zmiany_na_planszy(self, plansza_ukryta, plansza_jawna, wiersz, kolumna):
            """W zależności od współrzędnych podanych przez użytkownika
            zaznacza na wyświetlanej planszy "X", jeśli użytkownik trafił, a "-",
            jeśli mu się nie udało"""
            if plansza_ukryta[wiersz][kolumna] == 1:
                plansza_jawna[wiersz][kolumna] = termcolor.colored("X", "green")
                return True
            else:
                plansza_jawna[wiersz][kolumna] = termcolor.colored("-", "red")
                return False

        def czy_trafione_pole(self,plansza_ukryta,wiersz,kolumna):
            if plansza_ukryta[wiersz][kolumna] == 1:
                return True
            else:
                return False
            
    def zgadywanie_uzytkownik(self):
        self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
        wiersz = self.podaj_wiersz()
        kolumna = self.podaj_kolumne()
        pole = (wiersz,kolumna)
        if not pole in self.wykorzystane_uzytkownik:
            self.wykorzystane_uzytkownik.append(pole)
            time.sleep(1)
            os.system("cls")
            self.zmiany_na_planszy(self.plansza_ukryta_komputer,self.plansza_zgadywanie_uzytkownik,wiersz,kolumna)
            self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
            self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
            if self.czy_trafione_pole(self.plansza_ukryta_komputer,wiersz,kolumna):
                print("Trafiony!")
                time.sleep(1)
                self.statki_komputer.remove((wiersz,kolumna))
                self.zgadywanie_uzytkownik()
            else:
                print("Pudło!")
                time.sleep(0.5)
        else:
            print("Już tam trafiałeś!")
            time.sleep(0.5)
            os.system("cls")
            self.zgadywanie_uzytkownik()

    def losowanie_wiersza(self):
        wiersz = random.randint(0,9)
        return wiersz

    def losowanie_kolumny(self):
        kolumna = random.randint(0,9)
        return kolumna

    def pobieranie_pola(self):
        wiersz = self.losowanie_wiersza()
        kolumna = self.losowanie_kolumny()
        pole = (wiersz,kolumna)
        return wiersz,kolumna,pole

    def zgadywanie_komputer(self): 
        while True:
            if not self.cele:
                wiersz,kolumna,pole = self.pobieranie_pola()
            else:
                pole = random.choice(self.cele)
                wiersz = pole[0]
                kolumna = pole[1]
                self.cele.remove(pole)
            if pole in self.wykorzystane:
                continue
            else:
                self.wykorzystane.append(pole)
                time.sleep(1.5)
                os.system("cls")
                self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
                self.wyswietl_plansze(self.plansza_zgadywanie_komputer
                print("Komputer zgaduje!")
                time.sleep(0.65)
                cyfry_na_litery = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
                kolumna_lit = cyfry_na_litery[kolumna]
                print(str(wiersz+1)+kolumna_lit)
                time.sleep(1)
                self.zmiany_na_planszy(self.plansza_ukryta_uzytkownik,self.plansza_zgadywanie_komputer,wiersz,kolumna)
                os.system("cls")
                self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
                self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
                if self.czy_trafione_pole(self.plansza_ukryta_uzytkownik,wiersz,kolumna):
                    print("Trafiony!")
                    self.statki_uzytkownik.remove(pole)
                    potencjalne_cele = (wiersz+1,kolumna),(wiersz-1,kolumna),(wiersz,kolumna+1),(wiersz,kolumna-1)
                    for cel in potencjalne_cele:
                        if not self.wystaje(cel[0],cel[1]):
                            self.cele.append(cel)
                    self.zgadywanie_komputer()
                time.sleep(0.5)
                break
                print("Pudło!")
                
moja_gra = Gra()
moja_gra.rozloz_statki_dla_komputera()
moja_gra.poloz_uzytkownik()
for i in range(20):
    moja_gra.zgadywanie_uzytkownik()
    moja_gra.zgadywanie_komputer()
