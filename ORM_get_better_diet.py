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
        engine = create_engine("mysql+mysqlconnector://root:@localhost/get_better_diet2",
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

class CategoryProduct:
    __tablename__ = 'category_product'
    __table_args__ = ()



cnx = Connection()
