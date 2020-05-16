"""

    This module interacts with the local DB, which is a mySQL DB.
    It is based on SQLAlchemy ORM.
    For the relation with the controller, dedicated classes are available.

    Classes:

    Base: parent class for all the classes to be converted into tables

    ORMConnection: manage the querying methods under a same umbrella.

    Category: inherits from Base, in order to connect with the local DB.
    It manages the categories uploaded from Open Food Facts.
    Can be looked at as a parent table towards CategoryProduct.

    Product: Inherits from Base, in order to connect with the local DB.
    It manages the Products uploaded from Open Food Facts.
    To be looked at as a parent table towards StoreProduct, CategoryProduct
    and ProductComparrison.

    Store: Inherits from Base, in order to connect with the local DB.
    It manages the stores uploaded from Open Food Facts.
    Can be looked at as a parent table towards StoreProduct.

    CategoryProduct:  Inherits from Base, in order to connect with the local DB.
    As a join table, is a child of Category and Product tables.Each product may 
    have several entries, as they are often listed in many categories.

    StoreProduct:  Inherits from Base, in order to connect with the local DB.
    As a join table, is a child of Store and Product tables. Each product is sold 
    in different stores, therefore this join table.

    ProductComparrison:  Inherits from Base, in order to connect with the local DB.
    As a join table, is a child of product table. 
    To be noticed: this table refers twice to product table: once as for 
    the best_product, the other for the reference product, named ref_prod.

    CategoryController: Manage the connection with the Controller for the categories. 
    Each and every category to be displayed is instantiated through this very class.

    ProductController: Manage the connection with the Controller for the products. 
    Each and every product to be displayed is instantiated through this very class.

    StoreController: Manage the connection with the Controller. 
    Each and every store to be displayed is instantiated through this very class.

    Date: Manage the connection with the Controller. Each and every date to be
    displayed is converted in a more readable format and instantiated 
    through this very class.

    Exceptions:

    NIL.

    Functions:

    query_settings(answer): insert a % before and after each word of selected fields \
        in order to broaden the search.

    """
import mysql.connector
from datetime import datetime

from sqlalchemy import Table, Column, Integer, DateTime, String, Index, \
    ForeignKeyConstraint, ForeignKey, select, and_, func, asc, desc, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased


import AppView
import AppController.config as cfg

DB_PARAMETERS = "AppModel/local_DB/db_parameters.py"

Base = declarative_base()


class Category(Base):
    """

        Inherits from Base, in order to connect with the local DB.
        It manages the categories uploaded from Open Food Facts.
        Can be looked at as a parent table towards CategoryProduct.

        Methods:

        NIL

        Arguments:
        id_category: id determined by the local DB. Is the primary key.
        name: self explanatory.

        """
    __tablename__ = 'category'
    __table_args__ = (Index('idx_category', 'name'),)

    id_category = Column(Integer(), primary_key=True, autoincrement=True,
                         nullable=False)
    name = Column(String(600), nullable=False)


class Product (Base):
    """

        Inherits from Base, in order to connect with the local DB.
        It manages the Products uploaded from Open Food Facts.
        To be looked at as a parent table towards StoreProduct, CategoryProduct
        and ProductComparrison.

        Methods:

        NIL

        Arguments:

        code: used in Open Food Facts as the unique identifier for products.
        Therefore, used in this DB as the id and primary key for this table.

        brand: self explanatory.

        name: self explanatory.

        nutrition_grade: is a letter and currently based on the French so called
        "Nutriscore", which is a letter between "a" and "e".

        """
    __tablename__ = 'product'

    code = Column(String(13), nullable=False, primary_key=True)
    brand = Column(String(200), nullable=False)
    name = Column(String(600), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)


class Store (Base):
    """

        Inherits from Base, in order to connect with the local DB.
        It manages the stores uploaded from Open Food Facts.
        Can be looked at as a parent table towards StoreProduct.

        Methods:

        NIL

        Arguments:

        id_store: id determined by the local DB. Is the primary key.

        name: self explanatory.

        An index is defined for more efficiency when looking for a store.
        """
    __tablename__ = 'store'
    __table_args__ = (Index('idx_store', 'name'),)

    id_store = Column(Integer(), nullable=False, primary_key=True,
                      autoincrement=True)
    name = Column(String(600), nullable=False)


class CategoryProduct (Base):
    """

        Inherits from Base, in order to connect with the local DB.
        As a join table, is a child of Category and Product tables.
        Each product may have several entries, as they are often listed in many
        categories.

        Methods:

        NIL

        Arguments:

        id_cat_prod: id determined by the local DB. Is the primary key.

        idcategory: take over the id of each category to join with table category.

        code: take over the product code in order to join with table product.
        """
    __tablename__ = 'category_product'

    id_cat_prod = Column(Integer(), primary_key=True, autoincrement=True,
                         nullable=False)
    idcategory = Column(Integer(),
                        ForeignKey('category.id_category',
                                   name='FK_id_category'), nullable=False)
    code = Column(String(13),
                  ForeignKey('product.code', name='FK_product_category',
                             ondelete='CASCADE', onupdate='CASCADE'),
                  nullable=False, )


