import pytest
from models.bot import Bot
from models.player import Player
from models.deck import Deck
from game.game import Game
from models.languagemanager import LanguageManager


def setup_new_game():
    lm = LanguageManager("en")
    player1 = Bot("czlowiek", lm, 0)
    player2 = Bot("Claude", lm, 0)
    player3 = Bot("Gemini", lm, 0)

    gameplay = Game([player1, player2, player3], None, lm)
    gameplay.deck = Deck()
    gameplay.deck.create_deck()
    gameplay.starting_player.shuffle(gameplay.deck)
    return gameplay


def test_game_ends_when_score_exceeds_1000():
    gameplay = setup_new_game()

    with pytest.raises(SystemExit):
        while True:
            gameplay.deck.deal_cards(gameplay)
            gameplay.auction()
            gameplay.round()
            gameplay.show_score()
            gameplay.players[gameplay.bidding_player].shuffle(gameplay.deck)

    scores = [player.points for player in gameplay.players]
    print(f"\nWyniki po zakończeniu gry: {scores}")
    assert any(score > 1000 for score in scores)