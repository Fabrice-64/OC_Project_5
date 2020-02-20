import curses
from curses import textpad
import time

def test_textpad(stdscr, insert_mode=False):
    ncols, nlines = 6, 1
    uly, ulx = 3, 2
    if insert_mode:
        mode = 'insert mode'
    else:
        mode = 'overwrite mode'

    stdscr.addstr(uly-3, ulx, "Use Ctrl-G to end editing (%s)." % mode)
    stdscr.addstr(uly-2, ulx, "Be sure to try typing in the lower-right corner.")
    win = curses.newwin(nlines, ncols, uly, ulx)
    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols+1)
    stdscr.refresh()

    box = textpad.Textbox(win, insert_mode= True)
    contents = box.edit()
    stdscr.addstr("Text entered in the box")
    stdscr.addstr(repr(contents))
    stdscr.addstr(' ')
    stdscr.addstr('Press any key')
    stdscr.getch()
    time.sleep(3)

    

"""
    for i in range(3):
        stdscr.move(uly+ncols+2 + i, 0)
        stdscr.clrtoeol() 
"""
curses.wrapper(test_textpad)