import seaborn as sn
import matplotlib.pyplot as plt
import sys
import pandas as pd
from database.common.connect import connectDB
import src.dataSource.atlassian.utils.loadConfig as conf
from sqlalchemy import create_engine, text, MetaData, schema, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from mlxtend.plotting import scatterplotmatrix



#conn = connectDB(sys.argv[1], sys.argv[2])


class predictQA(connectDB):
    env=[]
    localTest=[]
    conDB=[]
    lastCycle = 1
    

    def __init__(self):
        super().__init__(sys.argv[1], sys.argv[2])
        self.lastCycle= self.getLastCycle()

        self.trConfig = conf.loadConfig().readTRConfig()
        self.jiConfig = conf.loadConfig().readConfig()
        self.config = pd.merge(self.trConfig, self.jiConfig, on="jira_id")
        pass

    def getLastCycle(self):
        with self.engine.connect() as connection:
            lastCycle = str(pd.read_sql("select max(IDX) from sq.dim_refresh_history",connection).iat[0,0])
            print(lastCycle)
        return lastCycle

# Collecting data from the flight control
    def getData(self, sql_string):
        with self.engine.connect() as connection:
            
            results = pd.read_sql(sql_string ,connection)
        
        return results
    
    def getTestRailID(self, project):
        print(project)
        testrail_id = self.config[self.config['jira_project'] == project]["testrail_id"].iloc[0]

        if not testrail_id:
            return "1"
        else:
            return testrail_id
            


    def getFieldCorrelation(self):
        sql_str = ("select * from sq.etl_bugs_stats")

        bugs_stats = self.getData(sql_str)
        
        bugs_stats['testrail_id'] = bugs_stats['Project'].apply(lambda x: self.getTestRailID(x))
        
        
        print(bugs_stats.head())

        cols = ['sevScore','severity_val', 'releaseP_val']
        scatterplotmatrix(bugs_stats[cols].values, figsize=(10,8), names=cols, alpha=0.5)
        plt.tight_layout()
        plt.show()

    def getTestRunAggregated(self):
        sql_str = ("select DATEDIFF(day, created_on, updated_on) as duration, passed_count, blocked_count, untested_count, failed_count, retest_count,project_id, created_on, updated_on, is_completed "+
                   " from sq.fact_tr_runs " +
                   " where refresh_cycle = " + self.lastCycle)
        
        etl_latest_runs = self.getData(sql_str)

        print(etl_latest_runs.head())
        



if __name__ == '__main__':
    reg = predictQA()
    reg.getFieldCorrelation()
    reg.getTestRunAggregated()
        