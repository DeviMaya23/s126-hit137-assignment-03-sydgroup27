# main.py entry point of the application
from game_controller import GameController

if __name__ == "__main__":
    gameController = GameController()
    gameController.ui.mainloop()