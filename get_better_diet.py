"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module.

"""
import interface_management as im
import connect_to_mysql as sql
import config as cfg
import time

class UserDialog:
   def __init__(self):
        self.interface = im.Interface()
        self.queries = sql.MySQLQueries()

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
         self.interface.quit_display()

   def step_select_action(self):
      self.interface.title_bar(cfg.TITLE_2)
      self.interface.clear_window('left')
      self.interface.clear_window('right')
      self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
      self.interface.right_window_display_result(0, "The results will be displayed in this window\n")
      answer = self.interface.set_up_drop_down(cfg.S_A_OPERATE_ON_DB,cfg.SELECT_ANSWER)
      if answer == cfg.S_A_OPERATE_ON_DB[0]:
         self.interface.left_window_display_string(0, cfg.KEYPAD_INSTRUCTION_1)
         self.interface.left_window_display_string(1, cfg.S_A_SELECT_CATEGORY)
         self.interface.clear_window("right")
         self.queries.get_categories()
         for (id, category) in self.queries.cursor:
            self.interface.right_window_display_result("{}:  {}".format(id, category))
         self.interface.display_text_pad(2,1,2)
         # Fill the required fields to characterize the food item the user is looking for
         # Query for a substitution aliment
      elif answer == cfg.S_A_OPERATE_ON_DB[1]:
         # Query for getting a recorded food item
         pass
      elif answer == cfg.S_A_OPERATE_ON_DB[2]:
         # Upload new category from OFF
         # First designate a category to be uploaded
         # Fetch the category from OFF
         # Insert the result into the local DB
         pass
      elif answer == cfg.S_A_OPERATE_ON_DB[3]:
         self.interface.quit_display()

      time.sleep(2)

def main(user):
   user.interface.display_message(cfg.WELCOME_MESSAGE)
   time.sleep(1)
   user.interface.split_screen(cfg.TITLE_0)
   user.step_terms_and_conditions("Documentation/texte_T&C.txt")
   user.step_select_action()
   
if __name__ == "__main__":
   user = UserDialog()
   main(user)