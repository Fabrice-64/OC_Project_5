import mysql.connector
import config

cnx = mysql.connector.connect(**config.connection_to_database)

print(type(cnx))

cursor = cnx.cursor()

query = ("source /Users/fabricejaouen/DepotLocalGIT/OC_Project_5/select_categories.sql")

cursor.execute(query)

for (id, category) in cursor:
    print("{}:  {}".format(id, category))

cursor.close()
cnx.close()
