import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_YELLOW)
    CYAN_TEXT_YELLOW_BG = curses.color_pair(1)
    stdscr.border()
    win = curses.newwin(3, 18, 2, 2)
    box = Textbox(win)
    rectangle(stdscr, 1, 1, 5, 20)
    stdscr.refresh()
    box.edit()
    text = box.gather().strip().replace("\n", "")
    stdscr.addstr(10, 40, text)
    stdscr.getch()

wrapper(main)
