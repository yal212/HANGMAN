# HANGMAN

A classic terminal-based Hangman game written in Python. Guess the hidden word one letter at a time before the hangman is completed.

---

## Features

- Lightweight — no external libraries required
- Plays in your terminal with a simple text UI
- Randomized words from `words.txt` for every round
- Replayable without restarting the program

---

## Requirements

- Python 3.7+
- No other dependencies

Install Python (brief platform guide):

- macOS
  - Using Homebrew (recommended if you have Homebrew):

    ```bash
    brew update
    brew install python
    ```

    After install use python3 and pip3, e.g. `python3 --version`.
  - Or download the official installer from https://www.python.org/downloads/mac-osx/ and run it.

- Windows
  - Download the official installer from https://www.python.org/downloads/windows/ and run it. During installation, check "Add Python to PATH".
  - Alternatively install from the Microsoft Store or use a package manager (Chocolatey: `choco install python`).
  - Verify with `py -3 --version` or `python --version` in PowerShell/CMD.

- Linux
  - Debian/Ubuntu:

    ```bash
    sudo apt update
    sudo apt install python3 python3-venv
    ```

  - Fedora/CentOS:

    ```bash
    sudo dnf install python3
    ```

  - Most distributions provide Python 3 via their package manager; you can also use pyenv to install specific versions.

Verification

Run:

```bash
python3 --version
```

(or `py -3 --version` on some Windows setups) — it should report Python 3.7 or newer.

Optional (recommended for development)

Create and activate a virtual environment:

- macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

- Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

---

## Quick Start

1. Open a terminal in the project directory (the directory that contains `main.py`).
2. Run the game with:

    ```bash
    python3 main.py
    ```

   Notes:
   - The word list is read from `words.txt` (a JSON array of words). Do not edit the file format. To add more words, you have to use the exact file format.
   - Enter a single lowercase letter as your guess. The game expects lowercase input (words are stored and compared in lowercase).
   - To quit at any time, press Ctrl+C.

---

## How to Play

- When the program starts, type `start` to begin.
- During the game type a single letter and press Enter to guess.
- Correct guesses reveal that letter in the word.
- Incorrect guesses advance the hangman drawing. You are allowed 6 incorrect guesses; on the 7th stage the game ends.
- If you guess the entire word before running out of incorrect guesses, you win.
- After a round ends you may type `play again` to start another round.

---

## Example session (shortened)

> Type 'start' to start the game!

Then guess letters like:

```
_ _ _ _ _
Enter your guess: a
_ a _ _ _
```

The game will show the current hangman ASCII art, the partially revealed word, and prompt for the next guess.

---

## Project Structure

- `main.py` — game loop and input handling
- `hangman.py` — ASCII art and helper for printing the hangman
- `utilities.py` — input validation and result messages
- `words.txt` — JSON list of words used by the game
- `LICENSE.md` — project license

---

## Contributing

Contributions are welcome. If you'd like to propose a change or fix:

1. Fork the repository
2. Create a branch for your change
3. Open a pull request with a short description of your changes

---

## License

See `LICENSE.md` for license details.
