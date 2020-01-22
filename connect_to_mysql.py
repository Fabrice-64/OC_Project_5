"""
This module deals with the relation between the requests of the administrator/user an the database

The functionalities implemented consist in:
Administrator role:
-Download and upload a new category, this includes the cleaning of the DB
-Delete the items belonging to a certain category
-Recording the result of a query to a table
-
"""
import mysql.connector
import config



cnx = mysql.connector.connect(**config.connection_to_database)

print(type(cnx))

cursor = cnx.cursor()

query = ("select * from Categories")

cursor.execute(query)

for (id, category) in cursor:
    print("{}:  {}".format(id, category))

cursor.close()
cnx.close()

def send_item_search()
#Sends a search request for an item into the DB. The request is based on Category, name of the item, nutrition_score

# Function to record the  search result in a separate file