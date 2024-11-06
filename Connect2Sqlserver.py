import pandas as pd
import codecs
import pyodbc
import atlassian.ConnectAtlassian as ca
#import ownDev.defect_regression as dr
import atlassian.issuesReleases as ir
import atlassian.utils.loadConfig as conf
from database.common.connect import connectDB
from ownDev.Issues import Issues
from sqlalchemy import MetaData, Table, ForeignKeyConstraint, create_engine, URL, text
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, mapper
from sqlalchemy.schema import DropConstraint
from datetime import datetime
import sys
import json


class Connect2Sqlserver(connectDB):
    env=[]
    localTest=[]
    prefix="dim_"
    refresh_IDX=""
    connect2=[]
    jiraService=[]


    def __init__(self):
        self.env = sys.argv[1]
        self.localTest = sys.argv[2]
        self.jiraService = sys.argv[3]
        self.prefix = "dim_ji_"

        # Configure Database connnection

        
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        super().__init__(sys.argv[1], sys.argv[2])

        connData = pd.read_json(codecs.open(self.env+".json",'r','utf-8'))

        self.jiraCon = connData[self.jiraService]

        # get and set history index
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("select max([IDX]) as refreshIDX from sq.dim_refresh_history"))
                for row in result:
                    self.refresh_IDX = int(row.refreshIDX)+1
            except:
                self.refresh_IDX = 1

        datedata = {"IDX": self.refresh_IDX, "RefreshDate": datetime.today()}
        dateDF = pd.DataFrame([datedata])
        with self.engine.begin() as conn:
            # update refresh cylce history
            # enabl e inserting values into IDENTITY column
            conn.exec_driver_sql(f"SET IDENTITY_INSERT sq.dim_refresh_history ON")
            dateDF.to_sql("dim_refresh_history", conn,schema='SQ', chunksize=2000, index=False, if_exists='append')
            conn.commit()

        dfConfig = conf.loadConfig().readConfig()
        dfConfig["Refresh_Cycle"] = int(self.refresh_IDX)
        with self.engine.begin() as conn:
        #   conn.exec_driver_sql(f"delete from sq.dim_sq_config")
            dfConfig['project_RC'] = dfConfig['jira_project'] + str(self.refresh_IDX)
            dfConfig.to_sql('dim_sq_config', con=self.engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
        conn.commit()

    def getJiraReleases(self):
        pass
    # get the Jira releases
        isr = ir.issuesReleases(self.jiraCon, self.jiraService )
        dfReleases = isr.get_releases()
        dfReleases["Refresh_Cycle"] = int(self.refresh_IDX)
        dfReleases['project_RC'] = dfReleases['project'] + str(self.refresh_IDX)
        dfReleases.to_sql(self.prefix+'releases', con=self.engine,schema='SQ', chunksize=2000, index=False, if_exists='append')

        
    def getJiraIssues(self):
    # get the jira issues
        testproj =""
        jiraIssues = ca.ConnectAtlassian(self.jiraCon, self.jiraService)
        dfIssues=jiraIssues.GetIssues(testproj,self.jiraService, self.engine, self.refresh_IDX)
        dfIssues["Refresh_Cycle"] = int(self.refresh_IDX)
    
loadJiraData = Connect2Sqlserver()
loadJiraData.getJiraReleases()
loadJiraData.getJiraIssues()
