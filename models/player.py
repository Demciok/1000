from colorama import Fore, Style, init
from operator import attrgetter
from utils.auxiliary import MARRIAGE

init()
SEPARATOR = '-'*50

class Player():
    """Represents a human player and manages hand, bidding, and trick scoring."""

    def __init__(self,name: str,points: int ):
        self.name = name
        self.points = points
        self.hand = []
        self.bidding_score = 0 # points in auction (start from 100) Who has the most points start the round 
        self.has_bid = True # check if you are bidding in auction
        self.winned_tricks = [] # cards that you win from the turn
        self.bid_points = 0 # points for marriage 
        self.have_bomb = True


    @staticmethod # decorator used to separate prompt text blocks
    def rozdziel(funkcja):

        def wrapper(*args,**kwargs):
            print(f"{SEPARATOR}")

            wynik = funkcja(*args,**kwargs)

            print(f"{SEPARATOR}")
            return wynik
        
        return wrapper


    def reset_hand(self):
        """Reset player state to start a new round."""
        self.bid_points = 0
        self.winned_tricks = []
        self.hand = []
        self.bidding_score = 0
        self.has_bid = True

    def calculate_round_score(self) -> int:
        """Return the rounded score from tricks and marriage points."""
        amount = sum([card.value for trick in self.winned_tricks for card in trick]) + self.bid_points 
        amount_round = (amount + 5 ) // 10 * 10
        return amount_round

    def get_points(self) -> int:
        """Return the player's current total points."""
        return self.points
    
    def sort_by_card_value(self):
        """Sort the player's hand by card value in descending order."""
        current_hand = [card for card in self.hand]
        current_hand.sort(key=attrgetter("value"),reverse=True)
        self.hand = current_hand

    @rozdziel
    def show_cards_in_hand(self):
        """Sort and display the player's current hand by suit."""
        self.sort_by_card_value()          # {" ".join(f"{k.name({self.hand.index(k)})})}
        print("Twoja reka tak się prezentuje") # {" | ".join([f"{k.name}({self.hand.index(k)})" for k in self.hand if k.kolor == t_kolor]) }
        print(Fore.RED + f"Czerwa: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "czerwo"]) }" )
        print(Fore.RED + f"Dzwonki: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "dzwonek"]) }" )
        print(Fore.BLACK + f"Zoladzie: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "zoladz"]) }" )
        print(Fore.BLACK + f"Wina: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "wino"]) }" )
        print(Style.RESET_ALL, end="")

    def shuffle(self,deck):
        """Shuffle a deck."""
        deck.shuffle_deck()
    
    def add_points_for_marriage(self,card_played,t_parm): # added function for marriage points
        if card_played.figure == "Q" and len(t_parm.shift) == 0: # check if the player has a matching king in hand
            have_king = any(k.figure == "K" and k.color_text == card_played.color_text for k in self.hand)
            if have_king: 
                print("Rzucil meldunek")
                self.bid_points += MARRIAGE[card_played.color_text]
                return True
        else:
            return False

    def play_card(self,t_args):
        """Prompt the player to select a card to play."""
        self. show_cards_in_hand()
        ind = input(f"Podaj numer karty, którą chcesz wyrzucić (od 0 do {len(self.hand)-1}): ")
        while ind not in [str(a) for a in range(len(self.hand))]:
            ind = input(f"Zły wybór. Wybierz kartę (od 0 do {len(self.hand)-1}): ")
        ind = int(ind)
        while True:
          #  if ind > 0 and ind < len(self.hand) and type(ind) == "int": ind = int()
            if t_args.color != None and self.hand[ind].color != t_args.color:
                if len([card for card in self.hand if card.color == t_args.color]) != 0: 
                    ind = int(input(f"Nie możesz rzucić innego koloru niż {t_args.color}. Wybierz {" | ".join([f"{k.name}({self.hand.index(k)})" for k in self.hand if k.color == t_args.color]) }: "))
                else:
                    break
            else:
                break
        picked_card = self.hand.pop(ind)
        return picked_card, self.add_points_for_marriage(picked_card,t_args)

    def bid(self,current_rate):
        """Ask the player whether to raise the bid or pass."""
        self.show_cards_in_hand()
        print(f"\nGraczu: {self.name}")
        print(f"Trwa licytacja, podbijasz stawkę o 10? Obecna najwyższa stawka {current_rate}")
        choice = input("Dokonaj wyboru 1/0 (1 - podbijam, 0 - kończę): ")
        while choice not in ["0","1"]:
            choice = input("Zły wybór, wybierz poprawnie (1/0): ")
        return int(choice)

    def deal_one_card_each(self, players, me):
        """Give one card to each opponent after winning the bid."""
        opponents = [g for g in players if g != self]
        print(f"\nMusisz dać jedną kartę każdemu przeciwnikowi")
        for opponent in opponents:
            self.sort_by_card_value()
            self.show_cards_in_hand()
            while True:
                try:
                    choice = int(input(f"Wybierz numer karty do oddania graczowi {opponent.name}: "))
                    if 0 <= choice < len(self.hand):
                        dealt_card = self.hand.pop(choice)
                        opponent.hand.append(dealt_card)
                        break
                    else:
                        print("Niepoprawny numer karty. Spróbuj ponownie.")
                except ValueError:
                    print("Wprowadź liczbę całkowitą!")
