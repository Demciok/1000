from .baseplayer import BasePlayer
from utils.auxiliary import MARRIAGE
from .languagemanager import LanguageManager
import random


class Bot(BasePlayer):
    """A bot-controlled player with bidding and play decision logic."""

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

    def check_figure(self, figure):
        """Return indices of cards matching the requested figure."""
        return [e for e, card in enumerate(self.hand)
                if card.figure == figure]

    def return_lowest_value(self, color):
        """Return the lowest-value card of the specified color."""
        self.sort_by_card_value()
        return [card for card in self.hand
                if card.color == color][-1]

    def marriage_in_threecards(self, t_parm):
        """Return whether the trick includes a card in the marriage color."""
        return any([karta for karta in t_parm.shift.values()
                    if karta.color == t_parm.marriage_color])

    def check_marriages(self):
        """Return a set of marriage colors the bot holds in its hand."""
        queens = {k.color_text for k in self.hand if k.figure == "Q"}
        kings = {k.color_text for k in self.hand if k.figure == "K"}
        owned_marriages = queens & kings
        if len(owned_marriages) == 0:
            return []
        else:
            return owned_marriages
        
    def sum_marriages_points(self):
        """Calculate total marriage bonus points for the end of round."""
        return sum([MARRIAGE[color_mar] for color_mar in self.check_marriages()])
    

    def calculate_max_bid(self):
        """Estimate the maximum bid the bot is willing to make."""
        score = 0
        marriage_points = self.sum_marriages_points()
        score += marriage_points

        for card in self.hand:
            if card.value == 11:  # Ace
                score += 15
            elif card.value == 10:  # Ten
                score += 10
            elif card.value == 4:  # King
                score += 4

        for color in ["wino", "zoladz", "dzwonek", "czerwo"]:
            card_in_color = len(self.check_color(color))
            if card_in_color >= 4:
                score += 20

        max_bid = (score // 10) * 10
        if marriage_points == 0 and max_bid > 120:
            max_bid = 120

        return max_bid


    def check_shift(self, t_parm):
        """Choose the best card to play when following suit."""
        cards_in_color = self.check_color(t_parm.color)
        if len(cards_in_color) > 0:
            if self.marriage_in_threecards(t_parm):
                return self.return_lowest_value(t_parm.color)
            c = []
            if len(t_parm.shift) == 2:
                for sz_card in t_parm.shift.values():
                    c.append([card for card in self.hand
                              if sz_card.value < card.value])
                h_var = list(set(c[0]) - set(c[1]))
                if len(h_var) > 0 and h_var[0] != 0:
                    return h_var[0]
                else:
                    return self.return_lowest_value(t_parm.color)
            else:
                higher_cards = [card for card in self.hand
                                if list(t_parm.shift.values())[0].value < card.value]
                if any(higher_cards):
                    return higher_cards[0]
                else:
                    return self.return_lowest_value(t_parm.color)
        else:
            if t_parm.marriage_color is None:
                self.sort_by_card_value()
                return self.hand[-1]
            else:
                self.sort_by_card_value()
                cards = self.check_color(t_parm.marriage_color)
                if len(cards) > 0:
                    return cards[0]
                else:
                    return self.hand[-1]

    def simple_logic(self, turn_parms):
        """Execute the bot's simple play logic for the current turn."""
        if len(turn_parms.shift) == 0:
            aces = self.check_figure("A")
            cards_in_marriage_color = [e for e, card in enumerate(self.hand)
                                       if card.color_text == turn_parms.marriage_color]
            meld = self.check_marriages()
            if len(aces) > 0:
                return self.hand.pop(aces[0])
            if len(meld) > 0:
                return self.hand.pop([e for e, card in enumerate(self.hand)
                                      if card.color_text == list(meld)[0] and card.figure == "Q"][0])
            if len(cards_in_marriage_color) > 0:
                return self.hand.pop(cards_in_marriage_color[0])
            self.sort_by_card_value()
            return self.hand.pop(0)
        if len(turn_parms.shift) == 1:
            return self.hand.pop(self.hand.index(self.check_shift(turn_parms)))
        if len(turn_parms.shift) == 2:
            return self.hand.pop(self.hand.index(self.check_shift(turn_parms)))
        
    def bid(self, current_rate):
        """Decide whether the bot raises the bid or drops out."""
        if current_rate < self.calculate_max_bid():
            self._print_text(12, bot=self)
            return 1
        else:
            self._print_text(13, bot=self)
            return 0

    def play_card(self, turn_parms):
        """Play a card according to bot strategy and return it with marriage points."""
        card = self.simple_logic(turn_parms)
        self._print_text(14, bot=self, card=card)
        mar = self.add_points_for_marriage(card, turn_parms)
        return card, mar

    def deal_one_card_each(self, players, winner):
        """Deal one random card each to the other two players."""
        remaining = players
        remaining.remove(winner)
        for a in range(2):
            picked = random.choice(self.hand)
            self._print_text(15, bot=self, picked=picked, recipient=remaining[a])
            remaining[a].hand.append(picked)
            self.hand.remove(picked)
        remaining.append(winner)
        self.sort_by_card_value()