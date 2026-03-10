import json
from .card import Card
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # __file__ -> plik talia.py parent -> wczesniejszy katalog -> parent.parent -> wczesniejszy wczesniejszy katalog
KARTY_PATH = BASE_DIR / 'resources' / "cards.json"

class Deck():
    def __init__(self,deck =[]):
        self.deck = deck
        self.size = 24
    
    def get_deck(self):
        """Zwraca nazwy kart znajdujących się w talii"""
        return [self.deck[a].name for a in range(self.size)]
    
    def calculate_points_in_deck(self):
        """Zwraca sume punktow w talii"""
        return sum(card.value for card in self.deck)
    
    def create_deck(self):
        """Tworzy talie"""
        with open(KARTY_PATH) as cards:
            cards = json.load(cards)
            deck = [Card() for i in range(len(cards["cards"]))]
            for a in range(len(cards["cards"])):
                deck[a].color = cards["cards"][a]["kolor"]
                deck[a].figure = cards["cards"][a]["figura"]
                deck[a].value = cards["cards"][a]["wartosc"]
                deck[a].color_text = cards["cards"][a]["nazwa"]
                deck[a].name = deck[a].figure+"_"+cards["cards"][a]["nazwa"]
        self.deck = deck
    
    def shuffle_deck(self): # random.shuffle(self.deck)
        """Tasuje talie"""
        random.shuffle(self.deck)

    def deal_cards(self,game): # metoda do poprawy tylko na 3 graczy
        """Rozdaje karty kazdemu graczowi"""
        i = 7
        for e,card in enumerate(self.deck):
            if (len(game.players[0].hand) < i):
                game.players[0].hand.append(card)
            elif (len(game.players[1].hand) < i):
                game.players[1].hand.append(card)
            elif (len(game.players[2].hand) < i):
                game.players[2].hand.append(card)
            else:
                game.threecards.append(card)
