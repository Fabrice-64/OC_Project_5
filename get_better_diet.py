"""
This module is the starting point for the application based on Open Food Facts Data and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. It then jumps onto the next module.

"""
import interface_management as im
import connect_to_mysql as sql
import connect_to_OFF as OFF
import config_open_food_facts as coff
import config_queries as cq
import config as cfg
import time

class UserDialog:
   def __init__(self):
      self.interface = im.Interface()
      self.queries = sql.MySQLQueries()
      self.OFF = OFF.ConnectToOFF()

   def step_terms_and_conditions(self, file):
      y = 0
      self.interface.title_bar(cfg.TITLE_1)
      self.interface.left_window_display_string(y, cfg.T_C_LINE_1)
      self.interface.left_window_display_string(y+1, cfg.T_C_LINE_2)
      self.interface.display_file_right_window(file)
      self.interface.clear_window("left")
      self.interface.left_window_display_string(y, cfg.T_C_QUESTION_ACCEPT_T_C)
      self.interface.left_window_display_string(y+1, cfg.T_C_IF_REFUSAL)
      answer = self.interface.set_up_drop_down(cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
      if answer == "Yes":
         self.interface.clear_window('left')
         self.interface.left_window_display_string(y, "You have decided to go on with the program")
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

   def check_category_selection(self, y, categories):
      running = True
      while running:
         answer_category = self.interface.display_textpad(y+3,1,3)
         answer_category = self.ascii_to_string(answer_category)
         if answer_category.isdigit() == False or int(answer_category)  not in categories.keys():
            self.interface.right_window_display_warning()               
            running = True
         elif answer_category == "" or " ":
            answer_category = sql.query_settings(answer_category)
            running = False
         else:
            answer_category = int(answer_category)
            answer_category = categories.get(answer_category)
            running = False
         answer_category = categories.get(answer_category)
      return answer_category

   def step_select_action(self):
      y = 0
      self.interface.title_bar(cfg.TITLE_2)
      running_main = True
      while running_main:
         self.interface.clear_window('left')
         self.interface.clear_window('right')
         self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
         self.interface.right_window_display_result("The results will be displayed in this window\n")
         answer = self.interface.set_up_drop_down(cfg.S_A_OPERATE_ON_DB,cfg.SELECT_ANSWER)
         time.sleep(1)
         
         if answer == cfg.S_A_OPERATE_ON_DB[0]:
            self.interface.title_bar(cfg.TITLE_3)
            self.interface.clear_window("right")
            self.interface.clear_window("left")
            y = 0    
            self.interface.left_window_display_string(y, cfg.KEYPAD_INSTRUCTION_1)
            self.interface.left_window_display_string(y+1, cfg.S_A_SELECT_CATEGORY)
            self.interface.display_users_guide_textpad()   
            categories = self.queries.get_categories(cq.query_retrieve_available_categories)
            for (key, category) in categories.items():
               self.interface.right_window_display_result("{}:  {}\n".format(key, category))
            
            # In interface.display_textpad(y, nblines, nbcols), the y is incremented by 1 for every new line
            # The y is where the texpad starts, the number of lines and cols to select the category
            
            # Fill the required fields to characterize the food item the user is looking for
            answer_category = self.interface.display_textpad(y+3,1,3)
            running = True
            while running:
               answer_category = self.ascii_to_string(answer_category)
               if answer_category.isdigit() == False or int(answer_category) not in categories.keys():
                  self.interface.right_window_display_warning()
                  answer_category = self.interface.display_textpad(y+3,1,3)              
                  running = True
               else:
                  running = False

            answer_category = int(answer_category)
            answer_category = categories.get(answer_category)
                        
            self.interface.left_window_display_string(y+5, cfg.S_A_NAME_FOOD_ITEM)
            answer_name = self.interface.display_textpad(y+7,1,25)
            answer_name = sql.query_settings(answer_name)

            self.interface.left_window_display_string(y+9, cfg.S_A_NAME_ITEM_BRAND)
            answer_brand = self.interface.display_textpad(y+11, 1, 25)
            answer_brand = sql.query_settings(answer_brand)

            self.interface.left_window_display_string(y+13, cfg.S_A_NAME_ITEM_CODE)
            answer_code = self.interface.display_textpad(y+15, 1, 14)
            answer_code = sql.query_settings(answer_code)

            item_search = [answer_category, answer_name, answer_brand, answer_code]
            
            product_details = self.queries.get_product(cq.query_searched_item, item_search)
            
            # Displays the answers fetched from the local DB

            # Propose to record the substitution food item
         elif answer == cfg.S_A_OPERATE_ON_DB[1]:
            # Query for getting a recorded food item
            pass
         elif answer == cfg.S_A_OPERATE_ON_DB[2]:
            y = 0
            self.interface.clear_window("left")
            self.interface.clear_window("right")
            self.interface.left_window_display_string(y, cfg.S_A_INFO_ADD_NEW_CATEGORY)
            # A short sample of OFF categories is imported and displayed in the right window
            self.categories = self.queries.get_categories(cq.query_categories)
            y_categories = 0
            for (key, value) in self.categories.items():
               self.interface.right_window_display_result("{}:  {}\n".format(key, value))

            self.interface.display_users_guide_textpad()
            # The user is requested to designate a category to be uploaded
            answer_category = self.interface.display_textpad(y+3,1,3)
            answer_category = self.ascii_to_string(answer_category)
         
            running = True
            while running:
               if answer_category.isdigit() and int(answer_category) in self.categories.keys():
                  selected_category = self.categories.get(int(answer_category))
                  display_chosen_category = "You will import : " + str(selected_category)
                  self.interface.right_window_display_info(display_chosen_category)
                  running = False 
               else:
                  self.interface.right_window_display_warning()
                  answer_category = ""              
                  answer_category = self.interface.display_textpad(y+3,1,3)
                  answer_category = self.ascii_to_string(answer_category)
                  running = True

            # This methods fetches a range of data from Open Food Facts
            (nb_imported_items, items_left_apart, list_items) = self.OFF.import_products_list(selected_category)
            self.interface.right_window_display_info('{} food items have rejected because of bad data'.format(items_left_apart))
            self.interface.right_window_display_info('{} food items have been downloaded from Open Food Facts'.format(nb_imported_items))
            
            # This is where the excerpt of OFF is uploaded in the local DB
            self.queries.upload_dataset(cq.query_upload_new_category_products, list_items)
            nb_rows = self.queries.get_numbers_on_DB(cq.query_count_rows)
            self.interface.right_window_display_info('Now your local database counts {} food items'.format(nb_rows))
            time.sleep(1)
            running = False

         elif answer == cfg.S_A_OPERATE_ON_DB[3]:
            self.queries.close_connection()
            self.interface.quit_display()

      time.sleep(1)

def main(user):
   user.interface.display_message(cfg.WELCOME_MESSAGE)
   time.sleep(1)
   user.interface.split_screen(cfg.TITLE_0)
   user.step_terms_and_conditions("Documentation/texte_T&C.txt")
   user.step_select_action()
   
if __name__ == "__main__":
   user = UserDialog()
   main(user)
   