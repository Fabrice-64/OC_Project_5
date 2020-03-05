import curses
from time import sleep

menu = ["Home", "Play", "Scoreboard", "Exit"]

def print_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    for idx, row in enumerate(menu):
        y = h//2 - len(menu)//2 + idx
        x = w//2 - len(row)//2
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
        stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    
    h,w = stdscr.getmaxyx()
    current_row_idx = 0
    print_menu(stdscr, current_row_idx)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row_idx >0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) -1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            stdscr.addstr(0,0, "Youp pressed {}".format(menu[current_row_idx]))
            stdscr.refresh()
            key = stdscr.getch()
        print_menu(stdscr, current_row_idx)
    stdscr.refresh()
    



if __name__ == "__main__":
    curses.wrapper(main)