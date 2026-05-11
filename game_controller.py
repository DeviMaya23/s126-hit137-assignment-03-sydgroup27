"""A module that holds the GameController class, which connects the game logic and the UI.
"""
from game import Game
from game_ui import GameUI
from image_processor import ImageProcessor
from PIL import Image, ImageTk


class GameController:
    """A class to represent the game controller, which connects the game logic and the UI.
    Attributes:
        game (Game): The game state and logic.
        ui (GameUI): The game user interface.
        image_processor (ImageProcessor): The image processor that applies alterations.
    """
    def __init__(self):
        self.game = Game([])
        self.ui = GameUI(self)
        # self.image_processor = ImageProcessor()

    def handle_click(self, x: int, y: int) -> None:
        """Handles a click on the modified image at the given coordinates."""
        pass

    def on_image_selected(self, image_path: str) -> None:
        """Handles a new image being selected by the user."""

        # TODO: validation of image

        # TODO: remove this later, imageprocessing job
        image = Image.open(image_path).convert("RGB")
        image = image.resize((500, 350))
        img = ImageTk.PhotoImage(image)

        self.game.start_game([])  # TODO: pass in altered regions from image processor
        
        self.ui.load_new_images(img)
        
        state = self.game.get_game_state()
        self.ui.update_display(**state)
        
