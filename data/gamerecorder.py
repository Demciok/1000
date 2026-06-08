import json
import datetime

class Gamerecorder():
    def __init__(self):
        self.history = {
            "timestart": str(datetime.datetime.now()),
            "rounds": []   
        }
        self.round_number = 1
        self.current_round = self.new_round()
        self.gameid = "gra" + self.history["timestart"]

    def new_round(self):
       return {
            "round": self.round_number,
            "start_state": {},
            "bidding": [],
            "turns": [],
            "results": []
        }
    
    def save_round(self):
        self.history["rounds"].append(self.current_round)
        self.round_number = self.round_number+1
        self.current_round = self.new_round()
        # print(self.history)


    def record_bid(self,*args): # zapisz kto zaczynal licytacje jak wygladala licytacja tak/nie wynik
        self.current_round["bidding"].append(args)
    
    def record_start_game(self, hands, threecards): # zapisz reke kazdego gracza i trzy karty na srodku
        self.current_round["start_state"] = [hands, threecards]

    def record_turn(self, *args): # zapisuje jakie karty dostal wygrany licytacji - 1 tura = jaka karte dostal kazdy z graczy 
        self.current_round["turns"].append(args)

    def record_points(self,*args): # zapisuje wyniki na koniec rundy kto ile dostal 
        self.current_round["results"].append(args)
        

