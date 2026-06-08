import pytest
from models.player import Player
from models.card import Card
from models.turn import Turn
from unittest.mock import patch

@pytest.fixture
def player():
    return Player("TestPlayer")

def test_player_initialization(player):
    assert player.name == "TestPlayer"
    assert player.hand == []
    assert player.points == 0
    assert player.has_bid == True
    assert player.bidding_score == 0

def predefinied_test_set():
    return [Card("kier", "A", 11, "czerwo"),
            Card("karo", "K", 4, "dzwonek"),
            Card("pik", "Q", 3, "wino")]

def test_play_card_correct(player):
    player.hand = predefinied_test_set()
    test_turn = Turn(1,{},None,None)
    with patch("builtins.input", return_value="0"):
        played_card, points = player.play_card(test_turn)
        assert played_card.figure == "A"
        assert played_card.color == "kier"

def test_play_card_wrong_then_correct(player):
    player.hand = predefinied_test_set()
    test_turn = Turn(1,{},None,None)
    with patch("builtins.input", side_effect=["abd","DOASIFJFOIAJ","940328940","-2","2"]):
        played_card, points = player.play_card(test_turn)
        assert played_card.figure == "Q"
        assert played_card.color == "pik"
        assert points == False

def test_play_card_adding_points_for_marriage(player):
    player.hand = [Card("kier", "A", 11, "czerwo"),
                   Card("karo", "K", 4, "dzwonek"),
                   Card("pik", "Q", 3, "dzwonek")]
    test_turn = Turn(1,{},None,None)
    with patch("builtins.input", return_value="2"):
        played_card, points = player.play_card(test_turn)
        assert points == True

def test_player_bid_yes(player):
    with patch("builtins.input", side_effect=["abd","DOASIFJFOIAJ","940328940","-2","1"]):
        bid = player.bid(100)
        assert bid == 1

def test_player_bid_no(player):
    with patch("builtins.input", side_effect=["abd","FOIAJ","940328940","-2","0"]):
        bid = player.bid(100)
        assert bid == 0

def test_player_deal_one_card_each(player):
    other_players = [Player("P2"), Player("P3")]
    player.hand = predefinied_test_set()
    with patch("builtins.input", side_effect=["abd","0","1"]):
        player.deal_one_card_each(other_players, player)
        assert len(player.hand) == 1
        assert len(other_players[0].hand) == 1
        assert len(other_players[1].hand) == 1
    
        
# co mozemy testowac w playerze?

# inicjalizacje 
# zagrywanie kart przez mockowanie
# meldowanie przez mockowanie
# czy input wypierdala gre to znaczy czy jest dobrze zrobiony
# czy dziala funkcja do rozdawania kart

# player bez gry powinien dzialac ogolnie bo on tutaj zwraca karte 

