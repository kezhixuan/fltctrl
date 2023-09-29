from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import sys
import json
import pandas as pd
import codecs 
from sqlalchemy import URL

env = sys.argv[1]
localTest = sys.argv[2]
prefix = "dim_"

# Configure Database connnection
connData = pd.read_json(codecs.open(env+".json",'r','utf-8'))

connect2 = connData[localTest]

print(connect2.head())
url_object = URL.create(
            "mssql+pyodbc",
            username=connect2["username"]+"@"+connect2["DB.host"],
            password=connect2["password"],  # plain (unescaped) text
            host=connect2["host"],
            database=connect2["database"],
            query={
                "driver": "ODBC Driver 17 for SQL Server"
            }
     )
############## end Database Connection Configuration ##################
# create and establish a database session
engine = create_engine(url_object)

with engine.connect() as connection:
    result = connection.execute(text('select GETDATE()'))
    print(result.all())