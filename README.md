# 🇵🇱  Polish version below
# Thousand (1000) - Polish Card Game


A digital implementation of the classic Polish card game "Tysiąc" (Thousand) written in Python - educational project.

## About

Welcome to a digital version of the classic Polish card game from the PRL era called "Tysiąc" (Thousand). This project serves educational purposes: learning complex projects, Git workflow, and the satisfaction of creating a playable computer version of the game.

## Table of Contents
- [Game Flow](#game-flow)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Future Updates](#future-updates)
- [Contributing](#contributing)
- [License](#license)

## Game Flow

1. A player is chosen to deal cards
2. The dealer shuffles the cards and lets the player to their left cut the deck
3. The dealer gives 7 cards to each player and creates a 3-card stack (mustered cards)
4. Bidding begins - the player after the dealer starts bidding at 100, then each player can raise the bid or pass
5. The 3-card stack is revealed and the bidding winner takes these 3 cards
6. This player now has 10 cards and must distribute one card to each player before gameplay begins
7. The player who won the bidding starts the game
8. At the end of the round, points are counted and a new round begins - the next player deals cards

## Game Rules

Each card has an assigned value:

| Card  | Value |
|-------|-------|
| Ace   | 11    |
| 10    | 10    |
| King  | 4     |
| Queen | 3     |
| Jack  | 2     |
| 9     | 0     |

### Rules:
- There are marriages (Hearts, Diamonds, Clubs, Spades) which add 100, 80, 60, 40 points respectively when declared
- A marriage consists of a King and Queen of the same suit
- To declare a marriage, you must lead with the Queen
- Marriages can only be declared when leading a trick
- After declaring a marriage, cards of that suit beat all other cards regardless of rank
- You must follow suit (play the same suit as the leading card)
- If you don't have the leading suit, you can play any card, but it will be beaten regardless of rank unless it's a trump
- In bidding, you can raise up to 120 maximum if you don't have a marriage
- At the end of a round, if a player didn't score the bid amount, those points are subtracted from their score
- The game is won by the first player to exceed 1000 points
- Between 860 and 1000 points, earned points are not recorded (barrel rule)
- A player must win the bidding and score the required points to win the game

## Project Structure
```
1000/
├── game/
│   └── game.py          # Main game logic, rounds, scoring
├── models/
│   ├── bot.py           # Bot class - AI opponent
│   ├── card.py          # Card class - single card
│   ├── deck.py          # Deck class - card deck
│   ├── player.py        # Player class - represents a player
│   └── turn.py          # Turn class - trick logic
├── resources/
│   └── cards.json       # Card data (optional)
├── utils/
│   └── auxiliary.py    # Helper functions
├── LICENSE              # MIT License
├── main.py              # Application entry point
├── README.md            # Description
└── requirements.txt     # Python dependencies
```

### Main Classes:

**`Game`** - manages game flow, rounds, scoring  
**`Player`** - represents a player, holds cards, points  
**`Bot`** - inherits from `Player`, implements simple AI logic  
**`Card`** - represents a single card (suit, rank, value)  
**`Deck`** - card deck, shuffling, dealing  
**`Turn`** - logic for a single trick/turn

## Installation and Setup

### Requirements
- Python 3.8+
- pip

### Installation
```bash
git clone https://github.com/Demciok/1000.git
cd 1000
pip install -r requirements.txt  
```

### Running the Game
```bash
python main.py  
```

## Future Updates
- [ ] Add bomb rule
- [ ] Implement advanced AI card-playing logic
- [ ] Create graphical version of the game
- [ ] Add save game state feature
- [ ] Enable online multiplayer
- [ ] Complete Polish version documentation

## Contributing

Educational project - pull requests welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# 🇵🇱 Wersja Polska / Polish Version

# Gra w 1000

Gra karciana w 1000 napisana w Pythonie - projekt edukacyjny.

## Wstęp 
Witaj w cyfrowej wersji klasycznej polskiej gry karcianej z PRL-u "Tysiąc". Projekt ma cele edukacyjne: naukę rozbudowanych projektów, obsługę Gita oraz satysfakcję z gry komputerowej w 1000.

## Spis treści
- [Przebieg Gry](#przebieg-gry)
- [Zasady Gry](#zasady-gry)
- [Struktura Projektu](#struktura-projektu-1)
- [Instalacja i Uruchomienie](#instalacja-i-uruchomienie)
- [Przyszłe Aktualizacje](#przyszłe-aktualizacje)
- [Contributing](#contributing-1)
- [Licencja](#licencja)

## Przebieg Gry
1. Wybiera się gracza, który ma zacząć rozdawać karty
2. Gracz tasuje karty i osobie siedzącej po lewej (zgodnie ze wskazówkami zegara) daje przełożyć karty 
3. Gracz rozdaje po 7 kart każdemu z graczy i tworzy kupkę 3 kart
4. Rozpoczyna się licytacja - następny gracz od tasującego rozpoczyna licytację wynikiem 100, następnie każdy może podbić stawkę lub zrezygnować
5. Odkrywana jest kupka z 3 kart, a wygrany licytacji bierze do siebie te 3 karty
6. Gracz ten ma 10 kart i musi rozdać po jednej każdemu graczu, aby zaczęła się rozgrywka
7. Grę zaczyna osoba, która wygrała licytację
8. Na koniec gry liczy się punkty i rozpoczyna kolejna runda - następny gracz rozdaje karty

## Zasady Gry

W grze obowiązują zasady, a każda karta ma swoją przypisaną wartość:

| Karta | Wartość |
|-------|---------|
| AS    | 11      |
| 10    | 10      |
| KRÓL  | 4       |
| DAMA  | 3       |
| WALET | 2       |
| 9     | 0       |

### Obowiązujące zasady:
- W grze istnieją meldunki (Serce, Dzwonek, Żołądź, Wino), które po zagraniu dodają graczowi odpowiednio 100, 80, 60, 40 punktów do wyniku 
- Meldunek składa się z Damy i Króla tego samego koloru
- Aby zameldować należy rzucić Damę 
- Meldunek można rzucić jedynie zaczynając turę 
- Po złożeniu meldunku karty z koloru meldunku biją wszystkie inne karty bez względu na figurę
- Karty należy rzucać w kolorze, jakim została położona pierwsza karta na stół
- Gdy nie ma się karty o tym samym kolorze, należy rzucić jakąkolwiek inną kartę, zważając na to, że niezależnie od figury, jeżeli nie jest w kolorze pierwszej zagranej karty, karta jest bita 
- W licytacji można maksymalnie podbijać do 120, jeżeli nie ma się meldunku na ręce 
- Na koniec rundy, gdy gracz nie zdobył wymaganej liczby punktów, którą zlicytował, należy odjąć mu te punkty
- Grę wygrywa gracz, który pierwszy przekroczy 1000 punktów 
- Poniżej 1000 i powyżej 860 punktów graczowi nie zapisuje się punktów zdobytych pod koniec rundy
- Gracz musi wygrać licytację i zdobyć odpowiednią ilość punktów, aby wygrać grę 

## Struktura Projektu
```
1000/
├── game/
│   └── game.py          # Główna logika gry, rundy, punktacja
├── models/
│   ├── bot.py           # Klasa Bot - AI przeciwnik
│   ├── card.py          # Klasa Card - pojedyncza karta
│   ├── deck.py          # Klasa Deck - talia kart
│   ├── player.py        # Klasa Player - reprezentuje gracza
│   └── turn.py          # Klasa Turn - logika tury
├── resources/
│   └── cards.json       # Dane kart (opcjonalnie)
├── utils/
│   └── auxilkiary.py    # Funkcje pomocnicze
├── LICENSE              # Licencja MIT
├── main.py              # Punkt startowy aplikacji
├── README.md            # Opis
└── requirements.txt     # Zależności Python
```

### Główne klasy:

**`Game`** - zarządza przebiegiem gry, rundami, punktacją  
**`Player`** - reprezentuje gracza, trzyma karty, punkty  
**`Bot`** - dziedziczy po `Player`, implementuje prostą logikę AI  
**`Card`** - reprezentuje pojedynczą kartę (kolor, figura, wartość)  
**`Deck`** - talia kart, tasowanie, rozdawanie  
**`Turn`** - logika pojedynczej lewy/tury

## Instalacja i Uruchomienie

### Wymagania
- Python 3.8+
- pip

### Instalacja
```bash
git clone https://github.com/Demciok/1000.git
cd 1000
pip install -r requirements.txt  
```

### Uruchomienie
```bash
python main.py  
```

## Przyszłe Aktualizacje
- [ ] Dodać zasadę bomby 
- [ ] Napisać zaawansowaną logikę rzucania kart dla bota
- [ ] Zrobić wersję graficzną gry
- [ ] Dodać opcję zapisu stanu gry 
- [ ] Umożliwić grę online multiplayer
- [ ] Dokończyć angielską wersję dokumentacji

## Contributing

Projekt edukacyjny - pull requesty mile widziane!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Licencja

Ten projekt jest na licencji MIT. Zobacz plik LICENSE dla szczegółów.