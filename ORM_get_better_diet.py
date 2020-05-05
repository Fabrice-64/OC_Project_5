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
        engine = create_engine("mysql+mysqlconnector://root:@localhost/get_better_diet3",
        echo = True, encoding = 'utf-8')
        res = engine.connect()
        res = engine.execute("SHOW TABLES")
        for re in res:
            print(re)

Base = declarative_base()

class Category:
    __tablename__ = 'category'
    __table_args__ = (Index('category_idx', 'name'),)

    idcategory = Column(Integer(6), primary_key = True, autoincrement = True,
            nullable = False)
    name = Column(String(45), nullable = False)
    

class Product:
    __tablename__ = 'product'
    code = Column(String(13), nullable = False, primary_key = True)
    brand = Column(String(200), nullable = False)
    name = Column(String(600), nullable = False)
    nutrition_grade = Column(String(1), nullable = False)


class Store:
    __tablename__ = 'store'

class CategoryProduct:
    __tablename__ = 'category_product'
    id_cat_prod = Column(Integer(6), primary_key = True, autoincrement = True,
        nullable = False)
    idcategory = Column(Integer(6), ForeignKey('category.idcategory'), nullable = False)
    code = Column(String(13), nullable = False)

class StoreProduct:
    __tablename__ = 'store_product'

cnx = Connection()
