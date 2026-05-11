"""A module that holds the GameController class, which connects the game logic and the UI.
"""
from enums import GuessResult
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
        self.game = Game([])
        self.ui = GameUI(self)
        self.image_processor = ImageProcessor()

    def handle_click(self, x: int, y: int) -> None:
        """Handles a click on the modified image at the given coordinates."""

        # Adjust click coordinates for guessing logic
        x1, y1, _, _ = self.ui.image_bounds
        result = self.game.guess(x - x1, y - y1)
        state = self.game.get_game_state()
        
        if result == GuessResult.CORRECT:
            self.ui.draw_circle(x, y, "red")
            self.ui.update_status_bar("Correct guess! There is only {} altered regions left.".format(state['remaining']))
        elif result == GuessResult.INCORRECT:
            self.ui.update_status_bar("Incorrect guess! Try again.")
        elif result == GuessResult.GAME_OVER:
            self.ui.update_status_bar("Game is already over. Please start a new game.")
        elif result == GuessResult.WIN:
            self.ui.draw_circle(x, y, "red")
            self.ui.update_display(**state)
            self.ui.update_status_bar("Congratulations! You've found all altered regions. Click the Browse button (Ctrl+O) to start a new game.")
            self.ui.show_popup("Congratulations!", "You've found all altered regions!")
            return
        elif result == GuessResult.LOSE:
            print(state)
            self.ui.update_display(**state)
            self.ui.update_status_bar("Game Over. You've lost all your lives. Click the Browse button (Ctrl+O) to start a new game.")
            self.ui.show_popup("Game Over", "You've lost all your lives... Better luck next time!")
            self.reveal_altered_regions()    
            return

        self.ui.update_display(**state)
    

    def on_image_selected(self, image_path: str) -> None:
        """Handles a new image being selected by the user."""

        try:
            self.image_processor.load_image(image_path)
        except ValueError as e:
            self.ui.show_popup("Error","Could not load image, please select a valid image file!", "error")
            self.ui.update_status_bar("Could not load image, please select a valid image file (*.jpg, *.jpeg, *.png, *.bmp).")
            return
    
        img = self.image_processor.get_original_image()
        altered_img = self.image_processor.get_processed_image()
        altered_regions = self.image_processor.get_altered_regions()

        self.game.start_game(altered_regions)
        self.ui.load_new_images(img, altered_img)
        
        state = self.game.get_game_state()
        self.ui.update_display(**state)
        self.ui.update_status_bar("New image loaded! Find the altered regions by clicking on the right-side image.")
        
    def reveal_altered_regions(self) -> None:
        """Handles reveal button click to update game state and UI."""
        self.game.reveal()
        self.game.get_all_altered_regions()
        state = self.game.get_game_state()
        found_regions = state['found_regions']
        revealed_regions = state['revealed_regions']

        x1, y1, _, _ = self.ui.image_bounds

        for region in revealed_regions:
            # Calculate the center of the region for circle drawing
            x = region[0] + region[2] // 2
            y = region[1] + region[3] // 2
            if region not in found_regions:
                self.ui.draw_circle(x + x1, y + y1, "blue")
        
        self.ui.update_display(**state)