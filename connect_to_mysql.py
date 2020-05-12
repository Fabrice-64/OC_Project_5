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
from datetime import datetime
import config
import config_queries as cq

from sqlalchemy import Table, Column, Integer, DateTime, String, Index, \
    ForeignKeyConstraint, ForeignKey, select, and_, func, asc, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased
import connect_to_OFF as cof
Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (Index('idx_category', 'name'),)

    id_category = Column(Integer(), primary_key=True, autoincrement=True,
                         nullable=False)
    name = Column(String(600), nullable=False)


class Product (Base):
    __tablename__ = 'product'

    code = Column(String(13), nullable=False, primary_key=True)
    brand = Column(String(200), nullable=False)
    name = Column(String(600), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)


class Store (Base):
    __tablename__ = 'store'
    __table_args__ = (Index('idx_store', 'name'),)

    id_store = Column(Integer(), nullable=False, primary_key=True,
                      autoincrement=True)
    name = Column(String(600), nullable=False)


class CategoryProduct (Base):
    __tablename__ = 'category_product'

    id_cat_prod = Column(Integer(), primary_key=True, autoincrement=True,
                         nullable=False)
    idcategory = Column(Integer(),
                        ForeignKey('category.id_category',
                                   name='FK_id_category'),
                        nullable=False)
    code = Column(String(13),
                  ForeignKey('product.code', name='FK_product_category',
                             ondelete='CASCADE', onupdate='CASCADE'),
                  nullable=False, )


