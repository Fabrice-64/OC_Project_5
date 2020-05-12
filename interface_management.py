"""
    
    This module manages the graphical interface for the application.

    As the application is built in a View-Model-Controller logic, \
        this module hosts all the necessary items to manage the View functionalities.
    This module is fed with orders coming the module named: get_better_diet.py.

    Class:

    Interface : based on curses library it provides a rough but functional graphic interface

    Exceptions:

    No exception is dealt with in this class.

    Functions:

    No function has been implemented. All methods belong to the Interface class.

    """
import curses
import os
import time
import webbrowser
from curses import textpad

import config


class Interface:
    """ 

        Manages the graphical interface of this application.

        The integrated library curses is used throughout the class.
        The main screen is split into two halves: 
        -The left one (from the User perspective) is used for the interaction with him, 
        -The right one displays the results of the queries or even a warning in some cases.

        Methods:

        __init__(): initialize the graphic interface to make it usable by the subsequent methods.

        title_bar(): display a title in the bar at the top of the main window. \
            This title is updated in accordance with the step of the program.

        split_screen(): split the screen in two separate windows. 
        In fact each window include a sub-window in which the text is displayed. 

        display_message(): display a message on the main window, at the center of the screen. \
            Is used for welcome message and for goodbye.

        left_window_display_string(): display an instruction on the left screen.

        left_window_display_string_textpad(): display an invitation to use the keypad \
            and just below the keypad itself. 
        It is composed of two other methods:  left_window_display_string() and display_textpad.

        clear_window(): reinitialize the sub-windows.

        display_file_right_window(): display larger files for to be scrolled down.

        right_window_display_result():  display the results of the queries sent to the DB.

        right_window_display_info(): display one line long pieces of info at the bottom of the right window.

        highlight_selection():  highlight the selected itemwhen using a drop-down list.

        set_up_drop_down(): operate the key UP and DOWN iot iterate in the menu displayed.

        display_users_guide_textpad(): display a short users guide at the bottom of left page

        display_textpad(): display a textpad used to capture the user's various inputs.

        quit_display(): desactivate in a clean way all the features activated by the use of curses.

        Attributes:

        Most attributes are used to set coordinates useful for displaying the content.

        title: display a title in the bar set at the top of the main window

        y_center and x_center: represent the centre of the main screen. Used later on to display text, ect.

        half_win_height & half_win_width: set the size of each half window \
            as the main window is split in 2.

        left_window & inner_left_window: cover, from a user's perspective, \
            the left half of the main window

        right_window and inner_right_window: cover, from a user's perspective, \
            the right half of the main window

        message: display a message on the screen centre at the beginning of the execution

        screen_x_center: calculate the center of the main screen for a well centered intro message.

        x_center_half_l_window & y_center_half_l_window: represent y \
            & x of the center of the left half window

        """

    def __init__(self):
        """

            The graphic screen is initialized from the very first step of the application.

            Arguments:

            NIL.

            Returns:

            NIL.

            """
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
        self.screen.addstr(curses.LINES - 1, 0, "Copyright Moi")
        self.height, self.width = self.screen.getmaxyx()
        self.y_center = self.height//2
        self.x_center = self.width//2

    def title_bar(self, title):
        """ 

            A new title bar is displayed for each and every step of the program. \
                This method is called through the module get_better_diet.py

            Argument : 

            title :  adapt the window title to the step of the program.

            Return:

            NIL.

            """
        self.screen.clear()
        self.title = title
        self.screen.bkgd(' ', curses.color_pair(1))
        self.screen.chgat(curses.A_REVERSE)
        self.screen.addstr(0, (self.x_center-len(self.title)//2),
                           self.title, curses.A_REVERSE)
        self.screen.refresh()

    def split_screen(self):
        """

            Split the screen in 2 halves to share between queries or requests and their outcome.

            Argument:

            NIL.

            Return:
            
            NIL.

            """
        # Setting up the parameters to get 2 split sub-windows
        self.half_win_height = self.height-2
        self.half_win_width = self.x_center - 2
        # create a left window and an innner window to display text
        self.left_window = curses.newwin(
            self.half_win_height, self.half_win_width, 1, 2)
        self.inner_left_window = self.left_window.subwin(
            self.half_win_height - 2, self.half_win_width - 2, 2, 3)
        self.left_window.noutrefresh()
        # Create a right window and an inner window to display results
        self.right_window = curses.newwin(
            self.half_win_height, self.half_win_width-2, 1, self.x_center + 3)
        self.inner_right_window = self.right_window.subwin(
            self.half_win_height - 2, self.half_win_width - 4, 2, self.x_center + 4)
        self.right_window.noutrefresh()
        self.screen.refresh()

    def display_message(self, message):
        """

            Display a message centered on the main screen

            Arguments:

            message: string defined in the module config.py.

            Return:
            
            NIL.

            """
        curses.curs_set(0)
        self.message = " ".join(message)
        self.screen_x_center = self.x_center - len(self.message)//2
        self.screen.addstr(self.y_center, self.screen_x_center,
                           self.message, curses.A_BOLD)
        self.screen.refresh()
        curses.beep()
        self.screen.clear()

    def left_display_string(self, y, string):
        """

            Display a string from module config.py. By default, x = 0.
            Vertical coordinate is used as an argument, x = 0 by default.

            Arguments:

            y: vertical coordinate, which 0 is the upper left corner of the inner left window.

            string: set in config.py. By default includes \n.

            Returns:

            NIL.

            """
        self.inner_left_window.addstr(y, 0, string)
        self.inner_left_window.refresh()

    def display_string_textpad(self, y, nb_lines, length_field, message):
        """

            Display a string followed, at the line below by a textpad aimed at catching a user's input.

            Arguments:

            y: vertical coordinate, which 0 is the upper left corner of the inner left window.

            nb_lines : number of lines of the keypad

            length_field: maximum number of characters allowed +1, due to curses specifications

            message: string from config.py explaining what is expected from the user.

            Returns:

            answer: under ASCII format, the string typed in the textpad by the user.

            y: incremented vertical coordinate.

            """
        self.left_window_display_string(y, message)
        answer = self.display_textpad(y+2, nb_lines, length_field)
        y = y + 2 + nb_lines + 1
        return answer, y

    def clear_window(self, window="both"):
        """

            Clear the window from all its content.

            Arguments:

            window: by default, both half screens are cleared, if required, \
                only the left or the right can be affected.

            Returns:
            
            NIL

            """
        if window == "left" or window == "both":
            self.inner_left_window.clear()
            self.inner_left_window.refresh()
        if window == "right" or window == "both":
            self.inner_right_window.clear()
            self.inner_right_window.refresh()

    def display_file(self, file):
        """

            Display a file line by line. The user is expected to click at every new line, \
            which appears in fact as a paragraph.
            Currently can only scroll down, not up. To be fixed in a future version.

            Arguments:

            file: any file in txt format.

            Returns:

            NIL

            """
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

    def display_result(self, string):
        """

            Display the result of a query, line by line, on the right window.

            Arguments:

            string: a string, usually out of a dictionary or a list, both being the result of a query.

            Returns: 

            NIL

            """
        self.inner_right_window.addstr(string)
        self.inner_right_window.refresh()

    def right_display_info(self, message, type="info"):
        """

            Display a information message at the bottom line of the right window.
            The line is cleared after the user has pressed any key.

            Arguments:

            message: the string to be displayed.

            type: depending on the type, the background color will change.

            Returns:

            NIL.

            """
        y, x = self.inner_right_window.getmaxyx()
        if type == "warning":
            color_pair = curses.color_pair(3)
        elif type == "info":
            color_pair = curses.color_pair(2)
        self.inner_right_window.attron(color_pair)
        self.inner_right_window.addstr(y-1, 0, message)
        self.inner_right_window.attroff(color_pair)
        self.inner_right_window.refresh()
        self.inner_right_window.getch()
        self.inner_right_window.move(y-1, 0)
        self.inner_right_window.clrtoeol()
        self.inner_right_window.refresh()

    def highlight_selection(self, active_row_idx, drop_down_list):
        """

            Highlight the selected row in a drop-down list.

            Arguments:

            active_row_idx (int): index of the row to be highlighted.

            drop_down_list (list); list to be displayed for the user to chose an item.

            Returns:

            NIL

            """
        height, width = self.inner_left_window.getmaxyx()
        for idx, row in enumerate(drop_down_list):
            # Recalculate the coordinate taking into account the length of each and every string.
            self.x_center_half_l_win = width//2 - len(row)//2
            self.y_center_half_l_win = height//2 - len(drop_down_list)//2 + idx
            # Highlight the item on which the cursor is set.
            if idx == active_row_idx:
                self.inner_left_window.attron(curses.color_pair(2))
                self.inner_left_window.addstr(
                    self.y_center_half_l_win, self.x_center_half_l_win, row)
                self.inner_left_window.attroff(curses.color_pair(2))
            else:
                self.inner_left_window.addstr(
                    self.y_center_half_l_win, self.x_center_half_l_win, row)
            self.inner_left_window.refresh()

    def set_up_drop_down(self, drop_down_list, question):
        """

            Manage the cursor movements within a drop-down list.
            It interacts closely with the method highlight_selection() of the same class.

            Arguments:

            drop_down_list (list): set in the config.py module

            question: set in the config.py module.

            Returns:

            answer : the choice made by the user after having higlighted it + pressed retun.

            """
        curses.curs_set(0)
        self.inner_left_window.keypad(True)
        active_row_idx = 0
        self.highlight_selection(active_row_idx, drop_down_list)
        # Loop to travel up and down through the list.
        while True:
            key = self.inner_left_window.getch()
            if key == curses.KEY_UP and active_row_idx > 0:
                active_row_idx -= 1
            elif key == curses.KEY_DOWN and active_row_idx < len(drop_down_list)-1:
                active_row_idx += 1
            # [10,13] is needed due to compatibility issues with some keyboards.
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.inner_left_window.clear()
                answer = drop_down_list[active_row_idx]
                self.inner_left_window.addstr(
                    0, 0, "You selected {}".format(answer))
                break
            self.highlight_selection(active_row_idx, drop_down_list)
        self.inner_left_window.refresh()
        return answer

    def display_guide(self, user_guide):
        """ 

            This method displays the list of keyboard shortcuts to be used with the keypad.
            It doesn't return anything

            Arguments:
                
            user_guide (list): is available in config.py

            Returns:

            NIL

            """
        y, x = self.inner_left_window.getmaxyx()
        y = y-1
        index = -1
        # Lines are printed in a reverse order: from the last line of the window upwards.
        for line in user_guide:
            line = user_guide[index]
            self.inner_left_window.addstr(y, 0, line)
            y -= 1
            index -= 1
        self.inner_left_window.refresh()

    def display_textpad(self, upper_left_y, nblines, nbcols):
        """

            Display a textpad enclosed in a rectangle, so it is visible.

            Arguments:

            upper_left_y: vertical coordinate of the upper left corner of the keypad.

            nb_lines: number of lines of the keypad

            nb_cols: number of max of authorized characters + 1 because of curses.

            Returns:

            content: values on ASCII format typed by the user.

            """
        self.win = self.inner_left_window.derwin(
            nblines, nbcols, upper_left_y, 1)
        self.win.clear()
        textpad.rectangle(self.inner_left_window, upper_left_y -
                          1, 0, upper_left_y + nblines, nbcols+1)
        curses.curs_set(1)
        self.win.refresh()
        box = textpad.Textbox(self.win, insert_mode=True)
        self.inner_left_window.refresh()
        content = box.edit()
        curses.curs_set(0)
        return content

    def quit_display(self):
        """

            This method is used to properly quit the Curses module and reinitialize the shell.

            Arguments:

            NIL.

            Returns:
            
            NIL.

            """
        self.clear_window()
        self.left_window_display_string(0, config.QUIT_MESSAGE)
        time.sleep(1)
        self.screen.clear()
        self.screen.keypad(False)
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
