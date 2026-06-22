from models.bot import Bot
from models.player import Player
from models.deck import Deck
from game.game import Game
from models.languagemanager import LanguageManager
from utils.auxiliary import pick_game_mode, name_a_player, random_player_name, choose_language
import os
import pickle
import sys

# SAVE GAME 

def _language_manager(game=None):
    if game is not None and getattr(game, "lm", None) is not None:
        return game.lm
    return LanguageManager()

 
def save_state(game_data, filename="savegame.pkl"):
        with open(filename,"wb") as f:
             pickle.dump(game_data,f)
        _language_manager(game_data).print_by_id(26)

def load_state(filename="savegame.pkl"):
     if os.path.exists(filename):
          with open(filename, "rb") as f:
               return pickle.load(f)
     return None

def main_save():
    state = load_state()
    game = None
    lm = _language_manager(state)

    if state:
        choice = lm.input_by_id(36)
        if choice.lower() == 't':
            game = state
            lm.print_by_id(27)
        else:
            game = setup_new_game()
    else:
        game = setup_new_game()

    try:
        run_game_loop(game)
    except KeyboardInterrupt:
        save_state(game)
        sys.exit(0) 


def setup_new_game():
    lan = choose_language()
    lm = LanguageManager(lan)
    if pick_game_mode(lm):
        Player1 = Player(random_player_name(),lm,0)
        Player2 = Player(random_player_name(),lm,0) 
        Player3 = Player(random_player_name(),lm,0) 
    else:
        Player1 = Player("czlowiek",lm,0) 
        Player2 = Bot("Claude",lm,0)
        Player3 = Bot("Gemini",lm,0)

    gameplay = Game([Player1,Player2,Player3],None,lm)
    gameplay.deck = Deck()
    gameplay.deck.create_deck()
    gameplay.starting_player.shuffle(gameplay.deck)
    return gameplay

def run_game_loop(gameplay):
    while True:
        gameplay.deck.deal_cards(gameplay)
        gameplay.auction()
        gameplay.round()
        gameplay.show_score()
        gameplay.players[gameplay.bidding_player].shuffle(gameplay.deck)


def main():
    game = setup_new_game()
    run_game_loop(game)

if __name__ == "__main__":
    main()
