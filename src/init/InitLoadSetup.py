import pandas as pd
import codecs
import src.dataSource.atlassian.ConnectAtlassian as ca

# import ownDev.defect_regression as dr
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


class InitLoadSetup(connectDB):
    env = []
    localTest = []
    prefix = "dim_"
    refresh_IDX = ""
    connect2 = []
    jiraService = []

    def __init__(self):
        self.env = sys.argv[1]
        self.localTest = sys.argv[2]
        self.jiraService = "jira_tsc"
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

        connData = pd.read_json(codecs.open(self.env + ".json", "r", "utf-8"))

        if self.jiraService == "jira_tsc1":
            self.jiraService = "jira_tsc"

        self.jiraCon = connData[self.jiraService]
        self.testrailCon = connData[self.testRail]

    def initFlag(self):

        self.refresh_IDX = 1
        # get and set history index
        with self.engine.connect() as conn:
            try:
                # check if on current day a refresh process has already be started.
                reidx = conn.execute(
                    text("select max([IDX]) as refreshIDX from sq.dim_refresh_history")
                )
                for idx in reidx:
                    self.refresh_IDX = int(idx.refreshIDX) + 1
            except:
                # The database is emply, this is the first run.
                self.refresh_IDX = 1

        datedata = {"IDX": self.refresh_IDX, "RefreshDate": datetime.today()}
        dateDF = pd.DataFrame([datedata])

        if self.upDate == False:
            with self.engine.begin() as conn:
                # update refresh cylce history
                # enabl e inserting values into IDENTITY column
                conn.exec_driver_sql(f"SET IDENTITY_INSERT sq.dim_refresh_history ON")
                dateDF.to_sql(
                    "dim_refresh_history",
                    conn,
                    schema="SQ",
                    chunksize=2000,
                    index=False,
                    if_exists="append",
                )
                conn.commit()

            # load the jira configuration
            dfConfig = conf.loadConfig().readConfig()
            dfConfig["Refresh_Cycle"] = int(self.refresh_IDX)
            with self.engine.begin() as conn:
                #   conn.exec_driver_sql(f"delete from sq.dim_sq_config")
                dfConfig["project_RC"] = dfConfig["jira_project"] + str(
                    self.refresh_IDX
                )
                dfConfig.to_sql(
                    "dim_sq_config",
                    con=self.engine,
                    schema="SQ",
                    chunksize=2000,
                    index=False,
                    if_exists="append",
                )
                conn.commit()

        refreshIDX_File = open("refreshIDX.txt", "w")
        refreshIDX_File.write(str(self.refresh_IDX))
        refreshIDX_File.close()

    def cleanUp_database(self):
        sql_script = "database/maintenance_scripts/cleanUp.sql"
        with codecs.open(sql_script, "r", "utf-8") as file:
            with self.engine.connect() as conn:
                try:
                    for line in file:
                        # check if on current day a refresh process has already be started.
                        print(line.rstrip())
                        trunc_script = "delete from " + line.rstrip()
                        check_count = "select count(*) amount from " + line.rstrip()
                        results = pd.read_sql(check_count, conn)
                        print(str(results["amount"].iloc[0]))
                        conn.execute(
                            text(trunc_script).execution_options(autocommit=True)
                        )
                        conn.commit()
                        results = pd.read_sql(check_count, conn)
                        print(str(results["amount"].iloc[0]))
                except Exception as e:
                    print(f"Integrity error: {e}")
                    print(line.rstrip())


loadJiraData = InitLoadSetup()
loadJiraData.cleanUp_database()
loadJiraData.initFlag()
