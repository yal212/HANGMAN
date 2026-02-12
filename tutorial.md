# Hangman with Curses – Tutorial & To‑Do List

## Context

This tutorial serves as a step‑by‑step learning guide **and** an explicit to‑do list for building a terminal‑based Hangman game with Python's `curses`. Each numbered step is a *todo* you should complete before moving on to the next one.

**Philosophy**: This tutorial follows a *test-as-you-build* approach. You'll write tests alongside your implementation, catching bugs early and building confidence in your code.

**Requirements**: Python 3.9+ (for `Literal` type hints and modern dataclass features)

---

## Project Structure Overview

Before diving in, understand the target file layout:

```
hangman/
├── game.py              # GameState dataclass and core logic
├── words.py             # Word list loading from words.txt
├── words.txt            # JSON array of words ["apple", "banana", ...]
├── utils.py             # Helper functions (random word selection)
├── ui.py                # Curses UI: screen setup, drawing helpers
├── main.py              # Entry point with game loop
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Shared pytest fixtures
│   ├── test_game_state.py
│   ├── test_utils.py
│   └── test_ui.py
├── requirements.txt
└── pyproject.toml       # Packaging configuration
```

---

## To‑Do List (Very Detailed)

### 1. Set Up Development Environment

#### 1.1 Create virtual environment
```bash
python -m venv .venv
```

#### 1.2 Activate the environment
* macOS/Linux: `source .venv/bin/activate`
* Windows: `.venv\Scripts\activate`

#### 1.3 Create `requirements.txt`
```
pytest>=7.0.0
windows-curses; sys_platform == 'win32'
```

#### 1.4 Install dependencies
```bash
pip install -r requirements.txt
```

#### 1.5 Verify curses works
Create `check_curses.py`:
```python
import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Hello, curses! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```
Run with `python check_curses.py`. If you see the message, curses is working.

---

### 2. Create `GameState` Dataclass (`game.py`)

This is the core data model. Pay close attention to the field and method names.

#### 2.1 Define the dataclass structure

```python
from dataclasses import dataclass, field
from typing import Set, Literal

@dataclass
class GameState:
    """Tracks the state of a Hangman game."""
    
    secret_word: str
    remaining_guesses: int = 6
    guessed_chr: Set[str] = field(default_factory=set)
    status: Literal["ongoing", "won", "lost"] = "ongoing"
```

#### 2.2 Implement helper properties

```python
    @property
    def display_word(self) -> str:
        """Returns the word with unguessed letters as underscores."""
        # TODO: Return string like "a p p _ e" for secret "apple" with guessed {'a','p','e'}
        pass
    
    @property
    def is_word_solved(self) -> bool:
        """Check if all letters in secret_word have been guessed."""
        # TODO: Return True if every letter in secret_word is in guessed_chr
        pass
```

#### 2.3 Implement validation methods

```python
    def is_valid_chr(self, letter: str) -> bool:
        """Check if input is a single alphabetic character."""
        return len(letter) == 1 and letter.isalpha()
    
    def is_already_guessed(self, letter: str) -> bool:
        """Check if letter was already guessed."""
        return letter.lower() in self.guessed_chr
    
    def is_correct_guess(self, letter: str) -> bool:
        """Check if letter exists in the secret word."""
        return letter.lower() in self.secret_word.lower()
```

#### 2.4 Implement the main guess method

**CRITICAL**: This method has several important requirements:

```python
    def guess_chr(self, letter: str) -> bool:
        """
        Process a letter guess. Returns True if guess was accepted.
        
        IMPORTANT IMPLEMENTATION NOTES:
        1. Convert to lowercase: letter = letter.lower()  # NOT just letter.lower()
        2. Validate before processing
        3. Add to guessed_chr set
        4. Decrement remaining_guesses ONLY on INCORRECT guesses
        5. Update status to "won" or "lost" when appropriate
        """
        # WARNING: This is wrong:    letter.lower()
        # This is correct:           letter = letter.lower()
        # The .lower() method returns a new string, it doesn't modify in place!
        
        letter = letter.lower()
        
        if not self.is_valid_chr(letter) or self.is_already_guessed(letter):
            return False
        
        self.guessed_chr.add(letter)
        
        # TODO: If incorrect guess, decrement remaining_guesses
        # TODO: Check win condition (is_word_solved) and set status = "won"
        # TODO: Check lose condition (remaining_guesses <= 0) and set status = "lost"
        
        return True
```

