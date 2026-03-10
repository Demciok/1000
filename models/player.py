from colorama import Fore, Style, init
from operator import attrgetter
from utils.auxiliary import MARRIAGE
import random
init()

class Player():
    def __init__(self,name: str,points: int ):
        self.name = name
        self.points = points
        self.hand = []
        self.bidding_score = 0
        self.has_bid = True
        self.winned_tricks = [] 
        self.bid_points = 0

    def reset_hand(self):
        """Resetuje klase gracze by zacząć nową runde"""
        self.bid_points = 0
        self.winned_tricks = []
        self.hand = []
        self.bidding_score = 0
        self.has_bid = True

    def calculate_round_score(self) -> int:
        """Zwraca sume zebranych punktów z kart i meldunku"""
        amount = sum([card.value for trick in self.winned_tricks for card in trick]) + self.bid_points 
        amount_round = (amount + 5 ) // 10 * 10
        return amount_round

    def get_points(self) -> int:
        """Zwraca posiadane punkty"""
        return self.points
    
    def sort_by_card_value(self):
        """Sortuje karty na rece po wartosciach"""
        current_hand = [card for card in self.hand]
        current_hand.sort(key=attrgetter("value"),reverse=True)
        self.hand = current_hand

    def show_cards_in_hand(self):
        """Sortuje i wyświetla posiadane obecnie karty""" 
        self.sort_by_card_value()          # {" ".join(f"{k.name({self.hand.index(k)})})}
        print("Twoja reka tak się prezentuje") # {" | ".join([f"{k.name}({self.hand.index(k)})" for k in self.hand if k.kolor == t_kolor]) }
        print(Fore.RED + f"Czerwa: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "czerwo"]) }" )
        print(Fore.RED + f"Dzwonki: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "dzwonek"]) }" )
        print(Fore.BLACK + f"Zoladzie: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "zoladz"]) }" )
        print(Fore.BLACK + f"Wina: {" | ".join([f"{k.name} ({self.hand.index(k)})" for k in self.hand if k.color_text == "wino"]) }" )
        print(Style.RESET_ALL, end="")

    def postpone_deck(self,deck):
        """Pozwala przełożyć karty graczowi"""
        print("Wybierasz od góry jak przełożyć karty np. 10 przekladasz 10 górnych kart na dół(0-24): ")
        choice = int(input(""))
        while (choice not in [0,24]):
            choice = int(input("Wybierz poprawny zakres"))
        if (choice in [0,24]):
            print("Nie przekladasz wiec grajmy")
            return 
        postpone_deck = deck.deck[choice:deck.size-1] + deck.deck[0:choice]
        deck.deck = postpone_deck
    
    def add_points_for_marriage(self,card_played,t_parm): # zmiana dodana funkcja za meldunek
        if card_played.figure == "Q" and len(t_parm.shift) == 0: # sprawdz czy gracz mial na rece krola o tym samym kolorze 
            have_king = any(k.figure == "K" and k.color_text == card_played.color_text for k in self.hand)
            if have_king: 
                print("Rzuciles meldunek")
                self.bid_points += MARRIAGE[card_played.color_text]
                return True
        else:
            return False

    def play_card(self,t_args):
        """"Mechanizm zagrywania karty przez gracza"""
        self. show_cards_in_hand()
        ind = input(f"Podaj numer karty, która chcesz wyrzucić (od 0 do {len(self.hand)-1}): ")
        while ind not in [str(a) for a in range(len(self.hand))]:
            ind = input(f"Zły choice. Wybierz karte (od 0 do {len(self.hand)-1}): ")
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
        """Gracz dokonuje wybór licytuje albo przestaje licytowac"""
        self.show_cards_in_hand()
        print(f"{"-"*50}\nGraczu: ", self.name)
        print(f"Trwa licytacja, podbijasz stawke o 10 ? Obecna najwyższa stawka {current_rate}")
        choice = input("Dokonaj choiceu 1/0 (1 - podbijam, 0 - koncze ): ")
        while choice not in ["0","1"]:
            choice = input("Zły wybór wybierz poprawnie (1/0): ")
        return int(choice)

    def deal_one_card_each(self, players, me):
        # 1. Find opponents (everyone except us)
        opponents = [g for g in players if g != self]
        
        print(f"\nYou must give one card to each opponent")
        for opponent in opponents:
            self.sort_by_card_value()
            self.show_cards_in_hand()
            while True:
                try:
                    choice = int(input(f"Select card number for player {opponent.name}: "))
                    if 0 <= choice < len(self.hand):
                        dealt_card = self.hand.pop(choice)
                        opponent.hand.append(dealt_card)
                        break
                    else:
                        print("Invalid card number. Try again.")
                except ValueError:
                    print("Please enter an integer!")


    def shuffle(self,deck):
        """Shuffle a deck"""
        deck.shuffle_deck()