from models.turn import Turn
import random
from models.player import Player


class Game():
    def __init__(self,players= [],threecards= [],):
        self.threecards = threecards
        self.players = players
        self.round_number = 1
        self.starting_player= self.draw_player()
        self.bidding_player = self.calculate_bidding_player()
        self.start_trick = None
        self.active_marriage = None # marriage is a pair of King and Queen
        self.game_mode = True


    def show_score(self): # dodac opcje zeby z dlugosci nazwy playera liczyło jak zrobić tabele
        print("-------Tabela wyników-------") 
        # dialogue("1")
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
        # dialogue(2)
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

    def show_threecards(self):
        """Odkrywa 3 karty na środku"""
        print(f"\nOsoba, ktora wygrala licytacje dostaje karty: {" ".join([card.name for card in self.threecards]) }")
        # dialogue(3)
 
    def auction(self): # do poprawy: player, który juz wygrał licytacje może podnieść jej wartość o 10 (w niektórych wypadkach)
        """Obsługuje całą licytacje"""
        print("Zaczynamy licytacje")
        # dialogue(4)
        self.players[self.bidding_player].bidding_score = 100 # ustawia wartośc na 100
        while(sum(player.has_bid for player in self.players) > 1):
            for player in self.players:
                if player.bidding_score == 100 and self.highest_bid() == 100:
                    continue
                if not player.has_bid:
                    continue
                if (player.bid(self.highest_bid())):
                    player.bidding_score = self.highest_bid() + 10
                else: 
                    player.has_bid = False
        winner = self.calculate_starting_player()
        self.start_trick  = winner
        print(f"{"-"*50}\nGre rozpocznie {winner.name}, musi ugrać {self.highest_bid()} \n{"-"*50}")
        self.show_threecards()
        self.bid_winner_takes_threecards(winner)
        winner.deal_one_card_each(self.players,winner) # winner.rozdaj_po_karcie(self.players)
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
        for player in self.players:
            player.show_cards_in_hand()
        print('Rozpoczynamy ture')
        marriage = None
        i = False # zmienna zeby zmieniac kolor meldunku za petla
        for i in range(8):
            n_turn = Turn(i+1,{},None,marriage)
            for j in range(3):
                start_player = self.players[(j+self.players.index(self.start_trick )) % 3]
                played_card, store_marriage = start_player.play_card(n_turn)
                if store_marriage: marriage = played_card.color
                if j == 0: n_turn.color = played_card.color
                n_turn.shift[start_player] = played_card
            trick_winner = self.trick_winner(n_turn)
            print(f"Ture wygrywa {trick_winner.name}")
            trick_winner.winned_tricks.append([card for card in n_turn.shift.values()])
            self.start_ture  = trick_winner 
        for player in self.players: 
            print("points", player.calculate_round_score())
        self.end_round()
        self.show_score()

    def check_winner(self):
        """Sprawdza czy ktoś już wygrał gre"""
        return any([1 for player in self.players if player.get_points() > 1000])

    def end_round(self):
        """Resetuje wszystkie zmienne by móc rozpocząć nową rundę"""
        self.round_number += 1 
        self.threecards = []
        player_bid = self.calculate_starting_player()
        for player in self.players:
            if player == player_bid: 
                if player.calculate_round_score() < player.bidding_score:
                    player.points -= player.bidding_score
                else:
                    player.points += player.calculate_round_score()
            else:
                if player.points > 900: # to nie dodawaj punktow bo musi byc licytujacy 
                    pass
                else:      
                    player.points += player.calculate_round_score()
        for player in self.players:
            player.reset_hand()

        if self.check_winner():
            print("koniec gry")

    def zapisz_stan_gry(self):
        pass