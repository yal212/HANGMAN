import curses
import json
from curses import wrapper

with open ("words.txt", "r") as f:
    words_list = json.load(f)

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(10, 10, "hello from main func in main.py", curses.A_BOLD)
    stdscr.addstr(10, 12, "overwrite")
    stdscr.refresh()
    stdscr.getch()


wrapper(main)
