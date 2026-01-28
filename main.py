import curses
import json
import time
from curses import wrapper

def load_word_list():
    with open ("words.txt", "r") as f:
        return json.load(f)
    
def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    CYAN_TEXT_YELLOW_BG = curses.color_pair(1)
    BLACK_TEXT_WHITE_BG = curses.color_pair(2)

    counter_win = curses.newwin(1, 20, 10, 10)
    stdscr.addstr("hello from main")
    stdscr.refresh()

    for i in range(100):
        counter_win.clear()

        if i % 2 == 0:
            color = BLACK_TEXT_WHITE_BG
        else:
            color = CYAN_TEXT_YELLOW_BG

        counter_win.addstr(f"Count: {i}", color)
        counter_win.refresh()
        time.sleep(0.1)
    stdscr.getch()


wrapper(main)
