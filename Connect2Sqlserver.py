import pandas as pd
import codecs
import src.dataSource.atlassian.ConnectAtlassian as ca
#import ownDev.defect_regression as dr
import src.dataSource.atlassian.issuesReleases as ir
import src.dataSource.atlassian.utils.loadConfig as conf
from src.dataSource.testrail import ConnectTestRail as testr
from database.common.connect import connectDB

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
        self.testRail = "testrail"
        self.prefix = "dim_ji_"
        self.trConfig = conf.loadConfig().readTRConfig()
        self.jiConfig = conf.loadConfig().readConfig()
        self.config = pd.merge(self.trConfig, self.jiConfig, on="jira_id")
        self.config = self.config.reset_index()
        self.upDate = False

        # Configure Database connnection
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        super().__init__(sys.argv[1], sys.argv[2])

        connData = pd.read_json(codecs.open(self.env+".json",'r','utf-8'))

        self.jiraCon = connData[self.jiraService]
        self.testrailCon = connData[self.testRail]

        ofile = open('refreshIDX.txt')
        IDX = ofile.readline()
        self.refresh_IDX = str(IDX)



    def getJiraReleases(self):
#    # get the Jira releases
        isr = ir.issuesReleases(self.jiraCon, self.jiraService )
        dfReleases = isr.get_releases()
        dfReleases["Refresh_Cycle"] = int(self.refresh_IDX)
        dfReleases['project_RC'] = dfReleases['project'] + str(self.refresh_IDX)
        dfReleases.to_sql(self.prefix+'releases', con=self.engine,schema='SQ', chunksize=2000, index=False, if_exists='append')
        #self.closeRun("Releases")
        
    def getJiraIssues(self):
#    # get the jira issues
        testproj =""
        jiraIssues = ca.ConnectAtlassian(self.jiraCon, self.jiraService)
        dfIssues=jiraIssues.GetIssues(testproj,self.jiraService, self.engine, self.refresh_IDX)
        dfIssues["Refresh_Cycle"] = int(self.refresh_IDX)
        #self.closeRun("Issues")
    
    def getTestRailData(self):
        project_id=""
        
        testR = testr.ConnectTestRail(self.testrailCon)
        testR.load_data(project_id, self.testRail, self.engine, self.refresh_IDX, self.config)
        #self.closeRun("TestRail")


    def closeRun(self, state):
        with self.engine.connect() as conn:
            try:
                #result = conn.execute(text("update sq.dim_refresh_history rh set SysJi1 = 'TSC1' where day(rh.RefreshDate) = day(getdate())"))
                if state == "Issues":
                    sql = "update sq.dim_refresh_history rh set SysJi1 = 'TSC1' where rh.IDX = %s"
                elif state == "Releases":
                    sql = "update sq.dim_refresh_history rh set SysJi2 = 'TSC1' where rh.IDX = %s"
                elif state == "TestRail":
                    sql = "update sq.dim_refresh_history rh set SysTr1 = 'TSC1' where rh.IDX = %s"
                else:
                    pass
                result = conn.execute(sql, self.refresh_IDX)
            except:
                print("jobs not closed: " + state)

    
loadJiraData = Connect2Sqlserver()
loadJiraData.getTestRailData()
loadJiraData.getJiraReleases()
loadJiraData.getJiraIssues()
