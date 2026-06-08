import pytest
from game.game import Game
from models.player import Player
from models.deck import Deck
from models.card import Card
from models.turn import Turn

@pytest.fixture
def deck():
    deck = Deck()
    deck.create_deck()
    return deck

@pytest.fixture
def players():
    return [Player(f"{i}") for i in range(3)]

@pytest.fixture
def game(deck, players):
    game = Game(players)
    game.deck = deck
    return game

def test_game_initialization(game):
    assert len(game.players) == 3
    assert game.deck.size == 24
    assert game.threecards == []

def test_calculate_quantity_of_bidding_players(game):
    assert game.calculate_quantity_of_bidding_players() == 3
    game.players[0].has_bid = False
    game.players[1].has_bid = False
    game.players[2].has_bid = False
    assert game.calculate_quantity_of_bidding_players() == 0

def test_calculate_starting_player(game):
    game.players[0].bidding_score = 100
    game.players[1].bidding_score = 120
    game.players[2].bidding_score = 100
    assert game.calculate_starting_player() == game.players[1]

def test_highest_bidder(game):
    game.players[0].bidding_score = 150
    game.players[1].bidding_score = 120
    game.players[2].bidding_score = 100
    assert game.highest_bid() == 150

def test_winner_takes_threecards(game):
    game.threecards = [Card("Czerwo", "A","11"), Card("Wino", "K","2"), Card("Dzwonek", "Q","3")]
    threecards_before = game.threecards.copy()
    winner = game.players[0]
    winner.hand = []
    game.bid_winner_takes_threecards(winner)
    assert len(winner.hand) == 3
    assert winner.hand == threecards_before
    assert game.threecards == []
# ♠ wino pik | ♣ zoladz trefl | ♦ dzwonek karo | ♥ czerwo kier
def test_trick_winner_casetest1(game):
    [k1, k2, k3] = [Card("kier", "A","11","czerwo"),
                    Card("karo", "K","4","dzwonek"), 
                    Card("pik", "Q","3","wino")]
    
    test_turn = Turn(0, {
        game.players[0]:k1,
        game.players[1]:k2,
        game.players[2]:k3
    },
    "kier","pik")

    assert game.trick_winner(test_turn) == game.players[2]

def test_trick_winner_casetest2(game):
    [k1, k2, k3] = [
        Card("kier", "A", "11", "czerwo"),
        Card("karo", "A", "11", "dzwonek"),
        Card("pik", "9", "0", "wino")
    ]

    test_turn = Turn(
        0,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3
        },
        "kier",
        "pik"
    )

    assert game.trick_winner(test_turn) == game.players[2]

def test_trick_winner_casetest3(game):
    [k1, k2, k3] = [
        Card("kier", "10", "10", "czerwo"),
        Card("kier", "K", "4", "czerwo"),
        Card("kier", "A", "11", "czerwo")
    ]

    test_turn = Turn(
        1,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3
        },
        "kier",
        None
    )

    assert game.trick_winner(test_turn) == game.players[2]

def test_trick_winner_casetest4(game):
    [k1, k2, k3] = [
        Card("kier", "A", "11", "czerwo"),
        Card("kier", "10", "10", "czerwo"),
        Card("pik", "J", "2", "wino")
    ]

    test_turn = Turn(
        2,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3
        },
        "kier",
        "pik"
    )

    assert game.trick_winner(test_turn) == game.players[2]

def test_trick_winner_casetest5(game):
    [k1, k2, k3] = [
        Card("karo", "Q", "3", "dzwonek"),
        Card("karo", "10", "10", "dzwonek"),
        Card("pik", "A", "11", "wino")
    ]

    test_turn = Turn(
        3,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3
        },
        "karo",
        None
    )

    assert game.trick_winner(test_turn) == game.players[1]

def test_end_round(game):

    game.players[0].points = 100
    game.players[1].points = 910
    game.players[2].points = 50

    game.players[0].winned_tricks = [[Card("kier", "A", 11, "czerwo"),Card("karo", "K", 4, "dzwonek"),Card("karo", "Q", 3, "dzwonek")]]
    game.players[1].winned_tricks = [[Card("karo", "A", 11, "dzwonek")]]
    game.players[2].winned_tricks = [[Card("pik", "A", 11, "wino")]]

    game.end_round()

    assert game.round_number == 2
    assert len(game.threecards) == 0
    assert game.players[0].points == 120
    assert game.players[1].points == 910
    assert game.players[2].points == 60

def test_check_winner(game):
    game.players[0].points = 940
    game.players[1].points = 720
    game.players[2].points = -540

    assert not game.check_winner()

    game.players[0].points = 1010

    assert game.check_winner()
