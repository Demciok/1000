import pytest
from game.game import Game
from models.bot import Bot
from models.deck import Deck
from models.card import Card
from models.turn import Turn

test_set_hand_1 = [
        Card("kier", "A", 11, "czerwo"),
        Card("kier", "K", 4, "czerwo"),
        Card("kier", "Q", 3, "czerwo"),
        Card("kier", "J", 2, "czerwo"),
        Card("kier", "10", 10, "czerwo"),
        Card("kier", "9", 0, "czerwo"),  # 9 ma teraz 0 pkt
        Card("karo", "A", 11, "dzwonek") # szum
    ]

test_set_hand_3 = [
    Card("kier", "9", 0, "czerwo"),
    Card("pik", "9", 0, "wino"),
    Card("karo", "9", 0, "dzwonek"),
    Card("trefl", "9", 0, "zoladz"),
    Card("pik", "J", 2, "wino"),
    Card("karo", "Q", 3, "dzwonek"),
    Card("trefl", "J", 2, "zoladz")
]

test_set_hand_4 = [
    Card("kier", "A", 11, "czerwo"),
    Card("pik", "A", 11, "wino"),
    Card("trefl", "A", 11, "zoladz"),
    Card("karo", "A", 11, "dzwonek"),
    Card("kier", "K", 3, "czerwo"),
    Card("trefl", "10", 10, "zoladz"),
    Card("karo", "10", 10, "dzwonek")
]

test_set_hand_random_7 = [
    Card("trefl", "10", 10, "zoladz"),
    Card("kier", "9", 0, "czerwo"),
    Card("pik", "J", 2, "wino"),
    Card("karo", "A", 11, "dzwonek"),
    Card("trefl", "K", 4, "zoladz"),
    Card("trefl", "Q", 3, "zoladz"),
    Card("pik", "10", 10, "wino")
]

test_turn_must_follow_suit = Turn(
    1,
    {
        2: Card("karo", "A", 11, "dzwonek"),
        3: Card("karo", "10", 10, "dzwonek")
    },
    "karo",
    None
)

test_turn_with_marriage = Turn(
    3,
    {
        2: Card("pik", "K", 4, "wino"),
        3: Card("pik", "9", 0, "wino")
    },
    "pik",
    "kier"
)

test_turn_trumped_by_opponent = Turn(
    2,
    {
        3: Card("trefl", "J", 2, "żołądź"),
        2: Card("karo", "9", 0, "dzwonek")
    },
    "trefl",
    "karo"
)

test_turn_opponent_discards_trash = Turn(
    3,
    {
        3: Card("kier", "10", 10, "czerwo"),
        2: Card("karo", "9", 0, "dzwonek")
    },
    "kier",
    "trefl"
)

@pytest.fixture
def bot():
    return Bot("Bot")


def test_check_marriage(bot):
    bot.hand = test_set_hand_random_7
    assert bot.check_marriages() != []

def test_check_marriage(bot):
    bot.hand = test_set_hand_3
    assert bot.check_marriages() == []

def test_calculate_max_bid_best_case(bot):
    bot.hand = test_set_hand_1()
    assert bot.calculate_max_bid() > 200

def test_calculate_max_bid_worst_case(bot):
    bot.hand = test_set_hand_3
    assert bot.calculate_max_bid() < 100

def test_calculate_max_bid_probably_without_marriage(bot):
    bot.hand = test_set_hand_4
    assert bot.calculate_max_bid() >= 120 

def test_calculate_max_bid_probably_without_marriage(bot):
    bot.hand = test_set_hand_random_7
    assert bot.calculate_max_bid() < 120 

def test_simple_logic_1(bot):
    bot.hand = test_set_hand_random_7
    test_turn = Turn(1, {}, None, None)
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "karo"
    assert played_card.figure == "A"
    
    second_played_card = bot.simple_logic(test_turn)
    assert second_played_card.color == "trefl"
    assert second_played_card.figure == "Q"

def test_simple_logic_4(bot):
    bot.hand = test_set_hand_4
    test_turn = Turn(1, {}, None, None)
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "A"
     
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "pik"
    assert played_card.figure == "A"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "trefl"
    assert played_card.figure == "A"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "karo"
    assert played_card.figure == "A"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "trefl"
    assert played_card.figure == "10"


def test_simple_logic_2(bot):
    bot.hand = test_set_hand_1()
    test_turn = Turn(1, {}, None, None)

    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "karo"
    assert played_card.figure == "A"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "Q"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "10"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "K"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "J"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "9"
    
    
    played_card = bot.simple_logic(test_turn)
    assert played_card.color == "kier"
    assert played_card.figure == "A"
    

def test_check_shift_1(bot):
    bot.hand = test_set_hand_random_7
    test_turn = test_turn_must_follow_suit
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "A"
    assert played_card.color == "karo"

def test_check_shift_2(bot):
    bot.hand = test_set_hand_random_7
    test_turn = test_turn_with_marriage
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "kier"

def test_check_shift_3(bot):
    bot.hand = test_set_hand_random_7
    bot.hand.append(Card("karo", "9", 0, "dzwonek"))
    test_turn = test_turn_with_marriage
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "karo"

def test_check_shift_4(bot):
    bot.hand = test_set_hand_random_7
    test_turn = test_turn_trumped_by_opponent
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "kier"

def test_check_shift_5(bot):
    bot.hand = test_set_hand_random_7
    test_turn = test_turn_opponent_discards_trash
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "10"
    assert played_card.color == "trefl"

def test_check_shift_6_1(bot):
    bot.hand = test_set_hand_3
    test_turn = test_turn_must_follow_suit
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "karo"
    
def test_check_shift_7_1(bot):
    bot.hand = test_set_hand_3
    test_turn = test_turn_with_marriage
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "kier"

def test_check_shift_8_1(bot):
    bot.hand = test_set_hand_3
    test_turn = test_turn_with_marriage
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "kier"

def test_check_shift_9_1(bot):
    bot.hand = test_set_hand_3
    test_turn = test_turn_with_marriage
    played_card = bot.check_shift(test_turn)
    assert played_card.figure == "9"
    assert played_card.color == "trefl"




# dobra bota mamy i w sumie spoko bo wiemy co chcemy 
# zeby wyrzucil w danej sytuacji wiec to fajnie bedzie mozna logike poprawic
# wiec tak bedziemy testowac

# calculate max bid tylko zrobimy takie zalozenie 
# damy mega mocna reke i np zeby licytowal do 140
# damy slaba reke i zeby nie licytowal za duzo 
# i tak samo bid mozna jeden test
# play card nie ma co testowac
# play card nam decyduje co mamy zwracac jak jestemy pierwsi
#a check shift jak jestesmy 2 lub 3 