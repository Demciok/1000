from models.deck import Deck
from game.game import Game
from models.player import Player
import copy
import pytest

@pytest.fixture
def deck():
    deck = Deck()
    deck.create_deck()
    return deck

def test_deck_size(deck):
    assert deck.size == 24

def test_deck_points(deck):
    assert deck.calculate_points_in_deck() == 120

def test_deck_shuffle(deck):
    deck_before = copy.copy(deck)
    deck.shuffle_deck()
    assert deck_before.deck[-1] == deck.deck[-1]

def test_deck_deal_cards(deck):
    P1 = Player("1")
    P2 = Player("2") 
    P3 = Player("3")
    gameplay = Game([P1,P2,P3])
    gameplay.deck = deck 
    deck.deal_cards(gameplay)
    assert len(P1.hand) == 7
    assert len(P2.hand) == 7
    assert len(P3.hand) == 7
    assert len(gameplay.threecards) == 3