#### 2.5 Implement status check methods

```python
    def has_won(self) -> bool:
        """Returns True if the game has been won."""
        return self.status == "won"
    
    def has_lost(self) -> bool:
        """Returns True if the game has been lost."""
        return self.status == "lost"
```

---

### 3. Testing Foundation

Set up your test infrastructure early to catch bugs as you build.

#### 3.1 Create test directory structure
```bash
mkdir -p tests
touch tests/__init__.py
```

#### 3.2 Create `tests/conftest.py` with shared fixtures

```python
import pytest
from game import GameState

@pytest.fixture
def new_game():
    """Fresh game state with word 'python'."""
    return GameState(secret_word="python", remaining_guesses=6)

@pytest.fixture
def nearly_won_game():
    """Game state one correct guess from winning."""
    game = GameState(secret_word="cat", remaining_guesses=6)
    game.guessed_chr = {'c', 'a'}  # Just needs 't'
    return game

@pytest.fixture
def nearly_lost_game():
    """Game state one wrong guess from losing."""
    game = GameState(secret_word="cat", remaining_guesses=1)
    game.guessed_chr = {'x', 'z', 'q', 'w', 'r'}
    return game
```

#### 3.3 Create `tests/test_game_state.py`

```python
import pytest
from game import GameState

class TestGameStateInit:
    def test_initial_status_is_ongoing(self, new_game):
        assert new_game.status == "ongoing"
    
    def test_initial_guessed_is_empty(self, new_game):
        assert new_game.guessed_chr == set()
    
    def test_default_remaining_guesses(self):
        game = GameState(secret_word="test")
        assert game.remaining_guesses == 6

class TestGuessing:
    def test_correct_guess_does_not_decrement(self, new_game):
        new_game.guess_chr('p')
        assert new_game.remaining_guesses == 6
    
    def test_incorrect_guess_decrements(self, new_game):
        new_game.guess_chr('z')
        assert new_game.remaining_guesses == 5
    
    def test_letter_added_to_guessed(self, new_game):
        new_game.guess_chr('a')
        assert 'a' in new_game.guessed_chr
    
    def test_duplicate_guess_returns_false(self, new_game):
        new_game.guess_chr('a')
        assert new_game.guess_chr('a') is False
    
    def test_case_insensitive(self, new_game):
        new_game.guess_chr('P')
        assert 'p' in new_game.guessed_chr
    
    def test_invalid_input_rejected(self, new_game):
        assert new_game.guess_chr('1') is False
        assert new_game.guess_chr('ab') is False
        assert new_game.guess_chr('') is False

class TestWinLoseConditions:
    def test_winning_sets_status(self, nearly_won_game):
        nearly_won_game.guess_chr('t')
        assert nearly_won_game.status == "won"
        assert nearly_won_game.has_won() is True
    
    def test_losing_sets_status(self, nearly_lost_game):
        nearly_lost_game.guess_chr('b')  # Wrong guess
        assert nearly_lost_game.status == "lost"
        assert nearly_lost_game.has_lost() is True
```

#### 3.4 Run tests
```bash
pytest tests/ -v
```

Fix any failures before proceeding!

---

### 4. Word Management

#### 4.1 Create `words.txt`

This file should be a JSON array:
```json
["python", "hangman", "curses", "terminal", "keyboard", "programming"]
```

#### 4.2 Implement `words.py`

```python
import json
from pathlib import Path

def load_word_list(filepath: str = "words.txt") -> list[str]:
    """Load words from a JSON array file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Word list not found: {filepath}")
    
    with open(path, 'r') as f:
        words = json.load(f)
    
    if not isinstance(words, list) or not words:
        raise ValueError("Word list must be a non-empty JSON array")
    
    return words
```

#### 4.3 Implement `utils.py`

