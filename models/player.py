from colorama import Fore, Style, init
from operator import attrgetter
from utils.auxiliary import MARRIAGE
from .baseplayer import BasePlayer
init()
SEPARATOR = '-'*50

class Player(BasePlayer):
    """Represents a human player and manages hand, bidding, and trick scoring."""

    @staticmethod # decorator used to separate prompt text blocks
    def rozdziel(funkcja):

        def wrapper(*args,**kwargs):
            print(f"{SEPARATOR}")

            wynik = funkcja(*args,**kwargs)

            print(f"{SEPARATOR}")
            return wynik
        
        return wrapper

    
    @rozdziel
    def show_cards_in_hand(self):
        """Sort and display the player's current hand by suit."""
        self.sort_by_card_value()          
        print("Twoja reka tak się prezentuje") 
        print(Fore.RED + f"Czerwa: {" | ".join(self.check_text_color("czerwo")) }" )
        print(Fore.RED + f"Dzwonki: {" | ".join(self.check_text_color("dzwonek")) }" )
        print(Fore.BLACK + f"Zoladzie: {" | ".join(self.check_text_color("zoladz")) }" )
        print(Fore.BLACK + f"Wina: {" | ".join(self.check_text_color("wino")) }" )
        print(Style.RESET_ALL, end="")


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
