"""Unit tests for the Game class using pytest."""

from enums import GuessResult
from game import Game

altered_regions = [
    (10, 10, 50, 50),
    (100, 100, 30, 30),
    (200, 200, 40, 40),
    (300, 300, 20, 20),
    (400, 400, 60, 60)]


class TestGame:
    """Test suite for the Game class."""
    def test_init(self):
        game = Game()

        self.assert_game_state(game, {
            'score': 0,
            'life': 0,
            'remaining': 0,
            'altered_regions': [],
            'found_regions': [],
            'revealed': False
        })

    def test_start_game(self):
        game = Game()
        game.start_game(altered_regions)

        self.assert_game_state(game, {
            'score': 0,
            'life': 3,
            'remaining': 5,
            'altered_regions': altered_regions,
            'found_regions': [],
            'revealed': False
        })

    def test_guess_incorrect(self):
        game = Game()
        game.start_game(altered_regions)

        result = game.guess(0, 0)  # Incorrect guess

        assert result == GuessResult.INCORRECT

        self.assert_game_state(game, {
            'score': 0,
            'life': 2,
            'remaining': 5,
            'altered_regions': altered_regions,
            'found_regions': [],
            'revealed': False
        })

    def test_guess_correct(self):
        game = Game()
        game.start_game(altered_regions)

        result = game.guess(20, 20)  # Within first region (10, 10, 50, 50)

        assert result == GuessResult.CORRECT

        self.assert_game_state(game, {
            'score': 1,
            'life': 3,
            'remaining': 4,
            'altered_regions': altered_regions,
            'found_regions': [altered_regions[0]],
            'revealed': False
        })

    def test_guess_already_found(self):
        game = Game()
        game.start_game(altered_regions)

        # First correct guess
        game.guess(20, 20)

        # Second guess in same region
        result = game.guess(30, 30)

        assert result == GuessResult.ALREADY_FOUND

        self.assert_game_state(game, {
            'score': 1,
            'life': 3,
            'remaining': 4,
            'altered_regions': altered_regions,
            'found_regions': [altered_regions[0]],
            'revealed': False
        })

    def test_guess_win(self):
        game = Game()
        game.start_game(altered_regions)

        # Find all 5 regions
        game.guess(20, 20)    # Region 0: (10, 10, 50, 50)
        game.guess(110, 110)  # Region 1: (100, 100, 30, 30)
        game.guess(210, 210)  # Region 2: (200, 200, 40, 40)
        game.guess(310, 310)  # Region 3: (300, 300, 20, 20)
        result = game.guess(420, 420)  # Region 4: (400, 400, 60, 60)

        assert result == GuessResult.WIN

        self.assert_game_state(game, {
            'score': 5,
            'life': 3,
            'remaining': 0,
            'altered_regions': altered_regions,
            'found_regions': altered_regions,
            'revealed': False
        })

    def test_guess_lose(self):
        game = Game()
        game.start_game(altered_regions)

        # Lose all 3 lives
        game.guess(0, 0)  # Life: 2
        game.guess(1, 1)  # Life: 1
        result = game.guess(2, 2)  # Life: 0

        assert result == GuessResult.LOSE

        self.assert_game_state(game, {
            'score': 0,
            'life': 0,
            'remaining': 5,
            'altered_regions': altered_regions,
            'found_regions': [],
            'revealed': False
        })

    def test_guess_game_over(self):
        game = Game()
        game.start_game(altered_regions)

        # Exhaust all lives
        game.guess(0, 0)
        game.guess(1, 1)
        game.guess(2, 2)

        # Try to guess when game is already over
        result = game.guess(20, 20)

        assert result == GuessResult.GAME_OVER

        self.assert_game_state(game, {
            'score': 0,
            'life': 0,
            'remaining': 5,
            'altered_regions': altered_regions,
            'found_regions': [],
            'revealed': False
        })

    def test_get_display_state(self):
        game = Game()
        game.start_game(altered_regions)

        game.guess(20, 20)  # Correct guess
        game.guess(0, 0)    # Incorrect guess
        state = game.get_display_state()
        assert state == {
            'score': 1,
            'life': 2,
            'remaining': 4,
            'game_over': False
        }

    def test_get_regions(self):
        game = Game()
        game.start_game(altered_regions)

        game.guess(20, 20)  # Correct guess in region 0
        game.guess(110, 110)  # Correct guess in region 1
        regions = game.get_regions()
        assert regions == {
            'found_regions': [altered_regions[0], altered_regions[1]],
            'altered_regions': altered_regions
        }

    def test_reveal(self):
        game = Game()
        game.start_game(altered_regions)

        game.reveal()

        self.assert_game_state(game, {
            'score': 0,
            'life': 3,
            'remaining': 0,
            'altered_regions': altered_regions,
            'found_regions': [],
            'revealed': True
        })

    def assert_game_state(self, game, expected):
        """Helper method to assert the game state matches expected values."""
        assert game.score == expected['score']
        assert game.life == expected['life']
        assert game.remaining == expected['remaining']
        assert game.altered_regions == expected['altered_regions']
        assert game.found_regions == expected['found_regions']