class StoreProduct (Base):
    """

        Inherits from Base, in order to connect with the local DB.
        As a join table, is a child of Store and Product tables.
        Each product is sold in different stores, therefore this join table.

        Methods:

        NIL

        Arguments:

        id_store_product: id determined by the local DB. Is the primary key.

        product_code: take over the id of each product to join with table product.

        store_id: take over the store id in order to join with table store.
        """
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
    """
        Inherits from Base, in order to connect with the local DB.
        As a join table, is a child of product table. 
        To be noticed: this table refers twice to product table: once as for 
        the best_product, the other for the reference product, named ref_prod.

        Methods:

        NIL

        Arguments:

        id_prod_comp: id determined by the local DB. Is the primary key.

        code_best_prod: take over the id of each product to join with table product.

        code_ref_prod: take over the product code in order to join with table product.

        date_best: date and time where the best product has been selectd.

        """

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


class CategoryController:
    """

        Manage the connection with the Controller for the categories. 
        Each and every category to be
        displayed is instantiated through this very class.

        Methods:

        NIL

        Arguments:

        name: category name.

        number_items: total of product items attached to this category.
        """

    def __init__(self, category, number_items):
        self.name = category.name
        self.number_items = number_items


class ProductController:
    """

        Manage the connection with the Controller for the products. 
        Each and every product to be displayed is instantiated through this very class.

        Methods:

        NIL

        Arguments:

        name: product name.

        brand : product brand.

        nutrition_grade: french nutriscore.

        code: product id.

        stores: default value 0, in order to intantiate the stores in a list as 
        they are fetched as a tuple.
        """

    def __init__(self, selected_product, stores=0):
        self.name = selected_product.name
        self.brand = selected_product.brand
        self.nutrition_grade = selected_product.nutrition_grade
        self.code = selected_product.code
        if stores != 0:
            self.stores = [store.name for store in stores]


class StoreController:
    """
        Manage the connection with the Controller. Each and every store to be
        displayed is instantiated through this very class.

        Methods:

        NIL

        Arguments:

        name: store name. Currently, each field may contain several stores.

        """

    def __init__(self, name):
        self.name = name


class Date:
    """
        Manage the connection with the Controller. Each and every date to be
        displayed is converted in a more readable format and instantiated 
        through this very class.

        Methods:

        NIL

        Arguments:

        date: self explanatory.

        """

    def __init__(self, date):
        self.date = "{: %d %B %y %H:%M}".format(date)


