"""
This module is intended to deal with the dialog with the user
"""
import time
import webbrowser
import os
import curses
import config
<<<<<<< HEAD
from curses import textpad
=======
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9

class Interface:
    def __init__(self):
        self.screen = curses.initscr()
<<<<<<< HEAD
        # Setting up the Curses parameters to use the screen
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

        # Setting up the parameters used to design the windows
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.y, self.x = self.screen.getmaxyx()
        self.y_center = self.y//2
        self.x_center = self.x//2
    
    def split_screen(self):
        self.half_win_height = self.y-3
        self.half_win_length = self.x_center -4
        self.screen.bkgd(' ',curses.color_pair(1))

        title = "Fenêtre de Titre"
        self.screen.chgat(curses.A_REVERSE)
        self.screen.addstr(0, (self.x_center -len(title)//2), title, curses.A_REVERSE)
        self.screen.addstr(curses.LINES -1, 0, "Type Q to quit" )
        self.screen.refresh()
        time.sleep(3)

    def display_message(self, message):
        curses.curs_set(0)
        message = " ".join(message)
=======
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        y,x = self.screen.getmaxyx()
        self.y_center = y//2
        self.x_center = x//2

    def display_message(self, message):
        curses.curs_set(0)
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9
        self.x_center = self.x_center - len(message)//2
        self.screen.addstr(self.y_center, self.x_center, message, curses.A_BOLD)
        self.screen.refresh()
        time.sleep(3)
        curses.beep()
        self.screen.clear()

    def display_menu(self, selected_row_idx, drop_down_list, question):
        self.screen.clear()
        guideline = "Please give a response to this request:"
        x = self.x_center
        y = self.y_center - len(drop_down_list)//2
        self.screen.addstr(y -4 , x - (len(guideline)//2), guideline)
        self.screen.addstr(y -2, x - (len(question)//2), question)
        self.screen.refresh()
        for idx,row in enumerate(drop_down_list):
            y_temp = y + idx
            if idx == selected_row_idx:
                self.screen.attron(curses.color_pair(1))
                self.screen.addstr(y_temp, x, row)
                self.screen.attroff(curses.color_pair(1))
                self.screen.refresh()
            else:
                self.screen.addstr(y_temp, x, row)
        self.screen.refresh()

    def set_up_drop_down(self, drop_down_list, question):
        curses.curs_set(0)
<<<<<<< HEAD
=======
        curses.start_color()
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        current_row = 0
        self.display_menu(current_row, drop_down_list, question)

        while True:
            key = self.screen.getch()
            if key == curses.KEY_UP and current_row> 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(drop_down_list) -1:
                current_row  += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.screen.addstr(0,0, "You selected {}".format(drop_down_list[current_row]))
                self.screen.refresh()
                answer = drop_down_list[current_row]
                break
                if current_row == len(drop_down_list) - 1:
                    self.quit_display()
            self.display_menu(current_row, drop_down_list, question)
        return(answer)

    def quit_display(self):
        self.screen.clear()
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        exit()

<<<<<<< HEAD


=======
class UserDialog:
    def __init__(self):
        self.interface = Interface()

    def request_registered_user(self, drop_down_list, question):
        answer = self.interface.set_up_drop_down(drop_down_list, question)
        if answer == "No":
            self.interface.screen.addstr(0,0, "You first ought to approve the Terms & Conditions of use")
            
            display_terms_conditions()
        elif answer == "Yes":
            authenticate_user()
            self.interface.screen.addstr(0,0, "You chose to identify")
            self.interface.screen.refresh()
            time.sleep(3)
        else:
            self.interface.screen.addstr(0,0, "You chose to quit")
            self.interface.screen.refresh()
            time.sleep(3)
            self.interface.quit_display()
            
        time.sleep(3)
    
    def display_terms_conditions(self):
        cwd = os.getcwd()
        file_location = str('file:'+ cwd + '/terms_conditions_users.pdf')
        webbrowser.open(file_location,new=1)
        
    def authenticate_user(self):
        pass


def main():
    dialog = UserDialog()
    dialog.interface.display_message(config.welcome_message)
    dialog.request_registered_user(config.reply_yes_no_quit, config.registered_user_y_n)

if __name__ == "__main__":
    main()
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9


    

