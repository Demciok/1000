from models.turn import Turn
import random
from models.player import Player
import sys
from data import gamerecorder


POINTS_TO_WIN = 1000
INITIAL_BID = 100
BID_RAISE = 10

class Game(): 
    def get_players_data(self): # [c.name for c in self.players[0].hand] 
        return {
            "1": {"imie": self.players[0].name, "reka": [c.name for c in self.players[0].hand]},
            "2": {"imie": self.players[1].name, "reka": [c.name for c in self.players[1].hand]},
            "3": {"imie": self.players[2].name, "reka": [c.name for c in self.players[2].hand]}
        }
    
    def __init__(self,players= [],threecards= [],):
        self.threecards = threecards
        self.players = players
        self.round_number = 1
        self.starting_player = self.draw_player()
        self.bidding_player = self.calculate_bidding_player()
        self.start_trick = None
        self.active_marriage = None # marriage is a pair of King and Queen
        self.gamemode = ""
        self.deck = []
        self.gamerecorder = gamerecorder.Gamerecorder()

    def calculate_quantity_of_bidding_players(self):
        return sum(player.has_bid for player in self.players)


    def show_score(self): # dodac opcje zeby z dlugosci nazwy playera liczyło jak zrobić tabele
        print("-------Tabela wyników-------") 
        for player in self.players:
            print("-"*20)
            print("-",player.name,"-", player.points, "-")
            print("-"*20)

    def calculate_starting_player(self):
        """Zwraca wygranego licytacji"""
        return  max(self.players, key=lambda player: player.bidding_score)

    def draw_player(self):
        """Zwraca osobe zaczynająca calą gre"""
        player = random.choice(self.players)
        print(f"Gre rozpoczyna: {player.name}")
        return player
    
    def calculate_bidding_player(self):
        """Zwraca playera który zaczyna licytacje"""
        return (self.players.index(self.starting_player) + self.round_number) % len(self.players)

    def highest_bid(self):
        """Zwraca playera, który obstawił najwyzsza stawke """
        return max([player.bidding_score for player in self.players])
    
    def bid_winner_takes_threecards(self,winner):
        """Powieksza reke playera o 3 karty """
        winner.hand.extend(self.threecards)
        self.threecards = []

    def show_threecards(self):
        """Odkrywa 3 karty na środku"""
        print(f"\nOsoba, ktora wygrala licytacje dostaje karty: {" ".join([card.name for card in self.threecards]) }")
    
    def check_winner(self):
        """Sprawdza czy ktoś już wygrał gre"""
        return any([1 for player in self.players if player.get_points() > POINTS_TO_WIN])
 
    def auction(self): # do poprawy: player, który juz wygrał licytacje może podnieść jej wartość o 10 (w niektórych wypadkach)
        """Obsługuje całą licytacje"""
        # GAME RECORD

        self.gamerecorder.record_start_game(self.get_players_data(),{" ".join([card.name for card in self.threecards]) })

        print("Zaczynamy licytacje")

        self.bidding_player = self.calculate_bidding_player()
        self.players[self.bidding_player].bidding_score = INITIAL_BID # ustawia wartośc na 100

    
        start_index = self.bidding_player
        ordered_players = self.players[start_index:] + self.players[:start_index]

        while(self.calculate_quantity_of_bidding_players() > 1):
            for player in ordered_players:

                if player.bidding_score == INITIAL_BID and self.highest_bid() == INITIAL_BID: # nie wiem po co to jest ale musi byc 
                    continue
                d = player.bid(self.highest_bid())

                # GAME RECORD

                self.gamerecorder.record_bid(player.name,d, self.highest_bid(),self.calculate_quantity_of_bidding_players())
        
                if not player.has_bid:
                    continue
                
                if self.calculate_quantity_of_bidding_players() == 1:
                    break
                if (d):
                    player.bidding_score = self.highest_bid() + 10
                else: 
                    player.has_bid = False
        winner = self.calculate_starting_player()
        self.start_trick  = winner
        print(f"{"-"*50}\nGre rozpocznie {winner.name}, musi ugrać {self.highest_bid()} \n{"-"*50}")
        self.show_threecards()
        self.bid_winner_takes_threecards(winner)
        winner.deal_one_card_each(self.players,winner) 
        # GAME RECORD

        self.gamerecorder.record_turn(self.get_players_data())

        print(f"{"-"*50}\n Zaczynamy grę \n{"-"*50}")

    def trick_winner(self,turn: Turn) -> Player:
        """Zwraca playera który wygrywa szychte"""
        players_with_color = {
        player: card for player, card in turn.shift.items() 
        if card.color == turn.marriage_color
        }
        if not players_with_color:
            return max(turn.shift, key=lambda g: turn.shift[g].value)
        winner = max(players_with_color, key=lambda g: players_with_color[g].value)
        return winner

    def round(self): # mozna rzucic marriage nie bedac pierwszy = blad ale te
        """Funkcja obsługująca runde """
        print('Rozpoczynamy ture')
        marriage = None
        for i in range(8):
            n_turn = Turn(i+1,{},None,marriage)

            gm_helper = {}
            for j in range(3):
                start_player = self.players[(j+self.players.index(self.start_trick )) % 3] 
                played_card, store_marriage = start_player.play_card(n_turn)
                # GAME RECORD

                gm_helper[start_player.name] = played_card.name

                if store_marriage: marriage = played_card.color
                if j == 0: n_turn.color = played_card.color
                n_turn.shift[start_player] = played_card

            # GAME RECORD

            self.gamerecorder.record_turn({i:gm_helper})
            
            trick_winner = self.trick_winner(n_turn)
            print(f"Ture wygrywa {trick_winner.name}")
            trick_winner.winned_tricks.append([card for card in n_turn.shift.values()])
            self.start_trick  = trick_winner 
        

        
        for player in self.players: 
            print(player.name, " points", player.calculate_round_score())
        self.end_round()
        self.show_score()

    def end_round(self):
        """Resetuje wszystkie zmienne by móc rozpocząć nową rundę"""
        self.round_number += 1 
        self.threecards = []
        player_bid = self.calculate_starting_player()
        for player in self.players:
            points_to_add = 0 
            if player == player_bid:
                if player.calculate_round_score() < player.bidding_score:
                    points_to_add = -player.bidding_score
                else:
                    points_to_add = player.calculate_round_score()
            else:
                if player.points > 900: # to nie dodawaj punktow bo musi byc licytujacy 
                    pass
                else:      
                    points_to_add = player.calculate_round_score()
            player.points += points_to_add
            
            # GAME RECORD
            self.gamerecorder.record_points((player.name,points_to_add))
        
        for player in self.players:
            player.reset_hand()

        if self.check_winner():
            for player in self.players:
                if player.get_points() >= 1000:    
                    print(f"koniec gry, GRE WYGRYWA {player.name}")
                    self.show_score()
                    sys.exit()
        
        # GAME RECORD

        self.gamerecorder.save_round()

    def zapisz_stan_gry(self):
        pass