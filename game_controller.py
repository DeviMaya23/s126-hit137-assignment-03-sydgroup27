"""A module that holds the GameController class, which connects the game logic and the UI.
"""
from game import Game
from game_ui import GameUI
from image_processor import ImageProcessor


class GameController:
    """A class to represent the game controller, which connects the game logic and the UI.
    Attributes:
        game (Game): The game state and logic.
        ui (GameUI): The game user interface.
        image_processor (ImageProcessor): The image processor that applies alterations.
    """
    def __init__(self):
        self.game = Game()
        self.ui = GameUI()
        self.image_processor = ImageProcessor()

    def handle_click(self, x: int, y: int) -> None:
        """Handles a click on the modified image at the given coordinates."""
        pass
