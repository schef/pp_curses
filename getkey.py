#!/usr/bin/python3
import curses

def main(stdscr):
    y = 0
    x = 0


    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break  # Exit the while loop
        else:
            stdscr.clear()
            stdscr.addstr(y, x, curses.keyname(c))
            stdscr.refresh()

curses.wrapper(main)
