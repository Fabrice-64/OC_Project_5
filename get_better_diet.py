"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module.

"""
import interface_management as im
import config as cfg
import time

class UserDialog:
   def __init__(self):
        self.interface = im.Interface()

   def step_terms_and_conditions(self, file):
      self.interface.title_bar(cfg.TITLE_1)
      self.interface.left_window_display_string(0, cfg.T_C_LINE_1)
      self.interface.left_window_display_string(1, cfg.T_C_LINE_2)
      self.interface.display_file_right_window(file)
      self.interface.clear_window("left")
      self.interface.left_window_display_string(0, cfg.T_C_QUESTION_ACCEPT_T_C)
      self.interface.left_window_display_string(1, cfg.T_C_IF_REFUSAL)
      answer = self.interface.set_up_drop_down(cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
      if answer == "Yes":
         self.interface.clear_window('left')
         self.interface.left_window_display_string(0, "You have decided to go on with the program")
         time.sleep(3)
      elif answer == "No":
         self.interface.clear_window('left')
         self.interface.clear_window('right')
         self.interface.left_window_display_string(0, "The program will quit in a few seconds")
         time.sleep(3)
         self.interface.quit_display()

   def step_select_action(self):
      self.interface.title_bar(cfg.TITLE_2)
      self.interface.clear_window('left')
      self.interface.clear_window('right')
      self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
      self.interface.right_window_display_result(0, "The results will be displayed in this window\n")
      time.sleep(3)
      pass     

def main(user):
   user.interface.display_message(cfg.WELCOME_MESSAGE)
   time.sleep(3)
   user.interface.split_screen(cfg.TITLE_0)
   user.step_terms_and_conditions("Documentation/texte_T&C.txt")
   user.step_select_action()
   
if __name__ == "__main__":
   user = UserDialog()
   main(user)