import pandas as pd
import codecs
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import URL
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, mapper
from sqlalchemy import text
import json
import sys

# jbruewer@flightcontrol-test.database.windows.net
# pw: TotalS€cureAnd0bscure
# Connect to database: FC_JBR_DEV

#### establish the SSH tunnel to get SQl Server connection ############
'''
ssh  -i ~/.ssh/bastion.pem joerg.bruewer@bastion.toolbox.aws.signintra.com -L 1433:flightcontrol-test.database.windows.net:1433
'''

class myTable(object):
    pass

env = sys.argv[1]
localTest = sys.argv[2]

# Configure Database connnection
connData = pd.read_json(codecs.open(env+".json",'r','utf-8'))

#with open(env+".json", "r",'UTF-8') as f:
#    connectionData = json.load(f)

#    connData = pd.DataFrame.from_dict(connectionData)
#    print(connData.head())

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
#     
# create and establish a database session
# create and establish a database session
# create and establish a database session

print(url_object)
engine = create_engine(url_object)
session = Session(engine)

# get and set history index
conn= engine.connect()
try:
    result = conn.execute(text("select * from sysobjects where xtype = 'U';"))
    for row in result:
            refresh_IDX = row
            print(refresh_IDX)
except:
    print("No value found") 
