"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module

"""
import dialog_with_user

if __name__ =="__main__":
   dialog_with_user.display_welcome_message()

dialog_with_user.read_OFF_warning()