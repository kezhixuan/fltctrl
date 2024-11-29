from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import sys
import json
import pandas as pd
import codecs 
from sqlalchemy import URL
import logging as log

logger = log.getLogger(__name__)
log.basicConfig(filename='SQDashboard.log', encoding='utf-8', level=log.INFO)

class connectDB():
    
    
    def __init__(self, env, localTest):
        env = env
        localTest = localTest

        # Configure Database connnection
        connData = pd.read_json(codecs.open(env+".json",'r','utf-8'))

        connect2 = connData[localTest]

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
        print("Test the Engined file")
        return str(self.engine)
    
    def getLogger(self):
        return log
        
    
    def write2DB(self, engine, data: pd.DataFrame , tableName, prefix):
        log.info('Start writing into table ' + tableName )
        try:
            with engine.begin() as conn:
                data.to_sql(prefix+ tableName, con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
            conn.commit()
            success = True
            log.info('Successfull writen into table ' + tableName + ' and ' + str(data.size) + ' records saved!')
        except Exception as e:
            success = False
            print(e.with_traceback())
            log.critical('Writing into table ' + tableName + ' failed!')
        return success