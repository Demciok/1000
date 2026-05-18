import pexpect.popen_spawn
import sys
import os
import time

class Test():
    def __init__(self):
        self.python = sys.executable
        self.skrypt_gry = r"../main.py"
    
    def born_child(self):
        return pexpect.popen_spawn.PopenSpawn([self.python,self.skrypt_gry])
    
    def main_loop(self):
        child = self.born_child()
        child.logfile = sys.stdout.buffer # w fazie rozwoju 
        child.expect('Witaj w grze w 1000')
        child.sendline('0') #
        child.expect("Gre rozpoczyna")
    

# dobra jak to ma wygladac ?
# wybieramy tryb z botami bo go chcemy w sumie najbardziej przetestować bo tam są errory
# licytacja zawsze 0 i gramy dalej 
# mozliwy scenariusz ze gramy bez licytacji i musimy oddac karty wtedy wysylamy 9 8 po kolei ( najslabsze karty)
# pozniej zawsze wysylamy 0, jeżeli nie możemy wysłać 0 to czekamy na tekst
# Nie możesz rzucić innego koloru niż â™¦. Wybierz 10_dzwonek(1) | K_dzwonek(4) | J_dzwonek(6):
# tutaj by sie przydało jakas funkcja 
# taka mozliwosc jak ponizej 
# Gra zapisuje temp_state.txt.
# Test czeka na komunikat child.expect('ZAPISANO').
# Test otwiera plik, czyta wartość i robi child.sendline()
# i jezeli juz to zrobimy to koniec w sumie bedzie mozna testowac bez konca 

# teraz pytanie czy musimy lapac pierwszy wypisany tekst przez expect czy jakikolwiek jaki sie pojawi na ekranie?
# czy może zrobimy jeszcze klase tutaj zeby to ladnie banglało 
skrypt_gry = r"c:/Things/A programming journey/the thousand game ( 1000)/repo/main.py"
python = sys.executable

print("test")
child = pexpect.popen_spawn.PopenSpawn([python,skrypt_gry])
child.logfile = sys.stdout.buffer
try:
    child.expect('Witaj w grze w 1000') # start menu 
    print("Menu")
    child.sendline('0')
    time.sleep(2)
    child.expect("Graczu")
    child.sendline('0')
    child.expect("Gre")
    child.sendline('0')

    while True:
        index = child.expect([
            'Kolejny krok',              # Sukces (dopasuj do swojej gry)
            r'Wybierz .*\((\d+)\):'      # Błąd - szukamy liczby w nawiasie przed dwukropkiem
        ])

        if index == 0:
            print("Karta zaakceptowana!")
            break
            
        elif index == 1:
            # Wyciągamy to, co wpadło w nawias (\d+) w regexie
            poprawny_indeks = child.match.group(1).decode('utf-8')
            print(f"Oho! Zły kolor. Gra podpowiada indeks: {poprawny_indeks}")
            
            # Wysyłamy poprawną kartę
            child.sendline(poprawny_indeks)
    
except pexpect.EOF:
    print("Gra zakończyła się niespodziewanie (EOF).")
except pexpect.TIMEOUT:
    print("Gra przestała odpowiadać (Timeout) - może czeka na inny tekst?")