```python
import random
from words import load_word_list

def select_random_word(words: list[str] | None = None) -> str:
    """
    Select a random word from the provided list or default word list.
    
    Args:
        words: Optional list of words. If None, loads from words.txt
    
    Returns:
        A randomly selected word (lowercase)
    """
    if words is None:
        words = load_word_list()
    
    # TODO: Use random.choice to select and return a lowercase word
    pass
```

#### 4.4 Create `tests/test_utils.py`

```python
import pytest
from utils import select_random_word

def test_returns_word_from_list():
    words = ["apple", "banana", "cherry"]
    result = select_random_word(words)
    assert result in words

def test_returns_lowercase():
    words = ["APPLE", "BANANA"]
    result = select_random_word(words)
    assert result == result.lower()

def test_loads_default_list(tmp_path, monkeypatch):
    # Create a temporary word list
    word_file = tmp_path / "words.txt"
    word_file.write_text('["test", "word"]')
    monkeypatch.chdir(tmp_path)
    
    result = select_random_word()
    assert result in ["test", "word"]
```

---

### 5. Curses Screen Setup (`ui.py`)

#### 5.1 Screen initialization

```python
import curses
from contextlib import contextmanager

def init_screen(stdscr):
    """
    Initialize curses screen with proper settings.
    
    Call this at the start of your main function.
    """
    curses.curs_set(0)          # Hide cursor
    curses.noecho()             # Don't echo keypresses
    stdscr.keypad(True)         # Enable special keys
    stdscr.clear()
    
    # Optional: Set up color pairs if terminal supports it
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Correct
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Wrong
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Prompt

@contextmanager
def curses_wrapper():
    """
    Context manager for safe curses initialization/cleanup.
    
    Usage:
        with curses_wrapper() as stdscr:
            # your game code
    """
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        yield stdscr
    finally:
        if stdscr:
            stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
```

---

### 6. UI Drawing Helpers (`ui.py`)

#### 6.1 Gallows ASCII Art

The hangman has 7 stages (0 = full body, 6 = empty gallows):

```python
HANGMAN_STAGES = [
    # Stage 0: Full hangman (lost)
    """
     ┌───┐
     │   O
     │  /│\\
     │  / \\
     │
    ─┴─
    """,
    # Stage 1: Both legs
    """
     ┌───┐
     │   O
     │  /│\\
     │  /
     │
    ─┴─
    """,
    # Stage 2: One leg
    """
     ┌───┐
     │   O
     │  /│\\
     │
     │
    ─┴─
    """,
    # Stage 3: Both arms
    """
     ┌───┐
     │   O
     │  /│
     │
     │
    ─┴─
    """,
    # Stage 4: One arm
    """
     ┌───┐
     │   O
     │   │
     │
     │
    ─┴─
    """,
    # Stage 5: Head only
    """
     ┌───┐
     │   O
     │
     │
     │
    ─┴─
    """,
    # Stage 6: Empty gallows (start)
    """
     ┌───┐
     │
     │
     │
     │
    ─┴─
    """,
]
```

#### 6.2 Drawing functions

```python
def draw_gallows(win, remaining_guesses: int, start_row: int = 1):
    """
    Draw the hangman gallows based on remaining guesses.
    
    Args:
        win: curses window
        remaining_guesses: Number of guesses left (0-6)
        start_row: Row to start drawing
    """
    # Clamp to valid range
    stage = max(0, min(6, remaining_guesses))
    art = HANGMAN_STAGES[stage]
    
    for i, line in enumerate(art.strip().split('\n')):
        win.addstr(start_row + i, 2, line)
    
    win.refresh()

def draw_word(win, state, row: int):
    """
    Display the secret word with underscores for unguessed letters.
    
    Example: "p y _ _ o n" for "python" with guessed {'p', 'y', 'o', 'n'}
    """
    display = state.display_word  # Uses the property you implemented
    win.addstr(row, 2, f"Word: {display}")
    win.refresh()

def draw_guessed_letters(win, state, row: int):
    """
    Show all guessed letters, sorted alphabetically.
    
    Example: "Guessed: a, e, i, o, u"
    """
    letters = sorted(state.guessed_chr)
    guessed_str = ", ".join(letters) if letters else "(none)"
    win.addstr(row, 2, f"Guessed: {guessed_str}")
    win.refresh()

def draw_status(win, message: str, row: int, color_pair: int = 0):
    """
    Display a status message (instructions, errors, game result).
    """
    win.move(row, 0)
    win.clrtoeol()  # Clear the line first
    win.addstr(row, 2, message, curses.color_pair(color_pair))
    win.refresh()
```

