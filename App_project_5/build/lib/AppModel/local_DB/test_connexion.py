from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
from sqlalchemy.exc import ProgrammingError

mdp = "pouet"
i = 0
while i<= 3:
    i +=1
    print("Tentative de connexion")
    params= "mysql+mysqlconnector://root:{}@localhost".format(mdp)
    engine = create_engine(params, echo = False)
    try:
        connection = engine.connect()
    except Exception:
        print("Exception levée")
        if i == 3:
            mdp = "test"
            print("mdp changé")
res = connection.execute("SELECT 1")
print("test: ", res)


