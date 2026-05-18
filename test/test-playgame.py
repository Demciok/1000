"""
Interaktywny runner gry w 1000.
Rozgrywa podana liczbe tur, wypisujac caly output gry na ekran.

Uzycie:
    python play_game.py 10       # zagraj 10 tur
    python play_game.py          # zapyta o liczbe tur
"""

import os
import re
import sys
import time
from pexpect.popen_spawn import PopenSpawn
import pexpect

# ── konfiguracja ─────────────────────────────────────────────────────────────
PYTHON      = sys.executable
_HERE       = os.path.dirname(os.path.abspath(__file__))
# Jesli play_game.py lezy w repo/test/ -> idziemy poziom wyzej do repo/main.py
# Jesli lezy w repo/              -> main.py jest obok
_candidate_test = os.path.normpath(os.path.join(_HERE, "..", "main.py"))
_candidate_same = os.path.normpath(os.path.join(_HERE, "main.py"))
GAME_SCRIPT = _candidate_test if os.path.exists(_candidate_test) else _candidate_same
TIMEOUT     = 15
MAX_MOVES   = 300   # max akcji na ture – zabezpieczenie
# ─────────────────────────────────────────────────────────────────────────────

# Kolory ANSI dla czytelnosci
GRN  = "\033[92m"   # odpowiedz gracza
YEL  = "\033[93m"   # naglowek tury / rundy
CYN  = "\033[96m"   # info systemowe
RST  = "\033[0m"


def print_section(text: str) -> None:
    print(f"\n{YEL}{'='*60}{RST}")
    print(f"{YEL}  {text}{RST}")
    print(f"{YEL}{'='*60}{RST}")


def send(child: PopenSpawn, value: str, label: str = "") -> None:
    """Wyslij odpowiedz i wypisz co wysylamy."""
    tag = f"  [{label}]" if label else ""
    print(f"{GRN}>>> wysylam: {value!r}{tag}{RST}")
    child.sendline(value)


def last_number(line: str) -> str:
    """Wyciaga ostatni numer z 'Wybierz K_czerwo(5) | J_czerwo(7):'"""
    numbers = re.findall(r"\((\d+)\)", line)
    return numbers[-1] if numbers else "0"


def read_and_print(child: PopenSpawn, pattern_list: list, timeout: int = TIMEOUT):
    """
    Czeka na jeden z wzorcow, wypisuje wszystko co sie pojawilo
    i zwraca indeks dopasowanego wzorca.
    """
    idx = child.expect(pattern_list, timeout=timeout)
    # child.before = tekst PRZED dopasowaniem
    # child.after  = dopasowany tekst LUB klasa (pexpect.EOF / pexpect.TIMEOUT)
    before = child.before if isinstance(child.before, str) else ""
    after  = child.after  if isinstance(child.after,  str) else ""
    output = before + after
    if output.strip():
        print(output, end="", flush=True)
    return idx


# ── fazy gry ─────────────────────────────────────────────────────────────────

def handle_auction(child: PopenSpawn) -> None:
    """Licytacja: czlowiek zawsze pasuje (0)."""
    while True:
        idx = read_and_print(child, [
            r"Dokonaj choiceu 1/0",   # 0 – pytanie o podbicie
            r"Gre rozpocznie",         # 1 – koniec, bot wygraL
            r"Zaczynamy gr",           # 2 – koniec, zaczynamy grac
            pexpect.TIMEOUT,
            pexpect.EOF,
        ])
        if idx == 0:
            send(child, "0", "pas")
        elif idx in (1, 2):
            return
        else:
            print(f"{CYN}[!] Timeout/EOF podczas licytacji{RST}")
            return


def handle_card_giving(child: PopenSpawn) -> None:
    """Rozdawanie kart: pierwsza -> 9, druga -> 8."""
    cards_given = 0
    while cards_given < 2:
        idx = read_and_print(child, [
            r"Select card number for player",   # 0
            r"Zaczynamy gr",                    # 1 – bot rozdal, zaczynamy
            pexpect.TIMEOUT,
            pexpect.EOF,
        ])
        if idx == 0:
            answer = "9" if cards_given == 0 else "8"
            send(child, answer, f"karta {cards_given + 1}")
            cards_given += 1
        elif idx == 1:
            return
        else:
            print(f"{CYN}[!] Timeout/EOF podczas rozdawania kart{RST}")
            return


