import pytest
from game import GameState

class TestGameStateInit:
    def test_initial_status_is_ongoing(self, new_game):
        assert new_game.status == "ongoing"
    
    def test_initial_guessed_is_empty(self, new_game):
        assert len(new_game.guessed_chr) == 0
    
    def test_default_remaining_guesses(self):
        game = GameState("test")
        assert game.remaining_guesses == 6

class TestGuessing:
    def test_correct_guess_does_not_decrement(self, new_game):
        original_remaining_guesses = new_game.remaining_guesses
        new_game.guess_chr("p")
        assert new_game.remaining_guesses == original_remaining_guesses
    
    def test_incorrect_guess_decrements(self, new_game):
        original_remaining_guesses = new_game.remaining_guesses
        new_game.guess_chr("a")
        assert new_game.remaining_guesses == original_remaining_guesses - 1
    
    def test_letter_added_to_guessed(self, new_game):
        new_game.guess_chr("a")
        assert "a" in new_game.guessed_chr
    
    def test_duplicate_guess_returns_false(self, new_game):
        new_game.guess_chr("a")
        assert new_game.guess_chr("a") == False
    
    def test_case_insensitive(self, new_game):
        new_game.guess_chr("A")
        assert "a" in new_game.guessed_chr
    
    def test_invalid_input_rejected(self, new_game):
        assert new_game.guess_chr("1") == False
        assert new_game.guess_chr("/") == False
        assert new_game.guess_chr("") == False

class TestWinLoseConditions:
    def test_winning_sets_status(self, nearly_won_game):
        nearly_won_game.guess_chr("t")
        assert nearly_won_game.status == "won"
        assert nearly_won_game.has_won() == True
    
    def test_losing_sets_status(self, nearly_lost_game):
        nearly_lost_game.guess_chr("z")
        assert nearly_lost_game.status == "lost"
        assert nearly_lost_game.has_won() == False
