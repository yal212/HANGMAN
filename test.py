import curses


def main(stdscr):
    stdscr.clear()
    s1 = "s1 s1 s1 s1 s1"
    s1 = """
         ┌───┐
         │
         │
         │
         │
        ─┴─
        """
    stdscr.addstr(1, 0, s1)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
