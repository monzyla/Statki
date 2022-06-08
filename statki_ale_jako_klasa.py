import random


class Gra():
    def __init__(self):
        self.wiersze = 10
        self.kolumny = 10
        self.wymiary = 10
        self.plansza_ukryta = []
        self.stworz_plansze(self.plansza_ukryta)
        self.plansza_do_gry = []
        self.stworz_plansze(self.plansza_do_gry)
        self.statki = [5,4,4,3,3,3,2,2,2,2,1,1,1,1,1]


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

    def rozloz_statki_dla_komputera(self):
        """Dla każdej długości statku podanego na liście wywołuje funkcje
        naloz_na_plansze_losowo"""
        jakie_statki = self.statki
        plansza = self.plansza_ukryta
        for statek in jakie_statki:
            self.naloz_na_plansze_losowo(statek, plansza)

    def naloz_na_plansze_losowo(self,statek,plansza):
        """Dopóki nie da się położyć statku, losuje orientację statku
        i pozycję jego lewego górnego rogu"""
        da_sie_polozyc = False
        orientacja = None
        wiersz = None
        kolumna = None

        while da_sie_polozyc == False:
            orientacja = random.choice(["pionowo","poziomo"])
            wiersz = random.randint(0,len(plansza))
            kolumna = random.randint(0,len(plansza[0]))
            da_sie_polozyc = self.sprawdz(plansza,wiersz,kolumna,orientacja,statek)

        self.poloz_statek(plansza,wiersz,kolumna,orientacja,statek)


    def generuj(self,wiersz,kolumna,orientacja,dlugosc):
        """Na podstawie orientacji statku i współrzędnych jego lewego górnego rogu
        generuje listę wszystkich współrzędnych statku o przekazanej długości"""
        wspolrzedne = []
        if orientacja == "poziomo":
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

    def poloz_statek(self,plansza,wiersz,kolumna,orientacja,dlugosc):
        """Kładzie statek"""
        gdzie = self.generuj(wiersz,kolumna,orientacja,dlugosc)
        for wiersz,kolumna in gdzie:
            plansza[wiersz][kolumna] = 1

    def poloz_uzytkownik(wiersz,kolumna,orientacja,dlugosc):
        """Do napisania"""
        pass

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
moja_gra.rozloz_statki_dla_komputera()
moja_gra.wyswietl_plansze(moja_gra.plansza_ukryta)


