import mysql.connector
import config
import connect_to_mysql

"""
cnx = mysql.connector.connect(**config.connection_to_database)

cursor = cnx.cursor()
"""
class Connection_DB:
    def connection():
        cnx_db = config.connection_to_database
        cnx = connect_to_mysql.initiate_connexion(cnx_db)
        cursor = cnx.cursor()

        test_outside = cnx.is_connected()
        print("externe :", test_outside)

        connect_to_mysql.get_categories(cursor)

Connection_DB.connection()