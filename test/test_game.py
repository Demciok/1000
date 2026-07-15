import pytest
from game.game import Game
from models.player import Player
from models.deck import Deck
from models.card import Card
from models.turn import Turn
import random

@pytest.fixture(scope="function")
def deck():
    deck = Deck()
    deck.create_deck()
    return deck

@pytest.fixture(scope="function")
def players():
    return [Player(f"{i}") for i in range(3)]

@pytest.fixture(scope="function")
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
    game.threecards = [Card("Czerwo", "A", 11), Card("Wino", "K", 2), Card("Dzwonek", "Q", 3)]
    threecards_before = game.threecards.copy()
    winner = game.players[0]
    winner.hand = []
    game.bid_winner_takes_threecards(winner)
    assert len(winner.hand) == 3
    assert winner.hand == threecards_before
    assert game.threecards == []
# ♠ wino pik | ♣ zoladz trefl | ♦ dzwonek karo | ♥ czerwo kier
def test_trick_winner_casetest1(game):
    [k1, k2, k3] = [Card("kier", "A", 11, "czerwo"),
                    Card("karo", "K", 4, "dzwonek"), 
                    Card("pik", "Q", 3, "wino")]
    
    test_turn = Turn(0, {
        game.players[0]:k1,
        game.players[1]:k2,
        game.players[2]:k3
    },
    "kier","pik")

    assert game.trick_winner(test_turn) == game.players[2]

