import curses
from curses import textpad
from curses.textpad import 
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

def display_menu(self, selected_row_idx, drop_down_list, question):
        self.inner_left_window.clear()
        y, x = self.inner_left_window.getmaxyx()
        guideline = "Please give a response to this request:"
        self.y_middle_inner_left_window = y//2 - len(drop_down_list)//2
        self.x_middle_inner_left_window = x//2
        self.inner_left_window.addstr(0 , 0, guideline)
        self.inner_left_window.addstr(1, 0, question)
        self.inner_left_window.refresh()
        
        for idx,row in enumerate(drop_down_list):
            curses.curs_set(1)
            y_temp = self.y_middle_inner_left_window + idx
            x_temp = self.x_middle_inner_left_window - len(row)//2
            if idx == selected_row_idx:
                self.inner_left_window.attron(curses.color_pair(2))
                self.inner_left_window.addstr(y_temp, x_temp, row)
                self.inner_left_window.attroff(curses.color_pair(2))
            else:
                self.inner_left_window.addstr(y_temp, x_temp, row)
            self.inner_left_window.refresh()
            self.screen.refresh()
        
    def set_up_drop_down(self, drop_down_list, question):
        curses.curs_set(0)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        current_row = 0                                                                 
        self.display_menu(current_row, drop_down_list, question)
        while True:
            key = self.inner_left_window.getch()
            self.inner_left_window.clear()
            if key == curses.KEY_UP and current_row> 0:
                self.inner_left_window.addstr(0, 0, "You presse UP ")
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(drop_down_list) -1:
                current_row  += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.inner_left_window.addstr(-1,0, "You selected {}".format(drop_down_list[current_row]))
                self.screen.refresh()
                answer = drop_down_list[current_row]
                time.sleep(5)
                break
            self.inner_left_window.refresh()
            """
                if current_row == len(drop_down_list) - 1:
                    self.quit_display()
                    """
            self.display_menu(current_row, drop_down_list, question)
            self.inner_left_window.refresh()
curses.wrapper(test_textpad)