---

### 7. Input Handling

#### 7.1 Implement `get_letter()`

```python
def get_letter(win, state, prompt_row: int) -> str | None:
    """
    Wait for and validate a letter input from the user.
    
    Returns:
        A valid, unguessed lowercase letter, or None if invalid
    """
    draw_status(win, "Guess a letter: ", prompt_row, color_pair=3)
    
    key = win.getch()
    
    # Handle special keys (quit on 'q' or ESC)
    if key == ord('q') or key == 27:  # ESC
        return None
    
    # Convert to character
    try:
        letter = chr(key).lower()
    except (ValueError, OverflowError):
        draw_status(win, "Invalid key. Press a letter.", prompt_row, color_pair=2)
        return get_letter(win, state, prompt_row)  # Retry
    
    # Validate
    if not letter.isalpha():
        draw_status(win, "Please enter a letter (a-z).", prompt_row, color_pair=2)
        win.getch()  # Wait for acknowledgment
        return get_letter(win, state, prompt_row)
    
    if state.is_already_guessed(letter):
        draw_status(win, f"'{letter}' already guessed. Try another.", prompt_row, color_pair=2)
        win.getch()
        return get_letter(win, state, prompt_row)
    
    return letter
```

---

### 8. Main Game Loop (`main.py`)

#### 8.1 Game flow pseudocode

```
1. Initialize curses
2. Select random word
3. Create GameState
4. Loop while status == "ongoing":
   a. Clear screen
   b. Draw gallows
   c. Draw word (with underscores)
   d. Draw guessed letters
   e. Get letter input
   f. Process guess
5. Display final result
6. Wait for keypress
7. Cleanup curses
```

#### 8.2 Implementation

```python
import curses
from game import GameState
from utils import select_random_word
from ui import (
    init_screen, draw_gallows, draw_word,
    draw_guessed_letters, draw_status, get_letter
)

def main(stdscr):
    """Main game function, called by curses.wrapper()."""
    init_screen(stdscr)
    
    # Setup
    word = select_random_word()
    state = GameState(secret_word=word)
    
    # Game loop
    while state.status == "ongoing":
        stdscr.clear()
        
        # Draw UI elements
        draw_gallows(stdscr, state.remaining_guesses)
        draw_word(stdscr, state, row=10)
        draw_guessed_letters(stdscr, state, row=12)
        draw_status(stdscr, f"Remaining: {state.remaining_guesses}", row=14)
        
        # Get input
        letter = get_letter(stdscr, state, prompt_row=16)
        
        if letter is None:  # User quit
            break
        
        # Process guess
        state.guess_chr(letter)
    
    # Game over
    stdscr.clear()
    draw_gallows(stdscr, state.remaining_guesses)
    draw_word(stdscr, state, row=10)
    
    if state.has_won():
        draw_status(stdscr, "Congratulations! You won!", row=14, color_pair=1)
    elif state.has_lost():
        draw_status(stdscr, f"Game over! The word was: {state.secret_word}", row=14, color_pair=2)
    else:
        draw_status(stdscr, "Thanks for playing!", row=14)
    
    draw_status(stdscr, "Press any key to exit...", row=16)
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
```

---

### 9. UI Rendering Tests (`tests/test_ui.py`)

#### 9.1 Mock curses window

