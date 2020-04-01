"""

This module interacts with the local DB, which is a mySQL DB.

Classes:
MySQLQueries: manage the querying methods under a same umbrella
    
Exceptions:
NIL.
    
Functions:
query_settings(answer): insert a % before and after each word of selected fields \
    in order to broaden the search.

"""
import mysql.connector
import config
import config_queries as cq
import datetime


class MySQLQueries:
    """

    Organized around an initialization of the connection to the DB at the instanciation, \
    followed by different queries to be used as the program unfolds.

    Methods:
    get_categories(): get the names of the categories from which the user can afterwards load the data from OFF.

    get_product(): get a selection of product from the local DB, iaw the criterion filled by the user.

    get_best_product(): get a filtered list of products as close as possible to a selected product.

    retrieve_recorded_products(): get the list of best products recorded in the local DB.

    get_numbers_on_DB(): fetch some figures related to the local DB, like the number of rows, etc.

    upload_product(): upload a single product into the local DB, e.g. a selected best product.

    upload_dataset(): upload to the local DB a bunch of rows downloaded from OFF.

    close_connection(): closes the connection to mySQL iot to avoid free access.

    Instance variables:
    self.cnx: establish the connection to the local mySQL DB.

    self.cursor (tuple): contain the data gathered in the local DB.

    Comment:
    self.test_outside = self.cnx.is_connected()
    can be included in the __init__ to check the connection.

    """

    def __init__(self):
        """

        Initialize the connexion with the local DB with parameters stored in config.

        Arguments:
        NIL.

        Returns:
        NIL.

        """
        self.cnx = mysql.connector.connect(**config.DB_CONNECTION_PARAMETERS)
        self.cursor = self.cnx.cursor(buffered=True)

    def get_categories(self, query):
        """

        Get the name of categories already recorded in the local DB.

        Arguments:
        query: query designed to fetch the categories, including their id number.

        Returns:
        categories with their id number.

        """
        categories = {}
        self.cursor.execute(query)
        for (key, category) in self.cursor:
            categories.update({int(key): category})
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
        counter = 1
        for result in results:
            result = {int(counter): result}
            products.append(result)
            counter += 1
        return products

    def get_best_product(self, query, best_product):
        """

        Get a list of products with a better nutrition grade that the initially selected.

        Arguments: 
        query: self explanatory.

        best-product (tuple): contain the criterion to sort out the matching products.

        Returns:
        best_products (list): list of selected products, with an index number.

        """
        best_products = []
        result = []
        query = query.format(best_product[0], best_product[1], best_product[2])
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size=5)
        counter = 1
        for result in results:
            result_list = [int(counter), result]
            best_products.append(result_list)
            counter += 1
        return best_products

    def retrieve_recorded_products(self, query):
        """

        Fetch the last recorded best products and the products used for the comparrison. 

        Arguments:
        query : self explanatory

        Returns:
        recorded_products (list): list of both best and reference products, with a index.

        """
        recorded_products = []
        result = []
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size=5)
        counter = 1
        for result in results:
            result_list = [int(counter), result]
            recorded_products.append(result_list)
            counter += 1
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

        Uploads only one item in the local DB. Currently formatted to record a best product.

        Arguments:
        query: self explanatory
        item: the food item to be recorded in the table best_product.

        Returns:
        NIL

        """
        query = query.format(item[0], item[1], item[2])
        self.cursor.execute(query)
        self.cnx.commit()

    def upload_dataset(self, query, item_list):
        """

        After the selection of a new category, comes it upload in the local DB.

        Arguments:
        query: self explanatory

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
    requete = MySQLQueries()
    query = cq.query_retrieve_recorded_product
    result = requete.retrieve_recorded_products(
        cq.query_retrieve_recorded_product)
    print(result)
