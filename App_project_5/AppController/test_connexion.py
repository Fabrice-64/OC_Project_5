from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector

engine = create_engine("mysql+mysqlconnector://root:test@localhost", echo = True)

connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
res = connection.execute("SHOW DATABASES")
print(res)
for re in res:
    print(re)
