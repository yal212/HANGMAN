import pytest
from game import GameState

@pytest.fixture
def new_game():
    return GameState("python", remaining_guesses=6)

@pytest.fixture
def nearly_won_game():
    return GameState("cat", remaining_guesses=6, guessed_chr={"c", "a"})

@pytest.fixture
def nearly_lost_game():
    return GameState("cat", remaining_guesses=1, guessed_chr={"b", "d", "e", "f", "g"})
