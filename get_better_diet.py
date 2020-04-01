"""
This module is the starting point for the application based on Open Food Facts Data \
   and aiming at finding a better nutrition grade

It displays a welcome message and the  Open Food Facts disclaimer. \
   It then jumps onto the next module.

"""
import interface_management as im
import connect_to_mysql as sql
import connect_to_OFF as OFF
import config_open_food_facts as coff
import config_queries as cq
import config as cfg
import time
from datetime import datetime


class UserDialog:
    def __init__(self):
        self.interface = im.Interface()
        self.queries = sql.MySQLQueries()
        self.OFF = OFF.ConnectToOFF()

    def step_terms_and_conditions(self, file):
        """
        Accepting the terms and conditions allows to go on, if not: quit.

        """

        y = 0
        self.interface.title_bar(cfg.TITLE_1)
        self.interface.left_window_display_string(y, cfg.T_C_LINE_1)
        self.interface.left_window_display_string(y+1, cfg.T_C_LINE_2)
        self.interface.display_file_right_window(file)
        self.interface.clear_window("left")
        self.interface.left_window_display_string(
            y, cfg.T_C_QUESTION_ACCEPT_T_C)
        self.interface.left_window_display_string(y+1, cfg.T_C_IF_REFUSAL)
        answer = self.interface.set_up_drop_down(
            cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
        if answer == "Yes":
            self.interface.clear_window('left')
            self.interface.left_window_display_string(y, cfg.T_C_APPROVAL)
            time.sleep(1)
        return answer

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
            answer_category = self.interface.display_textpad(y+3, 1, 3)
            answer_category = self.ascii_to_string(answer_category)
            if answer_category.isdigit() == False or int(answer_category) not in categories.keys():
                self.interface.right_window_display_info(
                    cfg.WARNING_MESSAGE_0, "warning")
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
        """
        This method deals with what is a sort of main menu. \
           It proposses different options to navigate into the app.
        """
        y = 0
        self.interface.title_bar(cfg.TITLE_2)
        running_main = True
        while running_main:
            self.interface.clear_window()
            self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
            self.interface.right_window_display_result(
                cfg.S_A_INFO_LOC_DISPLAY_RESULTS)
            answer = self.interface.set_up_drop_down(
                cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)
            time.sleep(1)

            # This part deals with the use of the local DB to search and find food items.
            if answer == cfg.S_A_OPERATE_ON_DB[0]:
                self.interface.title_bar(cfg.TITLE_3)
                self.interface.clear_window()
                # A list of categories previously recorded is displayed on the right window
                categories = self.queries.get_categories(
                    cq.query_retrieve_available_categories)
                for (key, category) in categories.items():
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME.format(key, category))

                running_data_not_null = True
                # This loop is intended to avoid that a too precise request leads to an empty selection
                while running_data_not_null:
                    # y is the reference coordinate for all the following dialog boxes in this loop.
                    y = 0
                    self.interface.left_window_display_string(
                        y, cfg.KEYPAD_INSTRUCTION_1)
                    self.interface.left_window_display_string(
                        y+1, cfg.S_A_SELECT_CATEGORY)
                    self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                    y = y+3
                    # These fields help to characterize the food item the user is looking for
                    answer_category = self.interface.display_textpad(y, 1, 3)

                    running = True
                    while running:
                        # The category is the only field which is compulsary
                        answer_category = self.ascii_to_string(answer_category)
                        if answer_category.isdigit() == False or int(answer_category) not in categories.keys():
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_0, "warning")
                            answer_category = self.interface.display_textpad(
                                y, 1, 3)
                            running = True
                        else:
                            running = False

                    answer_category = int(answer_category)
                    answer_category = categories.get(answer_category)

                    answer_name, y = self.interface.left_window_display_string_textpad(
                        5, 1, 25, cfg.S_A_ITEM_NAME)
                    answer_name = sql.query_settings(answer_name)

                    answer_brand, y = self.interface.left_window_display_string_textpad(
                        y, 1, 25, cfg.S_A_ITEM_BRAND)
                    answer_brand = sql.query_settings(answer_brand)

                    answer_code, y = self.interface.left_window_display_string_textpad(
                        y, 1, 13, cfg.S_A_ITEM_CODE)
                    answer_code = sql.query_settings(answer_brand)

                    answer_nutrition_grade = ""

                    item_search = [answer_category,
                                   answer_name, answer_brand, answer_code]
                    detailed_products = self.queries.get_product(
                        cq.query_searched_item, item_search)

                    # This refers to the top of the loop, so one avoids getting 0 choice
                    if len(detailed_products) > 0:
                        running_data_not_null = False
                    else:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")

                # Displays the answers fetched from the local DB
                list_selection = []
                list_item = []
                self.interface.clear_window("right")
                self.interface.right_window_display_result(
                    cfg.S_A_INFO_ITEM_SEARCH_OUTCOME)
                for item in detailed_products:
                    for (key, values) in item.items():
                        self.interface.right_window_display_result(
                            cfg.S_A_INDEX_NAME .format(key, values[0]))
                        self.interface.right_window_display_result(
                            cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(values[1], values[2]))
                        self.interface.right_window_display_result(
                            cfg.S_A_SINGLE_RETURN)
                        list_item = [key, values]
                    list_selection.append(list_item)

                # Requests the user to select a food item with which a comparrison is to be made.
                index_reference_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_COMPARE_FOOD_ITEMS)

                item_key_list = [
                    key for item in detailed_products for key in item]
                running = True
                while running:
                    index_reference_item = self.ascii_to_string(
                        index_reference_item)
                    if index_reference_item.isdigit() == False or int(index_reference_item) not in item_key_list:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        index_reference_item = self.interface.display_textpad(
                            y-2, 1, 3)
                        running = True
                    else:
                        running = False
                # The user is requested to enter keywords iot broaden the search.
                index_reference_item = int(index_reference_item)
                keywords_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 25, cfg.S_A_ADD_KEYWORDS)

                # This part prepares the data for looking for the best food items.
                running = True
                while running:
                    keywords_item = sql.query_settings(keywords_item)
                    sql_result = answer_category, keywords_item, list_selection[
                        index_reference_item-1][1][2]
                    sql_result = tuple(sql_result)
                    list_best_products = self.queries.get_best_product(
                        cq.query_best_product, sql_result)
                    self.interface.right_window_display_info(
                        str(len(list_best_products)))
                    if len(list_best_products) > 0:
                        break
                    else:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_1, "warning")
                        keywords_item = self.interface.display_textpad(
                            y-2, 1, 25)

                self.interface.clear_window()
                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                # This is where all the features of each and every food item are displayed.
                index_list_best_products = []
                for item in list_best_products:
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(item[0], item[1][0]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(item[1][1], item[1][2]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_STORES.format(item[1][4]))
                    self.interface.right_window_display_result(
                        cfg.S_A_SINGLE_RETURN)
                    index_list_best_products.append(str(item[0]))

                # Here is an interaction with the user, so that he can select the food item he would like to see in detail.
                y = 0
                self.interface.left_window_display_string(
                    y, cfg.S_A_ASK_CHECK_DETAILED_RESULTS)
                process_result, y = self.interface.left_window_display_string_textpad(
                    y+1, 1, 2, cfg.SELECT_Y_N)
                running = True
                while running:
                    process_result = self.ascii_to_string(
                        process_result).upper()
                    if process_result not in ["Y", "N"]:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        process_result = self.interface.display_textpad(
                            y-2, 1, 3)
                        running = True
                    else:
                        if process_result == "N":
                            self.interface.right_window_display_info(
                                cfg.BACK_MAIN_MENU)
                            running = False
                            time.sleep(1)
                            user.step_select_action()
                        else:
                            running = False

                y = 0
                self.interface.clear_window("left")
                check_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 2, cfg.S_A_USE_BROWSER)
                running = True
                while running:
                    check_item = self.ascii_to_string(check_item)
                    if check_item not in index_list_best_products:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        check_item = self.interface.display_textpad(y-2, 1, 2)
                        running = True
                    else:
                        # Call the hyperlink to open the product file in the browser
                        check_item = int(check_item)
                        code_product = list_best_products[check_item-1][1][3]
                        self.OFF.open_product_file_OFF(code_product)
                        running = False

                # Process for recording an item in the local DB
                decide_record_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 2, cfg.S_A_ASK_RECORD_SELECTED_ITEM)
                running = True
                while running:
                    decide_record_item = self.ascii_to_string(
                        decide_record_item).upper()
                    if decide_record_item not in ["Y", "N"]:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        decide_record_item = self.interface.display_textpad(
                            y-2, 1, 2)
                        running = True
                    else:
                        if decide_record_item == "N":
                            self.interface.right_window_display_info(
                                cfg.BACK_MAIN_MENU)
                            time.sleep(2)
                            running = False
                        else:
                            record_date_time = datetime.now()
                            record_date_time = record_date_time.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            best_product_record = code_product, record_date_time, list_selection[
                                index_reference_item - 1][1][3]
                            self.queries.upload_product(
                                cq.query_record_best_product, best_product_record)
                            self.interface.right_window_display_info(
                                cfg.S_A_PROCESSING_RECORD)
                            running = False
                    running = False
                user.step_select_action()

                # This step is where the user gets back to recorded food items
            elif answer == cfg.S_A_OPERATE_ON_DB[1]:
                self.interface.clear_window()
                last_recorded_products = self.queries.retrieve_recorded_products(
                    cq.query_retrieve_recorded_product)
                index_list_products = []
                # The number of food items displayed is limited in the query an can be changed.
                for item in last_recorded_products:
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(item[0], item[1][0]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(item[1][1], item[1][3]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_STORES.format(item[1][4]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_INITIAL_PRODUCT.format(item[1][6]))
                    self.interface.right_window_display_result(
                        cfg.S_A_COMPARRISON_DATE.format(item[1][5]))
                    self.interface.right_window_display_result(
                        cfg.S_A_SINGLE_RETURN)
                    index_list_products.append(str(item[0]))

                running_recorded_products = True
                while running_recorded_products:
                    y = 0
                    self.interface.left_window_display_string(
                        y, cfg.S_A_INFO_LAST_RECORDS)
                    check_item, y = self.interface.left_window_display_string_textpad(
                        y+1, 1, 2, cfg.S_A_USE_BROWSER)
                    running = True
                    while running:
                        check_item = self.ascii_to_string(check_item)
                        if check_item not in index_list_products:
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_0, "warning")
                            check_item = self.interface.display_textpad(
                                y-2, 1, 2)
                            running = True
                        else:
                            # Calls the hyperlink to open the product file in the browser.
                            check_item = int(check_item)
                            code_product = last_recorded_products[check_item-1][1][2]
                            self.OFF.open_product_file_OFF(code_product)

                            # The user is asked whether he wants to check another item.
                            process_result, y = self.interface.left_window_display_string_textpad(
                                y, 1, 2, cfg.S_A_GO_ON_CHECK_FOOD_ITEMS_Y_N)

                            running_approval = True
                            while running_approval:
                                process_result = self.ascii_to_string(
                                    process_result).upper()
                                if process_result not in ["Y", "N"]:
                                    self.interface.right_window_display_info(
                                        cfg.WARNING_MESSAGE_0, "warning")
                                    process_result = self.interface.display_textpad(
                                        y-2, 1, 2)
                                    running_approval = True
                                else:
                                    if process_result == "N":
                                        self.interface.right_window_display_info(
                                            cfg.BACK_MAIN_MENU)
                                        user.step_select_action()
                                    else:
                                        running_approval = False
                                running = False
                        running_recorded_products = True

            # This part of the program is for adding a new category
            elif answer == cfg.S_A_OPERATE_ON_DB[2]:
                y = 0
                self.interface.clear_window()

                # A short sample of OFF categories is imported and displayed in the right window.
                self.categories = self.queries.get_categories(
                    cq.query_categories)
                y_categories = 0
                for (key, value) in self.categories.items():
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(key, value))

                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                # The user is requested to designate a category to be uploaded.
                answer_category, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_INFO_ADD_NEW_CATEGORY)
                answer_category = self.ascii_to_string(answer_category)

                running = True
                while running:
                    if answer_category.isdigit() and int(answer_category) in self.categories.keys():
                        selected_category = self.categories.get(
                            int(answer_category))
                        display_chosen_category = cfg.S_A_INFO_NAME_IMPORTED_CATEGORY + \
                            str(selected_category)
                        self.interface.right_window_display_info(
                            display_chosen_category)
                        running = False
                    else:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        answer_category = ""
                        answer_category = self.interface.display_textpad(
                            y+3, 1, 3)
                        answer_category = self.ascii_to_string(answer_category)
                        running = True

                # This methods fetches a range of data from Open Food Facts.
                (nb_imported_items, items_left_apart,
                 list_items) = self.OFF.import_products_list(selected_category)
                # Here some pieces of info related to the downloaded data are given for info.
                self.interface.right_window_display_info(
                    coff.NUMBER_REJECTED_ITEMS.format(items_left_apart))
                self.interface.right_window_display_info(
                    coff.NUMBER_DOWNLOADED_ITEMS.format(nb_imported_items))

                # This is where the excerpt of OFF is uploaded in the local DB.
                self.queries.upload_dataset(
                    cq.query_upload_new_category_products, list_items)
                nb_rows = self.queries.get_numbers_on_DB(cq.query_count_rows)
                self.interface.right_window_display_info(
                    cfg.S_A_SIZE_LOCAL_DB.format(nb_rows))
                time.sleep(1)
                running = False

            # This last option is to close properly the program and reinitialize the shell.
            elif answer == cfg.S_A_OPERATE_ON_DB[3]:
                running_main = False

        self.queries.close_connection()


def main(user):
    # The graphic interface is initialized right there.
    user.interface.display_message(cfg.WELCOME_MESSAGE)
    time.sleep(1)
    user.interface.split_screen()
    answer = user.step_terms_and_conditions(cfg.T_C_FILE)
    if answer == "Yes":
        user.step_select_action()
    user.interface.quit_display()


if __name__ == "__main__":
    user = UserDialog()
    main(user)
