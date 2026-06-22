from colorama import Fore, Style, init
from operator import attrgetter
from utils.auxiliary import MARRIAGE
from .baseplayer import BasePlayer
from .languagemanager import LanguageManager
init()
SEPARATOR = '-'*50

class Player(BasePlayer):
    """Represents a human player and manages hand, bidding, and trick scoring."""

    def _language_manager(self):
        if self.lm is None:
            self.lm = LanguageManager()
        return self.lm

    def _text(self, message_id, **kwargs):
        text = self._language_manager().get_text(message_id)
        if text is None:
            return None

        try:
            return text.format(**kwargs)
        except Exception:
            return text

    def _print_text(self, message_id, **kwargs):
        return self._language_manager().print_by_id(message_id, **kwargs)

    def _input_text(self, prompt_id, **kwargs):
        return self._language_manager().input_by_id(prompt_id, **kwargs)

    def _print_separator(self):
        print(SEPARATOR)

    @staticmethod # decorator used to separate prompt text blocks
    def rozdziel(funkcja):

        def wrapper(*args,**kwargs):
            args[0]._print_separator()

            wynik = funkcja(*args,**kwargs)

            args[0]._print_separator()
            return wynik
        
        return wrapper

    
    @rozdziel
    def show_cards_in_hand(self):
        """Sort and display the player's current hand by suit."""
        self.sort_by_card_value()          
        self._print_text(16)
        print(Fore.RED + self._text(17, cards=' | '.join(self.check_text_color('czerwo'))))
        print(Fore.RED + self._text(18, cards=' | '.join(self.check_text_color('dzwonek'))))
        print(Fore.BLACK + self._text(19, cards=' | '.join(self.check_text_color('zoladz'))))
        print(Fore.BLACK + self._text(20, cards=' | '.join(self.check_text_color('wino'))))
        print(Style.RESET_ALL, end="")


    def play_card(self,t_args):
        """Prompt the player to select a card to play."""
        self. show_cards_in_hand()
        ind = self._input_text(30, max_index=len(self.hand) - 1)
        while ind not in [str(a) for a in range(len(self.hand))]:
            ind = self._input_text(31, max_index=len(self.hand) - 1)
        ind = int(ind)
        while True:
          #  if ind > 0 and ind < len(self.hand) and type(ind) == "int": ind = int()
            if t_args.color != None and self.hand[ind].color != t_args.color:
                if len([card for card in self.hand if card.color == t_args.color]) != 0: 
                    options = ' | '.join([f"{k.name}({self.hand.index(k)})" for k in self.hand if k.color == t_args.color])
                    ind = int(self._input_text(32, color=t_args.color, choices=options))
                else:
                    break
            else:
                break
        picked_card = self.hand.pop(ind)
        return picked_card, self.add_points_for_marriage(picked_card,t_args)

    def bid(self,current_rate):
        """Ask the player whether to raise the bid or pass."""
        self.show_cards_in_hand()
        self._print_text(21, player=self)
        self._print_text(22, current_rate=current_rate)
        choice = self._input_text(33)
        while choice not in ["0","1"]:
            choice = self._input_text(34)
        return int(choice)

    def deal_one_card_each(self, players, me):
        """Give one card to each opponent after winning the bid."""
        opponents = [g for g in players if g != self]
        self._print_text(23)
        for opponent in opponents:
            self.sort_by_card_value()
            self.show_cards_in_hand()
            while True:
                try:
                    choice = int(self._input_text(35, opponent=opponent))
                    if 0 <= choice < len(self.hand):
                        dealt_card = self.hand.pop(choice)
                        opponent.hand.append(dealt_card)
                        break
                    else:
                        self._print_text(24)
                except ValueError:
                    self._print_text(25)