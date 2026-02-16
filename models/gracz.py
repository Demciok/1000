from colorama import Fore, Style, init
from operator import attrgetter
from utils.pomocnicze import MELDUNKI
import random
init()

class Gracz():
    def __init__(self,imie: str,punkty: int ):
        self.imie = imie
        self.punkty = punkty
        self.reka = []
        self.wynik_licytacja = 0
        self.licytacja = True
        self.wygrane_szychty = [] 
        self.punkty_meldunek = 0

    def zresetuj_reke(self):
        """Resetuje klase gracze by zacząć nową runde"""
        self.punkty_meldunek = 0
        self.wygrane_szychty = []
        self.reka = []
        self.wynik_licytacja = 0
        self.licytacja = True

    def policz_punkty_na_koniec_tury(self) -> int:
        """Zwraca sume zebranych punktów z kart i meldunku"""
        suma =sum([karta.wartosc for szychta in self.wygrane_szychty for karta in szychta]) + self.punkty_meldunek 
        suma_zaokr = (suma + 5 ) // 10 * 10
        return suma_zaokr

    def get_punkty(self) -> int:
        """Zwraca posiadane punkty"""
        return self.punkty
    
    def posortuj_po_wartosciach(self):
        """Sortuje karty na rece po wartosciach"""
        obecna_reka = [card for card in self.reka]
        obecna_reka.sort(key=attrgetter("wartosc"),reverse=True)
        self.reka = obecna_reka

    def posiadane_karty(self):
        """Sortuje i wyświetla posiadane obecnie karty""" 
        self.posortuj_po_wartosciach()          # {" ".join(f"{k.nazwa({self.reka.index(k)})})}
        print("Twoja reka tak się prezentuje") # {" | ".join([f"{k.nazwa}({self.reka.index(k)})" for k in self.reka if k.kolor == t_kolor]) }
        print(Fore.RED + f"Czerwa: {" | ".join([f"{k.nazwa} ({self.reka.index(k)})" for k in self.reka if k.kolor_slownie == "czerwo"]) }" )
        print(Fore.RED + f"Dzwonki: {" | ".join([f"{k.nazwa} ({self.reka.index(k)})" for k in self.reka if k.kolor_slownie == "dzwonek"]) }" )
        print(Fore.BLACK + f"Zoladzie: {" | ".join([f"{k.nazwa} ({self.reka.index(k)})" for k in self.reka if k.kolor_slownie == "zoladz"]) }" )
        print(Fore.BLACK + f"Wina: {" | ".join([f"{k.nazwa} ({self.reka.index(k)})" for k in self.reka if k.kolor_slownie == "wino"]) }" )
        print(Style.RESET_ALL, end="")

    def przeloz_karty(self,talia):
        """Pozwala przełożyć karty graczowi"""
        print("Wybierasz od góry jak przełożyć karty np. 10 przekladasz 10 górnych kart na dół(0-24): ")
        wybor = int(input(""))
        while (wybor not in [0,24]):
            wybor = int(input("Wybierz poprawny zakres"))
        if (wybor in [0,24]):
            print("Nie przekladasz wiec grajmy")
            return 
        przelozona_talia = talia.deck[wybor:talia.size-1] + talia.deck[0:wybor]
        talia.deck = przelozona_talia
    
    def dodaj_za_meldunek(self,rzucona_karta,t_parm): # zmiana dodana funkcja za meldunek
        if rzucona_karta.figura == "Q" and len(t_parm.szychta) == 0: # sprawdz czy gracz mial na rece krola o tym samym kolorze 
            print("wchodze do meldunku")
            ma_krola = any(k.figura == "K" and k.kolor_slownie == rzucona_karta.kolor_slownie for k in self.reka)
            if ma_krola: 
                print("Rzuciles meldunek")
                self.punkty_meldunek += MELDUNKI[rzucona_karta.kolor_slownie]
                return True
        else:
            return False

    def zagraj_karte(self,t_args):
        """"Mechanizm zagrywania karty przez gracza"""
        self.posiadane_karty()
        ind = input(f"Podaj numer karty, która chcesz wyrzucić (od 0 do {len(self.reka)-1}): ")
        while ind not in [str(a) for a in range(len(self.reka))]:
            ind = input(f"Zły wybor. Wybierz karte (od 0 do {len(self.reka)-1}): ")
        ind = int(ind)
        while True:
          #  if ind > 0 and ind < len(self.reka) and type(ind) == "int": ind = int()
            if t_args.klr != None and self.reka[ind].kolor != t_args.klr:
                if len([karta for karta in self.reka if karta.kolor == t_args.klr]) != 0: 
                    ind = int(input(f"Nie możesz rzucić innego koloru niż {t_args.klr}. Wybierz {" | ".join([f"{k.nazwa}({self.reka.index(k)})" for k in self.reka if k.kolor == t_args.klr]) }: "))
                else:
                    break
            else:
                break
        wyb_karta = self.reka.pop(ind)
        return wyb_karta, self.dodaj_za_meldunek(wyb_karta,t_args)


    def licytuj(self,aktualna_stawka):
        """Gracz dokonuje wybór licytuje albo przestaje licytowac"""
        self.posiadane_karty()
        print(f"{"-"*50}\nGraczu: ", self.imie)
        print(f"Trwa licytacja, podbijasz stawke o 10 ? Obecna najwyższa stawka {aktualna_stawka}")
        wybor = input("Dokonaj wyboru 1/0 (1 - podbijam, 0 - koncze ): ")
        while wybor not in ["0","1"]:
            wybor = input("Zły wybór wybierz poprawnie (1/0): ")
        return int(wybor)

    def rozdaj_po_karcie(self, gracze, ja):
    # 1. Znajdujemy przeciwników (wszyscy poza nami)
        przeciwnicy = [g for g in gracze if g != self]
        
        print(f"\n Musisz oddać po jednej karcie przeciwnikom ")
        for przeciwnik in przeciwnicy:
            self.posortuj_po_wartosciach()
            self.posiadane_karty()
            while True:
                try:
                    wybor = int(input(f"Wybierz numer karty dla gracza {przeciwnik.imie}: "))
                    if 0 <= wybor < len(self.reka):
                        oddana_karta = self.reka.pop(wybor)
                        przeciwnik.reka.append(oddana_karta)
                        break
                    else:
                        print("Niepoprawny numer karty. Spróbuj ponownie.")
                except ValueError:
                    print("Podaj liczbę całkowitą!")
            
        def og_reka(self): # wedlug kolorów
            pass

    def potasuj_talie(self,talia):
        """Shuffle a deck"""
        talia.przetasuj_talie()