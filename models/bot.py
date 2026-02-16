from .gracz import Gracz
from utils.pomocnicze import MELDUNKI
import random


class Bot(Gracz): # funkcja dziala jak bot ma meldunki to zwraca wartość
    def sprawdz_meldunki(self):
        damy = {k.kolor_slownie for k in self.reka if k.figura == "Q"} # set()
        krole = {k.kolor_slownie for k in self.reka if k.figura == "K"} # set()
        posiadane_meldunki = damy & krole # część wspólna
        if len(posiadane_meldunki) == 0:
            return []
        else:
            return posiadane_meldunki

    def punkty_za_meldunek(self):
        return sum([MELDUNKI[kolor_mel] for kolor_mel in self.sprawdz_meldunki()])
    
    def przelicz_reke(self):
        return sum(karta.wartosc for karta in self.reka)
    
    def oblicz_max_licytacje(self):
        wynik = 0
        meldunki_punkty = self.punkty_za_meldunek()
        wynik += meldunki_punkty

        for karta in self.reka:
            if karta.wartosc == 11: # As
                wynik += 15
            elif karta.wartosc == 10: # 10
                wynik += 10
            elif karta.wartosc == 4: # Król
                wynik += 4

        for kolor in ["wino", "zoladz", "dzwonek", "czerwo"]:
            kart_w_kolorze = len(self.sprawdz_kolor(kolor))
            if kart_w_kolorze >= 4:
                score += 20
        
        max_lic = (wynik // 10 ) * 10
        if meldunki_punkty == 0 and max_lic > 120:
            max_lic = 120
        
        return max_lic
    
    def licytuj(self, aktualna_stawka): # pomyslec jeszcze nad tym 
        punkty_meld = self.punkty_za_meldunek()
        p_punkty = self.przelicz_reke() + punkty_meld
        if aktualna_stawka < self.oblicz_max_licytacje() :
            print(f"Bot: {self.imie} podbija stawke ! ")
            return 1
        else:
            print(f"Bot: {self.imie} konczy licytacje ")
            return 0

    def sprawdz_figure(self,figura):
        return [e for e,karta in enumerate(self.reka) if karta.figura == figura]
    
    def sprawdz_kolor(self,kolor):
        return [karta for e,karta in enumerate(self.reka) if karta.kolor == kolor ]     
    
    def zwroc_najmniejsza(self,kolor):
        self.posortuj_po_wartosciach()
        return [karta for karta in self.reka if karta.kolor == kolor ][-1]
    
    def meldunek_w_kupce(self,t_parm):
        return any([karta for karta in t_parm.szychta.values() if karta.kolor == t_parm.klr_meldunku])
    
    def sprawdz_szychte(self,t_parm): # tu zawsze nam zwraca karte ktora mamy zagrac
        karty_w_kolorze = self.sprawdz_kolor(t_parm.klr)
        if len(karty_w_kolorze) > 0:
            if self.meldunek_w_kupce(t_parm):
                return self.zwroc_najmniejsza(t_parm.klr)
            c = []
            if len(t_parm.szychta) == 2:
                for sz_karta in t_parm.szychta.values():
                    c.append([karta for karta in self.reka if sz_karta.wartosc < karta.wartosc])
                jakas_zmienna = list(set(c[0])- set(c[1]))
                if len(jakas_zmienna) > 0 and jakas_zmienna[0] != 0:

                    return jakas_zmienna[0]
                else:

                    return self.zwroc_najmniejsza(t_parm.klr)
            else:
                karty_wieksze = [karta for karta in self.reka if list(t_parm.szychta.values())[0].wartosc < karta.wartosc]
                if any(karty_wieksze):

                    return karty_wieksze[0]
                else:

                    return self.zwroc_najmniejsza(t_parm.klr)
        else: # tu jest blad 
            if t_parm.klr_meldunku == None:
                self.posortuj_po_wartosciach()
                return self.reka[-1]
            else: # tu cos nie dziala 
                self.posortuj_po_wartosciach()
                karty = self.sprawdz_kolor(t_parm.klr_meldunku)
                if len(karty) > 0:

                    return karty[0]
                else:

                    return self.reka[-1]
            
    def karty_pokaz(self):
        return [karta.nazwa for karta in self.reka]
    def prosta_logika(self,tura_parms):
        if len(tura_parms.szychta) == 0: # jezeli zaczyna ture rzuca najpierw wszystkie asy(bo wiadomo ze wygra) pozniej wszystkie meldunki, na koniec karte najwyzsza 
            asy = self.sprawdz_figure("A")
            karty_w_klr_meldunku = [e for e,karta in enumerate(self.reka) if karta.kolor_slownie == tura_parms.klr_meldunku]
            meld = self.sprawdz_meldunki() # jak zaczyna to musi wyrzucić wszystkie asy
            if len(asy) > 0:
                return self.reka.pop(asy[0]) 
            if len(meld) > 0: # szuka karty z figura dama i kolorem meldunku zwraca index a pozniej popuje i zwraca karte
                return self.reka.pop([e for e,karta in enumerate(self.reka) if karta.kolor_slownie == list(meld)[0] and karta.figura == "Q"][0])
            if len(karty_w_klr_meldunku) > 0:
                return self.reka.pop(karty_w_klr_meldunku[0])
            self.posortuj_po_wartosciach()
            return self.reka.pop(0)
        if len(tura_parms.szychta) == 1:
            return self.reka.pop(self.reka.index(self.sprawdz_szychte(tura_parms)))
        if len(tura_parms.szychta) == 2:
            return self.reka.pop(self.reka.index(self.sprawdz_szychte(tura_parms)))
        
    def zaawansowana_logika(self, tura_parms):
        pass # kiedys zrobie jakas lepsza    
        
    def zagraj_karte(self, tura_parms):
        k = self.prosta_logika(tura_parms)
        print(f"{"-"*50}\n {self.imie} rzuca {k.nazwa} \n {"-"*50}")
        d = self.dodaj_za_meldunek(k,tura_parms)
        return k,d
        

    def rozdaj_po_karcie(self,gracze,wygrany):
        """Funkcja ktora byla poniewaz nie chcialo mi sie robic """
        d = gracze 
        d.remove(wygrany) 
        for a in range(2): 
            if a == 0:
                picked = random.choice(self.reka)
                print(f"{self.imie} daje {picked} graczu {d[a].imie}")
                d[a].reka.append(picked)
                self.reka.remove(picked)
            else:
                picked = random.choice(self.reka)
                print(f"{self.imie} daje {picked} graczu {d[a].imie}")
                d[a].reka.append(picked)
                self.reka.remove(picked)
        d.append(wygrany)
        self.posortuj_po_wartosciach()