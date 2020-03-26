"""
    This module intends to play the role of an interface with the user when navigating in the program.

    This module is fed with orders coming form get_better_diet.py module.
    It encompasses only one class, named Interface.
Methods:
    title_bar(): displays a title in the bar at the top of the main window. This title is updated in accordance with the step of the program.
    split_screen(): splits the screen in two separate windows. In fact each window includes a sub-window in which the text is displayed. 
    This is demanded when using curses in order to avoid having the text stepping over the borders of the window.
    display_message():  this method displays a message on the main window, at the center of the screen. Is used for welcome message and for goodbye.
    left_window_display_string() : this method is set to display an instruction on the left screen.
    clear_window():  is needed to reinitialize the sub-window and remove the useless text.
    display_file_right_window(): the right window is used for displaying larger files for which this method allows to scroll them down.
    right_window_display_result(): the results of the queries sent to the DB are displayed on this window. The outcome is formatted by this method
    highlight_selection(): when using a drop-down list, this methods highlights the selected item
    set_up_drop_down(): this method is used in connexion with the method highlight_selection, as it provides the latter with the relevant index. 
    It activates the key UP and DOWN iot iterate in the menu displayed.
    quit_display(): as the module Curses activate many features of the shell, this method intends to desactivate all the features activated by the script.

Attributes:
    Most attributes are used to set coordinates useful for displaying the content.
    title:  used to display a title in the bar set at the top of the main window
    half_win_height & half_win_width:   when the main window is split in 2, it sets the size of each half window
    left_window & right_window: cover half of the main window
    inner_left_window and inner_right_window: are inside the half windows and are uses to better manage the displayed text.
    message: used to display a message at the center of the screen at welcome and in a future version by exiting the program
    y_center & x_center: set the center of the main screen
    screen_x_center: used to get the x of the center of the main window, whatever the length of the string to be displayed is
    x_center_half_l_window & y_center_half_l_window:    y & x of the center of the left half window

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
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        self.screen.addstr(curses.LINES -1, 0, "Copyright Moi" )
        self.height, self.width = self.screen.getmaxyx()
        self.y_center = self.height//2
        self.x_center = self.width//2

    # Setting up a title bar for the main window
    def title_bar(self, title):
        """ 
            A new title bar is displayed for each and every step of the program. This method is called through the module get_better_diet.py
            Attribute : title
            The constant pair of colors, background and characters, are set in the __init__ method of this class.
        """
        self.screen.clear()
        self.title = title
        self.screen.bkgd(' ',curses.color_pair(1))
        self.screen.chgat(curses.A_REVERSE)
        self.screen.addstr(0, (self.x_center-len(self.title)//2), self.title, curses.A_REVERSE)
        self.screen.refresh()

    def split_screen(self, title):
        # Setting up the parameters to get 2 split sub-windows
        self.half_win_height = self.height-2
        self.half_win_width = self.x_center -2

        #create a left window and an innner window to display text
        self.left_window = curses.newwin(self.half_win_height, self.half_win_width, 1, 2)
        self.inner_left_window = self.left_window.subwin(self.half_win_height -2, self.half_win_width -2,2,3)
        self.left_window.noutrefresh()
        
        # Create a right window and an inner window to display results
        self.right_window = curses.newwin(self.half_win_height, self.half_win_width-2, 1, self.x_center +3)
        self.inner_right_window = self.right_window.subwin(self.half_win_height -2, self.half_win_width -4,2,self.x_center +4)
        self.right_window.noutrefresh()
        self.screen.refresh()
        
    def get_cursor_position(self):
        y, x = curses.getsyx()
        return y,x
    
    def set_cursor_position(self,y,x):
        self.inner_left_window.move(0,x)
        self.inner_left_window.refresh()
        
    def display_message(self, message):
        curses.curs_set(0)
        self.message = " ".join(message)
        self.screen_x_center = self.x_center - len(self.message)//2
        self.screen.addstr(self.y_center, self.screen_x_center, self.message, curses.A_BOLD)
        self.screen.refresh()
        curses.beep()
        self.screen.clear()
    
    def left_window_display_string(self, y, string):
        self.inner_left_window.addstr(y, 0, string)
        self.inner_left_window.refresh()
    
    def clear_window(self, window = "both"):
        if window == "left":
            self.inner_left_window.clear()
            self.inner_left_window.refresh()
        elif window == "right":
            self.inner_right_window.clear()
            self.inner_right_window.refresh()
        elif window == "both":
            self.inner_left_window.clear()
            self.inner_left_window.refresh()
            self.inner_right_window.clear()
            self.inner_right_window.refresh()

    def display_file_right_window(self, file):
        with open(file, "rb") as file:
            self.inner_right_window.scrollok(True)
            file = file.readlines()
            self.inner_right_window.addstr(file[0])
            self.inner_right_window.refresh()
            for line in file[1:]:
                self.inner_right_window.scrollok(1)
                self.inner_right_window.getch()
                self.inner_right_window.addstr(line)
                self.inner_right_window.refresh()
    
    def right_window_display_result(self,string):
        self.inner_right_window.addstr(string)
        self.inner_right_window.refresh()

    def right_window_display_warning(self):
        y, x = self.inner_right_window.getmaxyx()
        self.inner_right_window.attron(curses.color_pair(3))
        self.inner_right_window.addstr(y-1, 0, "PLEASE ENTER A CORRECT VALUE")
        self.inner_right_window.attroff(curses.color_pair(3))
        self.inner_right_window.refresh()
        self.inner_right_window.getch()
        self.inner_right_window.move(y-1,0)
        self.inner_right_window.clrtoeol()
        self.inner_right_window.refresh()
    
    def right_window_display_info(self, info_string):
        y, x = self.inner_right_window.getmaxyx()
        self.inner_right_window.addstr(y-1, 0, info_string)
        self.inner_right_window.refresh()
        self.inner_right_window.getch()
        self.inner_right_window.move(y-1,0)
        self.inner_right_window.clrtoeol()
        self.inner_right_window.refresh()

    def highlight_selection(self, active_row_idx, drop_down_list):
        """
            This method depends on set_up_drop_down() method and is solely used for highlighting the selected row.

            Args:
            active_row_idx (int): gives the index of the row to be highlighted.
            drop_down_list (list); used to display the list in the center of the inner left window.

            Returns:
            This method does not return anything.
        """
        h,w = self.inner_left_window.getmaxyx()
        for idx, row in enumerate(drop_down_list):
            self.x_center_half_l_win = w//2 - len(row)//2
            self.y_center_half_l_win = h//2 - len(drop_down_list)//2 +idx
            if idx == active_row_idx:
                self.inner_left_window.attron(curses.color_pair(2))
                self.inner_left_window.addstr(self.y_center_half_l_win, self.x_center_half_l_win, row)
                self.inner_left_window.attroff(curses.color_pair(2))
            else:
                self.inner_left_window.addstr(self.y_center_half_l_win, self.x_center_half_l_win, row)
            self.inner_left_window.refresh()
        
    def set_up_drop_down(self, drop_down_list, question):
        """
            This method manages the cursor movements within a drop-down list, in order to highlight the selected item of the list.
            Therefore it interacts closely with the method highlight_selection() of the same class.

            Args:
            drop_down_list is set in the config.py module and is conceived as a list.
            question is set in the config.py module and is to be looked at either as a request to the user or an advice so that he can better understand the purpose of this list.

            Returns:
            The answer returned is subsequently used in the get_better_diet_py module to operate the program.
        """
        curses.curs_set(0)
        self.inner_left_window.keypad(True)
        active_row_idx = 0
        self.highlight_selection(active_row_idx, drop_down_list)
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
            self.highlight_selection(active_row_idx, drop_down_list)
        self.inner_left_window.refresh()
        return answer

    def display_users_guide_textpad(self):
        """
            This method displays the list of keyboard shortcuts to be used with the keypad.
            It doesn't return anything
        """
        y,x = self.inner_left_window.getmaxyx()
        self.inner_left_window.addstr(y-1, 0, config.KEYBOARD_INFO_1)
        self.inner_left_window.addstr(y-2, 0, config.KEYBOARD_INFO_2)
        self.inner_left_window.addstr(y-3, 0, config.KEYBOARD_INFO_3)
        self.inner_left_window.addstr(y-4, 0, config.KEYBOARD_INFO_4)
        self.inner_left_window.addstr(y-5,0 , config.KEYBOARD_INFO_5)
        self.inner_left_window.addstr(y-6, 0, config.KEYBOARD_INFO_0)
        self.inner_left_window.addstr(y-7, 0, config.KEYBOARD_INFO_00)
        self.inner_left_window.refresh()

    def display_textpad(self, upper_left_y, nblines, nbcols):
        self.win = self.inner_left_window.derwin(nblines , nbcols, upper_left_y, 1)
        self.win.clear()
        textpad.rectangle(self.inner_left_window, upper_left_y-1, 0, upper_left_y + nblines, nbcols+1)
        curses.curs_set(1)
        self.win.refresh()
        box = textpad.Textbox(self.win, insert_mode= True)
        self.inner_left_window.refresh()
        content = box.edit()
        curses.curs_set(0)
        return content

    def quit_display(self):
        """
            This method is used to properly quit the Curses module and reinitialize the shell.

            Args:
            It takes no argument

            Returns:
            It doesn't return anything
        """
        self.clear_window('left')
        self.clear_window('right')
        self.left_window_display_string(0, "The program will quit in a few seconds")
        time.sleep(1)
        self.screen.clear()
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        exit()
    

