from .player import Player
from utils.auxiliary import MARRIAGE
import random


class Bot(Player): # funkcja dziala jak bot ma meldunki to zwraca wartość
    def check_marriages(self):
        queens = {k.color_text for k in self.hand if k.figure == "Q"} # set()
        kings = {k.color_text for k in self.hand if k.figure == "K"} # set()
        owned_marriages = queens & kings # część wspólna
        if len(owned_marriages) == 0:
            return []
        else:
            return owned_marriages

    def add_marriages_points_end_round(self):
        return sum([MARRIAGE[color_mar] for color_mar in self.check_marriages()])
    
    def calculate_hand(self):
        return sum(card.value for card in self.hand)
    
    def calculate_max_bid(self):
        score = 0
        meldunki_punkty = self.add_marriages_points_end_round()
        score += meldunki_punkty

        for card in self.hand:
            if card.value == 11: # As
                score += 15
            elif card.value == 10: # 10
                score += 10
            elif card.value == 4: # Król
                score += 4

        for color in ["wino", "zoladz", "dzwonek", "czerwo"]:
            card_in_color = len(self.check_color(color))
            if card_in_color >= 4:
                score += 20
        
        max_bid = (score // 10 ) * 10
        if meldunki_punkty == 0 and max_bid > 120:
            max_bid = 120
        
        return max_bid
    
    def bid(self, current_rate): # pomyslec jeszcze nad tym 
        if current_rate < self.calculate_max_bid() :
            print(f"Bot: {self.name} podbija stawke ! ")
            return 1
        else:
            print(f"Bot: {self.name} konczy licytacje ")
            return 0

    def check_figure(self,figure):
        return [e for e,card in enumerate(self.hand) 
                if card.figure == figure]
    
    def check_color(self,color):
        return [card for e,card in enumerate(self.hand) 
                if card.color == color ]     
    
    def return_lowest_value(self,color):
        self.sort_by_card_value()
        return [card for card in self.hand 
                if card.color == color ][-1]
    
    def marriage_in_threecards(self,t_parm): # i forget what this functio does 
        return any([karta for karta in t_parm.shift.values() 
                    if karta.color == t_parm.marriage_color])
    
    def check_shift(self,t_parm): # tu zawsze nam zwraca karte ktora mamy zagrac
        cards_in_color = self.check_color(t_parm.color)
        if len(cards_in_color) > 0:
            if self.marriage_in_threecards(t_parm):
                return self.return_lowest_value(t_parm.color)
            c = []
            if len(t_parm.shift) == 2:
                for sz_card in t_parm.shift.values():
                    c.append([card for card in self.hand 
                              if sz_card.value < card.value])
                h_var = list(set(c[0])- set(c[1]))
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
        else: # tu jest blad 
            if t_parm.marriage_color == None:
                self.sort_by_card_value()
                return self.hand[-1]
            else: # tu cos nie dziala 
                self.sort_by_card_value()
                cards = self.check_color(t_parm.marriage_color)
                if len(cards) > 0:

                    return cards[0]
                else:

                    return self.hand[-1]
            
    def show_cards(self):
        return [card.name for card in self.hand]
    def simple_logic(self,turn_parms):
        if len(turn_parms.shift) == 0: # jezeli zaczyna ture rzuca najpierw wszystkie aces(bo wiadomo ze wygra) pozniej wszystkie meldunki, na koniec karte najwyzsza 
            aces = self.check_figure("A")
            cards_in_marriage_color = [e for e,card in enumerate(self.hand) if card.color_text == turn_parms.marriage_color]
            meld = self.check_marriages() # jak zaczyna to musi wyrzucić wszystkie aces
            if len(aces) > 0:
                return self.hand.pop(aces[0]) 
            if len(meld) > 0: # szuka cards z figure dama i kolorem meldunku zwraca index a pozniej popuje i zwraca karte
                return self.hand.pop([e for e,card in enumerate(self.hand) if card.color_text == list(meld)[0] and card.figure == "Q"][0])
            if len(cards_in_marriage_color) > 0:
                return self.hand.pop(cards_in_marriage_color[0])
            self.sort_by_card_value()
            return self.hand.pop(0)
        if len(turn_parms.shift) == 1:
            return self.hand.pop(self.hand.index(self.check_shift(turn_parms)))
        if len(turn_parms.shift) == 2:
            return self.hand.pop(self.hand.index(self.check_shift(turn_parms)))
        
    def advance_logic(self, turn_parms):
        pass # kiedys zrobie jakas lepsza    
        
    def play_card(self, turn_parms):
        k = self.simple_logic(turn_parms)
        print(f"{"-"*50}\n {self.name} rzuca {k.name} \n {"-"*50}")
        d = self.add_points_for_marriage(k,turn_parms)
        return k,d
        

    def deal_one_card_each(self,players,winner):
        """Funkcja ktora byla poniewaz nie chcialo mi sie robic """
        d = players 
        d.remove(winner) 
        for a in range(2): 
            if a == 0:
                picked = random.choice(self.hand)
                print(f"{self.name} daje {picked} graczu {d[a].name}")
                d[a].hand.append(picked)
                self.hand.remove(picked)
            else:
                picked = random.choice(self.hand)
                print(f"{self.name} daje {picked} graczu {d[a].name}")
                d[a].hand.append(picked)
                self.hand.remove(picked)
        d.append(winner)
        self.sort_by_card_value()