"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module.

"""
import interface_management as im
import connect_to_mysql as sql
import connect_to_OFF
import config_open_food_facts as coff
import config_queries as cq
import config as cfg
import time

class UserDialog:
   def __init__(self):
        self.interface = im.Interface()
        self.queries = sql.MySQLQueries()

   def step_terms_and_conditions(self, file):
      self.interface.title_bar(cfg.TITLE_1)
      self.interface.left_window_display_string(0,cfg.T_C_LINE_1)
      self.interface.left_window_display_string(1, cfg.T_C_LINE_2)
      self.interface.display_file_right_window(file)
      self.interface.clear_window("left")
      self.interface.left_window_display_string(0, cfg.T_C_QUESTION_ACCEPT_T_C)
      self.interface.left_window_display_string(1, cfg.T_C_IF_REFUSAL)
      answer = self.interface.set_up_drop_down(cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
      if answer == "Yes":
         self.interface.clear_window('left')
         self.interface.left_window_display_string(0, "You have decided to go on with the program")
         time.sleep(1)
      elif answer == "No":
         self.interface.quit_display()

   def ascii_to_string(self, ascii_string):
      """
      This method is needed to make sure that the return of methods using the 
      curses textpad are in the right format. 
      Otherwise it may happen that the figures displayed on the terminal are OK, 
      although they are in ASCII, causing some parsing errors.
      """
      conversion_list = [d for d in str(ascii_string)]
      converted_string = "".join(conversion_list).strip()
      return converted_string

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
         self.OFF = connect_to_OFF.ConnectToOFF()
         self.interface.clear_window("left")
         self.interface.clear_window("right")
         self.interface.left_window_display_string(0,cfg.S_A_INFO_ADD_NEW_CATEGORY)
         # A short sample of OFF categories is imported and displayed in the right window
         self.OFF.import_static_data()
         for (key, value) in self.OFF.OFF_category_dict.items():
            self.interface.right_window_display_result(y+1,"{}:  {}\n".format(key, value))
            y += 1
         self.interface.display_users_guide_textpad()
         # The user is requested to designate a category to be uploaded
         answer_category = self.interface.display_textpad(2,1,3)
         answer_category = self.ascii_to_string(answer_category)
         
         running = True
         while running:
            if answer_category.isdigit():
               self.interface.right_window_display_info("Test OK")
               running = False 
            else:
               self.interface.right_window_display_warning()               
               answer_category = self.interface.display_textpad(2,1,3)
               running = True

         self.interface.right_window_display_info("Ready to import result of query")           
         # This methods fetches a range of data from Open Food Facts
         (nb_imported_items, items_left_apart) = self.OFF.import_products(answer_category)
         self.interface.right_window_display_info('{} food items have rejected because of bad data'.format(items_left_apart))
         self.interface.right_window_display_info('{} food items have been downloaded from Open Food Facts'.format(nb_imported_items))
        
         nb_rows = self.queries.get_numbers_on_DB(cq.query_count_rows)
         self.interface.right_window_display_info('Currently your locals database counts {} food items'.format(nb_rows))
         # Insert the result into the local DB
         time.sleep(2)
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