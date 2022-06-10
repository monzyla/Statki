def zmiany_na_planszy(self, plansza_zgadywanie, plansza_ukryta, wiersz, kolumna): 
    """W zależności od współrzędnych podanych przez użytkownika
    zaznacza na wyświetlanej planszy "X", jeśli użytkownik trafił, a "-",
    jeśli mu się nie udało"""
    """
    global plansza_ukryta #tego chyba nie moze byc
    global plansza_do_gry
    """

    if plansza_ukryta[wiersz][kolumna] == 1:
        plansza_zgadywanie[wiersz][kolumna] = "X"
    else:
        plansza_zgadywanie[wiersz][kolumna] = "-"
