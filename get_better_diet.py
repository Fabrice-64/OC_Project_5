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

        sql.MySQLQueries(): manage the queries to the local DB. In order to check\
            whether there already exists a DB, this class is instanciated\
            in the step_select_action() method.

        OFF.ConnectToOFF(): manage the download of data from Open Food Facts.

        Methods:

        step_terms_and_conditions(): require approval of the T & C to go on with the app.

        ascii_to_string(): convert the inputs from the textpad from ASCII into strings.

        select_action(): main loop through which the whole program runs.

        create_cnx_parameters(): create connection parameters for a further use
        of a local DB.

        Instance variables:

        NIL

        """

    def __init__(self):
        self.interface = im.Interface()
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
            This is where the connection with the class MySQLQueries is instantiated.

            Arguments:

            NIL

            Returns:

            decision: used to give the main function the order to quit the app.

            """
        # Check whether a local DB has already been created. If not, starts a process.
        has_to_create_db = False
        while check_DB := True:
            try:
                self.queries = sql.ORMConnection()
                break
            except Exception:
                self.interface.clear_window("right")
                self.interface.right_window_display_info(
                    cfg.WARNING_MESSAGE_4, "warning")
                self.create_cnx_parameters()
                has_to_create_db = True
                check_DB = False

        if has_to_create_db == True:
            print("Database should be created now")
            time.sleep(2)
            self.queries.create_database()
            self.interface.right_window_display_info(
                cfg.C_DB_CREATE_LOCAL_DB)
            # Open the connection to the local DB
            self.queries = sql.ORMConnection()
            self.queries.open_session()
            # Import categories from Open Food Facts
            OFF_categories = self.OFF.import_static_data(coff.URL_STATIC_CAT)
            # Configure the data and upload categories into the local DB
            self.queries.upload_categories(OFF_categories)
            self.interface.right_window_display_info(
                cfg.C_DB_INFO_CATEGORIES_FETCHED)
            # Import stores from Open Food Facts
            OFF_stores = self.OFF.import_static_data(coff.URL_STATIC_STORES)
            # Configure the data and upload stores into the local DB
            self.queries.upload_stores(OFF_stores)
            self.interface.right_window_display_info(
                cfg.C_DB_INFO_STORES_FETCHED)           

        self.interface.title_bar(cfg.TITLE_2)
        # Display a drop down menu to navigate in the application
        self.interface.clear_window()
        self.interface.left_window_display_string(0, cfg.S_A_INFO_LINE_1)
        self.interface.right_window_display_result(
            cfg.S_A_INFO_LOC_DISPLAY_RESULTS)
        answer = self.interface.set_up_drop_down(
            cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)
        #Here start the work on the DB to find, select and record a product
        y = 0
        running_main = True
        while running_main:
            # Open a session with the ORM iot work with the DB
            self.queries.open_session()
            # Look for a product !!
            if answer == cfg.S_A_OPERATE_ON_DB[0]:
                self.interface.title_bar(cfg.TITLE_3)
                self.interface.clear_window()
                # list of categories previously recorded is displayed on the right window
                top_categories = self.queries.get_categories()
                rank_categories = dict()
                rank_counter = 0
                for category in top_categories:
                    rank_counter += 1
                    self.interface.right_window_display_result\
                        (cfg.RANK_NAME_QTY.format(rank_counter, category.name,\
                        category.number_items))
                    rank_categories[rank_counter] = category.name

                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)

                # This loop is intended to avoid that a too precise request leads to an empty selection.
                running_data_not_null = True
                while running_data_not_null:
                    if running_data_not_null is True:
                        y = 0
                        self.interface.left_window_display_string(
                            y, cfg.KEYPAD_INSTRUCTION_1)
                        self.interface.left_window_display_string(
                            y+1, cfg.SELECT_CATEGORY)
                        self.interface.display_users_guide_textpad(
                            cfg.USER_GUIDE)
                        y = y + 3
                        # Characterize the food item the user is looking for.
                        answer_rank = self.interface.display_textpad(
                            y, 1, 3)
                        answer_rank = self.ascii_to_string(answer_rank)
                        y = y + 3
                        # The category is the only field which is compulsary.
                        running_category_choice = True
                        while running_category_choice:
                            if answer_rank.isdigit() and int(answer_rank) \
                                    in rank_categories.keys():
                                answer_rank= int(answer_rank)
                                answer_category = rank_categories.get(answer_rank)
                                running_category_choice = False
                            else:
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                answer_rank = ""
                                answer_rank= self.interface.display_textpad(
                                    y, 1, 3)
                                answer_rank = self.ascii_to_string(
                                    answer_rank)
                                running_category_choice = True

                        # Input the parameters to search for a food item.
                        answer_name, y = self.interface.left_window_display_string_textpad(
                            y, 1, 25, cfg.ITEM_NAME)
                        # Launch the query in the local DB.
                        brand_name, y = self.interface.left_window_display_string_textpad(
                            y, 1, 25, cfg.ITEM_BRAND)
                        item_search = [answer_category, answer_name, brand_name]
                        refer_products = self.queries.refer_products(item_search)
                        # If the criterion are too specific, avoid a null outcome.
                        if len(refer_products) == 0:
                            running_data_not_null = True
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_2, "warning")
                        else:
                            running_data_not_null = False

                # Display a selection of products.
                rank_item_dict = dict()
                rank_counter = 0
                self.interface.clear_window("right")
                self.interface.right_window_display_result(
                    cfg.S_A_INFO_ITEM_SEARCH_OUTCOME)
                for product in refer_products:
                    rank_counter += 1
                    self.interface.right_window_display_result(
                            cfg.S_A_INDEX_NAME.format(rank_counter, product.name))
                    self.interface.right_window_display_result(
                            cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(product.brand, product.nutrition_grade))
                    self.interface.right_window_display_result(
                            cfg.S_A_SINGLE_RETURN)
                    # Create key_value of rank and product for further check
                    rank_item_dict[rank_counter] = product.code

                # Requests the user to select a food item to be compared with.
                rank_reference_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_COMPARE_FOOD_ITEMS)

                running_check_selection = True
                while running_check_selection:
                    rank_reference_item = self.ascii_to_string(
                        rank_reference_item)
                    if rank_reference_item.isdigit() == False \
                            or int(rank_reference_item) not in rank_item_dict.keys():
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        rank_reference_item = self.interface.display_textpad(
                            y-2, 1, 3)
                        running_check_selection = True
                    else:
                        running_check_selection = False
                # The user is requested to enter keywords iot broaden the search.
                rank_reference_item = int(rank_reference_item)
                code_ref_prod = rank_item_dict.get(rank_reference_item)

                keywords_item, y = self.interface.left_window_display_string_textpad(
                    y, 1, 25, cfg.S_A_ADD_KEYWORDS)

                # If the keywords are too restrictive new ones are demanded.
                running_fetch_top_products = True
                while running_fetch_top_products:
                    # Create tuple with characteristics of reference product
                    if running_fetch_top_products is True:
                        # Set up search criterion
                        selected_prod = answer_category, keywords_item, code_ref_prod
                        selected_prod = tuple(selected_prod)
                        list_top_products = self.queries.top_products(selected_prod)
                        if len(list_top_products) == 0:
                            self.interface.right_window_display_info(
                                cfg.WARNING_MESSAGE_1, "warning")
                            keywords_item = self.interface.display_textpad(
                                y-2, 1, 25)
                        else:
                            running_fetch_top_products = False
                self.interface.clear_window()
                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                # This is where all the features of each and every food item are displayed.
                top_products_dict = {}
                rank_counter = 0
                for item in list_top_products:
                    rank_counter += 1
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(rank_counter, item.name))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(item.brand, 
                        item.nutrition_grade))
                    stores = [store.name for store in item.stores]
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_STORES.format(", ".join(stores)))
                    self.interface.right_window_display_result(
                        cfg.S_A_SINGLE_RETURN)
                    top_products_dict[rank_counter] = item.code

                y = 0
                # The user is offered to view the item in a browser and to record it.
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
                        rank_item, y = self.interface.left_window_display_string_textpad(
                            y, 1, 2, cfg.S_A_USE_BROWSER)
                        running_detailed_product = True
                        while running_detailed_product:
                            rank_item = self.ascii_to_string(rank_item)
                            rank_item = int(rank_item)
                            if rank_item not in top_products_dict.keys():
                                self.interface.right_window_display_info(
                                    cfg.WARNING_MESSAGE_0, "warning")
                                rank_item = self.interface.display_textpad(
                                    y-2, 1, 3)
                                running_detailed_product = True
                            else:
                                # Call the hyperlink to open the product file in the browser
                                rank_item = int(rank_item)
                                code_best_prod = top_products_dict.get(rank_item)
                                self.OFF.open_product_file_OFF(code_best_prod)
                            running_detailed_product = False

                        record_item, y = self.interface.left_window_display_string_textpad(
                            y, 1, 2, cfg.S_A_ASK_RECORD_SELECTED_ITEM)

                        running_record_item = True
                        # Invite to record the food item in the local DB
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
                                time.sleep(1)
                                running_record_item = False
                            else:
                                record_date_time = datetime.now()
                                record_date_time = record_date_time.strftime(
                                    '%Y-%m-%d %H:%M:%S')
                                compared_prods = code_best_prod, record_date_time,\
                                    code_ref_prod
                                self.queries.record_comparred_products(compared_prods)
                                self.interface.right_window_display_info(
                                    cfg.S_A_PROCESSING_RECORD)
                                running_record_item = False
                        running_get_details = False

                # Used to quit this loop
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.S_A_OPERATE_ON_DB, cfg.SELECT_ANSWER)
            # Step where the user looks into the best products he has recorded.
            elif answer == cfg.S_A_OPERATE_ON_DB[1]:
                self.interface.clear_window()
                last_recorded_products = self.queries.retrieve_compared_products()
                best_products_dict = dict()
                rank_counter = 0 
                for item in last_recorded_products:
                    rank_counter += 1
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(rank_counter, item.item_features[0]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_BRAND_NUTRISCORE.format(item.item_features[1],\
                            item.item_features[3]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_STORES.format(item.item_features[4]))
                    self.interface.right_window_display_result(
                        cfg.S_A_DISPLAY_INITIAL_PRODUCT.format(item.item_features[6]))
                    self.interface.right_window_display_result(
                        cfg.S_A_COMPARRISON_DATE.format(item.item_features[5]))
                    self.interface.right_window_display_result(
                        cfg.S_A_SINGLE_RETURN)
                    best_products_dict[rank_counter] = item.code
                # The user can see a product in detail.
                running_recorded_products = True
                while running_recorded_products:
                    if len(best_products_dict) == 0:
                        self.interface.right_window_display_info(
                            cfg.WARNING_MESSAGE_3, "warning")
                        running_recorded_products = False
                    else:
                        if running_recorded_products is True:
                            y = 0
                            self.interface.left_window_display_string(
                                y, cfg.S_A_INFO_LAST_RECORDS)
                            check_item, y = self.interface.left_window_display_string_textpad(
                                y+1, 1, 2, cfg.S_A_USE_BROWSER)
                            running_use_browser = True
                            while running_use_browser:
                                rank_item = self.ascii_to_string(rank_item)
                                if rank_item not in best_products_dict.keys():
                                    self.interface.right_window_display_info(
                                        cfg.WARNING_MESSAGE_0, "warning")
                                    rank_item = self.interface.display_textpad(
                                        y-2, 1, 2)
                                    running_use_browser = True
                                else:
                                    # Calls the hyperlink to open the product file in the browser.
                                    rank_item = int(rank_item)
                                    code_product = best_products_dict.get(rank_item)
                                    self.OFF.open_product_file_OFF(
                                        code_product)
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
            # This is to import products from one of the most popular categories.
            elif answer == cfg.S_A_OPERATE_ON_DB[2]:
                y = 0
                self.interface.clear_window()
                # A short sample of OFF categories is imported and displayed in the right window.
                categories = self.queries.display_categories()
                index_categories = []
                for category in categories:
                    self.interface.right_window_display_result(
                        cfg.S_A_INDEX_NAME .format(category.id_category, category.name))
                    index_categories.append(category.id_category)

                self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
                # The user is requested to designate a category to be uploaded.
                answer_category, y = self.interface.left_window_display_string_textpad(
                    y, 1, 3, cfg.S_A_INFO_ADD_NEW_CATEGORY)
                answer_category = self.ascii_to_string(answer_category)
                running = True
                while running:
                    if answer_category.isdigit() and int(answer_category) \
                            in index_categories:
                        answer_category = int(answer_category)
                        selected_category = categories[answer_category-1].name
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

                self.interface.right_window_display_info(cfg.S_A_BE_PATIENT)
                # This is where the excerpt of OFF is uploaded in the local DB.
                self.queries.upload_products(list_items)
                nb_rows = self.queries.total_items()
                self.interface.right_window_display_info(
                    cfg.S_A_SIZE_LOCAL_DB.format(nb_rows))
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

    def create_cnx_parameters(self):
        """
            This method is activated if no DB has been created. All the parameters\
                are asked and the script for the creation is run

            Arguments:

            NIL

            Returns:

            NIL
            """
        self.interface.clear_window("left")
        self.interface.display_users_guide_textpad(cfg.USER_GUIDE)
        y = 0
        # Ask for the connection parameters. Default value in config.py
        self.interface.left_window_display_string(y, cfg.C_DB_INITIAL_INFO)
        user, y = self.interface.left_window_display_string_textpad(1, 1, 15,
                                                                    cfg.C_DB_USER)
        user = self.ascii_to_string(user)
        if user != '':
            cfg.DB_USER = user
        
        password, y = self.interface.left_window_display_string_textpad(y, 1, 20,
                                                                        cfg.C_DB_PASSWORD)
        password = self.ascii_to_string(password)
        if password != '':
            cfg.DB_PASSWORD = password
        
        connection_string = cfg.DB_CONNEXION_STRING.format(cfg.DB_USER, cfg.DB_PASSWORD, "")
        # Connection parameters are saved in a separate file to be reused.
        with open("db_parameters.txt", "w") as file:
            file.write(connection_string)

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
        user.interface.quit_display()
    else:
        quit = user.step_select_action()
        if quit == "Quit":
            user.interface.quit_display()


if __name__ == "__main__":
    user = UserDialog()
    main(user)
