from models.bot import Bot
from models.gracz import Gracz
from models.talia import Talia
from game.gra import Gra
from utils.pomocnicze import wybierz_tryb, nazwij_gracza

def main():
    if wybierz_tryb():
        Gracz1 = Gracz("ola",0) # nazwij_gracz()
        Gracz2 = Gracz("ula",0) # nazwij_gracz()
        Gracz3 = Gracz("ala",0) # nazwij_gracz()
    else:
        Gracz1 = Gracz("czlowiek",0) 
        Gracz2 = Bot("LLama",0)
        Gracz3 = Bot("Claude",0)

    granie = Gra([Gracz1,Gracz2,Gracz3])
    talia_kart = Talia()
    talia_kart.stworz_talie()
     
    granie.zaczynajacy_gre.potasuj_talie(talia_kart)
    while True:
        talia_kart.rozdaj_karty(granie)
        granie.licytacja()
        granie.runda()
        granie.zakoncz_runde()
        granie.pokaz_wyniki()
        granie.gracze[granie.zaczynajacy_licytacje].potasuj_talie(talia_kart)


if __name__ == "__main__":
    main()

# rzucanie bomby moze ciekawa mechanika mozna dodac bo w sumie sie przyda
# dodac jakies poprawki UI graficzne 
# dodac tą bombe moze 
# dodac mechanike ze jak sie dojdzie do > 880 to trzeba wygrac gre tylko licytujac 
# opisać jutro jak to wszysztko wygląda co robi dana klasa 
# zasady dodatkowo i napisac co bym chcial zeby usprawnic 
# wytlumaczyc czemu wszystkie zmienne są po polsku  
# pozniej zrobic wersje po angielsku 
# jak zrobie wersje po
# na koniec sprobowac to pozniej postawic na stronce zeby byl cli i mozna bylo sobie grac
# i zaczac robic swoja strone portfolio dodac najciekawsze linki  

# jak rzucilem wino claude rzucil asa i wygrał 
# i cos wypisuje na ekran losowo