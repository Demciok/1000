from models.tura import Tura
import random
from models.gracz import Gracz
import sys


class Gra():
    def __init__(self,gracze= [],trzykarty= [],):
        self.trzykarty = trzykarty
        self.gracze = gracze
        self.numer_rundy = 1
        self.zaczynajacy_gre = self.wylosuj_gracza()
        self.zaczynajacy_licytacje = self.oblicz_licytatora()
        self.start_ture = None
        self.aktualny_meldunek = None
        self.tryb_gry = True


    def pokaz_wyniki(self): # dodac opcje zeby z dlugosci nazwy gracza liczyło jak zrobić tabele
        print("-------Tabela wyników-------")
        for gracz in self.gracze:
            print("-"*20)
            print("-",gracz.imie,"-", gracz.punkty, "-")
            print("-"*20)

    def oblicz_startującego(self):
        """Zwraca wygranego licytacji"""
        return  max(self.gracze, key=lambda gracz: gracz.wynik_licytacja)

    def wylosuj_gracza(self):
        """Zwraca osobe zaczynająca calą gre"""
        gracz = random.choice(self.gracze)
        print(f"Gre rozpoczyna: {gracz.imie}")
        return gracz
    
    def oblicz_licytatora(self):
        """Zwraca gracza który zaczyna licytacje"""
        return (self.gracze.index(self.zaczynajacy_gre) + self.numer_rundy) % len(self.gracze)

    def najwyzsza_stawka(self):
        """Zwraca gracza, który obstawił najwyzsza stawke """
        return max([gracz.wynik_licytacja for gracz in self.gracze])
    
    def trzykarty_do_wygranego(self,zwyciezca):
        """Powieksza reke gracza o 3 karty """
        zwyciezca.reka.extend(self.trzykarty)

    def pokaz_kupke(self):
        """Odkrywa 3 karty na środku"""
        print(f"\nOsoba, ktora wygrala licytacje dostaje karty: {" ".join([card.nazwa for card in self.trzykarty]) }")
 
    def licytacja(self): # do poprawy: gracz, który juz wygrał licytacje może podnieść jej wartość o 10 (w niektórych wypadkach)
        """Obsługuje całą licytacje"""
        print("Zaczynamy licytacje")
        self.gracze[self.zaczynajacy_licytacje].wynik_licytacja = 100 # ustawia wartośc na 100
        while(sum(gracz.licytacja for gracz in self.gracze) > 1):
            for gracz in self.gracze:
                if gracz.wynik_licytacja == 100 and self.najwyzsza_stawka() == 100:
                    continue
                if not gracz.licytacja:
                    continue
                if (gracz.licytuj(self.najwyzsza_stawka())):
                    gracz.wynik_licytacja = self.najwyzsza_stawka() + 10
                else: 
                    gracz.licytacja = False
        wygrany = self.oblicz_startującego()
        self.start_ture  = wygrany
        print(f"{"-"*50}\nGre rozpocznie {wygrany.imie}, musi ugrać {self.najwyzsza_stawka()} \n{"-"*50}")
        self.pokaz_kupke()
        self.trzykarty_do_wygranego(wygrany)
        wygrany.rozdaj_po_karcie(self.gracze,wygrany) # wygrany.rozdaj_po_karcie(self.gracze)
        print(f"{"-"*50}\n Zaczynamy grę \n{"-"*50}")

    def wygrany_tury(self,tura: Tura) -> Gracz:
        """Zwraca gracza który wygrywa szychte"""
        print(tura.klr,tura.szychta,tura.nr_tury,tura.klr_meldunku)
        gracze_z_kolorem = {
        gracz: karta for gracz, karta in tura.szychta.items() 
        if karta.kolor == tura.klr_meldunku
        }
        if not gracze_z_kolorem:
            return max(tura.szychta, key=lambda g: tura.szychta[g].wartosc)
        zwyciezca = max(gracze_z_kolorem, key=lambda g: gracze_z_kolorem[g].wartosc)
        return zwyciezca

    def runda(self): # mozna rzucic meldunek nie bedac pierwszy = blad ale te
        """Funkcja obsługująca runde """
        for gracz in self.gracze:
            gracz.posiadane_karty()
        print('Rozpoczynamy ture')
        meldunek = None
        i = False # zmienna zeby zmieniac kolor meldunku za petla
        for i in range(8):
            n_tura = Tura(i+1,{},None,meldunek)
            for j in range(3):
                gracz_zacz = self.gracze[(j+self.gracze.index(self.start_ture )) % 3]
                zagrana_karta, zapamietaj_meldunek = gracz_zacz.zagraj_karte(n_tura)
                if zapamietaj_meldunek: meldunek = zagrana_karta.kolor
                if j == 0: n_tura.klr = zagrana_karta.kolor
                n_tura.szychta[gracz_zacz] = zagrana_karta
            
            wygrany_tury = self.wygrany_tury(n_tura)
            print(f"Ture wygrywa {wygrany_tury.imie}")
            wygrany_tury.wygrane_szychty.append([karta for karta in n_tura.szychta.values()])
            self.start_ture  = wygrany_tury 
        for gracz in self.gracze: 
            print("punkty", gracz.policz_punkty_na_koniec_tury())
        self.zakoncz_runde()
        self.pokaz_wyniki()

    def sprawdz_wygranego(self):
        """Sprawdza czy ktoś już wygrał gre"""
        return any([1 for gracz in self.gracze if gracz.get_punkty() > 1000])

    def zakoncz_runde(self):
        """Resetuje wszystkie zmienne by móc rozpocząć nową rundę"""
        self.numer_rundy += 1
        self.trzykarty = []
        gracz_lic = self.oblicz_startującego()
        for gracz in self.gracze:
            if gracz == gracz_lic: 
                if gracz.policz_punkty_na_koniec_tury() < gracz.wynik_licytacja:
                    gracz.punkty -= gracz.wynik_licytacja
                else:
                    gracz.punkty += gracz.policz_punkty_na_koniec_tury()
            else:
                gracz.punkty += gracz.policz_punkty_na_koniec_tury()
        for gracz in self.gracze:
            gracz.zresetuj_reke()

        if self.sprawdz_wygranego():
            print("koniec gry")

    def zapisz_stan_gry(self):
        pass