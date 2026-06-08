from abc import ABC, abstractmethod
from operator import attrgetter
from utils.auxiliary import MARRIAGE
from models.languagemanager import LanguageManager

# ABSTRACT BASE CLASS 
# You cannot create this class
# you must implement 3 base function play_card, bid, deal_one_card_each
# because it's the 3 states in the game when you need pick a decision 
# other functions are shared into player and bot as well
class BasePlayer(ABC):
    """Common player state and shared helper methods for human and bot players."""
    def __init__(self, name: str, language: LanguageManager = None, points: int = 0):
        self.name = name
        self.points = points
        self.lm = language
        self.hand = []
        self.bidding_score = 0 # points in auction (start from 100) Who has the most points start the round 
        self.has_bid = True # check if you are bidding in auction
        self.winned_tricks = [] # cards that you win from the turn
        self.bid_points = 0 # points for marriage 
        

    @abstractmethod
    def play_card(self, turn):
        raise NotImplementedError

    @abstractmethod
    def bid(self, current_rate):
        raise NotImplementedError

    @abstractmethod
    def deal_one_card_each(self, players, me):
        raise NotImplementedError

    def reset_hand(self):
        """Reset player state to start a new round."""
        self.bid_points = 0
        self.winned_tricks = []
        self.hand = []
        self.bidding_score = 0
        self.has_bid = True

    def calculate_round_score(self) -> int:
        """Return the rounded score from tricks and marriage points."""
        amount = sum(card.value for trick in self.winned_tricks for card in trick) + self.bid_points
        return (amount + 5) // 10 * 10 # this magic numbers rounding scores from 0-4 -> 0 from 5-9 to 10 

    def get_points(self) -> int:
        """Return the player's current total points."""
        return self.points

    def sort_by_card_value(self):
        """Sort the player's hand by card value in descending order."""
        self.hand.sort(key=attrgetter("value"), reverse=True)

    def add_points_for_marriage(self, card_played, t_parm):
        """Add marriage points when a valid Queen is played first in suit."""
        if card_played.figure == "Q" and len(t_parm.shift) == 0:
            have_king = any(
                k.figure == "K" and k.color_text == card_played.color_text
                for k in self.hand
            )
            if have_king:
                self.bid_points += MARRIAGE[card_played.color_text]
                return True
        return False

    def shuffle(self, deck):
        # in a standard game the player is person who's shuffling a deck
        """Shuffle a deck."""
        deck.shuffle_deck()

    def check_color(self, color):
        """Return all cards in hand matching the requested color."""
        return [card for e, card in enumerate(self.hand)
                if card.color == color]
    
    def check_text_color(self, color):
        """Return all cards in hand matching the requested color."""
        return [str(card.name +" " + str(e)) for e, card in enumerate(self.hand)
                if card.color_text == color]