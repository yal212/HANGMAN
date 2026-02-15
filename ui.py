import curses
from contextlib import contextmanager


def init_screen(stdscr):
    curses.curs_set(0)
    curses.noecho()
    stdscr.clear()

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red on Black
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green on Black


@contextmanager
def curses_wrapper():
    stdscr = None
    try:
        stdscr = curses.initscr()
        yield stdscr
    finally:
        curses.endwin()


HANGMAN_STAGES = [
    # Stage 0: Full hangman (lost)
    """
     ┌───┐
     │   O
     │  /│\
     │  / \
     │
    ─┴─
    """,
    # Stage 1: Both legs
    """
     ┌───┐
     │   O
     │  /│\
     │  /
     │
    ─┴─
    """,
    # Stage 2: One leg
    """
     ┌───┐
     │   O
     │  /│\
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


def draw_gallows(win, remaining_guesses: int, start_row: int = 1):
    stage = HANGMAN_STAGES[remaining_guesses]
    for i, line in enumerate(stage.splitlines()):
        win.addstr(start_row + i, 0, line)


def draw_word(win, state, row: int):
    win.addstr(row, 0, f"Word: {state.display_word}")


def draw_guessed_letters(win, state, row: int):
    if len(state.guessed_chr) == 0:
        line = "(none)"
    else:
        line = "Guessed: "
        chrs = sorted(state.guessed_chr)
        for i, c in enumerate(chrs):
            if i == 0:
                line += c
            else:
                line += ", " + c
    win.addstr(row, 0, line)


def draw_status(win, message: str, row: int, color_pair: int = 0):
    # TODO: use custom colors for different type of message. For example, Green for success, Red for Fail
    win.move(row, 0)
    win.clrtoeol()
    win.addstr(row, 0, message, curses.color_pair(color_pair))