def test_trick_winner_casetest2(game):
    [k1, k2, k3] = [
        Card("kier", "A", 11, "czerwo"),
        Card("karo", "A", 11, "dzwonek"),
        Card("pik", "9", 0, "wino")
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
        Card("kier", "10", 10, "czerwo"),
        Card("kier", "K", 4, "czerwo"),
        Card("kier", "A", 11, "czerwo")
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
        Card("kier", "A", 11, "czerwo"),
        Card("kier", "10", 10, "czerwo"),
        Card("pik", "J", 2, "wino")
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
        Card("karo", "Q", 3, "dzwonek"),
        Card("karo", "10", 10, "dzwonek"),
        Card("pik", "A", 11, "wino")
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

    assert game.trick_winner(test_turn).name == game.players[1].name

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


# ──────────────────────────────────────────────
# CASE 6 – wszyscy grają w kolor wiodący (trefl), brak atutu
# Wygrywa gracz z najwyższą kartą koloru wiodącego
# ──────────────────────────────────────────────
def test_trick_winner_casetest6(game):
    [k1, k2, k3] = [
        Card("trefl", "10", 10, "żołądź"),
        Card("trefl", "A", 11, "żołądź"),
        Card("trefl", "K", 4, "żołądź"),
    ]

    test_turn = Turn(
        4,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "trefl",
        None,
    )

    assert game.trick_winner(test_turn) == game.players[1]


# ──────────────────────────────────────────────
# CASE 7 – atut (trefl) bije kolor wiodący (karo)
# Tylko jeden gracz zagrał atutem – on wygrywa
# ──────────────────────────────────────────────
def test_trick_winner_casetest7(game):
    [k1, k2, k3] = [
        Card("karo",  "A", 11, "dzwonek"),
        Card("karo",  "10", 10, "dzwonek"),
        Card("trefl", "9", 0, "żołądź"),
    ]

    test_turn = Turn(
        5,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "karo",
        "trefl",
    )

    assert game.trick_winner(test_turn) == game.players[2]


# ──────────────────────────────────────────────
# CASE 8 – dwa atuty (kier), wygrywa wyższy atut
# Kolor wiodący: pik, atut: kier
# ──────────────────────────────────────────────
def test_trick_winner_casetest8(game):
    [k1, k2, k3] = [
        Card("pik",  "A", 11, "wino"),
        Card("kier", "9", 0, "czerwo"),
        Card("kier", "J", 2, "czerwo"),
    ]

    test_turn = Turn(
        6,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "pik",
        "kier",
    )

    assert game.trick_winner(test_turn) == game.players[2]


# ──────────────────────────────────────────────
# CASE 9 – mieszane kolory, brak atutu (None)
# Karty: karo, pik, trefl – wygrywa najwyższa karta koloru wiodącego (karo)
# ──────────────────────────────────────────────
def test_trick_winner_casetest9(game):
    [k1, k2, k3] = [
        Card("karo",  "Q", 3, "dzwonek"),
        Card("pik",   "A", 11, "wino"),
        Card("trefl", "A", 11, "żołądź"),
    ]

    test_turn = Turn(
        7,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "karo",
        None,
    )

    # Gracze 1 i 2 nie zagrali koloru wiodącego – wygrywa gracz[0]
    assert game.trick_winner(test_turn) == game.players[0]


# ──────────────────────────────────────────────
# CASE 10 – atut (karo) vs atut (karo), wyższy wygrywa
# Kolor wiodący: trefl, obaj rywale dorzucili atuty
# ──────────────────────────────────────────────
def test_trick_winner_casetest10(game):
    [k1, k2, k3] = [
        Card("trefl", "K", 4, "żołądź"),
        Card("karo",  "10", 10, "dzwonek"),
        Card("karo",  "A", 11, "dzwonek"),
    ]

    test_turn = Turn(
        8,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "trefl",
        "karo",
    )

    assert game.trick_winner(test_turn) == game.players[2]


# ──────────────────────────────────────────────
# CASE 11 – atut (pik) dorzucony jako jedyny
# Kolor wiodący: kier, meldunek: pik
# ──────────────────────────────────────────────
def test_trick_winner_casetest11(game):
    [k1, k2, k3] = [
        Card("kier", "A", 11, "czerwo"),
        Card("pik",  "9", 0, "wino"),
        Card("kier", "10", 10, "czerwo"),
    ]

    test_turn = Turn(
        9,
        {
            game.players[0]: k1,
            game.players[1]: k2,
            game.players[2]: k3,
        },
        "kier",
        "pik",
    )

    assert game.trick_winner(test_turn) == game.players[1]


# ══════════════════════════════════════════════
# TESTY Z LOSOWYMI DANYMI
# ══════════════════════════════════════════════

KOLORY   = ["kier", "karo", "pik", "trefl"]
SYMBOLE  = ["kier", "karo", "pik", "trefl"]  # nazwy graficzne (możesz dostosować)
FIGURY   = ["9", "J", "Q", "K", "10", "A"]
PUNKTY   = {"9": 0, "J": 2, "Q": 3, "K": 4, "10": 10, "A": 11}
GRAFIKI  = {"kier": "czerwo", "karo": "dzwonek", "pik": "wino", "trefl": "żołądź"}


def _losowa_karta(kolor):
    figure = random.choice(FIGURY)
    return Card(kolor, figure, PUNKTY[figure], GRAFIKI[kolor])


def _wyznacz_zwyciezce(karty_graczy, kolor_wiodacy, atut):
    """
    Pomocnicza funkcja odtwarzająca logikę trick_winner –
    służy do obliczenia oczekiwanego wyniku w losowych testach.
    """
    gracze = list(karty_graczy.keys())
    karty  = list(karty_graczy.values())

    # Jeśli podano atut, wybieramy najwyższą kartę w tym kolorze.
    # Jeśli nikt nie zagrał atutem, bierzemy najwyższą wartość spośród wszystkich kart.
    if atut:
        atuty = [(i, karty[i]) for i in range(3) if karty[i].color == atut]
        if atuty:
            winner_idx = max(atuty, key=lambda x: x[1].value)[0]
            return gracze[winner_idx]

    winner_idx = max(range(3), key=lambda i: karty[i].value)
    return gracze[winner_idx]


def test_trick_winner_random_no_trump(game):
    """Losowy test – wszyscy grają w ten sam kolor, brak atutu."""
    random.seed()  # prawdziwa losowość przy każdym uruchomieniu
    kolor_wiodacy = random.choice(KOLORY)

    karty = [_losowa_karta(kolor_wiodacy) for _ in range(3)]
    karty_graczy = {
        game.players[0]: karty[0],
        game.players[1]: karty[1],
        game.players[2]: karty[2],
    }

    test_turn = Turn(
        10,
        karty_graczy,
        kolor_wiodacy,
        None,
    )

    oczekiwany = _wyznacz_zwyciezce(karty_graczy, kolor_wiodacy, None)

    print(
        f"\n[RANDOM no-trump] wiodący={kolor_wiodacy} | "
        + " | ".join(f"p{i}: {karty[i].figure}" for i in range(3))
        + f" | winner=players[{list(game.players).index(oczekiwany)}]"
    )

    assert game.trick_winner(test_turn) == oczekiwany


def test_trick_winner_random_with_trump(game):
    """Losowy test – kolor wiodący i atut są różne; co najmniej jeden gracz zagrywa atutem."""
    random.seed()
    kolor_wiodacy = random.choice(KOLORY)
    atut = random.choice([k for k in KOLORY if k != kolor_wiodacy])

    # Gracz 0: kolor wiodący, gracz 1: losowy (może atut), gracz 2: atut
    k0 = _losowa_karta(kolor_wiodacy)
    k1 = _losowa_karta(random.choice([kolor_wiodacy, atut]))
    k2 = _losowa_karta(atut)

    karty_graczy = {
        game.players[0]: k0,
        game.players[1]: k1,
        game.players[2]: k2,
    }

    test_turn = Turn(
        11,
        karty_graczy,
        kolor_wiodacy,
        atut,
    )

    oczekiwany = _wyznacz_zwyciezce(karty_graczy, kolor_wiodacy, atut)

    print(
        f"\n[RANDOM with-trump] wiodący={kolor_wiodacy} atut={atut} | "
        f"p0: {k0.color}/{k0.figure} | p1: {k1.color}/{k1.figure} | p2: {k2.color}/{k2.figure}"
        + f" | winner=players[{list(game.players).index(oczekiwany)}]"
    )

    assert game.trick_winner(test_turn) == oczekiwany
