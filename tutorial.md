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
    secret_word: str
    remaining_guesses: int = 6
    guessed_chr: Set[str] = field(default_factory=set)
    status: Literal["ongoing", "won", "lost"] = "ongoing"
```

#### 2.2 Implement helper properties

```python
    @property
    def display_word(self) -> str:
        # TODO: Return word with unguessed letters as underscores, spaces between chars
        pass
    
    @property
    def is_word_solved(self) -> bool:
        # TODO: Return True if every letter in secret_word is in guessed_chr
        pass
```

#### 2.3 Implement validation methods

```python
    def is_valid_chr(self, letter: str) -> bool:
        # TODO: Return True if letter is a single alphabetic character
        pass
    
    def is_already_guessed(self, letter: str) -> bool:
        # TODO: Return True if lowercase letter is in guessed_chr
        pass
    
    def is_correct_guess(self, letter: str) -> bool:
        # TODO: Return True if lowercase letter exists in lowercase secret_word
        pass
```

#### 2.4 Implement the main guess method

**CRITICAL BUG WARNING**: Use `letter = letter.lower()` NOT `letter.lower()` (strings are immutable!)

```python
    def guess_chr(self, letter: str) -> bool:
        # TODO: Convert letter to lowercase, validate, add to guessed_chr
        # TODO: Decrement remaining_guesses ONLY on INCORRECT guesses
        # TODO: Update status to "won" or "lost" when appropriate
        # TODO: Return True if guess accepted, False otherwise
        pass
```

#### 2.5 Implement status check methods

```python
    def has_won(self) -> bool:
        # TODO: Return True if status is "won"
        pass
    
    def has_lost(self) -> bool:
        # TODO: Return True if status is "lost"
        pass
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
    # TODO: Return a fresh GameState with word "python" and 6 guesses
    pass

@pytest.fixture
def nearly_won_game():
    # TODO: Return GameState for "cat" with {'c','a'} guessed (needs 't' to win)
    pass

@pytest.fixture
def nearly_lost_game():
    # TODO: Return GameState for "cat" with 1 guess left and wrong letters guessed
    pass
```

#### 3.3 Create `tests/test_game_state.py`

```python
import pytest
from game import GameState

class TestGameStateInit:
    def test_initial_status_is_ongoing(self, new_game):
        # TODO: Assert status equals "ongoing"
        pass
    
    def test_initial_guessed_is_empty(self, new_game):
        # TODO: Assert guessed_chr is empty set
        pass
    
    def test_default_remaining_guesses(self):
        # TODO: Create GameState and assert remaining_guesses is 6
        pass

class TestGuessing:
    def test_correct_guess_does_not_decrement(self, new_game):
        # TODO: Guess correct letter, verify remaining_guesses unchanged
        pass
    
    def test_incorrect_guess_decrements(self, new_game):
        # TODO: Guess wrong letter, verify remaining_guesses decreased by 1
        pass
    
    def test_letter_added_to_guessed(self, new_game):
        # TODO: Guess a letter, verify it's in guessed_chr
        pass
    
    def test_duplicate_guess_returns_false(self, new_game):
        # TODO: Guess same letter twice, verify second returns False
        pass
    
    def test_case_insensitive(self, new_game):
        # TODO: Guess uppercase letter, verify lowercase stored in guessed_chr
        pass
    
    def test_invalid_input_rejected(self, new_game):
        # TODO: Test that numbers, multi-char, empty string return False
        pass

class TestWinLoseConditions:
    def test_winning_sets_status(self, nearly_won_game):
        # TODO: Guess final letter, verify status is "won" and has_won() is True
        pass
    
    def test_losing_sets_status(self, nearly_lost_game):
        # TODO: Guess wrong letter, verify status is "lost" and has_lost() is True
        pass
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
    # TODO: Load and return words from JSON array file
    # TODO: Raise FileNotFoundError if file doesn't exist
    # TODO: Raise ValueError if not a non-empty list
    pass
```

#### 4.3 Implement `utils.py`

```python
import random
from words import load_word_list

def select_random_word(words: list[str] | None = None) -> str:
    # TODO: If words is None, load from words.txt
    # TODO: Return random.choice() from list, lowercase
    pass
```

#### 4.4 Create `tests/test_utils.py`

```python
import pytest
from utils import select_random_word

def test_returns_word_from_list():
    # TODO: Call with a list, verify result is in that list
    pass

def test_returns_lowercase():
    # TODO: Call with uppercase words, verify result is lowercase
    pass

def test_loads_default_list(tmp_path, monkeypatch):
    # TODO: Create temp words.txt, change dir, verify select_random_word() works
    pass
```

---

### 5. Curses Screen Setup (`ui.py`)

#### 5.1 Screen initialization

```python
import curses
from contextlib import contextmanager

def init_screen(stdscr):
    # TODO: Hide cursor, disable echo, enable keypad, clear screen
    # TODO: (Optional) Set up color pairs if terminal supports colors
    pass

@contextmanager
def curses_wrapper():
    # TODO: Implement context manager that initializes curses in try block
    # TODO: Clean up with curses.endwin() in finally block (must always run!)
    pass
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
    # TODO: Get correct stage from HANGMAN_STAGES based on remaining_guesses
    # TODO: Draw each line of ASCII art with win.addstr()
    pass

def draw_word(win, state, row: int):
    # TODO: Display "Word: {state.display_word}" at the given row
    pass

def draw_guessed_letters(win, state, row: int):
    # TODO: Display sorted guessed letters like "Guessed: a, e, i" or "(none)"
    pass

def draw_status(win, message: str, row: int, color_pair: int = 0):
    # TODO: Clear line, then display message with optional color
    pass
```

---

### 7. Input Handling

#### 7.1 Implement `get_letter()`

```python
def get_letter(win, state, prompt_row: int) -> str | None:
    # TODO: Show prompt, get keypress, return None on quit (q/ESC)
    # TODO: Validate: alphabetic, not already guessed
    # TODO: On invalid input, show error and retry
    # TODO: Return valid lowercase letter
    pass
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
    # TODO: Initialize screen, select word, create GameState
    # TODO: Game loop: draw UI, get input, process guess until win/lose/quit
    # TODO: Show final result and wait for keypress
    pass

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
    # TODO: Create mock that records addstr() calls in self.calls list
    # TODO: Implement: __init__, addstr, clear, clrtoeol, move, refresh, getch
    # TODO: Add helper get_text_at(row) to find text drawn at specific row
    pass

def test_draw_word_shows_underscores():
    # TODO: Create MockWindow, create GameState with partial guesses
    # TODO: Call draw_word(), verify underscores appear for unguessed letters
    pass
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
    # TODO: Return a random unguessed letter from secret_word, or None
    pass
```

#### 11.2 Persistent scores (`scores.json`)
```python
import json

def save_score(word: str, won: bool, guesses_used: int):
    # TODO: Load existing scores, append new result, save to file
    pass
```

#### 11.3 Difficulty levels
```python
DIFFICULTY = {
    "easy": (4, 6),
    "medium": (7, 9),
    "hard": (10, 15),
}

def select_word_by_difficulty(difficulty: str) -> str:
    # TODO: Filter word list by length range, return random choice
    pass
```

#### 11.4 Automated gameplay tests
```python
def test_full_game_win():
    # TODO: Guess all correct letters, verify has_won() is True
    pass

def test_full_game_loss():
    # TODO: Guess all wrong letters until remaining_guesses=0, verify has_lost()
    pass
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