```python
import pytest
from unittest.mock import MagicMock, call
from game import GameState

class MockWindow:
    """Mock curses window that records all addstr calls."""
    
    def __init__(self):
        self.calls = []
        self.cleared = False
    
    def addstr(self, row, col, text, *args):
        self.calls.append((row, col, text))
    
    def clear(self):
        self.cleared = True
        self.calls = []
    
    def clrtoeol(self):
        pass
    
    def move(self, row, col):
        pass
    
    def refresh(self):
        pass
    
    def getch(self):
        return ord('a')
    
    def get_text_at(self, row):
        """Helper to find text drawn at a specific row."""
        return [text for r, c, text in self.calls if r == row]

# Example test
def test_draw_word_shows_underscores():
    from ui import draw_word
    
    mock_win = MockWindow()
    state = GameState(secret_word="cat")
    state.guessed_chr = {'c', 't'}
    
    draw_word(mock_win, state, row=5)
    
    texts = mock_win.get_text_at(5)
    assert any("c _ t" in text or "c_t" in text for text in texts)
```

---

### 10. Packaging & Distribution

#### 10.1 Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "hangman-curses"
version = "0.1.0"
description = "Terminal-based Hangman game using curses"
readme = "README.md"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.0.0"]
windows = ["windows-curses"]

[project.scripts]
hangman = "main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

#### 10.2 Update `README.md`

Ensure your README includes:
- [ ] Installation instructions (with venv)
- [ ] How to run the game: `python main.py` or `hangman` after install
- [ ] How to run tests: `pytest`
- [ ] Windows-specific note about `windows-curses`

---

### 11. Optional Features

Once the core game works, consider these enhancements:

#### 11.1 Hint system
```python
def get_hint(state: GameState) -> str | None:
    """Reveal a random unguessed letter."""
    unguessed = set(state.secret_word.lower()) - state.guessed_chr
    if unguessed:
        return random.choice(list(unguessed))
    return None
```

#### 11.2 Persistent scores (`scores.json`)
```python
import json

def save_score(word: str, won: bool, guesses_used: int):
    """Append game result to scores file."""
    # TODO: Load existing scores, append new one, save
    pass
```

#### 11.3 Difficulty levels
```python
DIFFICULTY = {
    "easy": (4, 6),      # 4-6 letter words
    "medium": (7, 9),    # 7-9 letter words
    "hard": (10, 15),    # 10+ letter words
}

def select_word_by_difficulty(difficulty: str) -> str:
    min_len, max_len = DIFFICULTY[difficulty]
    words = [w for w in load_word_list() if min_len <= len(w) <= max_len]
    return random.choice(words)
```

#### 11.4 Automated gameplay tests
```python
def test_full_game_win():
    """Simulate a complete winning game."""
    state = GameState(secret_word="cat")
    for letter in "cat":
        state.guess_chr(letter)
    assert state.has_won()

def test_full_game_loss():
    """Simulate a complete losing game."""
    state = GameState(secret_word="xyz", remaining_guesses=3)
    for letter in "abc":
        state.guess_chr(letter)
    assert state.has_lost()
```

---

## Troubleshooting

### Terminal size issues
If you get errors about terminal size, ensure your terminal is at least 80x24 characters:
```python
height, width = stdscr.getmaxyx()
if height < 24 or width < 80:
    raise RuntimeError("Terminal too small. Need at least 80x24.")
```

### Windows-specific issues
- Install `windows-curses`: `pip install windows-curses`
- Use Windows Terminal or PowerShell for best results
- CMD.exe may have rendering issues with Unicode characters

### SSH/Remote terminal issues
- Set `TERM=xterm-256color` if colors don't work
- Use `curses.has_colors()` to check support before using colors

### "addstr() returned ERR"
This usually means you're trying to write outside the window bounds:
- Check `stdscr.getmaxyx()` for actual dimensions
- Ensure row/col values are within bounds
- Leave room for the cursor at the bottom-right corner

---

## Commit Checkpoints

Commit your work at these milestones:
1. After environment setup and curses verification
2. After GameState with passing tests
3. After word selection with tests
4. After UI helpers implemented
5. After main game loop works
6. After all tests pass
7. After packaging configured

---

## Next Steps

- Open each file in the order listed above
- Follow the guidance to implement the functionality step‑by‑step
- Run `pytest` after each component to verify correctness
- Run `python main.py` after major changes to test the game
- Commit frequently at the checkpoints listed above
