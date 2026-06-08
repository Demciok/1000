from models.bot import Bot
from models.player import Player
from models.deck import Deck
from game.game import Game
from utils.auxiliary import pick_game_mode, name_a_player, random_player_name
import os
import pickle
import sys

# SAVE GAME 

 
def save_state(game_data, filename="savegame.pkl"):
        with open(filename,"wb") as f:
             pickle.dump(game_data,f)
        print("Zapisano gre")

def load_state(filename="savegame.pkl"):
     if os.path.exists(filename):
          with open(filename, "rb") as f:
               return pickle.load(f)
     return None

def main_save():
    state = load_state()
    game = None

    if state:
        choice = input("Znaleziono zapisany stan gry! Czy chcesz kontynuować? (t/n): ")
        if choice.lower() == 't':
            game = state
            print("Wczytano grę!")
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

    if pick_game_mode():
        Player1 = Player(random_player_name(),0)
        Player2 = Player(random_player_name(),0) 
        Player3 = Player(random_player_name(),0) 
    else:
        Player1 = Bot("czlowiek",0) 
        Player2 = Bot("Claude",0)
        Player3 = Bot("Gemini",0)

    gameplay = Game([Player1,Player2,Player3])
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
    main_save()
