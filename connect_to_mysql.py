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

    def get_categories(self):
    # Purpose of this function is to send a query to the DB and fetch the required data
        query = cq.query_categories
        liste = []
        self.cursor.execute(query)
        for (id, category) in self.cursor:
            liste.append((id, category))
        return liste

    def upload_products(self):
        query = ("""LOAD DATA INFILE 
        '/Users/fabricejaouen/DepotLocalGIT/OC_Project_5/Response_API.txt' 
        INTO TABLE Products 
        FIELDS TERMINATED BY ';' ENCLOSED BY '"' 
        LINES STARTING BY ' ' TERMINATED BY '\n'
        (brands, name, category_id, code, nutrition_grade, stores, ingredients)""")
        self.cursor.execute(query)
        self.cnx.commit()

    def close_connection(self):
        self.cursor.close()

query = MySQLQueries()
#query.upload_products()
query.get_categories()

