from connect import engine
import jira_tabs
import testrail_tabs

print("CREATING TABLES")
jira_tabs.m.create_all(bind=engine)
testrail_tabs.m.create_all(bind=engine)