class StoreProduct (Base):
    __tablename__ = 'store_product'

    id_store_product = Column(Integer(), primary_key=True, autoincrement=True,
                              nullable=False)
    product_code = Column(String(13),
                          ForeignKey('product.code', name='FK_product_store',
                                     onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    store_id = Column(Integer(),
                      ForeignKey('store.id_store', name='FK_store_id', onupdate='CASCADE',
                                 ondelete='CASCADE'), nullable=False)


class ProductComparrison (Base):
    __tablename__ = 'product_comparrison'

    id_prod_comp = Column(Integer(), primary_key=True, autoincrement=True,
                          nullable=False)
    code_best_prod = Column(String(13),
                            ForeignKey('product.code', name='FK_code_product_best',
                                       onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    code_ref_prod = Column(String(13),
                           ForeignKey('product.code', name='FK_code_product_ref',
                                      onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    date_best = Column(DateTime(), nullable=False)


class TopCategory:

    def __init__(self, category, number_items):
        self.name = category.name
        self.number_items = number_items


class SelectedProduct:

    def __init__(self, selected_product, stores=0):
        self.name = selected_product.name
        self.brand = selected_product.brand
        self.nutrition_grade = selected_product.nutrition_grade
        self.code = selected_product.code
        if stores != 0:
            self.stores = [store.name for store in stores]


class SelectedStore:
    def __init__(self, name):
        self.name = name


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
                                    echo=False)
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
                                    echo=False)
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
        self.engine = create_engine(connection_parameters, echo=False)
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
            category = Category(name=category)
            obj_category.append(category)
        self.upload_many(obj_category)

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
            store = Store(name=store)
            obj_store.append(store)
        self.upload_many(obj_store)

    def display_categories(self):
        selected_categories = self.session.query(Category).\
            order_by(Category.id_category)[:30]
        return selected_categories

    def upload_products(self, products):
        obj_product = []
        obj_stores_product = []
        obj_category_product = []
        # Create a list including product characteristics for table product
        for item in products:
            if self.check_duplicate(item[2]) is False:
                product = Product(brand=item[0],
                                  name=item[1],
                                  code=item[2],
                                  nutrition_grade=item[3])
                obj_product.append(product)
                # Get for each product the list of stores it is sold in
                store_list = item[4].split(",")
                # Bind each store name with its id
                for store in store_list:
                    store_id = self.get_store_id(store)
                    # Instantiate product_code and store_id  for join table
                    for store in store_id:
                        store_product = StoreProduct(product_code=product.code,
                                                     store_id=store[0])
                        # Add the instance to the list of all duets  store - product
                        obj_stores_product.append(store_product)
                # Get for each product the list of categories it belongs to
                category_list = item[5].split(",")
                # Bind each category name of the product with its category_id
                for category in category_list:
                    category_id = self.get_category_id(category)
                    # Instantiate category id and product code for join table.
                    for category in category_id:
                        category_product = CategoryProduct(idcategory=category[0],
                                                           code=product.code)
                        obj_category_product.append(category_product)
        # Upload first in the table product and then in join tables.
        self.upload_many(obj_product)
        self.upload_many(obj_stores_product)
        self.upload_many(obj_category_product)

    def get_categories(self):
        list_top_categories = []
        query = self.session.query(
            Category, func.count(CategoryProduct.idcategory))
        result = query.join(CategoryProduct).group_by(CategoryProduct.idcategory).\
            order_by(desc(func.count(CategoryProduct.idcategory)))[:20]
        # Instantiate each result of the query
        for category in result:
            top_category = TopCategory(category[0], category[1])
            list_top_categories.append(top_category)
        return list_top_categories

    def refer_products(self, item_search):
        # Select a list of N products matching the requirement set by the user
        list_refer_products = []
        product_category = item_search[0]
        product_name = self.query_settings(item_search[1])
        brand_name = self.query_settings(item_search[2])
        query = self.session.query(
            Product.name, Product.brand, Product.nutrition_grade, Product.code)
        query = query.join(CategoryProduct).join(Category)
        result = query.filter(and_(Category.name == product_category,
                                   Product.name.ilike(product_name), Product.brand.ilike(brand_name)))[:10]

        for product in result:
            refer_product = SelectedProduct(product)
            list_refer_products.append(refer_product)
        return list_refer_products

    def top_products(self, item_search):
        list_top_products = []
        c_p = aliased(CategoryProduct)
        c = aliased(Category)
        p = aliased(Product)
        product_name = self.query_settings(item_search[1])
        query = self.session.query(p)
        query = query.join(c_p, c_p.code == p.code)
        query = query.join(c, c.id_category == c_p.idcategory)
        query = query.filter(
            and_(c.name == item_search[0], p.name.ilike(product_name)))
        query = query.filter(p.nutrition_grade <
                             self.session.query(p.nutrition_grade).
                             filter(p.code == item_search[2]))[:10]

        for product in query:
            stores = self.find_stores(product.code)
            product = SelectedProduct(product, stores)
            list_top_products.append(product)
        return list_top_products

    def find_stores(self, product_code):
        stores_list = []

        query = self.session.query(Store.name)
        query = query.join(StoreProduct)
        result = query.filter(StoreProduct.product_code == product_code)
        for store in result:
            store = SelectedStore(store[0])
            stores_list.append(store)
        return stores_list

    def record_comparred_products(self, comparrison):
        compared_prod = ProductComparrison(code_best_prod=comparrison[0],
                                           date_best=comparrison[1], code_ref_prod=comparrison[2])
        self.add_one_item(compared_prod)

    def get_compared_products(self):
        list_compared_products = []
        best_p = aliased(Product)
        ref_p = aliased(Product)
        p_c = aliased(ProductComparrison)
        query = self.session.query(best_p, p_c.date_best, ref_p)
        query = query.join(best_p, best_p.code == p_c.code_best_prod)
        query = query.join(ref_p, ref_p.code == p_c.code_ref_prod)
        result = query.order_by(desc(p_c.date_best))[:5]
        for item in result:
            stores = self.find_stores(item[0].code)
            best_product = SelectedProduct(item[0], stores)
            date = self.best_date(item[1])
            ref_product = SelectedProduct(item[2])
            compared_product = best_product, date, ref_product
            list_compared_products.append(compared_product)
        return list_compared_products

    def total_items(self):
        result = self.session.query(func.count(Product.code))
        for nb_rows in result:
            nb_rows = nb_rows[0]
        return nb_rows

    def best_date(self, date):
        self.date = "{: %d %B %y %H:%M}".format(date)
        return self.date

    def open_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def upload_many(self, many_items):
        self.session.bulk_save_objects(many_items)
        self.session.commit()

    def close_session(self):
        self.session.close()

    def add_one_item(self, one_item):
        self.session.add(one_item)
        self.session.commit()

    def get_category_id(self, category):
        category_id = self.session.query(Category.id_category).filter(
            Category.name.ilike(category))
        return category_id

    def get_store_id(self, store):
        store_id = self.session.query(
            Store.id_store).filter(Store.name.ilike(store))
        return store_id

    def check_duplicate(self, code):
        duplicate = self.session.query(self.session.query(Product).
                                       filter_by(code=code).exists()).scalar()
        return duplicate

    def query_settings(self, answer):
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
    #connection = cof.ConnectToOFF()
    #nb_items, nb_rejected, results = connection.import_products_list('Fromages')

    requete = ORMConnection()
    requete.open_session()
    item_search = ["Desserts", "Chocolat", "3270160587551"]
    result = requete.get_compared_products()
    for res in result:
        print(res)
