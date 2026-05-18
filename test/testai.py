"""
Testy automatyczne dla gry w 1000 (tryb z botami).
Używa modułu pexpect.popen_spawn.PopenSpawn – działa na Windows.

Strategia gracza 'czlowiek':
  - Licytacja:          zawsze odpowiada '0' (nie podbija)
  - Rozdawanie kart:    najpierw '9', potem '8'
  - Rzucanie karty:     zawsze '0'; jeśli pojawi się komunikat o błędnym
                        kolorze, wyciąga ostatni numer z listy dozwolonych
                        kart i wysyła go
"""

import os
import re
import sys
import unittest
from pexpect.popen_spawn import PopenSpawn
import pexpect


# ── konfiguracja ─────────────────────────────────────────────────────────────
PYTHON = sys.executable   # interpreter Pythona

# Skrypt testowy leży w repo/test/testai.py
# main.py jest poziom wyżej: repo/main.py
_HERE       = os.path.dirname(os.path.abspath(__file__))
GAME_SCRIPT = os.path.normpath(os.path.join(_HERE, "..", "main.py"))

TIMEOUT    = 15   # sekund – czas oczekiwania na każdy prompt
MAX_ROUNDS = 200  # zabezpieczenie przed nieskończoną pętlą
# ─────────────────────────────────────────────────────────────────────────────


def _last_number_from_choices(line: str) -> str:
    """
    Z komunikatu w stylu:
        'Nie mozesz rzucic... Wybierz K_czerwo(5) | J_czerwo(7):'
    wyciąga OSTATNI numer w nawiasach i zwraca go jako string.
    """
    numbers = re.findall(r"\((\d+)\)", line)
    if numbers:
        return numbers[-1]
    return "0"   # fallback


