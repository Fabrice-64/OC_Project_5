"""

    This module is the starting point for the application based on Open Food \
        Facts Data and aims at finding a better nutrition grade.

    It displays a welcome message and the Open Food Facts disclaimer.\
    It then jumps onto the next module which leads the user to navigate \
    between different options, from looking for a product to uploading \
    a new category of food items from Open Food Facts.

    Classes:

    UserDialog: encompass all the required processes to run the application.

    Exceptions:

    NIL.

    Functions:

    main: launch the application and interrupts it when requested.

    """
import time
from datetime import datetime

from AppView.interface_management import Interface
from AppModel.open_food_facts.connect_to_OFF import ConnectToOFF
from AppController import config as cfg
from AppModel.open_food_facts import config_open_food_facts as coff
from AppModel.local_DB import connect_to_mysql as sql


class UserDialog:
    """

        Is the cornerstone of the application.

        It is a composite class, with following components:
        im.Interface: manage the itf.

        sql.ORMConnection: manage the queries to the local DB.
        In order to check whether there already exists a DB,\
        this class is instanciated in the step_select_action() method.

        OFF.ConnectToOFF: manage the download of data from Open Food Facts.

        Methods:

        step_terms_and_conditions(): require approval of the T & C \
        to go on with the app.

        __ascii_to_string(): convert the inputs from the textpad from ASCII\
            into strings.

        select_action(): main loop through which the whole program runs.

        __create_cnx_parameters(): used exclusively for the first use,\
        when the local DB has not been created yet.

        __compared_products: Display the last recorded products,\
        best and reference.

        __top_products: Display a list of the products matching\
        the best with the user's request.

        __display_top_categories: Display the most popular categories\
            in the local DB.

        __check_valid_answer:Check whether the number given by the user\
        belongs to the keys of a dictionary. If not, the loop runs.

        __initialize_DB : Create and initialize a new DB, including \
            the downloading and uploading of two lists from Open Food Facts: \
                the stores and the categories.

        __record_current_DTG(self): Record the current date time \
            and format it for the DB.

        """

    def __init__(self):
        """
            Integrates the classes Interface and ConnectToOFF as components.

            Arguments:

            self.itf: manage the relation with the display (View).
            self.OFF: used either to download data from OFF, or to access a product page.

            Returns:

            NIL

            """
        self.itf = Interface()
        self.OFF = ConnectToOFF()

    def step_terms_and_conditions(self, file):
        """
            Accept the terms and conditions allows to go on, if not: quit.

            Arguments:

            file: text file containing the terms & conditions. \
                Location in Documentation folder

            Returns:

            NIL

            """
        y = 0
        self.itf.title_bar(cfg.TITLE_1)
        self.itf.left_display_string(y, cfg.T_C_LINE_1)
        self.itf.left_display_string(y+1, cfg.T_C_LINE_2)
        self.itf.display_file(file)
        self.itf.clear_window("left")
        self.itf.left_display_string(y, cfg.ACCEPT_T_C)
        self.itf.left_display_string(y+1, cfg.IF_REFUSAL)
        answer = self.itf.set_up_drop_down(
            cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
        if answer == "Yes":
            self.itf.clear_window('left')
            self.itf.left_display_string(y, cfg.T_C_APPROVAL)
            time.sleep(1)
        return answer

    def __ascii_to_string(self, ascii_string):
        """
            Convert the textpad returns in a usable format, as they are \
                ASCII objects.

            Arguments:

            ascii_string: ascii is the normal outcome from a textpad \
                input in Curses

            Returns:

            converted_string: string.

            """
        conversion_list = [d for d in str(ascii_string)]
        converted_string = "".join(conversion_list).strip()
        return converted_string

    def step_select_action(self):
        """

            Represent the main menu to navigate in the application.
            This is where the connection with the class MySQLQueries is instantiated.

            Arguments:

            self.queries: instanciate the class sql.ORMConnection iot manage the
            relation with the model.

            Returns:

            decision: used to give the main function the order to quit the app.

            """
        # Check whether a local DB has already been created.
        while True:
            try:
                # Check whether a connection with an existing local DB is OK.
                self.queries = sql.ORMConnection()
                break
            except Exception:
                # Creation of a connexion, iot prepare the DB creation
                self.itf.clear_window("right")
                self.itf.right_display_info(cfg.WARNING_MESSAGE_4, "warning")
                self.__create_cnx_parameters()
                # Creation of the DB through a method hosted in this module
                self.__initialize_DB()
        self.itf.title_bar(cfg.TITLE_2)
        # Display a drop down menu to navigate in the application
        self.itf.clear_window()
        self.itf.left_display_string(0, cfg.INFO_LINE_1)
        self.itf.display_result(cfg.INFO_DISPLAY_RESULTS)
        answer = self.itf.set_up_drop_down(cfg.OPERATE_ON_DB,
                                           cfg.SELECT_ANSWER)
        # Here start the work on the DB to find, select and record a product
        y = 0
        while True:
            # Open a session with the ORM iot work with the DB.
            self.queries.open_session()
            result = self.queries.total_items()
            # check that the DB is not empty
            if result == 0:
                self.itf.right_display_info(cfg.EMPTY_DB, "warning")
                answer = cfg.OPERATE_ON_DB[2]
            # Look for a product !!
            if answer == cfg.OPERATE_ON_DB[0]:
                self.itf.title_bar(cfg.TITLE_3)
                self.itf.clear_window()
                # list of recorded categories is displayed on the right window.
                top_categories = self.queries.get_categories()
                rank_categories_dict = \
                    self.__display_top_categories(top_categories)
                self.itf.display_guide(cfg.USER_GUIDE)
                # Avoid that a too narrow request leads to an empty selection.
                while True:
                    y = 0
                    self.itf.left_display_string(y, cfg.KEYPAD_INSTRUCTION_1)
                    y += 1
                    answer_category, y = self.__check_valid_answer(y, 1, 3,
                            cfg.SELECT_CATEGORY, rank_categories_dict)
                    # Input the parameters to search for a food item.
                    answer_name, y = self.itf.display_string_textpad(
                        y, 1, 25, cfg.ITEM_NAME)
                    # Launch the query in the local DB.
                    brand_name, y = self.itf.display_string_textpad(
                        y, 1, 25, cfg.ITEM_BRAND)
                    item_search = [answer_category, answer_name, brand_name]
                    refer_products = self.queries.refer_products(item_search)
                    # If the criterion are too specific, avoid a null outcome.
                    if len(refer_products) > 0:
                        break
                    else:
                        self.itf.right_display_info(cfg.WARNING_MESSAGE_2,
                                                    "warning")
                # Display a selection of products.
                rank_item_dict = dict()
                rank_counter = 0
                self.itf.clear_window("right")
                self.itf.display_result(cfg.ITEM_SEARCH_OUTCOME)
                for product in refer_products:
                    rank_counter += 1
                    self.itf.display_result(
                        cfg.PRODUCT_RANK_NAME.format(rank_counter,
                                                     product.name))
                    self.itf.display_result(
                        cfg.PRODUCT_BRAND_NUTR_GR.
                        format(product.brand, product.nutrition_grade))
                    self.itf.display_result(cfg.EMPTY_LINE)
                    # Create key_value of rank and product for further check
                    rank_item_dict[rank_counter] = product.code
                # Requests the user to select a food item to be compared with.
                while True:
                    code_ref_prod, y = self.__check_valid_answer(y, 1, 3,
                                        cfg.COMPARE_FOOD_ITEMS, rank_item_dict)
                    # New keywords are demanded if to restrictive.
                    while True:
                        # The user to enter keywords iot broaden the search
                        keywords_item, y = self.itf.display_string_textpad(
                            y, 1, 25, cfg.ADD_KEYWORDS)
                        # Create tuple with features of reference product
                        selected_prod = answer_category, keywords_item, \
                            code_ref_prod
                        selected_prod = tuple(selected_prod)
                        list_top_products = self.queries.top_products(
                            selected_prod)
                        # Make sure that user's choice isn't too restrictive
                        if len(list_top_products) > 0:
                            break
                        else:
                            self.itf.right_display_info(
                                cfg.WARNING_MESSAGE_1, "warning")
                            y -= 4
                    break
                self.itf.clear_window()
                self.itf.display_guide(cfg.USER_GUIDE)
                # Display the products matching the best user's request.
                top_products_dict = self.__display_top_products(
                    list_top_products)
                while True:
                    y = 0
                    # The user can view the item in a browser and to record it.
                    self.itf.left_display_string(
                        y, cfg.CHECK_DETAILED_RESULT)
                    answer, y = self.itf.display_string_textpad(
                        y+1, 1, 2, cfg.SELECT_Y_N)
                    answer = self.__ascii_to_string(answer).upper()
                    if answer == "Y":
                        code_best_prod, y = self.__check_valid_answer(y, 1, 3,
                                            cfg.USE_BROWSER, top_products_dict)
                        self.OFF.open_product_file_OFF(code_best_prod)
                        self.itf.right_display_info(
                            cfg.RECORD_SELECTED_ITEM)
                        date_time = self.__record_current_DTG()
                        compared_prods = code_best_prod, date_time, \
                            code_ref_prod
                        # Record automatically both selected and ref. products.
                        self.queries.record_comparred_products(compared_prods)
                        self.itf.right_display_info(cfg.PROCESSING_RECORD)
                        break
                    elif answer == "N":
                        break
                    else:
                        answer = self.itf.left_error_input()
                        y -= 4
                # Used to quit this loop an return to the main menu
                self.itf.clear_window()
                answer = self.itf.set_up_drop_down(
                    cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # Step where the user looks into the best products he has recorded.
            elif answer == cfg.OPERATE_ON_DB[1]:
                self.itf.clear_window()
                last_compared_products = self.queries.get_compared_products()
                # Display the last compared product, reference and best.
                best_products_dict = self.__display_compared_products(
                    last_compared_products)
                # The user can see a product in detail.
                if len(best_products_dict) > 0:
                    self.itf.display_guide(cfg.USER_GUIDE)
                    # User to confirm he wants to see the item in the browser.
                    no_further_check = False
                    while True:
                        y = 0
                        answer, y = self.itf.display_string_textpad(
                                y, 1, 2, cfg.CHECK_AGAIN_ITEMS_Y_N)
                        answer = self.__ascii_to_string(answer).upper()
                        if answer == "Y":
                            # Display the product in the default browser
                            code_product, y =\
                                self.__check_valid_answer(y, 1,
                                                          3, cfg.USE_BROWSER,
                                                          best_products_dict)
                            self.OFF.open_product_file_OFF(code_product)
                        elif answer == "N":
                            no_further_check = True
                            break
                        else:
                            answer = self.itf.left_error_input()
                            y -= 4
                else:
                    # Inform the user that he has no best product yet
                    self.itf.right_display_info(
                        cfg.WARNING_MESSAGE_3, "warning")
                    no_further_check = True
                # Return to the main menu, end of this loop.
                if no_further_check:
                    self.itf.clear_window()
                    answer = self.itf.set_up_drop_down(
                        cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # Import products from one of the most popular categories.
            elif answer == cfg.OPERATE_ON_DB[2]:
                y = 0
                self.itf.clear_window()
                # Import a short sample of OFF categories and displayed it.
                categories = self.queries.display_categories()
                categories_dict = dict()
                rank_counter = 0
                for category in categories:
                    rank_counter += 1
                    self.itf.display_result(
                        cfg.CAT_RANK_NAME.format(rank_counter, category.name))
                    categories_dict[rank_counter] = category.name

                self.itf.display_guide(cfg.USER_GUIDE)
                # The user is requested to designate a category to be uploaded.
                y = 0
                selected_category, y = \
                    self.__check_valid_answer(y, 1, 3, cfg.ADD_CATEGORY,
                                              categories_dict)
                display_chosen_category = cfg.NAME_IMPORTED_CATEGORY + \
                    selected_category
                self.itf.right_display_info(display_chosen_category)
                # This methods fetches a range of data from Open Food Facts.
                nb_imported, left_apart, list_items = \
                    self.OFF.import_products_list(selected_category)
                # Pieces of info from the downloaded data are given for info.
                self.itf.right_display_info(
                    coff.NUMBER_REJECTED_ITEMS.format(left_apart))
                self.itf.right_display_info(
                    coff.NUMBER_DOWNLOADED_ITEMS.format(nb_imported))
                self.itf.right_display_info(cfg.BE_PATIENT)
                # This is where the excerpt of OFF is uploaded in the local DB.
                self.queries.upload_products(list_items)
                nb_rows = self.queries.total_items()
                self.itf.right_display_info(
                    cfg.ROWS_LOCAL_DB.format(nb_rows))
                # Used to quit this step
                self.itf.clear_window()
                answer = self.itf.set_up_drop_down(
                    cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # Close properly the program and reinitialize the shell.
            elif answer == cfg.OPERATE_ON_DB[3]:
                self.itf.clear_window()
                self.queries.close_session()
                self.decision = "Quit"
                break
        return self.decision

    def __create_cnx_parameters(self):
        """
            This method is activated if no DB has been created. \
            All the parameters are asked and the script for the creation is run

            Arguments:

            NIL

            Returns:

            NIL
            """
        self.itf.clear_window("left")
        self.itf.display_guide(cfg.USER_GUIDE)
        y = 0
        # Ask for the connection parameters. Default value in config.py
        """
        self.itf.left_display_string(y, cfg.DB_INITIAL_INFO)
        user, y = self.itf.display_string_textpad(1, 1, 15,
                                                  cfg.DB_USER_INVITE)
        user = self.__ascii_to_string(user)
        if user != '':
            cfg.DB_USER = user
        """
        password, y = self.itf.display_string_textpad(y, 1, 20,
                                                      cfg.DB_PASSWORD_INVITE)
        password = self.__ascii_to_string(password)
        if password != '':
            cfg.DB_PASSWORD = password
        connection_string = cfg.DB_CONNEXION_STRING.format(
            cfg.DB_USER, cfg.DB_PASSWORD, "")
        # Connection parameters are saved in a separate file to be reused.
        with open(cfg.DB_PARAMETERS, "w") as file:
            file.write(connection_string)

    def __check_valid_answer(self, y, height, length, instruction, items_dict):
        """
            Check whether the number given by the user belongs to the keys of
            a dictionary. If not, the loop runs.

            Arguments:

            y: y of the instruction line

            height: height of the textpad

            length: length of the texpad

            instruction: inform the user to fill the textpad with the number
            corresponding to his choice

            items_dict: dictionary in which the values to select are located.
            The keys of this dictionary are the index displayed on the screen.

            Returns:

            item: the value of the dictionary

            y: incremented cursor on the screen.

            """
        while True:
            try:
                # Characterize the food item the user is looking for.
                answer, y = self.itf.display_string_textpad(y, height,
                                                            length,
                                                            instruction)
                answer = self.__ascii_to_string(answer)
                answer = int(answer)
                if answer in items_dict.keys():
                    item = items_dict.get(answer)
                    break
                else:
                    answer = self.itf.left_error_input()
                    y -= (3 + height)
            except Exception:
                answer = self.itf.left_error_input()
                y -= (3 + height)
        return item, y

    def __initialize_DB(self):
        """

            Create and initialize a new DB, including the downloading and \
            uploading of two lists from Open Food Facts: the stores and the\
            categories.

            Arguments:

            NIL

            Returns:

            NIL

            """
        self.queries = sql.ORMConnection()
        self.queries.create_database()
        self.itf.right_display_info(cfg.DB_CREATE_LOCAL_DB)
        self.queries = sql.ORMConnection()
        # Open the connection to the local DB
        self.queries.open_session()
        # Import categories from Open Food Facts
        OFF_categories = self.OFF.import_static_data(coff.URL_STATIC_CAT)
        # Configure the data and upload categories into the local DB
        self.queries.upload_categories(OFF_categories)
        self.itf.right_display_info(cfg.DB_CATEGORIES_FETCHED)
        # Import stores from Open Food Facts
        OFF_stores = self.OFF.import_static_data(coff.URL_STATIC_STORES)
        # Configure the data and upload stores into the local DB
        self.queries.upload_stores(OFF_stores)
        self.itf.right_display_info(cfg.DB_STORES_FETCHED)
        # Informs the user that the DB is empty.
        self.itf.right_display_info(cfg.EMPTY_DB, "warning")

    def __record_current_DTG(self):
        """

            Record the current date time and format it for the DB.

            Arguments:

            NIL

            Returns:

            current_DTG: current date and time formatted for SQL DB

            """
        current_DTG = datetime.now()
        current_DTG = current_DTG.strftime('%Y-%m-%d %H:%M:%S')
        return current_DTG

    def __display_compared_products(self, last_compared_products):
        """

            Display the last recorded products, best and reference.

            Arguments:

            last_compared_products: list of tuples containing the last recorded
            comparrisons.

            Returns: a dictionnary containing the code of each best product as\
             a value and a key being the index displayed on the screen.
            """
        best_products_dict = dict()
        rank_counter = 0
        # Display an ordered list of comparred products.
        for product in last_compared_products:
            rank_counter += 1
            self.itf.display_result(
                cfg.PRODUCT_RANK_NAME.format(rank_counter, product[0].name))
            self.itf.display_result(
                cfg.PRODUCT_BRAND_NUTR_GR.format(product[0].brand,
                                                 product[0].nutrition_grade))
            self.itf.display_result(
                cfg.DISPLAY_STORES.format(", ".join(product[0].stores)))
            self.itf.display_result(
                cfg.INITIAL_PRODUCT.format(product[2].name))
            self.itf.display_result(
                cfg.COMPARRISON_DATE.format(product[1].date))
            self.itf.display_result(cfg.EMPTY_LINE)
            best_products_dict[rank_counter] = product[0].code
        return best_products_dict

    def __display_top_products(self, list_top_products):
        """
            Display a list of the products matching the best with the user's 
            request.

            Arguments:

            list_top_products: list tuples containing the products matching 
            the best with the request.

            Returns:

            top_products_dict: dict with the product code as a value and the 
            product index used on the display. The latter being used as a key for
            further use of the dictionary.

            """
        top_products_dict = dict()
        rank_counter = 0
        for product in list_top_products:
            rank_counter += 1
            self.itf.display_result(
                cfg.PRODUCT_RANK_NAME.format(rank_counter, product.name))
            self.itf.display_result(cfg.PRODUCT_BRAND_NUTR_GR.format(
                product.brand, product.nutrition_grade))
            self.itf.display_result(
                cfg.DISPLAY_STORES.format(", ".join(product.stores)))
            top_products_dict[rank_counter] = product.code
        return top_products_dict

    def __display_top_categories(self, top_categories):
        """
            Display the most popular categories in the local DB.

            Arguments: 

            top_categories: list of tuples containing the most popular categories
            of the local DB.

            Returns: 
            
            rank_categories_dict: dict with the category name as a value and the 
            category index used on the display. The latter being used as a key for
            further use of the dictionary.

            """
        rank_categories_dict = dict()
        rank_counter = 0
        for category in top_categories:
            rank_counter += 1
            self.itf.display_result(
                cfg.RANK_NAME_QTY.format(rank_counter, category.name,
                                                 category.number_items))
            rank_categories_dict[rank_counter] = category.name
        return rank_categories_dict


def main(user):
    """

        Launch the main menu of the app.

        Methods:

        NIL

        Variables:

        answer: as return from the terms and conditions if they are rejected.

        quit: as return from the main menu, iot quit properly the application.

        """
    user.itf.display_message(cfg.WELCOME_MESSAGE)
    time.sleep(1)
    user.itf.split_screen()
    answer = user.step_terms_and_conditions(cfg.T_C_FILE)
    if answer == "No":
        user.itf.quit_display()
    else:
        quit = user.step_select_action()
        if quit == "Quit":
            user.itf.quit_display()
