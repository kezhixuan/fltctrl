from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import sys
import json
import pandas as pd
import codecs 
from sqlalchemy import URL


class connectDB():

    def __init__(self, env, localTest):
        env = env
        localTest = localTest

        # Configure Database connnection
        connData = pd.read_json(codecs.open(env+".json",'r','utf-8'))

        connect2 = connData[localTest]
        self.jiraCon = connData[self.jiraService]

        print(connect2.head())
        self.url_object = URL.create(
                    "mssql+pyodbc",
                    username=connect2["username"],
                    password=connect2["password"],  # plain (unescaped) text
                    host=connect2["host"],
                    database=connect2["database"],
                    query={
                        "driver": "ODBC Driver 17 for SQL Server"
                    }
            )
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        self.engine = create_engine(self.url_object)

        self.connection = self.engine.connect()
        #    result = connection.execute(text('select GETDATE()'))
        #    print(result.all())
        
        pass

    def getEngine(self):
        return str(self.engine)