class ThousandGameBotModeTest(unittest.TestCase):
    """
    Testuje tryb gry z botami (opcja 0 na starcie).
    """

    def setUp(self):
        """Uruchamia process gry i wybiera tryb z botami."""
        # PopenSpawn – jedyna opcja pexpect dzialajaca na Windows
        self.child = PopenSpawn(
            [PYTHON, GAME_SCRIPT],
            encoding="utf-8",
            timeout=TIMEOUT,
        )
        self.child.expect(r"Tryb z botami - 0 tryb z graczami - 1")
        self.child.sendline("0")

    def tearDown(self):
        """Zamknij process po tescie."""
        try:
            self.child.proc.terminate()
        except Exception:
            pass

    # ── metody pomocnicze ─────────────────────────────────────────────────────

    def _handle_auction(self):
        """Zawsze odpowiada '0'. Konczy sie gdy licytacja sie zakonczy."""
        while True:
            idx = self.child.expect([
                r"Dokonaj choiceu 1/0",
                r"Gre rozpocznie",
                r"Zaczynamy gr",
                pexpect.TIMEOUT,
                pexpect.EOF,
            ])
            if idx == 0:
                self.child.sendline("0")
            elif idx in (1, 2):
                return
            else:
                self.fail("Timeout/EOF podczas licytacji")

    def _handle_card_giving(self):
        """Pierwsza karta -> '9', druga -> '8'. No-op jesli bot wygraL."""
        cards_given = 0
        while cards_given < 2:
            idx = self.child.expect([
                r"Select card number for player",
                r"Zaczynamy gr",
                pexpect.TIMEOUT,
                pexpect.EOF,
            ])
            if idx == 0:
                answer = "9" if cards_given == 0 else "8"
                self.child.sendline(answer)
                cards_given += 1
            elif idx == 1:
                return
            else:
                self.fail("Timeout/EOF podczas rozdawania kart")

    def _handle_play_card(self):
        """
        Jeden prompt rzucania:  '0' -> jesli blad koloru -> ostatni numer.
        Zwraca False gdy runda/gra sie skonczona.
        """
        idx = self.child.expect([
            r"Podaj numer karty.*\(od 0 do \d+\)",
            r"points \d+",
            r"Tabela wynik",
            r"Zaczynamy licytacje",
            pexpect.EOF,
            pexpect.TIMEOUT,
        ])

        if idx == 0:
            self.child.sendline("0")
            idx2 = self.child.expect([
                r"Nie mo.esz rzuci.*Wybierz(.+):",
                r"rzuca",
                r"Ture wygrywa",
                pexpect.TIMEOUT,
            ])
            if idx2 == 0:
                forced = _last_number_from_choices(self.child.after)
                self.child.sendline(forced)
            return True

        elif idx in (1, 2, 3, 4):
            return False
        else:
            self.fail("Timeout/EOF podczas rzucania karty")

    # ── testy ────────────────────────────────────────────────────────────────

    def test_game_starts_with_bot_mode(self):
        """Gra uruchamia sie i przechodzi do licytacji.
        Uwaga: setUp juz wyslal '0' i skonsumowal poczatkowy output,
        wiec 'Witaj...' jest juz za nami – sprawdzamy tylko licytacje.
        """
        self.child.expect(r"Zaczynamy licytacje")

    def test_auction_human_always_passes(self):
        """Czlowiek nie podbija -> bot przejmuje licytacje."""
        self.child.expect(r"Zaczynamy licytacje")
        self.child.expect(r"Dokonaj choiceu 1/0")
        self.child.sendline("0")
        self.child.expect(r"Gre rozpocznie")

    def test_full_round_completes(self):
        """Pelna runda konczy sie tabela wynikow."""
        self.child.expect(r"Zaczynamy licytacje")
        self._handle_auction()
        self._handle_card_giving()
        for _ in range(MAX_ROUNDS):
            if not self._handle_play_card():
                break
        self.child.expect(r"Tabela wynik", timeout=TIMEOUT)

    def test_score_table_contains_all_players(self):
        """Tabela wynikow zawiera czlowiek, LLama i Claude."""
        self.child.expect(r"Zaczynamy licytacje")
        self._handle_auction()
        self._handle_card_giving()
        for _ in range(MAX_ROUNDS):
            if not self._handle_play_card():
                break
        # Po dopasowaniu "Tabela wynik" czytamy jeszcze chwile outputu
        # (gra nie konczy sie EOF – czeka na kolejna runde)
        self.child.expect(r"Zaczynamy licytacje|czlowiek", timeout=TIMEOUT)
        output = self.child.before  # tekst miedzy "Tabela wynik" a tym miejscem
        # Tabela powinna zawierac wszystkich graczy
        # (szukamy tez w before z dopasowania tabeli)
        full_output = self.child.buffer + output
        self.assertIn("czlowiek", full_output)
        self.assertIn("LLama",    full_output)
        self.assertIn("Claude",   full_output)

    def test_two_full_rounds(self):
        """Dwie pelne rundy bez zawieszenia."""
        for _ in range(2):
            self.child.expect(r"Zaczynamy licytacje", timeout=TIMEOUT)
            self._handle_auction()
            self._handle_card_giving()
            for _ in range(MAX_ROUNDS):
                if not self._handle_play_card():
                    break

    def test_invalid_color_prompt_is_handled(self):
        """Blad koloru jest obslugiwany – gra nie zawiesza sie."""
        self.child.expect(r"Zaczynamy licytacje")
        self._handle_auction()
        self._handle_card_giving()
        for _ in range(MAX_ROUNDS):
            idx = self.child.expect([
                r"Podaj numer karty.*\(od 0 do \d+\)",
                r"Nie mo.esz rzuci.*Wybierz(.+):",
                r"points \d+",
                r"Tabela wynik",
                pexpect.EOF,
                pexpect.TIMEOUT,
            ])
            if idx == 0:
                self.child.sendline("0")
            elif idx == 1:
                forced = _last_number_from_choices(self.child.after)
                self.child.sendline(forced)
            elif idx in (2, 3, 4):
                break
            else:
                self.fail("Timeout podczas obslugi bledu koloru")


# ── uruchomienie ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)