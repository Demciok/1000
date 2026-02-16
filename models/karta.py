class Karta():
    def __init__(self,kolor="",figura="",wartosc="",nazwa=""):
        self.kolor = kolor
        self.figura = figura
        self.wartosc = wartosc
        self.kolor_slownie = ""
        self.nazwa = self.figura + nazwa

    def __str__(self):
        return self.nazwa
    
    def get_wartosc(self):
        """getter"""
        return self.wartosc
    
    def set_wartosc(self,nowa):
        """setter"""
        self.wartosc = nowa