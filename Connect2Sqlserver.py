import pandas as pd
import codecs
import pyodbc
import atlassian.ConnectAtlassian as ca
import ownDev.defect_regression as dr
import atlassian.issuesReleases as ir
import atlassian.utils.loadConfig as conf
from ownDev.Issues import Issues
from sqlalchemy import MetaData, Table, ForeignKeyConstraint, create_engine, URL, text
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, mapper
from sqlalchemy.schema import DropConstraint
from datetime import datetime
import sys
import json


class Connect2Sqlserver(object):
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
        self.connData = pd.read_json(codecs.open(self.env+".json",'r','utf-8'))

        self.connect2 = self.connData[self.localTest]
        self.jiraCon = self.connData[self.jiraService]

        print(self.connect2.head())
        url_object = URL.create(
                    "mssql+pyodbc",
                    username=self.connect2["username"],
                    password=self.connect2["password"],  # plain (unescaped) text
                    host=self.connect2["host"],
                    database=self.connect2["database"],
                    query={
                        "driver": "ODBC Driver 17 for SQL Server"
                    }
            )
        print(url_object)
        
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        self.engine = create_engine(url_object)
        session = Session(self.engine)

        # get and set history index
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("select max([IDX]) as refreshIDX from sq.dim_refresh_history"))
                for row in result:
                    self.refresh_IDX = int(row.refreshIDX)+1
            except:
                self.refresh_IDX = 1

        #deactive Foreign Key Constraints

        #
        # with engine.connect() as conn:
        #    try:
        #        conn.execute(ForeignKeyConstraint(["index"],["SQ.dim_refresh_history.index"], use_alter=True, name="fk_index_refresh_hist").drop())
        #        conn.execute(ForeignKeyConstraint(columns=["index"],refcolumns=["SQ.dim_refresh_history.index"]).drop())
        #    except:
        #        print("No Index dropped!")



        #regression AI

        #dfIssues = dfIssues.reindex(columns=['project','created','severity','priority','issuetype','release phase'])
        #regressAI = dfIssues.reset_index(drop=True, inplace=True)

        # regressAI = pd.MultiIndex(dfIssues)
        #regressAI.query("issuetype == 'Bug' & priority != 'NaN' & severity != 'NaN' & 'release phase' != 'NaN'", inplace=True)



        #defreg = dr.defect_regression()
        #regressAI['severityScore'] = regressAI.apply(defreg.SevMapping, axis=1)
        #regressAI['priorityScore'] = regressAI.apply(defreg.PrioMapping, axis=1)
        #regressAI['sevScore'] = regressAI.apply(defreg.sevScore,axis=1)

        #defreg.calculate_regression(regressAI)


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
