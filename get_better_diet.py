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
      y = 0
      self.interface.title_bar(cfg.TITLE_2)
      self.interface.clear_window('left')
      self.interface.clear_window('right')
      self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
      self.interface.right_window_display_result(0, "The results will be displayed in this window\n")
      answer = self.interface.set_up_drop_down(cfg.S_A_OPERATE_ON_DB,cfg.SELECT_ANSWER)
      if answer == cfg.S_A_OPERATE_ON_DB[0]:
         self.interface.left_window_display_string(y, cfg.KEYPAD_INSTRUCTION_1)
         self.interface.left_window_display_string(y+1, cfg.S_A_SELECT_CATEGORY)
         self.interface.clear_window("right")
         categories = self.queries.get_categories()
         for (key, category) in categories.items():
            self.interface.right_window_display_result(y+1,"{}:  {}\n".format(key, category))
            y += 1
         self.interface.display_users_guide_textpad()
         # In interface.display_textpad(y, nblines, nbcols), the y is incremented by 1 for every new line
         # The y is where the texpad starts, the number of lines and cols to select the category
         answer_category = self.interface.display_textpad(2,1,3)
         answer_category = int(answer_category)
         running = True
         while running:
            if int(answer_category) in categories.keys():
               running = False
            else:
               self.interface.right_window_display_warning()               
               answer_category = self.interface.display_textpad(2,1,3)
               running = True
         
         self.interface.left_window_display_string(5,cfg.S_A_DESCRIBE_FOOD_ITEM)
         answer_description = self.interface.display_textpad(7,1,40)
         # Fill the required fields to characterize the food item the user is looking for
         # Query for a substitution aliment
      elif answer == cfg.S_A_OPERATE_ON_DB[1]:
         # Query for getting a recorded food item
         pass
      elif answer == cfg.S_A_OPERATE_ON_DB[2]:
         self.interface.clear_window("left")
         self.interface.left_window_display_string(0,cfg.S_A_INFO_ADD_NEW_CATEGORY)
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