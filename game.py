"""A module to represent the game state and logic.
"""


class Game:
    """
    A class to represent the game state.
    Attributes:
        life (int): The number of lives the player has.
        score (int): The player's current score.
    Functions:

    """
    def __init__(self):
        self.life = 3
        self.score = 0
