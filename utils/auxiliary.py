import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
NICKS_PATH = BASE_DIR / 'resources' / 'nicks.txt'

"""Utility helpers for the 1000 card game."""

MARRIAGE = {
    "wino": 40,
    "zoladz": 60,
    "dzwonek": 80,
    "czerwo": 100
}

def pick_game_mode():
    """Prompt the user to choose the game mode."""
    print("Witaj w grze w 1000, gra karciana pochodząca z PRL-U")
    print("Mam nadzieje że zasady już znasz teraz wybierz")
    tryb = input("Tryb z botami - 0 tryb z graczami - 1: ")
    while tryb not in ["0", "1"]:
        tryb = input("Zly wybor wybierz 0- tryb z botami, 1 - tryb z graczami: ")
    return int(tryb)

def random_player_name():
    """Take random nick from the file and name player"""
    with open(NICKS_PATH) as f:
        return random.choice(f.readlines())

def name_a_player():
    """Ask the user for a player name."""
    return str(input("Wybierz nazwe dla gracza"))


def choose_language():
    lan = input("Choose langauge (pl/en): ")
    while lan not in ["pl", "en"]:
        lan = input("Choose langauge (pl/en): ")
    return str(lan)