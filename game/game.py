from models.turn import Turn
import random
from models.player import Player
import sys
from data import gamerecorder


POINTS_TO_WIN = 1000
WINNING_THRESHOLD = 900
INITIAL_BID = 100
BID_RAISE = 10
SEPARATOR = "-" * 50
TOTAL_TURNS = 8


class Game():
    def get_players_data(self):
        """Return a summary of each player's name and hand for recording."""
        return {
            "1": {"name": self.players[0].name, "hand": [c.name for c in self.players[0].hand]},
            "2": {"name": self.players[1].name, "hand": [c.name for c in self.players[1].hand]},
            "3": {"name": self.players[2].name, "hand": [c.name for c in self.players[2].hand]}
        }

    def __init__(self, players=None, threecards=None):
        """Initialize the game state with players, the three-card pool, and a recorder."""
        self.threecards = threecards or []
        self.players = players or []
        self.round_number = 1
        self.starting_player = self.draw_player()
        self.bidding_player = self.calculate_bidding_player()
        self.start_trick = None
        self.active_marriage = None  # marriage is a pair of King and Queen
        self.gamemode = ""
        self.deck = []
        self.gamerecorder = gamerecorder.Gamerecorder()

    def calculate_quantity_of_bidding_players(self):
        """Count how many players are still active in the bidding."""
        return sum(player.has_bid for player in self.players)

    def show_score(self):
        """Print the current score table for all players."""
        print("-------Tabela wyników-------")
        for player in self.players:
            print("-" * 20)
            print("-", player.name, "-", player.points, "-")
            print("-" * 20)

    def calculate_starting_player(self):
        """Return the player who won the auction."""
        return max(self.players, key=lambda player: player.bidding_score)

    def draw_player(self):
        """Select a random player to start the game."""
        player = random.choice(self.players)
        print(f"Gre rozpoczyna: {player.name}")
        return player

    def calculate_bidding_player(self):
        """Return the index of the player who begins bidding."""
        return (self.players.index(self.starting_player) + self.round_number) % len(self.players)

    def highest_bid(self):
        """Return the highest current bid among players."""
        return max([player.bidding_score for player in self.players])

    def bid_winner_takes_threecards(self, winner):
        """Add the three central cards to the winner's hand."""
        winner.hand.extend(self.threecards)
        self.threecards = []

    def show_threecards(self):
        """Display the three cards in the center."""
        print(f"\nOsoba, ktora wygrala licytacje dostaje karty: {' '.join([card.name for card in self.threecards])}")

    def check_winner(self):
        """Return whether any player has exceeded the points threshold to win."""
        return any([1 for player in self.players if player.get_points() > POINTS_TO_WIN])

    def auction(self):
        """Handle the full auction phase and determine the bidding winner."""
        # Game recording
        self.gamerecorder.record_start_game(self.get_players_data(), {" ".join([card.name for card in self.threecards])})

        print("Zaczynamy licytacje")

        self.bidding_player = self.calculate_bidding_player()
        self.players[self.bidding_player].bidding_score = INITIAL_BID  # set initial bid to 100

        start_index = self.bidding_player
        ordered_players = self.players[start_index:] + self.players[:start_index]

        while self.calculate_quantity_of_bidding_players() > 1:
            for player in ordered_players:
                if player.bidding_score == INITIAL_BID and self.highest_bid() == INITIAL_BID:
                    continue
                player_bid_choice = player.bid(self.highest_bid())

                # Game recording
                self.gamerecorder.record_bid(player.name, player_bid_choice, self.highest_bid(), self.calculate_quantity_of_bidding_players())

                if not player.has_bid:
                    continue

                if self.calculate_quantity_of_bidding_players() == 1:
                    break
                if player_bid_choice:
                    player.bidding_score = self.highest_bid() + BID_RAISE
                else:
                    player.has_bid = False

        winner = self.calculate_starting_player()
        self.start_trick = winner
        print(f"{SEPARATOR}\nGre rozpocznie {winner.name}, musi ugrać {self.highest_bid()}\n{SEPARATOR}")
        self.show_threecards()
        self.bid_winner_takes_threecards(winner)
        winner.deal_one_card_each(self.players, winner)

        # Game recording
        self.gamerecorder.record_turn(self.get_players_data())

        print(f"{SEPARATOR}\n Zaczynamy grę \n{SEPARATOR}")

    def trick_winner(self, turn: Turn) -> Player:
        """Return the player who wins the current trick."""
        players_with_color = {
            player: card for player, card in turn.shift.items()
            if card.color == turn.marriage_color
        }
        if not players_with_color:
            return max(turn.shift, key=lambda g: turn.shift[g].value)
        winner = max(players_with_color, key=lambda g: players_with_color[g].value)
        return winner

    def round(self):
        """Play one full round of turns for all players."""
        print('Rozpoczynamy ture')
        marriage = None
        for i in range(TOTAL_TURNS):
            n_turn = Turn(i + 1, {}, None, marriage)

            gm_helper = {}
            for j in range(len(self.players)):
                start_player = self.players[(j + self.players.index(self.start_trick)) % len(self.players)]
                played_card, store_marriage = start_player.play_card(n_turn)

                # Game recording
                gm_helper[start_player.name] = played_card.name

                if store_marriage:
                    marriage = played_card.color
                if j == 0:
                    n_turn.color = played_card.color
                n_turn.shift[start_player] = played_card

            # Game recording
            self.gamerecorder.record_turn({i: gm_helper})

            trick_winner = self.trick_winner(n_turn)
            print(f"Ture wygrywa {trick_winner.name}")
            trick_winner.winned_tricks.append([card for card in n_turn.shift.values()])
            self.start_trick = trick_winner

        for player in self.players:
            print(player.name, "punkty", player.calculate_round_score())
        self.end_round()
        self.show_score()

    def end_round(self):
        """Reset the round state, update player scores, and save the round."""
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
                if player.points > WINNING_THRESHOLD:  # do not add points for this player if the bidder must still compete
                    pass
                else:
                    points_to_add = player.calculate_round_score()
            player.points += points_to_add

            # Game recording
            self.gamerecorder.record_points((player.name, points_to_add))

        for player in self.players:
            player.reset_hand()

        if self.check_winner():
            for player in self.players:
                if player.get_points() >= POINTS_TO_WIN:
                    print(f"koniec gry, GRE WYGRYWA {player.name}")
                    self.show_score()
                    sys.exit()

        # Game recording
        self.gamerecorder.save_round()

    def zapisz_stan_gry(self):
        """Placeholder for saving the current game state."""
        pass