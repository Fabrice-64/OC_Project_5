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

from AppView.interface_management import Interface
from AppModel.open_food_facts.connect_to_OFF import ConnectToOFF
from AppController import config as cfg
from AppModel.open_food_facts import config_open_food_facts as coff
from AppModel.open_food_facts import connect_to_OFF as OFF
from AppModel.local_DB import connect_to_mysql as sql


class UserDialog:
    """

        Is the cornerstone of the application.

        It is a composite class, with following components:
        im.Interface: manage the interface.

        sql.ORMConnection: manage the queries to the local DB. In order to check\
            whether there already exists a DB, this class is instanciated\
            in the step_select_action() method.

        OFF.ConnectToOFF: manage the download of data from Open Food Facts.

        Methods:

        step_terms_and_conditions(): require approval of the T & C to go on with the app.

        ascii_to_string(): convert the inputs from the textpad from ASCII into strings.

        select_action(): main loop through which the whole program runs.

        create_cnx_parameters(): used exclusively for the first use, when the local
        DB has not been created yet.

        open_product_browser(): sends the order to open a product page
        from Open Food Facts website.

        display_compared_products: Display the last recorded products, 
        best and reference.

        display_top_products: Display a list of the products matching 
        the best with the user's request.

        Instance variables:

        NIL

        """

    def __init__(self):
        """
            Integrates the classes Interface and ConnectToOFF as components.

            Arguments:

            self.interface: manage the relation with the display (View).
            self.OFF: used either to download data from OFF, or to access a product page.

            Returns:

            NIL

            """
        self.interface = Interface()
        self.OFF = ConnectToOFF()

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
        self.interface.left_display_string(y, cfg.T_C_LINE_1)
        self.interface.left_display_string(y+1, cfg.T_C_LINE_2)
        self.interface.display_file(file)
        self.interface.clear_window("left")
        self.interface.left_display_string(y, cfg.ACCEPT_T_C)
        self.interface.left_display_string(y+1, cfg.IF_REFUSAL)
        answer = self.interface.set_up_drop_down(
            cfg.REPLY_YES_NO, cfg.SELECT_ANSWER)
        if answer == "Yes":
            self.interface.clear_window('left')
            self.interface.left_display_string(y, cfg.T_C_APPROVAL)
            time.sleep(1)
        return answer

    def ascii_to_string(self, ascii_string):
        """
            Convert the textpad returns in a usable format, as they are ASCII objects.

            Arguments:

            ascii_string: ascii is the normal outcome from a textpad input in Curses

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
        # Check whether a local DB has already been created. If not, starts a process.
        create_DB = False
        while True:
            try:
                # Check whether a connection with an existing local DB is established.
                self.queries = sql.ORMConnection()
                break
            except Exception:
                # Creation of a connexion, iot prepare the DB creation
                self.interface.clear_window("right")
                self.interface.right_display_info(
                    cfg.WARNING_MESSAGE_4, "warning")
                self.create_cnx_parameters()
                create_DB = True
            if create_DB:
            # Creation of the DB through a method hosted in the model module
                self.queries = sql.ORMConnection()
                self.queries.create_database()
                self.interface.right_display_info(cfg.DB_CREATE_LOCAL_DB)
                self.queries = sql.ORMConnection()
                # Open the connection to the local DB
                self.queries.open_session()
                # Import categories from Open Food Facts
                OFF_categories = self.OFF.import_static_data(
                    coff.URL_STATIC_CAT)
                # Configure the data and upload categories into the local DB
                self.queries.upload_categories(OFF_categories)
                self.interface.right_display_info(cfg.DB_CATEGORIES_FETCHED)
                # Import stores from Open Food Facts
                OFF_stores = self.OFF.import_static_data(
                    coff.URL_STATIC_STORES)
                # Configure the data and upload stores into the local DB
                self.queries.upload_stores(OFF_stores)
                self.interface.right_display_info(cfg.DB_STORES_FETCHED)
                # Informs the user that the DB is empty. 
                self.interface.right_display_info(cfg.EMPTY_DB, "warning")
                break

        self.interface.title_bar(cfg.TITLE_2)
        # Display a drop down menu to navigate in the application
        self.interface.clear_window()
        self.interface.left_display_string(0, cfg.INFO_LINE_1)
        self.interface.display_result(cfg.INFO_DISPLAY_RESULTS)
        answer = self.interface.set_up_drop_down(
            cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)
        # Here start the work on the DB to find, select and record a product
        y = 0
        while True:
            # Open a session with the ORM iot work with the DB.
            self.queries.open_session()
            # Look for a product !!
            if answer == cfg.OPERATE_ON_DB[0]:
                self.interface.title_bar(cfg.TITLE_3)
                self.interface.clear_window()
                # list of categories previously recorded is displayed on the right window.
                top_categories = self.queries.get_categories()
                rank_categories = dict()
                rank_counter = 0
                for category in top_categories:
                    rank_counter += 1
                    self.interface.display_result(
                        cfg.RANK_NAME_QTY.format(rank_counter, category.name,
                                                 category.number_items))
                    rank_categories[rank_counter] = category.name
                self.interface.display_guide(cfg.USER_GUIDE)
                # This loop avoids that a too narrow request leads to an empty selection.
                while True:
                    while True:
                        try:
                            y = 0
                            self.interface.left_display_string(
                                y, cfg.KEYPAD_INSTRUCTION_1)
                            self.interface.left_display_string(
                                y+1, cfg.SELECT_CATEGORY)
                            y = y + 3
                            # Characterize the food item the user is looking for.
                            answer = self.interface.display_textpad(y, 1, 3)
                            answer = self.ascii_to_string(answer)
                            # The category is the only field which is compulsary.
                            answer = int(answer)
                            if answer in rank_categories.keys():
                                answer_category = rank_categories.get(answer)
                                break
                            else:
                                answer = self.interface.left_error_input()
                                y = 0
                        except Exception:
                            answer = self.interface.left_error_input()
                            y = 0
                    # Input the parameters to search for a food item.
                    y += 3
                    answer_name, y = self.interface.display_string_textpad(
                        y, 1, 25, cfg.ITEM_NAME)
                    # Launch the query in the local DB.
                    brand_name, y = self.interface.display_string_textpad(
                        y, 1, 25, cfg.ITEM_BRAND)
                    item_search = [answer_category, answer_name, brand_name]
                    refer_products = self.queries.refer_products(item_search)
                    # If the criterion are too specific, avoid a null outcome.
                    if len(refer_products) > 0:
                        break
                    else:
                        self.interface.right_display_info(
                            cfg.WARNING_MESSAGE_2, "warning")

                # Display a selection of products.
                rank_item_dict = dict()
                rank_counter = 0
                self.interface.clear_window("right")
                self.interface.display_result(cfg.ITEM_SEARCH_OUTCOME)
                for product in refer_products:
                    rank_counter += 1
                    self.interface.display_result(
                        cfg.PRODUCT_RANK_NAME.format(rank_counter, product.name))
                    self.interface.display_result(
                        cfg.PRODUCT_BRAND_NUTR_GR.format(product.brand,
                                                         product.nutrition_grade))
                    self.interface.display_result(cfg.EMPTY_LINE)
                    # Create key_value of rank and product for further check
                    rank_item_dict[rank_counter] = product.code

                # Requests the user to select a food item to be compared with.
                while True:
                    while True:
                        try:
                            # Check whether the answer is both an int & in the dict.
                            answer, y = self.interface.display_string_textpad(
                                y, 1, 3, cfg.COMPARE_FOOD_ITEMS)
                            answer = self.ascii_to_string(answer)
                            answer = int(answer)
                            if answer in rank_item_dict.keys():
                                code_ref_prod = rank_item_dict.get(answer)
                                break
                            else:
                                answer = self.interface.left_error_input()
                                y -= 4
                        except Exception:
                            answer = self.interface.left_error_input()
                            y -= 4
                    # If the keywords are too restrictive new ones are demanded.
                    while True:
                        # The user is requested to enter keywords iot broaden the search
                        keywords_item, y = self.interface.display_string_textpad(
                            y, 1, 25, cfg.ADD_KEYWORDS)
                        # Create tuple with characteristics of reference product
                        selected_prod = answer_category, keywords_item, code_ref_prod
                        selected_prod = tuple(selected_prod)
                        list_top_products = self.queries.top_products(
                                                                    selected_prod)
                        # Make sure that the user's choice isn't too restrictive
                        if len(list_top_products) > 0:
                            break
                        else:
                            self.interface.right_display_info(
                                cfg.WARNING_MESSAGE_1, "warning")
                            y -= 4
                    break

                self.interface.clear_window()
                self.interface.display_guide(cfg.USER_GUIDE)
                # Display the products matching the best user's request.
                top_products_dict = self.display_top_products(list_top_products)
                while True:
                    y = 0
                    # The user is offered to view the item in a browser and to record it.
                    self.interface.left_display_string(
                        y, cfg.CHECK_DETAILED_RESULT)
                    answer, y = self.interface.display_string_textpad(
                        y+1, 1, 2, cfg.SELECT_Y_N)
                    answer = self.ascii_to_string(answer).upper()
                    if answer == "Y":
                        while True:
                            try:
                                # Check whether the answer is both an int & in the dict.
                                answer, y = self.interface.display_string_textpad(
                                    y, 1, 2, cfg.USE_BROWSER)
                                answer = self.ascii_to_string(answer)
                                answer = int(answer)
                                if answer in top_products_dict.keys():
                                    code_best_prod = top_products_dict.get(
                                        answer)
                                    self.OFF.open_product_file_OFF(
                                        code_best_prod)
                                    break
                                else:
                                    answer = self.interface.left_error_input()
                                    y -= 4
                            except Exception:
                                answer = self.interface.left_error_input()
                                y -= 4
                        self.interface.right_display_info(
                            cfg.RECORD_SELECTED_ITEM)
                        record_date_time = datetime.now()
                        record_date_time = record_date_time.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        compared_prods = code_best_prod, record_date_time,\
                            code_ref_prod
                        # Record automatically both selected and ref. products.
                        self.queries.record_comparred_products(compared_prods)
                        self.interface.right_display_info(
                            cfg.PROCESSING_RECORD)
                        break
                    elif answer == "N":
                        break
                    else:
                        answer = self.interface.left_error_input()
                        y -= 4
                # Used to quit this loop an return to the main menu
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # Step where the user looks into the best products he has recorded.
            elif answer == cfg.OPERATE_ON_DB[1]:
                self.interface.clear_window()
                last_compared_products = self.queries.get_compared_products()
                # Display the last compared product, reference and best.
                best_products_dict = self.display_compared_products(last_compared_products)
                # The user can see a product in detail.
                if len(best_products_dict) > 0:
                    # User to confirm he wants to see the item in the browser.
                    while True:
                        answer = ""
                        while answer not in ["Y", "N"]:
                            y = 0
                            answer, y = self.interface.display_string_textpad(
                                y, 1, 2, cfg.CHECK_AGAIN_ITEMS_Y_N)
                            answer = self.ascii_to_string(answer).upper()
                            if answer not in ["Y", "N"]:
                                answer = self.interface.left_error_input()
                                y = 0
                        if answer == "N":
                            break
                        try:
                            # Check whether the input meets the requirements.
                            answer, y = self.interface.display_string_textpad(
                                y+1, 1, 2, cfg.USE_BROWSER)
                            answer = self.ascii_to_string(answer)
                            answer = int(answer)
                            if answer in best_products_dict.keys():
                                code_product = best_products_dict.get(answer)
                                # Calls the hyperlink to open the product in the browser.
                                self.OFF.open_product_file_OFF(code_product)
                            else:
                                answer = self.interface.left_error_input()
                                self.interface.clear_window('left')
                                y = 0
                        except Exception:
                            answer = self.interface.left_error_input()
                            self.interface.clear_window('left')
                            y = 0
                else:
                    self.interface.right_display_info(
                        cfg.WARNING_MESSAGE_3, "warning")
                # Return to the main menu, end of this loop.
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # This is to import products from one of the most popular categories.
            elif answer == cfg.OPERATE_ON_DB[2]:
                y = 0
                self.interface.clear_window()
                # A short sample of OFF categories is imported and displayed in the right window.
                categories = self.queries.display_categories()
                categories_dict = dict()
                rank_counter = 0
                for category in categories:
                    rank_counter += 1
                    self.interface.display_result(
                        cfg.CAT_RANK_NAME.format(rank_counter, category.name))
                    categories_dict[rank_counter] = category.name

                self.interface.display_guide(cfg.USER_GUIDE)
                # The user is requested to designate a category to be uploaded.
                while True:
                    y = 0
                    try:
                        # Check that the user's input meets the requirements.
                        answer, y = self.interface.display_string_textpad(
                            y, 1, 3, cfg.ADD_CATEGORY)
                        answer = self.ascii_to_string(answer)
                        answer = int(answer)
                        if answer in categories_dict.keys():
                            selected_category = categories_dict.get(answer)
                            display_chosen_category = cfg.NAME_IMPORTED_CATEGORY + \
                                selected_category
                            self.interface.right_display_info(
                                display_chosen_category)
                            break
                        else:
                            self.interface.right_display_info(
                                cfg.WARNING_MESSAGE_0, "warning")
                            answer = ""
                            y = y-4
                    except Exception:
                        self.interface.right_display_info(
                            cfg.WARNING_MESSAGE_0, "warning")
                        answer = ""
                        y = y-4

                # This methods fetches a range of data from Open Food Facts.
                (nb_imported_items, items_left_apart,
                    list_items) = self.OFF.import_products_list(selected_category)
                # Here some pieces of info related to the downloaded data are given for info.
                self.interface.right_display_info(
                    coff.NUMBER_REJECTED_ITEMS.format(items_left_apart))
                self.interface.right_display_info(
                    coff.NUMBER_DOWNLOADED_ITEMS.format(nb_imported_items))

                self.interface.right_display_info(cfg.BE_PATIENT)
                # This is where the excerpt of OFF is uploaded in the local DB.
                self.queries.upload_products(list_items)
                nb_rows = self.queries.total_items()
                self.interface.right_display_info(
                    cfg.ROWS_LOCAL_DB.format(nb_rows))
                # Used to quit this step
                self.interface.clear_window()
                answer = self.interface.set_up_drop_down(
                    cfg.OPERATE_ON_DB, cfg.SELECT_ANSWER)

            # This last option is to close properly the program and reinitialize the shell.
            elif answer == cfg.OPERATE_ON_DB[3]:
                self.interface.clear_window()
                self.queries.close_session()
                self.decision = "Quit"
                break
        return self.decision

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
        self.interface.display_guide(cfg.USER_GUIDE)
        y = 0
        # Ask for the connection parameters. Default value in config.py
        self.interface.left_display_string(y, cfg.DB_INITIAL_INFO)
        user, y = self.interface.display_string_textpad(1, 1, 15,
                                                        cfg.DB_USER_INVITE)
        user = self.ascii_to_string(user)
        if user != '':
            cfg.DB_USER = user
        password, y = self.interface.display_string_textpad(y, 1, 20,
                                                            cfg.DB_PASSWORD_INVITE)
        password = self.ascii_to_string(password)
        if password != '':
            cfg.DB_PASSWORD = password
        connection_string = cfg.DB_CONNEXION_STRING.format(
            cfg.DB_USER, cfg.DB_PASSWORD, "")
        # Connection parameters are saved in a separate file to be reused.
        with open(cfg.DB_PARAMETERS, "w") as file:
            file.write(connection_string)

    def open_product_browser(self, answer, dictionary):
        """
            Opens the browser and access the Open Food Facts website to display
            a the detailed data on a product.

            Arguments:

            NIL

            Returns:

            NIL
            """
        try:
            # Check that the input meets the requirements.
            answer = self.ascii_to_string(answer)
            answer = int(answer)
            if answer in dictionary.keys():
                code_product = dictionary.get(answer)
                # Calls the hyperlink to open the product in the browser.
                self.OFF.open_product_file_OFF(code_product)
        except Exception:
            self.interface.right_display_info(cfg.WARNING_MESSAGE_0, "warning")
            answer = ""
        return answer

    def display_compared_products(self, last_compared_products):
        """

            Display the last recorded products, best and reference.

            Arguments:

            last_compared_products: list of tuples containing the last recorded
            comparrisons.

            Returns: a dictionnary containing the code of each best product as 
            a value and a key being the index displayed on the screen.
            """
        best_products_dict = dict()
        rank_counter = 0
        # Display an ordered list of comparred products.
        for product in last_compared_products:
            rank_counter += 1
            self.interface.display_result(
                cfg.PRODUCT_RANK_NAME.format(rank_counter, product[0].name))
            self.interface.display_result(
                cfg.PRODUCT_BRAND_NUTR_GR.format(product[0].brand, 
                product[0].nutrition_grade))
            self.interface.display_result(
                cfg.DISPLAY_STORES.format(", ".join(product[0].stores)))
            self.interface.display_result(
                cfg.INITIAL_PRODUCT.format(product[2].name))
            self.interface.display_result(
                cfg.COMPARRISON_DATE.format(product[1].date))
            self.interface.display_result(cfg.EMPTY_LINE)
            best_products_dict[rank_counter] = product[0].code
        return best_products_dict

    def display_top_products(self, list_top_products):
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
            self.interface.display_result(
                    cfg.PRODUCT_RANK_NAME.format(rank_counter, product.name))
            self.interface.display_result(cfg.PRODUCT_BRAND_NUTR_GR.format(
                    product.brand, product.nutrition_grade))
            self.interface.display_result(
                    cfg.DISPLAY_STORES.format(", ".join(product.stores)))
            top_products_dict[rank_counter] = product.code
        return top_products_dict
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