def handle_play_card(child: PopenSpawn) -> bool:
    """
    Rzucanie jednej karty.
    Zwraca False gdy runda sie skonczyla.
    """
    idx = read_and_print(child, [
        r"Podaj numer karty.*\(od 0 do \d+\)",   # 0 – normalny prompt
        r"points \d+",                             # 1 – koniec rundy
        r"Tabela wynik",                           # 2 – tabela
        r"Zaczynamy licytacje",                    # 3 – nowa runda
        pexpect.EOF,
        pexpect.TIMEOUT,
    ])

    if idx == 0:
        send(child, "0", "rzut")

        # czy gra odrzucila karte (zly kolor)?
        idx2 = read_and_print(child, [
            r"Nie mo.esz rzuci.*Wybierz(.+):",   # 0 – blad koloru
            r"rzuca",                              # 1 – zaakceptowano
            r"Ture wygrywa",                       # 2 – koniec tury
            pexpect.TIMEOUT,
        ])
        if idx2 == 0:
            forced = last_number(child.after)
            send(child, forced, "wymuszony kolor")
        return True   # gra trwa

    elif idx in (1, 2, 3, 4):
        return False  # runda / gra skonczona
    else:
        print(f"{CYN}[!] Timeout/EOF podczas rzucania karty{RST}")
        return False


def play_one_round(child: PopenSpawn, round_num: int) -> None:
    """Rozgrywa jedna pelna runde (licytacja + karty + gra)."""
    print_section(f"RUNDA {round_num}")

    # czekaj na start licytacji (moze byc juz skonsumowan przez poprzedni krok)
    handle_auction(child)
    handle_card_giving(child)

    moves = 0
    while moves < MAX_MOVES:
        still_going = handle_play_card(child)
        if not still_going:
            break
        moves += 1

    print(f"\n{CYN}[runda {round_num} zakonczona po {moves} ruchach]{RST}")


# ── glowna petla ─────────────────────────────────────────────────────────────

def main() -> None:
    # ── ustal liczbe tur ─────────────────────────────────────────────────────
    if len(sys.argv) >= 2:
        try:
            num_rounds = int(sys.argv[1])
        except ValueError:
            print("Podaj liczbe calkowita jako argument, np.: python play_game.py 10")
            sys.exit(1)
    else:
        try:
            num_rounds = int(input("Ile tur chcesz rozegrac? "))
        except ValueError:
            print("Nieprawidlowa liczba.")
            sys.exit(1)

    print_section(f"START – rozgrywamy {num_rounds} tur")
    print(f"{CYN}Skrypt gry: {GAME_SCRIPT}{RST}\n")

    # ── uruchom gre ──────────────────────────────────────────────────────────
    child = PopenSpawn(
        [PYTHON, GAME_SCRIPT],
        encoding="cp1250",
        timeout=TIMEOUT,
    )

    # wybierz tryb z botami
    idx = read_and_print(child, [
        r"Tryb z botami - 0 tryb z graczami - 1",
        pexpect.TIMEOUT,
        pexpect.EOF,
    ])
    if idx != 0:
        print("Gra nie uruchomila sie poprawnie.")
        sys.exit(1)
    send(child, "0", "tryb botow")

    # ── rozegraj N tur ───────────────────────────────────────────────────────
    for runda in range(1, num_rounds + 1):
        # czekaj na start licytacji (lub EOF jesli gra sie skonczyla)
        idx = read_and_print(child, [
            r"Zaczynamy licytacje",   # 0
            pexpect.EOF,              # 1 – gra sie zamknela
            pexpect.TIMEOUT,          # 2
        ])
        if idx != 0:
            print(f"\n{CYN}Gra zakonczyla sie przed runda {runda}.{RST}")
            break

        handle_auction(child)
        handle_card_giving(child)

        moves = 0
        while moves < MAX_MOVES:
            still_going = handle_play_card(child)
            if not still_going:
                break
            moves += 1

        print(f"\n{CYN}--- koniec rundy {runda}/{num_rounds} ---{RST}\n")

    # ── zamknij process ───────────────────────────────────────────────────────
    print_section("KONIEC GRY")
    try:
        child.proc.terminate()
    except Exception:
        pass


if __name__ == "__main__":
    main()