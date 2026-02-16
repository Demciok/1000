import json
from .karta import Karta
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # __file__ -> plik talia.py parent -> wczesniejszy katalog -> parent.parent -> wczesniejszy wczesniejszy katalog
KARTY_PATH = BASE_DIR / 'resources' / "karty.json"

class Talia():
    def __init__(self,deck =[]):
        self.deck = deck
        self.size = 24
    
    def get_deck(self):
        """Zwraca nazwy kart znajdujących się w talii"""
        return [self.deck[a].nazwa for a in range(self.size)]
    
    def przelicz_punkty_w_talii(self):
        """Zwraca sume punktow w talii"""
        return sum(karta.wartosc for karta in self.deck)
    
    def stworz_talie(self):
        """Tworzy talie"""
        with open(KARTY_PATH) as cards:
            cards = json.load(cards)
            deck = [Karta() for i in range(len(cards["cards"]))]
            for a in range(len(cards["cards"])):
                deck[a].kolor = cards["cards"][a]["kolor"]
                deck[a].figura = cards["cards"][a]["figura"]
                deck[a].wartosc = cards["cards"][a]["wartosc"]
                deck[a].kolor_slownie = cards["cards"][a]["nazwa"]
                deck[a].nazwa = deck[a].figura+"_"+cards["cards"][a]["nazwa"]
        self.deck = deck
    
    def przetasuj_talie(self): # random.shuffle(self.deck)
        """Tasuje talie"""
        drawn = []
        tmp_deck = []
        print("Tasowanie kart")
        while (len(drawn) < 24):
            r_card = random.randint(0,23)
            if (r_card not in drawn):
                drawn.append(r_card)
                tmp_deck.append(self.deck[r_card])
        self.deck = tmp_deck

    def rozdaj_karty(self,gra): # metoda do poprawy tylko na 3 graczy
        """Rozdaje karty kazdemu graczowi"""
        i = 7
        for e,karta in enumerate(self.deck):
            if (len(gra.gracze[0].reka) < i):
                gra.gracze[0].reka.append(karta)
            elif (len(gra.gracze[1].reka) < i):
                gra.gracze[1].reka.append(karta)
            elif (len(gra.gracze[2].reka) < i):
                gra.gracze[2].reka.append(karta)
            else:
                gra.trzykarty.append(karta)
