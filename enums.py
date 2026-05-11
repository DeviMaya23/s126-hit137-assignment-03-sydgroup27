"""Enums for the game."""
from enum import Enum


class GuessResult(Enum):
    """Enum to represent the result of a player's guess."""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    ALREADY_FOUND = "already_found"
    GAME_OVER = "game_over"