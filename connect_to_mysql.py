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

def initiate_connexion(cnx_db):
    print('link established')
    cnx = mysql.connector.connect(**cnx_db)
    return(cnx)

def get_categories(cursor):
# Purpose of this function is to send a query to the DB and fetch the required data
    query = ("select * from Categories")
    cursor.execute(query)
    for (id, category) in cursor:
        print("{}:  {}".format(id, category))


















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


