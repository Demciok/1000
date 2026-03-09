from models.bot import Bot
from models.gracz import Gracz
from models.talia import Talia
from game.gra import Gra
from utils.pomocnicze import wybierz_tryb, nazwij_gracza

def main():
    if wybierz_tryb():
        Gracz1 = Gracz("gracz1",0) # nazwij_gracz()
        Gracz2 = Gracz("gracz2",0) # nazwij_gracz()
        Gracz3 = Gracz("gracz3",0) # nazwij_gracz()
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
