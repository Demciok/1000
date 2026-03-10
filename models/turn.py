from dataclasses import dataclass
@dataclass
class Turn:
    """Helper class for a round"""
    turn_number: int
    shift: dict # szychta
    color: str
    marriage_color: str # kolor meldunku 