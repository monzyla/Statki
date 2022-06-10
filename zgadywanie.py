def zgadywanie_uzytkownik(self):
    self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)
    wiersz = self.podaj_wiersz()
    kolumna = self.podaj_kolumne()
    self.zmiany_na_planszy(self.plansza_zgadywanie_uzytkownik,self.plansza_ukryta_komputer,wiersz,kolumna)
    self.wyswietl_plansze(self.plansza_zgadywanie_uzytkownik)

def losowanie_wiersza(self):
    wiersz = random.randint(1,10)
    return wiersz

def losowanie_kolumny_litera(self):
    kolumny = "ABCDEFGHIJ"
    kolumna_lit = random.choice(kolumny)
    return kolumna_lit

def losowanie_kolumny(self):
    kolumna_lit = self.losowanie_kolumny_litera()
    litery_na_cyfry = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
    kolumna = litery_na_cyfry[kolumna_lit]
    return kolumna

def pobieranie_pola(self):
    wiersz = str(self.losowanie_wiersza())
    kolumna = self.losowanie_kolumny_litera()
    wybor = wiersz + kolumna
    return wybor

def zgadywanie_komputer(self): #to miało być tak, żeby się nie powtarzały strzały komputera ale nie jestem pewna czy działa czy nie
    while True:
        time.sleep(1)
        os.system("cls")
        self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
        pole = self.pobieranie_pola()
        if pole in self.wylosowane:
            continue
        else:
            self.wylosowane.append(pole)
            wiersz = self.losowanie_wiersza()
            kolumna = self.losowanie_kolumny()
            self.zmiany_na_planszy(self.plansza_zgadywanie_komputer,self.plansza_ukryta_uzytkownik,wiersz,kolumna)
            time.sleep(0.5)
            os.system("cls")
            self.wyswietl_plansze(self.plansza_zgadywanie_komputer)
            break

def trafione_komputer(self,wiersz,kolumna): #żeby komputer strzelał obok kiedy trafi ale czy tu dziala cos to ja nie wiem
    while True:
        opcje = [[trafiony_wiersz+1,trafiona_kolumna],[trafiony_wiersz-1,trafiona_kolumna],[trafiony_wiersz,trafiona_kolumna+1],[trafiony_wiersz,trafiona_kolumna-1]]
        if self.plansza_ukryta_uzytkownik[wiersz][kolumna] == 0:
            break
        elif self.plansza_ukryta_uzytkownik[wiersz][kolumna] == 1:
            trafiony_wiersz = self.plansza_ukryta_uzytkownik[wiersz]
            trafiona_kolumna = self.plansza_ukryta_uzytkownik[kolumna]
            trafione_pole = [trafiony_wiersz, trafiona_kolumna]
            wybor = random.randint(0,3)
            nowy_wiersz = opcje[liczba][0]
            nowa_kolumna = opcje[liczba][1]
