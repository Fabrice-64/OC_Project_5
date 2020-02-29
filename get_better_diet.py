"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module

"""
import interface_management as im
<<<<<<< HEAD
import config as cfg
import time

class UserDialog:
   def __init__(self):
        self.interface = im.Interface()
        

def main(user):
   user.interface.display_message(cfg.WELCOME_MESSAGE)
   time.sleep(3)
   user.interface.split_screen()
   

   
if __name__ == "__main__":
   user = UserDialog()
   main(user)


=======

if __name__ =="__main__":
   user = im.UserDialog()
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9

