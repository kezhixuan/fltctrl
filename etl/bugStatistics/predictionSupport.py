import seaborn as sn
import matplotlib.pyplot as plt
import sys
import pandas as pd
from database.common.connect import connectDB
from sqlalchemy import create_engine, text, MetaData, schema, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from mlxtend.plotting import scatterplotmatrix



#conn = connectDB(sys.argv[1], sys.argv[2])


class predictQA(connectDB):
    env=[]
    localTest=[]
    conDB=[]
    

    def __init__(self):
        super().__init__(sys.argv[1], sys.argv[2])
        pass

# Collecting data from the flight control
    def getData(self, sql_string):
        with self.engine.connect() as connection:
            lastCycle = str(pd.read_sql("select max(IDX) from sq.dim_refresh_history",connection).iat[0,0])
            print(lastCycle)
            results = pd.read_sql(sql_string ,connection)
        
        return results

    def getFieldCorrelation(self):
        sql_str = ("select * from sq.etl_bugs_stats")

        bugs_stats = self.getData(sql_str)
        
        print(bugs_stats.head())

        cols = ['sevScore','severity_val', 'releaseP_val']
        scatterplotmatrix(bugs_stats[cols].values, figsize=(10,8), names=cols, alpha=0.5)
        plt.tight_layout()
        plt.show()

        



if __name__ == '__main__':
    reg = predictQA()
    reg.getFieldCorrelation()
        