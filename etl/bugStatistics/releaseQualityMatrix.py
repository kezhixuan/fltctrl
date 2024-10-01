import sys
import pandas as pd
from database.common.connect import connectDB
from sqlalchemy import create_engine, text


conn = connectDB(sys.argv[1], sys.argv[2])


class loadIssuse4Release(connectDB):
    env=[]
    localTest=[]
    conDB=[]
    

    def __init__(self):
        super().__init__(sys.argv[1], sys.argv[2])
        pass

    def getAllBug(self):
        with self.engine.connect() as connection:
            allBugs = pd.read_sql("select * from sq.fact_ji_issues where project='SLS Agile' and Refresh_Cycle=22",connection)

            print(allBugs)
            


xx = loadIssuse4Release()
xx.getAllBug()