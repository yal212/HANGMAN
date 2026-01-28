import curses
import json
import time
from curses import wrapper

with open ("words.txt", "r") as f:
    words_list = json.load(f)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    CYAN_TEXT_YELLOW_BG = curses.color_pair(1)
    BLACK_TEXT_WHITE_BG = curses.color_pair(2)

    for i in range(100):
        stdscr.clear()

        if i % 2 == 0:
            color = BLACK_TEXT_WHITE_BG
        else:
            color = CYAN_TEXT_YELLOW_BG

        stdscr.addstr(f"Count: {i}", color)
        stdscr.refresh()
        time.sleep(0.1)
    stdscr.getch()


wrapper(main)
