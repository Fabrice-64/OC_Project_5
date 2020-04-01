"""
The purpose of this short module is solely to initialize the local DB by downloading \
    a sample of categories from OFF and uploading them locally

"""
import mysql.connector
import config
import config_queries as cq
import config_open_food_facts as coff
import connect_to_OFF
import connect_to_mysql
import time

if __name__ == "__main__":
    initialization = connect_to_OFF.ConnectToOFF()
    initialization_SQL = connect_to_mysql.MySQLQueries()
    categories_list = initialization.import_static_data()
    for category in categories_list:
        initialization_SQL.upload_product(
            cq.query_upload_new_category, category)
