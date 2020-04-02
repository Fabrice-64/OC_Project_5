"""
    
    This module is the starting point for the application based on Open Food Facts Data \
    and aims at finding a better nutrition grade.

    It displays a welcome message and the Open Food Facts disclaimer. \
    It then jumps onto the next module which leads the user to navigate between \
    different options, from looking for a product to uploading a new category\
    of food items from Open Food Facts.

    Classes:

    UserDialog: encompass all the required processes to run the application.

    Exceptions:

    NIL.

    Functions:

    main(): launch the application and interrupts it when requested by the user.        

    """
import time
from datetime import datetime

import config as cfg
import config_open_food_facts as coff
import config_queries as cq
import connect_to_mysql as sql
import connect_to_OFF as OFF
import interface_management as im


class UserDialog:
    """

        Is the cornerstone of the application.

        It is a composite class, with following components:
        im.Interface(): manage the interface.

        sql.MySQLQueries(): manage the queries to the local DB.

        OFF.ConnectToOFF(): manage the download of data from Open Food Facts.

        Methods:

        step_terms_and_conditions(): require approval of the T & C to go on with the app.

        ascii_to_string(): convert the inputs from the textpad from ASCII into strings.

        check_category_selection():

        select_action()

        Instance variables:

        NIL

        """

    def __init__(self):
        self.interface = im.Interface()
        self.queries = sql.MySQLQueries()
        self.OFF = OFF.ConnectToOFF()

    def step_terms_and_conditions(self, file):
        """
            Accept the terms and conditions allows to go on, if not: quit.

            Arguments:

            file: text file containing the terms & conditions. Location in Documentation folder

            Returns:

            NIL

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
            Convert the textpad returns in a usable format, as they are ASCII objects.

            Arguments:

            ascii_string: normal outcome from a textpad input.

            Returns:

            converted_string: string in usual Python format.

            """
        conversion_list = [d for d in str(ascii_string)]
        converted_string = "".join(conversion_list).strip()
        return converted_string

    def step_select_action(self):
        """

            Represent the main menu to navigate in the application.

            Arguments:

            NIL

            Returns:

            decision: used to give the main function the order to quit the app.

            """
        self.interface.title_bar(cfg.TITLE_2)
        self.interface.clear_window()
        self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
        self.interface.right_window_display_result(
            cfg.S_A_INFO_LOC_DISPLAY_RESULTS)
        answer = self.interface.set_up_drop_down(
            cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)
        y = 0
        running_main = True
        while running_main:
            # Look for a product !!
            if answer == cfg.S_A_OPERATE_ON_DB[0]:
                self.interface.title_bar(cfg.TITLE_3)
                self.interface.clear_window()
                # list of categories previously recorded is displayed on the right window
                categories = self.queries.get_categories(
                    cq.query_retrieve_available_categories)
                for (key, category) in categories.items():
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME.format(key, category))

                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)

                running_data_not_null = True
                # This loop is intended to avoid that a too precise request leads to an empty selection
                while running_data_not_null:
                    if running_data_not_null is True:
                        y = 0
                        self.interface.left_window_display_string(
                            y, cfg.KEYPAD_INSTRUCTION_1)
                        self.interface.left_window_display_string(
                            y+1, cfg.S_A_SELECT_CATEGORY)
                        self.interface.display_users_guide_textpad(
                            cfg.USER_GUIDE)
                        y = y+3
                        # These fields help to characterize the food item the user is looking for
                        answer_category = self.interface.display_textpad(
                            y, 1, 3)
                        running_category_choice = True
                        while running_category_choice:
                            # The category is the only field which is compulsary
                            answer_category = self.ascii_to_string(
                                answer_category)
                            if answer_category.isdigit() is False or \
                                    int(answer_category) not in categories.keys():
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                answer_category = self.interface.display_textpad(
                                    y, 1, 3)
                            else:
                                running_category_choice = False
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
                        answer_code = sql.query_settings(answer_code)
                        answer_nutrition_grade = ""

                        item_search = [answer_category, answer_name, answer_brand,
                                       answer_code]
                        detailed_products = self.queries.get_product(
                            cq.query_searched_item, item_search)

                        if len(detailed_products) == 0:
                            running_data_not_null = True
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_2, "warning")
                        else:
                            running_data_not_null = False

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

                # Requests the user to select a food item to be compared with.
                index_reference_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_COMPARE_FOOD_ITEMS)
                item_key_list = [
                    key for item in detailed_products for key in item]

                running_check_selection = True
                while running_check_selection:
                    index_reference_item = self.ascii_to_string(
                        index_reference_item)
                    if index_reference_item.isdigit() == False \
                            or int(index_reference_item) not in item_key_list:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        index_reference_item = self.interface.display_textpad(
                            y-2, 1, 3)
                        running_check_selection = True
                    else:
                        running_check_selection = False
                # The user is requested to enter keywords iot broaden the search.
                index_reference_item = int(index_reference_item)
                keywords_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 25, cfg.S_A_ADD_KEYWORDS)

                running_fetch_best_products = True
                while running_fetch_best_products:
                    if running_fetch_best_products is True:
                        keywords_item = sql.query_settings(keywords_item)
                        sql_result = answer_category, keywords_item, list_selection[
                            index_reference_item-1][1][2]
                        sql_result = tuple(sql_result)
                        list_best_products = self.queries.get_best_product(
                            cq.query_best_product, sql_result)
                        if len(list_best_products) == 0:
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_1, "warning")
                            keywords_item = self.interface.display_textpad(
                                y-2, 1, 25)
                        else:
                            running_fetch_best_products = False
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

                y = 0
                self.interface.left_window_display_string(
                    y, cfg.S_A_ASK_CHECK_DETAILED_RESULT)
                check_answer, y = self.interface.left_window_display_string_textpad(
                    y+1, 1, 2, cfg.SELECT_Y_N)
                running_get_details = True
                while running_get_details:
                    check_answer = self.ascii_to_string(check_answer).upper()
                    if check_answer not in ["Y", "N"]:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        check_answer = self.interface.display_textpad(
                            y-2, 1, 2)
                        running_get_details = True
                    elif check_answer == 'N':
                        running_get_details = False
                    elif check_answer == "Y":
                        y = 0
                        self.interface.clear_window("left")
                        check_item, y = self.interface.left_window_display_string_textpad(
                            y, 1, 2, cfg.S_A_USE_BROWSER)
                        running_detailed_product = True
                        while running_detailed_product:
                            check_item = self.ascii_to_string(check_item)
                            if check_item not in index_list_best_products:
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                check_item = self.interface.display_textpad(
                                    y-2, 1, 2)
                                running_detailed_product = True
                            else:
                                # Call the hyperlink to open the product file in the browser
                                check_item = int(check_item)
                                code_product = list_best_products[check_item-1][1][3]
                                self.OFF.open_product_file_OFF(code_product)
                            running_detailed_product = False

                        record_item, y = self.interface.left_window_display_string_textpad(
                            y, 1, 2, cfg.S_A_ASK_RECORD_SELECTED_ITEM)

                        running_record_item = True
                        while running_record_item:
                            record_item = self.ascii_to_string(
                                record_item).upper()
                            if record_item not in ["Y", "N"]:
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                record_item = self.interface.display_textpad(
                                    y-2, 1, 2)
                                running_record_item = True
                            elif record_item == "N":
                                self.interface.right_window_display_info(
                                    cfg.BACK_MAIN_MENU)
                                time.sleep(2)
                                running_record_item = False
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
                                running_record_item = False
                        running_get_details = False

                # Used to quit this loop
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)

            elif answer == cfg.S_A_OPERATE_ON_DB[1]:
                self.interface.clear_window()
                last_recorded_products = self.queries.retrieve_recorded_products(
                    cq.query_retrieve_recorded_product)
                index_list_products = []
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
                    if running_recorded_products is True:
                        y = 0
                        self.interface.left_window_display_string(
                            y, cfg.S_A_INFO_LAST_RECORDS)
                        check_item, y = self.interface.left_window_display_string_textpad(
                            y+1, 1, 2, cfg.S_A_USE_BROWSER)
                        running_use_browser = True
                        while running_use_browser:
                            check_item = self.ascii_to_string(check_item)
                            if check_item not in index_list_products:
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                check_item = self.interface.display_textpad(
                                    y-2, 1, 2)
                                running_use_browser = True
                            else:
                                # Calls the hyperlink to open the product file in the browser.
                                check_item = int(check_item)
                                code_product = last_recorded_products[check_item-1][1][2]
                                self.OFF.open_product_file_OFF(code_product)
                                running_use_browser = False
                            # The user is asked whether he wants to check another item.
                        go_on_items, y = self.interface.left_window_display_string_textpad(
                            y, 1, 2, cfg.S_A_GO_ON_CHECK_FOOD_ITEMS_Y_N)
                        running_go_on = True
                        while running_go_on:
                            if running_go_on is True:
                                check_item = self.ascii_to_string(
                                    go_on_items).upper()
                                if check_item not in ["Y", "N"]:
                                    self.interface.right_window_display_info(
                                        cfg.WARNING_MESSAGE_0, "warning")
                                    go_on_items = self.interface.display_textpad(
                                        y-2, 1, 2)
                                    running_go_on = True
                                elif check_item == "N":
                                    running_recorded_products = False
                                else:
                                    running_recorded_products = True
                                running_go_on = False

                # Used to quit this loop
                self.interface.clear_window()
                # Used to quit this loop
                answer = self.interface.set_up_drop_down(
                    cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)

            elif answer == cfg.S_A_OPERATE_ON_DB[2]:
                y = 0
                self.interface.clear_window()
                # A short sample of OFF categories is imported and displayed in the right window.
                categories = self.queries.get_categories(
                    cq.query_categories)
                y_categories = 0
                for (key, value) in categories.items():
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(key, value))

                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                # The user is requested to designate a category to be uploaded.
                answer_category, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_INFO_ADD_NEW_CATEGORY)
                answer_category = self.ascii_to_string(answer_category)

                running = True
                while running:
                    if answer_category.isdigit() and int(answer_category) \
                            in categories.keys():
                        selected_category = categories.get(
                            int(answer_category))
                        selected_category = str(selected_category)
                        display_chosen_category = cfg.S_A_INFO_NAME_IMPORTED_CATEGORY + \
                            selected_category
                        self.interface.right_window_display_info(
                            display_chosen_category)
                        running = False
                    else:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        answer_category = ""
                        answer_category = self.interface.display_textpad(
                            y-2, 1, 3)
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
                    nb_rows = self.queries.get_numbers_on_DB(
                        cq.query_count_rows)
                    self.interface.right_window_display_info(
                        cfg.S_A_SIZE_LOCAL_DB.format(nb_rows))
                    time.sleep(1)
                    running = False
                # Used to quit this loop
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # This last option is to close properly the program and reinitialize the shell.
            elif answer == cfg.S_A_OPERATE_ON_DB[3]:
                self.interface.clear_window()
                running_main = False
                decision = "Quit"
        return decision


def main(user):
    """

        Launch the main menu of the app.

        Methods:

        NIL

        Variables:

        answer: as return from the terms and conditions if they are rejected.

        quit: as return from the main menu, iot quit properly the application.

        """
    user.interface.display_message(cfg.WELCOME_MESSAGE)
    time.sleep(1)
    user.interface.split_screen()
    answer = user.step_terms_and_conditions(cfg.T_C_FILE)
    if answer == "No":
        user.queries.close_connection()
        user.interface.quit_display()
    else:
        quit = user.step_select_action()
        if quit == "Quit":
            user.queries.close_connection()
            user.interface.quit_display()


if __name__ == "__main__":
    user = UserDialog()
    main(user)