class ORMConnection:
    """

        Organized around an initialization of the connection to the DB
        at the instanciation, followed by different queries to be used
        as the program unfolds.

        Methods:

        __init__: At the instantiation of the class, create and check the connection 
        parameters, if the DB is not found, an exception is raised and the DB
        is automatically created.

        creat_database: create a local DB to operate the application. Activated 
        solely at the first use.

        upload_categories: when creating a new DB, uploads the categories 
        downloaded from OFF to start working with the DB.

        upload_stores: hen creating a new DB, uploads the stores dowloaded
        from OFF in order to start working with the DB.

        display_categories: get a bunch of the most popular categories in the local DB.

        upload_products: upload a list of products from Open Food Facts 
        into the local DB. Duplicates are rejected, Stores and Categories 
        to which they are related are prepared for the join tables,
        children of product.

        get_categories: fetch the most popular categories from the local DB.

        refer_products: Get a list of products selected iaw with a series 
        of criterion set by the user during the initial search.

        top_products: Fetch a selection of products matching the requirements 
        input by the user, based on a reference product (used as a consequence of the
        choice done in the refer_products method)

        find_stores: Get the stores where a specific product is sold. 

        record_comparred_products: 

        close_connection: close the connection to mySQL via the ORM,
        iot to avoid free access.

        query_settings: Prepare the search criterion before looking 
        into the local DB, as "like" for the beginning and the end of each word 
        in a string.

        record_comparred_products: Record in the local DB the result of 
        a product comparrison, that is both products, a reference one 
        and the best one,including the date of the comparrison.

        get_comparred_products: Get out of the join table ProductComparrison 
        the last records of comparrisons. It joins twice with the table Product, 
        once to get the best product, one to get the reference one.
        It fetches as well the stores in which the best product is for sale.

        total_items: Gets the total number of food items from a product
        and convert it from a tuple into a variable for further processing.

        upload_many: Upload a mass of rows to the local DB in one pass.

        add_one_item: Add one row at a time to the local DB.

        get_category_id: Get the category id number based on the category name. 
        This id number is the primary key of the category table.
        Used to populate the join tables.

        get_store_id: Get the store id number based on the store name. 
        This id number is the primary key of the store table.
        Used to populate the join tables.

        check_duplicate: Check before insertion whether the product is already
        in the local DB. 
        Avoid an Exception : Integrity Error when uploading a dataset.

        open_session:  Opens a session, iot to connect with the local DB. 
        Uses the engine instantiated at the beginning.

        close_session: Used to close the session with the local DB 
        when the user quits.

        query_settings: Prepare the search criterion before looking 
        into the local DB, adding '%' for the beginning and the end of 
        each word in a string.

        Instance variables:

        engine: establish the connection to the local mySQL DB. It uses the DB
        connection parameters set by default or intentionnally by the user.

        """

    def __init__(self):
        """
            At the instantiation of the class, create and check the connection 
            parameters, if the DB is not found, an exception is raised and the DB
            is automatically created.

            Arguments:
            
            NIL

            Returns:

            NIL

            """
        with open(DB_PARAMETERS) as file:
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
        with open(DB_PARAMETERS) as file:
            connection_parameters = file.read()
        self.engine = create_engine(connection_parameters,
                                    echo=False)
        # Activate the Database to subsequently create the tables
        connection = self.engine.connect()
        connection.execute("COMMIT")
        connection.execute(
            "CREATE DATABASE get_better_diet CHARACTER SET utf8mb4")
        connection.close()
        # Add the name of the database to the parameters file for further use
        connection_parameters = connection_parameters + cfg.DB_NAME
        with open(DB_PARAMETERS, "w") as file:
            file.write(connection_parameters)
        # Add the tables to the new database
        self.engine = create_engine(connection_parameters, echo=False)
        self.engine.connect()

        Base.metadata.create_all(self.engine)

    def upload_categories(self, categories):
        """

            When creating a new DB, uploads the categories downloaded from OFF
            to start working with the DB.

            Arguments:

            categories: is a tuple containing all the categories for a product.
            list of categories downloaded from Open Food Facts.

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

            When creating a new DB, uploads a list of stores from OFF 
            to convert them into a list in order to start working with the DB.

            Arguments:

            stores: is a tuple containing all the stores downloaded from OFF. 

            Returns:

            NIL

            """
        obj_store = []
        for store in stores:
            store = Store(name=store)
            obj_store.append(store)
        self.upload_many(obj_store)

    def display_categories(self):
        """
            Get a bunch of the most popular categories in the local DB.

            Arguments:

            NIL

            Returns:

            selected_categories: for each category, a tuple with its name.

            """
        selected_categories = self.session.query(Category).\
            order_by(Category.id_category)[:30]
        return selected_categories

    def upload_products(self, products):
        """
            Upload a list of products from Open Food Facts into the local DB.
            Duplicates are rejected, Stores and Categories to which they are
            related are prepared for the join tables, children of product.

            Arguments:

            products: contains all the features needed for each product, including
            attached stores and categories.

            Return:

            NIL
            """
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
        """

            Fetch the most popular categories from the local DB.

            Arguments:

            NIL
            
            Returns:

            List of selected categories, indexed by popularity.

        """

        list_top_categories = []
        query = self.session.query(
            Category, func.count(CategoryProduct.idcategory))
        result = query.join(CategoryProduct).group_by(CategoryProduct.idcategory).\
            order_by(desc(func.count(CategoryProduct.idcategory)))[:20]
        # Instantiate each result of the query
        for category in result:
            top_category = CategoryController(category[0], category[1])
            list_top_categories.append(top_category)
        return list_top_categories

    def refer_products(self, item_search):
        """

            Get a list of products selected iaw with a series of criterion set 
            by the user during the initial search.

            Arguments:

            item_search: tuple containing the criterion set by the user, currently
            the category, name (like) and brand (like).

            Returns:

            list_refer_products: list of objects encompassing the product features.
        """
        # Select a list of N products matching the requirement set by the user
        list_refer_products = []
        product_category = item_search[0]
        product_name = self.query_settings(item_search[1])
        brand_name = self.query_settings(item_search[2])
        query = self.session.query(
            Product.name, Product.brand, Product.nutrition_grade, Product.code)
        query = query.join(CategoryProduct).join(Category)
        result = query.filter(and_(Category.name == product_category,
                                   Product.name.ilike(product_name), 
                                   Product.brand.ilike(brand_name)))[:10]
        # Instanciate the fetched products.
        for product in result:
            refer_product = ProductController(product)
            list_refer_products.append(refer_product)
        return list_refer_products

    def top_products(self, item_search):
        """
            Fetch a selection of products matching the requirements input by the 
            user, based on a reference product (used as a consequence of the
            choice done in the refer_products method)

            Arguments:
            item_search: as a tuple, includes the selection criterion, like the
            category, product name and the nutrition grade of the reference
            product.

            Returns:
            list_top_products : a list of ten products matching the requirements.
            It fetches all the fields of a product (name, brand, nutriscore
            and code as well).
            """
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
        query = query.filter(p.nutrition_grade <=
                             self.session.query(p.nutrition_grade).
                             filter(p.code == item_search[2]))[:10]

        for product in query:
            stores = self.find_stores(product.code)
            product = ProductController(product, stores)
            list_top_products.append(product)
        return list_top_products

    def find_stores(self, product_code):
        """

            Get the stores where a specific product is sold. 

            Arguments:
            
            product_code : the product code is the link between the Product and 
            the store via the join table StoreProduct.

            Returns:

            stores_list: list of stores to be displayed for each product.

            """
        stores_list = []

        query = self.session.query(Store.name)
        query = query.join(StoreProduct)
        result = query.filter(StoreProduct.product_code == product_code)
        for store in result:
            store = StoreController(store[0])
            stores_list.append(store)
        return stores_list

    def record_comparred_products(self, comparrison):
        """
            Record the result of a product comparrison, that is both products,
            a reference one and the best one, including the date of the comparrison.

            Arguments:

            comparrison: contains the both product codes, date and time of the 
            selection.

            Returns:

            NIL
            """
        compared_prod = ProductComparrison(code_best_prod=comparrison[0],
                                           date_best=comparrison[1], code_ref_prod=comparrison[2])
        self.add_one_item(compared_prod)

    def get_compared_products(self):
        """
            Get out of the join table ProductComparrison the last records of
            comparrisons. It joins twice with the table Product, once to get the best product, 
            one to get the reference one. It fetches as well the stores in which
            the best product is for sale.

            Arguments:

            NIL

            Returns:

            List of the best products. Each item is a tuple.

            """
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
            best_product = ProductController(item[0], stores)
            date = Date(item[1])
            ref_product = ProductController(item[2])
            compared_product = best_product, date, ref_product
            list_compared_products.append(compared_product)
        return list_compared_products

    def total_items(self):
        """
            Gets the total number of food items from a product and convert it 
            from a tuple into a variable for further processing.

            Arguments:

            NIL

            Returns:

            nb_rows: variable, ie the result of the query.
            """
        result = self.session.query(func.count(Product.code))
        for nb_rows in result:
            nb_rows = nb_rows[0]
        return nb_rows

    def upload_many(self, many_items):
        """
            Upload a mass of rows to the local DB in one pass.

            Arguments:

            many_items: list of tuples representing the rows to be uploaded.

            Returns:

            NIL

            """
        self.session.bulk_save_objects(many_items)
        self.session.commit()

    def add_one_item(self, one_item):
        """
            Add one row at a time to the local DB.

            Arguments:

            one_item: a row, presented as a tuple.

            Returns:

            NIL
            """
        self.session.add(one_item)
        self.session.commit()

    def open_session(self):
        """
            Opens a session, iot to connect with the local DB. Uses the engine
            instantiated at the beginning.

            Arguments:

            NIL

            Returns:

            NIL

            """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_session(self):
        """

            Used to close the session with the local DB when the user quits.

            Arguments:

            NIL

            Returns:
            
            NIL
        """
        self.session.close()

    def get_category_id(self, category):
        """

            Get the category id number based on the category name. This id number
            is the primary key of the category table.
            Used to populate the join tables.

            Arguments:

            category: name of the category for which the id number is needed.

            Returns:

            category_id: the id of the category for which the id is required.
        """
        category_id = self.session.query(Category.id_category).filter(
            Category.name.ilike(category))
        return category_id

    def get_store_id(self, store):
        """

            Get the store id number based on the store name. This id number
            is the primary key of the store table.
            Used to populate the join tables.

            Arguments:

            store: name of the store for which the id number is needed.

            Returns:

            store_id: the id of the category for which the id is required.

            """
        store_id = self.session.query(
            Store.id_store).filter(Store.name.ilike(store))
        return store_id

    def check_duplicate(self, code):
        """

            Check before insertion whether the product is already in the local DB.
            Avoid an Exception : Integrity Error when uploading a dataset.

            Arguments:

            code: code number of the product to be checked.

            Returns:

            NIL.

            """
        duplicate = self.session.query(self.session.query(Product).
                                       filter_by(code=code).exists()).scalar()
        return duplicate

    def query_settings(self, answer):
        """

            Prepare the search criterion before looking into the local DB, as like
            for the beginning and the end of each word in a string.

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
