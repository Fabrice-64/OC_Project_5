import curses
from curses import textpad as tp
import config
import time

def main(self):
    stdscr = curses.initscr()
    stdscr.addstr(0,0, "Waiting for ending the program")
    stdscr.refresh()
    win = curses.newwin(10,10,10,20)
    win.addstr(1,1, "Test \n il s'agit d'un test plutôt long")
    win.refresh()
    time.sleep(3)

if __name__ == "__main__":
    curses.wrapper(main)