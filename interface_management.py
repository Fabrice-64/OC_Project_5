"""
This module is intended to deal with the dialog with the user
"""
import time
import webbrowser
import os
import curses
import config
from curses import textpad

class Interface:
    def __init__(self):
        self.screen = curses.initscr()
        # Setting up the Curses parameters to use the screen
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

        # Setting up the parameters used to design the windows
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.screen.addstr(curses.LINES -1, 0, "Copyright Moi" )
        self.y, self.x = self.screen.getmaxyx()
        self.y_center = self.y//2
        self.x_center = self.x//2

    # Setting up a title bar for the main window
    def title_bar(self, title):
        """ A new title bar is displayed for each and every step of the program. This method is called through the module get_better_diet.py
            Attribute : title
            The constant pair of colors, background and characters, are set in the __init__ method of this class.
        """
        self.title = title
        self.screen.bkgd(' ',curses.color_pair(1))
        self.screen.chgat(curses.A_REVERSE)
        self.screen.addstr(0, (self.x_center-len(self.title)//2), self.title, curses.A_REVERSE)
        self.screen.refresh()

    def split_screen(self, title):
        # Setting up the parameters to get 2 split sub-windows
        self.half_win_height = self.y-2
        self.half_win_width = self.x_center -2

        #create a left window and an innner window to display text
        self.left_window = curses.newwin(self.half_win_height, self.half_win_width, 1, 2)
        self.left_window.box()
        self.inner_left_window = self.left_window.subwin(self.half_win_height -2, self.half_win_width -2,2,3)
        self.left_window.noutrefresh()
        
        # Create a right window and an inner window to display results
        self.right_window = curses.newwin(self.half_win_height, self.half_win_width-2, 1, self.x_center +3)
        self.right_window.box()
        self.inner_right_window = self.right_window.subwin(self.half_win_height -2, self.half_win_width -4,2,self.x_center +4)
        self.right_window.noutrefresh()
        
        self.screen.refresh()
    
    def display_message(self, message):
        curses.curs_set(0)
        self.message = " ".join(message)
        self.screen_x_center = self.x_center - len(self.message)//2
        self.screen.addstr(self.y_center, self.screen_x_center, self.message, curses.A_BOLD)
        self.screen.refresh()
        time.sleep(1)
        curses.beep()
        self.screen.clear()
    
    def left_window_display_string(self, y, string):
        self.inner_left_window.addstr(y,0,string)
        self.inner_left_window.refresh()
    
    def clear_window(self, window):
        if window == "left":
            self.inner_left_window.clear()
            self.inner_left_window.refresh()
        elif window == "right":
            self.inner_right_window.clear()

    def display_file_right_window(self, file):
        with open(file, "rb") as file:
            self.inner_right_window.scrollok(True)
            curses.curs_set(1)
            file = file.readlines()
            self.inner_right_window.addstr(file[0])
            self.inner_right_window.refresh()
            for line in file[1:]:
                self.inner_right_window.scrollok(1)
                self.inner_right_window.getch()
                self.inner_right_window.addstr(line)
                self.inner_right_window.refresh()


    def higlight_selection(self, active_row_idx, drop_down_list):
        h,w = self.inner_left_window.getmaxyx()
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        for idx, row in enumerate(drop_down_list):
            self.x_center = w//2
            self.y_center = h//2 - len(drop_down_list)//2 +idx
            if idx == active_row_idx:
                self.inner_left_window.attron(curses.color_pair(2))
                self.inner_left_window.addstr(self.y_center, self.x_center, row)
                self.inner_left_window.attroff(curses.color_pair(2))
            else:
                self.inner_left_window.addstr(self.y_center, self.x_center, row)
            self.inner_left_window.refresh()
        
    def set_up_drop_down(self, drop_down_list, question):
        curses.curs_set(0)
        self.inner_left_window.keypad(True)
        active_row_idx = 0
        self.higlight_selection(active_row_idx, drop_down_list)
        while True:
            key = self.inner_left_window.getch()
            if key == curses.KEY_UP and active_row_idx >0:
                active_row_idx -= 1
            elif key == curses.KEY_DOWN and active_row_idx < len(drop_down_list)-1:
                active_row_idx +=1
            elif key == curses.KEY_ENTER or key in [10,13]:
                self.inner_left_window.clear()
                answer = drop_down_list[active_row_idx]
                self.inner_left_window.addstr(0,0, "You selected {}".format(answer))
                break
            self.higlight_selection(active_row_idx, drop_down_list)
        self.inner_left_window.refresh()
        return answer

    def quit_display(self):
        self.screen.clear()
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        exit()
    
def display_terms_conditions(self):
    cwd = os.getcwd()
    file_location = str('file:'+ cwd + '/terms_conditions_users.pdf')
    webbrowser.open(file_location,new=1)
