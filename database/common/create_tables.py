from connect import connectDB
import pandas as pd
import codecs
from jira_tabs import jira_tabs
from testrail_tabs import testrail_tabs
from alter_db import alter_db
import sys

class create_db(connectDB):
    env=[]
    localTest=[]
    prefix="dim_"
    refresh_IDX=""
    connect2=[]
    jiraService=[]


    def __init__(self):
        self.env = sys.argv[1]
        self.localTest = sys.argv[2]
        # Configure Database connnection
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        super().__init__(sys.argv[1], sys.argv[2])


        print("CREATING TABLES")
        jt = jira_tabs(self.env, self.localTest)
        #jira_tabs.m.create_all(bind=self.engine)
        tt = testrail_tabs(self.env, self.localTest)
        #testrail_tabs.m.create_all(bind=self.engine)

        print("ALTER TABLES")
        at = alter_db(self.env, self.localTest)

cd = create_db()