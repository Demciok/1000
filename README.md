# Gra w 1000

Gra karciana w 1000 napisana w Pythonie głównie dla celów nauki i satysfakcji.


# Wstep 
Witaj w cyfrowej wersji klasycznej polskiej gry karcianej z PRL-u Tysiąc. Projekt ten ma cele edukacyjne, nauke nad rozbudowanymi projektami, obsługę gita i ogólną satysfakcję, żeby można było zagrać w 1000 w wersji na komputer.

## Sekcje:
- [Przebieg Gry](#przebieg-gry)
- [Zasady Gry](#zasady-gry)
- [Struktura Projektu](#struktura-projektu)
- [Instalacja i Uruchomienie](#instalacja-i-uruchomienie)
- [Struktura Projektu](#struktura-projektu)
- [Instalacja i Uruchomienie](#instalacja-i-uruchomienie)
- [Przyszłe Aktualizacje](#przyszłe-aktualizacje)
- [Contributing](#contributing)
- [License](#license)

## Przebieg Gry
1. Wybiera się gracza, który ma zacząć rozdawać karty
2. Gracz tasuje karty i osobie siedzacej po lewo ( zgodnie z wskazowkami zegara) daje przełożyć karty 
3. Gracz rozdaje po 7 kart każdemu z graczy i tworzy kupke 3-kart.
4. Rozpoczyna się licytacja, następny gracz od tasującego rozpoczyna licytacje wynikiem 100, następnie każdy może podbić stawke lub zrezgynować
5. Odkrywana jest kupka z 3 karta, a wygrany licytacji bierze do siebie te 3 karty.
6. Gracz ten ma 10 kart, musi rozdać po jednej każdemu graczu, by zaczęła się rozgrywka.
7. Grę zaczyna osoba, która wygrała licytacje.
8. Na koniec gry liczy się punkty, i rozpoczyna kolejna runda, nastepny gracz rozdaje karty. 

## Zasady Gry.

W grze obowiązują zasady, a każda karta ma swoją przypisaną własność:
| Karta | Wartosc |
|-------|---------|
|  AS   |   11    |
|  10   |   10    |
| KROL  |   04    |
| DAMA  |   03    |
| JOP   |   02    |
|  9    |   00    |

Obowiązujące zasady:
- W grze istnieją meldunki (Serce, Dzwonek, Żołądź, Wino), które po zagraniu dodają graczowi odpowiednio (100, 80 , 60 ,40) punktów do wyniku 
- Meldunek składa się z Damy i Króla
- Aby zameldować należy rzucić Dame 
- Meldunek można rzucić jedynie zaczynając ture 
- Po złożeniu meldunku karta z koloru meldunku bije wszystkie inne karty bez względu na figurę
- Karty należy rzucać w kolorze jakim została położona pierwsza karta na stół
- Gdy wystąpi sytuacja, że nie ma się karty o tym samym kolorze, należy rzucić jakąkolwiek inną, zważając na to, że niezależnie od figury, jeżeli nie jest w kolorze pierwszej zagranej karty, karta jest bita 
- W licytacji można maksymalnie podbijać do 120, jeżeli nie ma się meldunku na ręce 
- Na koniec rundy gdy gracz nie zdobył wymaganej liczby punktów, która zalicytował, należy oddjąć mu te punkty
- Gre wygrywa gracz, który pierwszy przekroczy 1000 punktów 
- Poniżej 1000 i powyżej 860 graczu nie zapisuje się punktów zdobytych pod koniec rundy
- Gracz musi wygrać licytacje i zdobyć odpowiednia ilość punktów, aby wygrać grę 

## Struktura Projektu
```
gra-1000/
├── main.py           # Rozpoczęcie grt
├── gra.py            # Główna logika gry, rozdawanie, rundy
├── gracz.py          # Klasa Gracz - reprezentuje gracza 
├── bot.py            # Klasa Bot - przeciwnik Ai
├── talia.py          # Klasa Talii
├── licytacja.py      # Logika licytacji
└── README.md
```

### Główne klasy:

**`Gra`** - Zarządza przebiegiem gry, rundami, punktacją
**`Gracz`** - Reprezentuje gracza, trzyma karty, punkty
**`Bot`** - Dziedziczy po Gracz'u, implementuje prostą logike do wyboru kart
**`Karta`** - Reprezentacka pojedynczej karty (kolor, figura, wartość)

## Instalacja i Uruchomienie

### Wymagania
- Python 3.8+
- pip

### Instalacja
```bash
#git clone https://github.com/Demciok/tysiąc.git
cd gra-1000
pip install -r requirements.txt  
```

### Uruchomienie
```bash
python main.py  
```

## Przyszłe akutalizacji:
- [ ] Dodac zasadę bomby 
- [ ] Napisać zaawasowana logike rzucania kart dla bota
- [ ] Zrobic wersje graficzna gry
- [ ] Dodac opcje zapisu stanu gry 
- [ ] Umozliwic gre online multiplayer
- [ ] Make en version

## Contributing

Projekt edukacyjny, pull requesty mile widziane!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Ten projekt jest na licencji MIT. Zobacz plik LICENSE dla szczegółów.


