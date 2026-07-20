import random
from pathlib import Path
from models.languagemanager import LanguageManager

BASE_DIR = Path(__file__).resolve().parent.parent
NICKS_PATH = BASE_DIR / 'resources' / 'nicks.txt'

"""Utility helpers for the 1000 card game."""

MARRIAGE = {
    "wino": 40,
    "zoladz": 60,
    "dzwonek": 80,
    "czerwo": 100
}


def _language_manager(language="pl"):
    if isinstance(language, LanguageManager):
        return language
    return LanguageManager(language)

def pick_game_mode(language=None):
    """Prompt the user to choose the game mode."""
    lm = _language_manager(language or "pl")
    lm.print_by_id(28)
    lm.print_by_id(29)
    tryb = lm.input_by_id(37)
    while tryb not in ["0", "1"]:
        tryb = lm.input_by_id(38)
    return int(tryb)

def random_player_name():
    """Take random nick from the file and name player"""
    with open(NICKS_PATH) as f:
        return random.choice(f.readlines())

def name_a_player(language=None):
    """Ask the user for a player name."""
    return str(_language_manager(language or "pl").input_by_id(39))


def choose_language(language=None):
    lm = _language_manager(language or "pl")
    lan = input("Choose language (pl/en/zh): ")
    while lan not in ["pl", "en", "zh"]:
        lan = lm.input_by_id(40)
    return str(lan)