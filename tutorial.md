# Hangman with Curses – Tutorial & To‑Do List

## Context
This tutorial serves as a step‑by‑step learning guide **and** an explicit to‑do list for building a terminal‑based Hangman game with Python’s `curses`. Each numbered step is a *todo* you should complete before moving on to the next one. Mark items as completed in your notes or a checklist.

---

## To‑Do List (Very Detailed)

1. **Set up a virtual environment**
   * Create env: `python -m venv .venv`.
   * Activate:
     * macOS/Linux: `source .venv/bin/activate`.
     * Windows: `.venv\Scripts\activate`.
   * Install curses dependency:
     * Windows: `pip install windows‑curses`.
     * Others: `pip install -r requirements.txt` if present.
   * Verify `curses` works:
     * Create a tiny script `check_curses.py`:
       ```python
       import curses
       stdscr = curses.initscr()
       stdscr.addstr(0,0,"Hello, curses!")
       stdscr.refresh()
       stdscr.getch()
       curses.endwin()
       ```
     * Run it and ensure the message displays.

2. **Create `GameState` dataclass** (`game.py`)
   * Define fields:
     ```python
     secret_word: str
     guessed: Set[str] = field(default_factory=set)
     remaining: int
     status: Literal["ongoing", "won", "lost"]
     ```
   * Methods to implement:
     * `make_guess(letter: str)`: update `guessed`, decrement `remaining` if miss, update `status`.
     * `is_won() -> bool` and `is_lost() -> bool` for convenience.
   * Add type hints and `from dataclasses import dataclass, field`.
   * Unit tests (`tests/test_game_state.py`):
     * Test initial state.
     * Test correct state after a correct guess.
     * Test state after an incorrect guess.
     * Test win/loss transitions.

3. **Word selection helper** (`utils.py`)
   * Implement `select_random_word(words: List[str]) -> str` using `random.choice`.
   * Load word list from `words.py`:
     * `from .words import WORDS` or read from a file if you choose.
   * Test (`tests/test_select_random_word.py`):
     * Ensure returned word is in the list.

4. **Curses screen setup** (`ui.py`)
   * `init_screen()`:
     * `stdscr = curses.initscr()`
     * `curses.cbreak()`, `curses.noecho()`, `stdscr.keypad(True)`.
     * Optional color pair setup.
   * `curses_wrapper(func)` context manager to guarantee `curses.endwin()`.

5. **UI drawing helpers** (`ui.py`)
   * `draw_gallows(win, remaining)` – draw scaffold and incremental body parts.
   * `draw_word(win, state)` – display underscores for missing letters.
   * `draw_guessed_letters(win, state)` – list guessed letters with a visual separator.
   * `draw_status(win, message)` – show instructions or game result at the bottom.
   * Each helper ends with `win.refresh()`.

6. **Input handling** (`ui.py` or separate `input.py`)
   * `get_letter(win) -> str`:
     * `key = win.getch()`.
     * Convert to lowercase letter.
     * Validate: alphabetic and not already guessed.
     * If invalid, display a warning via `draw_status`.

7. **Main game loop** (`main.py`)
   * Wrap entire flow in `curses_wrapper`.
   * Load word via `utils.select_random_word`.
   * Create `GameState` with initial remaining attempts (e.g., 6).
   * Loop until `state.status != "ongoing"`:
     * Call UI helpers to render.
     * Get user letter.
     * Update state with `make_guess`.
   * After loop, render final status and wait for any key.

8. **UI rendering tests** (`tests/test_ui_rendering.py`)
   * Use a mock `curses.window` that records `addstr` calls.
   * Verify gallows updates per remaining count.
   * Verify word display matches expected underscores.

9. **Documentation & packaging**
   * Update `README.md` with install, run, and test instructions.
   * Add a `setup.py` or `pyproject.toml` with a console‑script entry point `hangman=main:main`.
   * Optionally add `requirements.txt` listing `windows‑curses` and other deps.

10. **Optional features**
    * Hint system: a function that reveals a random unguessed letter.
    * Persistent score: store in `scores.json`.
    * Difficulty levels: select word length ranges.
    * Automated gameplay tests that simulate a sequence of guesses.

---

> This list provides a granular roadmap. Follow each sub‑step, commit when finished, and run the relevant tests before moving on.

---

## Next Steps
- Open each file in the order listed above.
- Follow the guidance to implement the functionality step‑by‑step.
- Run `python main.py` after each major change to verify progress.
- Commit frequently (but do not push until the tutorial is complete).