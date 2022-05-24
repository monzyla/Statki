def podaj_kolumne():
    kolumny = "ABCDEFGHIJ"
    litery_na_cyfry = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
    while True:
        print("Podaj kolumnę.")
        kolumna = input()
        if kolumna in kolumny:
            break
        else:
            print("Nieprawidłowy znak. Wprowadź pierwszą współrzędną jeszcze raz.")
    wspolrzedna1 = litery_na_cyfry[kolumna] + 1
    return wspolrzedna1

def podaj_wiersz():
    while True:
        print("Podaj wiersz.")
        wiersz = int(input())
        if wiersz > 0 and wiersz < 11:
            break
        else:
            print("Nieprawidłowy znak. Podaj drugą współrzędną jeszcze raz.")
    return wiersz

