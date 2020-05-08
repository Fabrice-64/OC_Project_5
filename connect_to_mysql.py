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
import time
import pickle
from sqlalchemy import create_engine
import mysql.connector

import config
import config_queries as cq

from sqlalchemy import Table, Column, Integer, DateTime, String, Index, \
    ForeignKeyConstraint, ForeignKey, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import connect_to_OFF as cof
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (Index('idx_category', 'name'),)

    id_category = Column(Integer(), primary_key = True, autoincrement = True,
            nullable = False)
    name = Column(String(600), nullable = False)

class Product (Base):
    __tablename__ = 'product'

    code = Column(String(13), nullable = False, primary_key = True)
    brand = Column(String(200), nullable = False)
    name = Column(String(600), nullable = False)
    nutrition_grade = Column(String(1), nullable = False)


class Store (Base):
    __tablename__ = 'store'
    __table_args__ = (Index('idx_store', 'name'),)

    id_store = Column(Integer(), nullable = False, primary_key = True, 
        autoincrement = True)
    name = Column(String(600), nullable = False)
       

class CategoryProduct (Base):
    __tablename__ = 'category_product'

    id_cat_prod = Column(Integer(), primary_key = True, autoincrement = True,
        nullable = False)
    idcategory = Column(Integer(), 
        ForeignKey('category.id_category', name = 'FK_id_category'), 
        nullable = False)
    code = Column(String(13), 
        ForeignKey('product.code', name = 'FK_product_category', 
        ondelete = 'CASCADE', onupdate = 'CASCADE'),
        nullable = False, )

    
class StoreProduct (Base):
    __tablename__ = 'store_product'

    id_store_product = Column(Integer(), primary_key = True, autoincrement = True,
        nullable = False)
    product_code = Column(String(13), 
        ForeignKey('product.code', name = 'FK_product_store',
        onupdate = 'CASCADE', ondelete = 'CASCADE'), nullable = False)
    store_id = Column(Integer(), 
        ForeignKey('store.id_store', name = 'FK_store_id', onupdate = 'CASCADE',
            ondelete = 'CASCADE'), nullable = False)

class ProductComparrison (Base):
    __tablename__ = 'product_comparrison'

    id_prod_comp = Column(Integer(), primary_key = True, autoincrement = True,
        nullable = False)
    code_best_prod = Column(String(13), 
        ForeignKey('product.code', name = 'FK_code_product_best',
        onupdate = 'CASCADE', ondelete = 'CASCADE'),nullable = False)
    code_ref_prod = Column(String(13), 
        ForeignKey('product.code', name = 'FK_code_product_ref',
        onupdate = 'CASCADE', ondelete = 'CASCADE'), nullable = False)
    date_best = Column(DateTime(), nullable = False)

class ORMConnection:
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
        with open("db_parameters.txt") as file:
            connection_parameters = file.read()
        self.engine = create_engine(connection_parameters,
        echo = False)
        self.engine.connect()


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
        with open("db_parameters.txt") as file:
            connection_parameters = file.read()
        self.engine = create_engine(connection_parameters,
        echo = False)
        # Activate the Database to subsequently create the tables
        connection = self.engine.connect()
        connection.execute("COMMIT")
        connection.execute("CREATE DATABASE get_better_diet \
                            CHARACTER SET utf8mb4")
        connection.close()
        # Add the name of the database to the parameters file for further use
        connection_parameters = connection_parameters + config.DB_NAME
        with open("db_parameters.txt", "w") as file:
            file.write(connection_parameters) 
        # Add the tables to the new database
        self.engine = create_engine(connection_parameters, echo = False)
        self.engine.connect()
        Base.metadata.create_all(self.engine)

    def upload_categories(self, categories):
        """

            When creating a new DB, uploads a list of categories to start working
            with the DB.

            Arguments:

            query: self explanatory

            categories: list of categories downloaded from Open Food Facts.

            Returns:

            NIL

            """
        obj_category = []
        for category in categories:
            category = Category(name = category)
            obj_category.append(category)
        return obj_category

    def upload_stores(self, stores):
        """

            When creating a new DB, uploads a list of stores to start working
            with the DB.

            Arguments:

            query: self explanatory

            categories: list of french stores downloaded from Open Food Facts.

            Returns:

            List of stores

            """
        obj_store = []
        for store in stores:
            store = Store(name = store)
            obj_store.append(store)
        return obj_store

    def display_categories(self):
        selected_categories = self.session.query(Category).\
            order_by(Category.id_category)[:30]
        return selected_categories
    
    def upload_products(self, products):
        obj_product = []
        obj_stores = []
        obj_category = []
        for product in products:
            product = Product(brand = product[0],
                    name = product[1],
                    code = product[2],
                    nutrition_grade = product[3])
            obj_product.append(product)
            
        return obj_product, 

    def open_session(self):
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
    
    def upload_many(self, many_items):
        self.session.bulk_save_objects(many_items)
        self.session.commit()

    def close_session(self):
        self.session.close()


    def test(self):
        test = self.session.query(Category.id_category).filter(Category.name.ilike("Produits à tartiner sucrés"))
        return test
        


        




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
    # Used to test the interaction with the local DB
    connection = cof.ConnectToOFF()
    #nb_items, nb_rejected, results = connection.import_products_list('Fromages')

    requete = ORMConnection()
    requete.open_session()
    result = requete.test()
    for res in result:
        print(res[0])
    
