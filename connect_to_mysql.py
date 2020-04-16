"""

    This module interacts with the local DB, which is a mySQL DB.

    Classes:

    MySQLQueries: manage the querying methods under a same umbrella.

    Product: create an instance for each product imported from the local DB.

    Exceptions:

    NIL.

    Functions:

    query_settings(answer): insert a % before and after each word of selected fields \
        in order to broaden the search.

    """
import datetime
import pickle

import mysql.connector

import config
import config_queries as cq
import script_create_database as scr


class Product:
    """

        This class convert the rows into object for further use in the controller.

        Methods:

        NIL

        Instance variables:

        item_features (tuple): contains all the features of the product fetched
        from the DB.

        index: gives an index, via a counter for a more friendly display
        of the results.

        Comment:

        Good to know: the counter has to be updated at each query in order to
        avoid incrementation within the same session.
        """

    counter = 1
    def __init__(self, item_features):
        self.item_features = item_features
        self.index = Product.counter
        Product.counter += 1


class MySQLQueries:
    """

        Organized around an initialization of the connection to the DB
        at the instanciation, followed by different queries to be used
        as the program unfolds.

        Methods:

        get_categories(): get the names of the categories from which the user can
        afterwards load the data from OFF.

        get_product(): get a selection of product from the local DB, iaw the criterion
        filled by the user.

        get_best_product(): get a filtered list of products as close as possible
        to a selected product.

        retrieve_recorded_products(): get the list of best products recorded in
        the local DB.

        get_numbers_on_DB(): fetch some figures related to the local DB, like
        the number of rows, etc.

        upload_product(): upload a single product into the local DB,
        e.g. a selected best product.

        update_best_product_date(): updates the best product record with the date.

        upload_dataset(): upload to the local DB a bunch of rows downloaded from OFF.

        close_connection(): close the connection to mySQL iot to avoid free access.

        upload_categories(): upload a list of categories from Open Food Facts

        create_database(): create a local DB for the first use of the App

        Instance variables:

        self.cnx: establish the connection to the local mySQL DB.

        self.cursor(tuple): contain the data gathered in the local DB.

        Comment:

        self.test_outside = self.cnx.is_connected()
        can be included in the __init__ to check the connection.

        """

    def __init__(self):
        """

            Initialize the connexion with the local DB with parameters stored
            in a separate file.

            Arguments:

            NIL.

            Returns:

            NIL.

            """
        with open("db_parameters.txt", "rb") as file:
            connection_parameters = pickle.load(file)
        self.cnx = mysql.connector.connect(**connection_parameters)
        self.cursor = self.cnx.cursor(buffered=True)
        # For maintenance purpose: use self.cnx.is_connected() to check connection

    def get_categories(self, query):
        """

            Get the name of categories already recorded in the local DB.

            Arguments:

            query: query designed to fetch the categories.

            Returns:

            categories with an index number.

            """
        categories = []
        self.cursor.execute(query)
        Product.counter = 1
        for category in self.cursor:
            category = Product(category)
            categories.append(category)
        return categories

    def get_product(self, query, searched_item):
        """

            Get a list of 10 products as close as possible to the criterion filled by the user

            Arguments:

            query: self explanatory

            searched_item (list): criterion to apply for the query.

            Returns:

            products: list of food items, augmented with an index starting at 1.

            """
        products = []
        query = query.format(
            searched_item[0], searched_item[1], searched_item[2], searched_item[3])
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size=10)
        Product.counter = 1
        for product in results:
            product = Product(product)
            products.append(product)
        return products

    def get_best_product(self, query, best_product):
        """

            Get a list of products with a better nutrition grade that the initially selected.

            Arguments:

            query: self explanatory.

            best-product(tuple): contain the criterion to sort out the matching products.

            Returns:

            best_products(list): list of selected products, with an index number.

            """
        best_products = []
        result = []
        query = query.format(best_product[0], best_product[1], best_product[2])
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size=5)
        Product.counter = 1
        for product in results:
            product = Product(product)
            best_products.append(product)
        return best_products

    def retrieve_recorded_products(self, query):
        """

            Fetch the last recorded best products and the products used for the comparrison.

            Arguments:

            query: self explanatory

            Returns:

            recorded_products(list): list of both best and reference products, with a index.

            """
        recorded_products = []
        result = []
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size=5)
        Product.counter = 1
        for product in results:
            product = Product(product)
            recorded_products.append(product)
        return recorded_products

    def get_numbers_on_DB(self, query):
        """

            Gets simple figures from the local DB.

            Arguments:

            query: self explanatory

            Returns:

            result[0][0]: currently the number of rows in the table product.

            """
        self.cursor.execute(query)
        result = self.cursor.fetchmany()
        return result[0][0]

    def upload_product(self, query, item):
        """

            Upload only one item in the local DB. Currently formatted to record a best product.

            Arguments:

            query: self explanatory

            item: the food item to be recorded in the table best_product.

            Returns:

            NIL

            """
        query = query.format(item[0], item[1], item[2])
        self.cursor.execute(query)
        self.cnx.commit()

    def update_best_product_date(self, query, item):
        """

            Update the field date of a recorded best product

            Arguments:

            query: self explanatory.

            item: date-time of the record and product code.

            Returns:

            NIL.

            """
        query = query.format(item[0], item[1])
        self.cursor.execute(query)
        self.cnx.commit()

    def upload_dataset(self, query, item_list):
        """

            After the selection of a new category, comes its upload in the local DB.

            Arguments:

            query: self explanatory, based on a category as main criterion.

            item_list: list of items downloaded from OFF. They have been largely cleaned beforehand.

            Returns;

            NIL

            """
        self.cursor.executemany(query, item_list)
        self.cnx.commit()

    def close_connection(self):
        """

            Close the connection with the local DB.

            Arguments:

            NIL

            Returns:

            NIL

            """
        self.cursor.close()

    def upload_categories(self, query, categories):
        """

            When creating a new DB, uploads a list of categories to start working
            with the DB.

            Arguments:

            query: self explanatory

            categories: list of categories downloaded from Open Food Facts.

            Returns:

            NIL

            """
        category_tuple = [(category,) for category in categories]
        self.cursor.executemany(cq.query_upload_new_category, category_tuple)
        self.cnx.commit()

    def create_database(self):
        """

            Create a local DB to operate the application.
            Activated solely at the first use.

            Arguments:

            NIL

            Returns:

            NIL

            """
        # Create a new and empty database
        self.cursor.execute(scr.DB_CREATION.format(config.DB_NAME['database']))
        # Add the name of the database to the parameters file for further use
        with open("db_parameters.txt", 'rb') as file:
            connection_parameters = pickle.load(file)
        connection_parameters.update(config.DB_NAME)
        with open("db_parameters.txt", "wb") as file:
            pickle.dump(connection_parameters, file)
        # Activate the Database to subsequently create the tables
        self.cursor.execute(scr.DB_USE.format(config.DB_NAME['database']))
        # Add the tables to the new database
        for table_name in scr.DB_TABLES:
            table_schema = scr.DB_TABLES[table_name]
            self.cursor.execute(table_schema)


def query_settings(answer):
    """

        Prepare the search criterion before looking into the local DB.

        Arguments:

        answer: keyword, search criterion to be prepared for the search.

        Returns:

        item_features: keyword made ready to be appended to the query.

        """
    temporary_list = []
    item_features = []
    temporary_list = answer.strip().split(" ")
    temporary_list = ["%"+word+"%" for word in temporary_list]
    item_features = " ".join(temporary_list)
    return item_features


if __name__ == "__main__":
    import pickle
    config.DB_CONNECTION_PARAMETERS['database'] = 'get_better_diet2'
    with open("db_parameters.txt", "wb") as file:
        pickle.dump(config.DB_CONNECTION_PARAMETERS, file)

    requete = MySQLQueries()
    result = requete.get_categories(cq.query_retrieve_available_categories)
    print(result)
    print(result[0].index, result[0].item_features[0],
          result[0].item_features[1])
