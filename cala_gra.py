import random
import time
import os
import termcolor


class Gra():
    def __init__(self):
        self.wiersze = 10
        self.kolumny = 10
        self.wymiary = 10
        # tablica na porozstawiane statki komputera
        self.plansza_ukryta_komputer = [] 
        self.stworz_plansze_dwa(self.plansza_ukryta_komputer)
        # tablica umożliwiająca wyświetlanie zmian po zgadywaniu użytkownika
        self.plansza_zgadywanie_uzytkownik = []
        self.stworz_plansze(self.plansza_zgadywanie_uzytkownik)
        # tablica na porozstawiane statki użytkownika
        self.plansza_ukryta_uzytkownik = []
        self.stworz_plansze(self.plansza_ukryta_uzytkownik)
        # tablica umożliwiająca wyświetlanie zmian po zgadywaniu komputera
        self.plansza_zgadywanie_komputer = []
        self.stworz_plansze_dwa(self.plansza_zgadywanie_komputer)
        self.statki = [5,4,4,3,3,3,2,2,2,2,1,1,1,1,1]
        # pola, w które już zostały oddane strzały
        self.wykorzystane_komputer = [] 
        self.wykorzystane_uzytkownik = []
        # pola targetowane przez komputer po dobrym trafieniu
        self.cele = []
        # pola statków, w które jeszcze nie było trafienia 
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

        while not da_sie_polozyc:
            orientacja = random.choice(["0","1"])
            wiersz = random.randint(0,self.wiersze)
            kolumna = random.randint(0,self.kolumny)
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

    def wystaje(self,wiersz,kolumna):
        """Zwraca True, jeśli (wiersz,kolumna) jest poza planszą"""
        return wiersz<0 or kolumna<0 or wiersz>=self.wiersze or kolumna>=self.kolumny

    def zly_sasiad(self,plansza,wiersz,kolumna):
        """Zwraca True, jeśli pole nie nadaje się nie sąsiada statku,
        ponieważ znajduje się na nim inny statek"""
        if not self.wystaje(wiersz,kolumna):
            return plansza[wiersz][kolumna] == 1
        return False

    def sprawdz(self,plansza,wiersz,kolumna,orientacja,statek):
        """Zwraca True, kiedy pole nie jest zajęte, a żadna ze współrzędnych statku
        nie znajduje się poza planszą oraz kiedy sąsiadem nie jest pole zajęte przez 
        inny statek"""
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
        """Umożliwia użytkownikowi postawienie statków na ukrytej planszy.
        Wykorzystuje pobrane od uzytkownika informacje o orientacji i współrzędnej 
        lewego górnego rogu. Wykorzystuje metodę self.czy_mozna_postawic do sprawdzenia, 
        czy w wybranym miejscu są puste pola i następnie wywołuje self.postaw statek"""                    
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
        """Pobiera od użytkownika numer wiersza od 1 do 10 
        i zwraca numer wiersza odpowiadający mu w tablicy"""
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
        """Pobiera od użytkownika oznaczenie kolumny i przekształca 
        literę na odpowiadający numer w tablicy"""
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
        """Zwraca True, jeśli przekazane pole zostało trafione"""
        if plansza_ukryta[wiersz][kolumna] == 1:
            return True
        else:
            return False
            
    def zgadywanie_uzytkownik(self):
        """Przekazuje podane przez użytkownika numer wiersza i kolumny do 
        zmiany_na_planszy i wyświetla plansze po strzale. Umożliwia kolejny strzał
        po poprawnym trafieniu. Informuje jeśli statek został zatopiony"""
        os.system("cls")
        self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
        self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
        wiersz = self.podaj_wiersz()
        kolumna = self.podaj_kolumne()
        pole = (wiersz,kolumna)
        if not pole in self.wykorzystane_uzytkownik:
            self.wykorzystane_uzytkownik.append(pole)
            self.zmiany_na_planszy(self.plansza_ukryta_komputer,self.plansza_zgadywanie_uzytkownik,wiersz,kolumna)
            time.sleep(1)
            os.system("cls")
            self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
            self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
            if self.czy_trafione_pole(self.plansza_ukryta_komputer,wiersz,kolumna):
                if self.czy_zatopiony(self.plansza_ukryta_komputer,wiersz,kolumna,self.wykorzystane_uzytkownik):
                    print("Trafiony! Zatopiony!")
                else:
                    print("Trafiony!)
                time.sleep(1)
                self.statki_komputer.remove((wiersz,kolumna))
                self.zgadywanie_uzytkownik()
            else:
                print("Pudło!")
                time.sleep(1)
        else:
            print("Już tam trafiałeś!")
            time.sleep(1)
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
        """Losuje numer wiersza i kolumny i przekazuje je do zmiany_na_planszy.
        Umożliwia ponowne losowanie wiersza i kolumny po poprawnym trafieniu.
        Jeśli komputer trafił to dodaje pola graniczące z tym polem do listy celów,
        z której potem losuje."""
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
                    if self.czy_zatopiony(self.plansza_ukryta_uzytkownik,wiersz,kolumna,self.wykorzystane_komputer):
                        print("Trafiony! Zatopiony!")   
                    else:
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
                                      
        def czy_zatopiony(self,plansza,wiersz,kolumna,trafione):
        """Zwraca True, jeśli pole, którego współrzędne zostały przekazane należy do zatopionego statku"""
            i=1
            while not self.wystaje(wiersz+i,kolumna):
                if plansza[wiersz+i][kolumna] == 1 and (wiersz+i,kolumna) not in trafione:
                    return False
                if plansza[wiersz+i][kolumna]!=1:
                    break
                i += 1
            i=1
            while not self.wystaje(wiersz-i,kolumna):
                if plansza[wiersz-i][kolumna] == 1 and (wiersz-i,kolumna) not in trafione:
                    return False
                if plansza[wiersz-i][kolumna]!=1:
                    break
                i += 1
            i=1
            while not self.wystaje(wiersz,kolumna+i):
                if plansza[wiersz][kolumna+i] == 1 and (wiersz,kolumna+i) not in trafione:
                    return False
                if plansza[wiersz][kolumna+i]!=1:
                    break
                i += 1
            i=1
            while not self.wystaje(wiersz,kolumna-i):
                if plansza[wiersz][kolumna-i] == 1 and (wiersz,kolumna-i) not in trafione:
                    return False
                if plansza[wiersz][kolumna-i]!=1:
                    break
                i += 1
            return True

print(termcolor.colored("WITAJ W GRZE W STATKI", "magenta"))
print("Statki rozmieszczane są na samym początku gry na planszy o wymiarach 10x10."
"\nNastępnie, użytkownik oraz komputer naprzemiennie zgadują pola, na których "
"potencjalnie mógłby się znajdować statek \nprzeciwnika.")
print("Gdy strzał jest niepoprawny, zgadywanie rozpoczyna przeciwnik."
"\nW przypadku trafienia w statek przeciwnika osobie zgadującej przysługuje "
"kolejny strzał. \nGra kończy się, gdy któraś ze stron zatopi wszystkie statki przeciwnika.")
print(termcolor.colored("Aby rozpocząć naciśnij enter.", "green"))
dzialanie = input()
if dzialanie == "enter":
    moja_gra = Gra()
os.system("cls")
moja_gra = Gra()
print("Plansza, na której będa pojawiać się wszystkie strzały użytkownika:")
moja_gra.wyswietl_plansze(moja_gra.plansza_zgadywanie_uzytkownik)
print("Plansza ukazująca wszystkie strzały komputera:")
moja_gra.wyswietl_plansze(moja_gra.plansza_zgadywanie_komputer)
print("Aby przejść dalej naciśnij enter")
if input() == "enter":
    print("Proszę, rozmieść swoje statki na planszy")
os.system("cls")
moja_gra.rozloz_statki_dla_komputera()
print("Proszę, rozmieść swoje statki na planszy")
moja_gra.wyswietl_plansze(moja_gra.plansza_ukryta_uzytkownik)
moja_gra.poloz_uzytkownik()
print("INSTRUKCJA:")
print("Czerwony", termcolor.colored("-", "red"), "oznacza strzał nietrafiony")
print("Zielony", termcolor.colored("X", "green"), "oznacza strzał trafiony")
print("Aby przejść dalej naciśnij enter")
if input() == "enter":
    os.system("cls")
while moja_gra.statki_komputer and moja_gra.statki_uzytkownik:
    moja_gra.zgadywanie_komputer()
    moja_gra.zgadywanie_uzytkownik()
if moja_gra.statki_uzytkownik:
    print("Udało Ci się wygrać!")
else:
    print("Niestety przegrałeś z komputerem!")
print("Aby zakończyć naciśnij enter")
if input() == "enter":
    os.system("quit")

