MELDUNKI = {
    "wino": 40,
    "zoladz": 60,
    "dzwonek": 80,
    "czerwo": 100
}

def wybierz_tryb():
    print("Witaj w grze w 1000, gra karciana pochodząca z PRL-U")
    print("Mam nadzieje że zasady już znasz teraz wybierz")
    tryb = input("Tryb z botami - 0 tryb z graczami - 1")
    while tryb not in ["0", "1"]:
        tryb = input("Zly wybor wybierz 0- tryb z botami, 1 - tryb z graczami")
    return int(tryb) 

def nazwij_gracza():
    return str(input("Wybierz nazwe dla gracza"))