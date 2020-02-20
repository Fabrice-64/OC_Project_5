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

class MySQLQueries:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config.db_connection_parameters)
        self.cursor = self.cnx.cursor()
        self.test_outside = self.cnx.is_connected()
        print("externe :", self.test_outside)

    def get_categories(self):
    # Purpose of this function is to send a query to the DB and fetch the required data
        query = ("select * from Categories")
        self.cursor.execute(query)
        for (id, category) in self.cursor:
            print("{}:  {}".format(id, category))

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
query.upload_products()














def send_item_search():
#Sends a search request for an item into the DB. The request is based on Category, name of the item, nutrition_score
    print("send_item_search trouvé")
    pass

def insert_query_result_to_table():
# Function to record the  search result into a separate table named XXXXX
    pass

def delete_part_of_table():
# Based on criteria determined in the administrator_role module, it is aimed at getting updated data
    pass

def insert_a_new_account():
#Links with the table where all users are recorded
    pass

def connect_recorded_account():
# Once existence in DB is confirmed, gives access to specific functionalities
    pass


