"""
This module deals with the relation between the requests of the administrator/user an the database

The functionalities implemented consist in:
Administrator role:
-Download and upload a new category, this includes the cleaning of the DB
-Delete the items belonging to a certain category
-Recording the result of a query to a table
"""
import mysql.connector
import config 
import config_queries as cq

class MySQLQueries:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config.db_connection_parameters)
        self.cursor = self.cnx.cursor()
        self.test_outside = self.cnx.is_connected()
        print("externe :", self.test_outside)

    def get_categories(self, query):
    # Purpose of this function is to send a query to the DB and fetch the required data
        categories = {}
        self.cursor.execute(query)
        for (key, category) in self.cursor:
            categories.update({int(key) : category})
        return categories
    
    def get_product(self, query, searched_item):
        products = []
        query = query.format(searched_item[0], searched_item[1], searched_item[2], searched_item[3])
        self.cursor.execute(query)
        results = self.cursor.fetchmany(size = 10)
        counter  = 1
        for result in results:
            result = {int(counter) : result}
            products.append(result)
            counter += 1
        return products

    def get_best_product(self, query, best_product):
        query = query.format(best_product[0], best_product[1], best_product[2])
        self.cursor.execute(query)
        result = self.cursor.fetchmany(size = 10)
        return result


    def get_numbers_on_DB(self,query):
        self.cursor.execute(query)
        result = self.cursor.fetchmany()
        print(result[0][0])
        return result[0][0]

    # Method used to upload only ONE item in the local DB.
    def upload_product(self, query, item):
        query = query.format(item)
        self.cursor.execute(query)
        self.cnx.commit()

    # Method used to upload a series of food items.
    def upload_dataset(self, query,item_list):
        self.cursor.executemany(query, item_list)
        self.cnx.commit()

    def close_connection(self):
        self.cursor.close()

def query_settings(answer):
    temporary_list = []
    item_features = []
    temporary_list = answer.strip().split(" ")
    temporary_list = ["%"+word+"%" for word in temporary_list]
    item_features = " ".join(temporary_list)
    return item_features

def query_research_set_up():
    pass


if __name__ == "__main__":
    requete = MySQLQueries()
    searched_item = ("Snacks", "%", "Carrefour", "%")
    products = requete.get_product(cq.query_searched_item, searched_item)
    print(products)
