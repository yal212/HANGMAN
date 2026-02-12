import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Hello, curses! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
