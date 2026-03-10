from models.bot import Bot
from models.player import Player
from models.deck import Deck
from game.game import Game
from utils.auxiliary import pick_game_mode, name_a_player

def main():
    if pick_game_mode():
        Player1 = Player("gracz1",0) # nazwij_gracz()
        Player2 = Player("gracz2",0) # nazwij_gracz()
        Player3 = Player("gracz3",0) # nazwij_gracz()
    else:
        Player1 = Player("czlowiek",0) 
        Player2 = Bot("LLama",0)
        Player3 = Bot("Claude",0)

    gameplay = Game([Player1,Player2,Player3])
    deck_of_cards = Deck()
    deck_of_cards.create_deck()
     
    gameplay.starting_player.shuffle(deck_of_cards)
    while True:
        deck_of_cards.deal_cards(gameplay)
        gameplay.auction()
        gameplay.round()
        gameplay.end_round()
        gameplay.show_score()
        gameplay.players[gameplay.bidding_player].shuffle(deck_of_cards)


if __name__ == "__main__":
    main()
