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


class Connect2TestRail(connectDB):
    # seperating testrail from jira connection

    env = []
    localTest = []
    prefix = "dim_"
    refresh_IDX = ""
    connect2 = []
    jiraService = []

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

        connData = pd.read_json(codecs.open(self.env + ".json", "r", "utf-8"))

        if self.jiraService == "jira_tsc1" or self.jiraService == "jira_gitdao":
            self.jiraCon = connData["jira_tsc"]
        else:
            self.jiraCon = connData[self.jiraService]

        self.testrailCon = connData[self.testRail]

        ofile = open("refreshIDX.txt")
        IDX = ofile.readline()
        self.refresh_IDX = str(IDX)

    def getTestRailData(self):
        project_id = ""
        # reading the system parameter
        jira_service = self.jiraService.split("_",1)[1].upper()

        config = pd.DataFrame(self.config[self.config["jira_system"] == jira_service])

        testR = testr.ConnectTestRail(self.testrailCon)
        testR.load_data(
            project_id, self.testRail, self.engine, self.refresh_IDX, config
        )


loadJiraData = Connect2TestRail()
loadJiraData.getTestRailData()
