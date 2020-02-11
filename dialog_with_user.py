"""
This module is intended to deal with the dialog with the user
"""
import time
import webbrowser
import os
import curses
import config
class Interface():
    def __init__(self):
        self.screen = curses.initscr()
        y,x = self.screen.getmaxyx()
        self.y_center = y//2
        self.x_center = x//2

    def display_message(self, message):
        self.x_center = self.x_center - len(message)//2
        self.screen.addstr(self.y_center, self.x_center, message, curses.A_BOLD)
        self.screen.refresh()
        self.screen.getch()
        curses.beep()
        self.screen.clear()
    
    def display_menu(self):
        print("Display Menu OK")
    
    def request_registered_user(self):
        self.display_menu()
        print("Registered User OK")
    """
        self.screen.keypad(0)
        curses.noecho()
        
        self.screen.refresh()
        self.screen.getch()
        curses.endwin()
    print("This program helps you to compare food items and get the one with a better nutrition grade")
    time.sleep(2)
    print("Before going ahead, you are requested to approve the Open Food Facts Disclaimer")
     def get_centre_screen():
        #scr = curses.initscr()
        screen_h, screen_w = self.screen.getmaxyx()
        return(screen_h, screen_w)

def display_terms_conditions():
    time.sleep(3)
    cwd = os.getcwd()
    file_location = str('file:'+cwd + '/terms_conditions_users.pdf')
    webbrowser.open(file_location,new=1)

def input_correct_answer():
    answer = ""
    counter = 0
    while answer not in ["n", "N","y","Y"] and counter <3:
        counter+=1
        answer = input("Please answer with Y or N:\n")
    return(answer)

def wish_to_quit():
    print("You didn't accept the terms and conditions of use, therefore the application is about to close!")
    time.sleep(5)
    exit()

def accept_OFF_T_C():
    display_terms_conditions()
    answer = input("You ought to accept the Open Food Facts Warning, if you intend to use the App. Do you accept them? (Y/N)\n")
    if answer in ["n","N","y","Y"]:
        if answer in ["n","N"]:
            wish_to_quit()
        else:
            return("OK")
    else:
        answer2 = input_correct_answer()
        if answer2 not in ["y","Y"]:
            wish_to_quit()
        else:
            return("OK après échecs")
            """
def main():
    screen = Interface()
    screen.display_message(config.welcome_message)
    screen.request_registered_user()

if __name__ == "__main__":
    main()


    

