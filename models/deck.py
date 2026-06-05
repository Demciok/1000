import json
from .card import Card
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_PATH = BASE_DIR / 'resources' / 'cards.json'

class Deck():
    """Represents a deck of cards and provides deck operations."""

    def __init__(self, deck=None):
        """Initialize the deck container and default deck size."""
        self.deck = deck or []
        self.size = 24

    def get_deck(self):
        """Return the names of cards currently in the deck."""
        return [self.deck[a].name for a in range(self.size)]

    def calculate_points_in_deck(self):
        """Return the total point value of all cards in the deck."""
        return sum(card.value for card in self.deck)

    def create_deck(self):
        """Create the deck from the JSON card definition file."""
        with open(CARDS_PATH) as cards_file:
            cards_data = json.load(cards_file)
            deck = [Card() for _ in range(len(cards_data['cards']))]
            for index, card_data in enumerate(cards_data['cards']):
                deck[index].color = card_data['kolor']
                deck[index].figure = card_data['figura']
                deck[index].value = card_data['wartosc']
                deck[index].color_text = card_data['nazwa']
                deck[index].name = deck[index].figure + '_' + card_data['nazwa']
        self.deck = deck

    def shuffle_deck(self):
        """Shuffle the deck in place."""
        random.shuffle(self.deck)

    def deal_cards(self, game):
        """Deal cards randomly to players and place 3 cards in the central pool."""
        destinations = [player.hand for player in game.players for _ in range(7)]
        destinations += [game.threecards] * 3

        random.shuffle(destinations)

        for card, hand in zip(self.deck, destinations):
            hand.append(card)        

    # def deal_cards(self, game):
    #     """Deal cards to each player and place remaining cards in the central pool."""
    #     i = 7
    #     for card in self.deck:
    #         if len(game.players[0].hand) < i:
    #             game.players[0].hand.append(card)
    #         elif len(game.players[1].hand) < i:
    #             game.players[1].hand.append(card)
    #         elif len(game.players[2].hand) < i:
    #             game.players[2].hand.append(card)
    #         elif len(game.threecards) < 3:
    #             game.threecards.append(card)
    #         else:
    #             continue

