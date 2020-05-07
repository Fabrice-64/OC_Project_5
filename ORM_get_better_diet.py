"""
    This module manages the connection with the local DB

    """

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, DateTime, String, Index, \
                    ForeignKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector

class Connection:
    def __init__(self):
        self.engine = create_engine("mysql+mysqlconnector://root:@localhost/get_better_diet3",
        echo = True, encoding = 'utf-8')
        res = self.engine.connect()
        res = self.engine.execute("SHOW TABLES")
        for re in res:
            print(re)

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (Index('idx_category', 'name'),)

    id_category = Column(Integer(), primary_key = True, autoincrement = True,
            nullable = False)
    name = Column(String(45), nullable = False)


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
    name = Column(String(60), nullable = False)
       

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


try : 
    print("Tentative de connexion")
    cnx = Connection() 
except Exception:
        print("la DB doit être créée")
        engine = create_engine("mysql+mysqlconnector://root:@localhost",
        echo = True, encoding = 'utf-8')
        connection = engine.connect()
        connection.execute("COMMIT")
        connection.execute("CREATE DATABASE get_better_diet3")
        connection.close()
        cnx = Connection()
        Base.metadata.create_all(cnx.engine)
