import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import datetime as dt
import time
import numpy as np
import codecs
import src.dataSource.atlassian.utils.loadConfig as lC 
from datetime import datetime
from numpy import int64
from database.common.connect import connectDB as connect
from src.dataSource.atlassian import IssueSatelites as atl
from src.dataSource.atlassian.utils import columnHandling as utl
from src.dataSource.atlassian.utils import columnHandlingCustom as cutl
from src.dataSource.atlassian.utils import manageLogin as mgl

pd.options.mode.copy_on_write = True


#define function to merge columns with same names together
def same_merge(x): return ','.join(x[x.notnull()].astype(str))

class ConnectAtlassian:
  
  def __init__(self, connectJira, instance):
    login = mgl.manageLogin()
    self.creds = login.getCreds(connectJira, instance)
    self.instance = instance
    
    pass
  
  def connect2jira(self, creds, project, jql_fields, filter, startDate):
# This function connects to the defined Jira Insance and collects all issues based on the pre-defined filter.
# The collected jire fileds are predifined to lean the network processing.
    start_at = 0
    end_of_stream = False
    issue_lst = []
    retries = 0


    while (not end_of_stream) and (retries < 4):

      url = f"{creds['url']}rest/api/2/search?startAt={start_at}&maxResults=100"

      headers = {
        "Accept": "application/json"
      }

      auth = HTTPBasicAuth(creds["username"], creds["api_token"])
      
      query = {
        #TODO: add custom JQL here
        'jql': "project in (" + project +
            ") AND created > '2019-01-01' and issuetype in (" + filter + ")", 
        'fields': "(" + jql_fields + ")"
      }
        
      response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
      )
      
      if response.status_code == 429: #rate limit hit
        print("Rate limited. Waiting 60 seconds...")
        retries += 1
        time.sleep(60)
      
      elif response.status_code == 401: #unauthorized:
        print("Unathorized. Please update credentials")
        end_of_stream = True
      
      elif response.status_code == 403: #forbidden:
        print("Forbidden")
        end_of_stream = True

      elif response.status_code == 200:
        if response.json()['issues'] == []:
          end_of_stream = True
        else:
          issue_lst.extend(response.json()['issues'])
          start_at = response.json()['startAt'] + response.json()['maxResults']
          # print(start_at)
          # print(end_of_stream)
          total_issues = response.json()['total'] 
          time.sleep(0.2)
      
      else:
        raise Exception(f"Error code {response.status_code}: {response.json()}")
        end_of_stream = True

    return issue_lst

  def createDataFrame(self, project, jiraService, engine, refresh_IDX):
# Preparation of the Jira JQL statement and the required jira fileds.
    columH = utl.columnHandling()
    columCH = cutl.columnHandlingCustom()

    jql = json.load(codecs.open("src/dataSource/atlassian/config/JiraAttributes.json",'r','utf-8'))

    if jiraService == "jira_tsc":
      jql_fields = ", ".join(jql["general"]["standard"]) + ", " + ", ".join(jql["general"]["customFields"])
      filter = ", ".join(jql["general"]["filter"])
    elif jiraService == "jira_gilds":
      jql_fields = ", ".join(jql["general"]["standardGilds"]) + ", " + ", ".join(jql["general"]["customFieldsGilds"])
      filter = ", ".join(jql["general"]["filterGilds"])

    startDate = jql["general"]["startDate"]

    issues = self.connect2jira(self.creds, project, jql_fields, filter, startDate)
    #Create a Pandas DataFrame
    df = pd.json_normalize(issues) 
    print("Successfully connected to jira")

    

    try:  
      cols = [col for col in df.columns if col not in ['fields.fixVersions','fields.customfield_11095','fields.labels','fields.customfield_14162','fields.versions','fields.components']]
     # df = df[cols].join(df_fixversions).join(df_labels).join(df_affected_version).join(df_versions).join(df_components)
    except:
      print("Issue: joining not working")  
      

    ### Customized fields from jira instance ####
    url = f"{self.creds['url']}rest/api/3/field"

    headers = {
      "Accept": "application/json"
    }

    auth = HTTPBasicAuth(self.creds["username"], self.creds["api_token"])

    response = requests.request(
      "GET",
      url,
      headers=headers,
      auth=auth
    )
    
### Creating general core jira attributes that are unique per definition
# fields.customfield_19890 --> severity
# fields.customfield_20083 --> severity_IRE
# fields.customfield_20005 --> severity_ATD
# fields.customfield_20118 --> severity_GPIS
# fields.customfield_19900 --> release_phase
# fields.customfield_20081 --> release_phase_IRE
# fields.customfield_20003 --> release_phase_ATD
# fields.customfield_20128 --> release_phase_GPIS
# fields.customfield_19901 --> bug_classification
# fields.customfield_20080 --> bug_classification_IRE
# fields.customfield_20004 --> bug_classification_ATD
# fields.customfield_20129 --> bug_classification_GPIS
# fields.customfield_20130 --> defect_age_GPIS
# fields.customfield_20141 --> Affecte_Version_GPIS
# fields.customfield_14162.name --> Affected Version
# fields.customfield_14162.id --> AffectedVersion.id
# fields.customfield_20006 --> Affected Version_ATD
# fields.customfield_20090.value --> Affected Version_IRE
# fields.customfield_20091.value --> Fixed Version_IRE
# fields.customfield_19916 --> FIMS ID
# fields.customfield_19100 --> SIMS_Demand_ext
# fields.customfield_10362 --> sprint
# GILDS
# fields.customfield_14455 --> Defect_age,
# fields.customfield_11487 --> bug_classification,
# fields."customfield_11106 --> Severity_GILDS,
# fields."customfield_11107 --> release_phase,
# fields."customfield_11095 --> SLS_squad 

    if jiraService == "jira_gilds":
      dfCore = df.loc[:, df.columns.isin(["id","key","fields.issuetype.name","fields.project.name", "fields.project.key","fields.priority.name",
        "fields.status.name","fields.creator.displayName", "fields.created","fields.summary",
        "fields.statuscategorychangedate","fields.duedate","fields.updated",
        "fields.customfield_14455.value","fields.customfield_11487.value","fields.customfield_11106.value","fields.customfield_11107.value"])]
      dfSatelite = df.loc[:, df.columns.isin(["id", "key","fields.customfield_11095","fields.project.name","fields.labels","fields.versions","fields.fixVersions","fields.components"])]

    elif jiraService == "jira_tsc":
      dfCore = df.loc[:, df.columns.isin(["id","key","fields.issuetype.name","fields.project.name", "fields.project.key","fields.priority.name",
        "fields.status.name","fields.creator.displayName", "fields.created","fields.summary",
        "fields.statuscategorychangedate","fields.duedate","fields.updated",
        "fields.customfield_19890.value","fields.customfield_20083.value", "fields.cusotmfield_20005.value","fields.customfield_20118.value",
        "fields.customfield_19900.value","fields.customfield_20081.value", "fields.cusotmfield_20003.value","fields.customfield_20128.value",
        "fields.customfield_19901.value","fields.customfield_20080.value", "fields.cusotmfield_20004.value","fields.customfield_20129.value",
        "fields.customfield_19890.value"])]

      ### Create collection of multiple dimension jira attribues. The dimension can be based on time or content and have multiple records
      dfSatelite = df.loc[:, df.columns.isin(["id", "key","fields.project.name","fields.labels","fields.versions","fields.fixVersions","fields.components",
        "fields.customfield_20006.id","fields.customfield_20006.name","fields.customfield_20006.archived","fields.customfield_20006.released","fields.customfield_20006.releaseDate",
        "fields.customfield_20141.id","fields.customfield_20141.name","fields.customfield_20141.archived","fields.customfield_20141.released","fields.customfield_20141.releaseDate",
        "fields.customfield_14162.id","fields.customfield_14162.name","fields.customfield_14162.archived","fields.customfield_14162.released","fields.customfield_14162.releaseDate"])]
          
    dfSatelite["key"] = dfSatelite["key"].astype("string")
    

    ### Change Column names to target database table design 
    dfCore , dfSatelite = columH.cleanColumnNames(project, dfCore, dfSatelite)

    return dfCore, dfSatelite

  def convertToDateTime(self,input):
    # function that reformats input string to datetime type
    try:
      try:
        return datetime.strptime(input, "%Y-%m-%d")
      except:
        return datetime.strptime(input, "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
      return datetime.strptime("1970-01-01", "%Y-%m-%d")
      
  
  def GetIssues(self, project, jiraService, engine, refresh_IDX):
      issue_lst =  pd.DataFrame()
      conf = lC.loadConfig()
# Getting all for the reporting configured projects from the json file, filtered by the Jira Instance (jiraSerivce)
# The porject can be collected separatelly, when it's empty all configured projects of an Jira Insance are collected.
      projects = conf.getIssueProjects(project, jiraService)


      strings = ['issue_key','summary', 'issuetype', 'creator',
            'severity','bug classification','project','priority','release phase','status','defect_age','affected version',
            'fixversions','labels','versions','componentsname']
      datetimex = ['statuscategorychangedate','created','duedate','updated','affected version releasedate']
      numbers = ['index','id']

      for index, row in projects.iterrows():
        issues, issues_copy = self.createDataFrame(row['jira_project'],jiraService, engine, refresh_IDX)

        prefix = "fact_ji_"
        issues["issueKey_RC"] = issues["issue_key"] + "-" + str(refresh_IDX)
        for s in strings:
          try:
            issues[s] = issues[s].astype("string")
          except KeyError:
            print("Field : " + s + " not found")
        for n in numbers:
          try:
            issues[n] = issues[n].astype(int64)
          except KeyError:
            print("Field : " + n + " not found")
        for x in datetimex:  
          try:
            issues[x] = issues.apply(lambda y: self.convertToDateTime(y[x]), axis=1)
          except KeyError:
              print("Field : " + x + " not found")

        if row['jira_project'] == "SIMS" or row['jira_project'] == "GCT" or row['jira_project'] == "AEC":
          issues['defect_age'] = 'NaN'
          print("missing fields: defect_age for project : " + row['jira_project'] + " has been set!")
        if row['jira_project'] == "GXD":
          issues['defect_age'] = "NaN"
          print("missing fields: defect_age and compontentsname for project : " + row['jira_project'] + " has been set!")
        if row['jira_project'] == "IRE":
          issues['defect_age'] = 'NaN'
          print("missing fields: ALL for project : " + row['jira_project'] + " has been set!")

        print("---------- Columns for project :  " + row['jira_project']  + "  ---------------------------------")
        print(issues.columns)

        
# Adding primary keys to the dataFrame
        issues["Refresh_Cycle"] = int(refresh_IDX)
        issues['project_RC'] = issues['jira_key'] + str(refresh_IDX)

# Storing the collected DataFrame in the database
        connect.write2DB(self, engine, issues, "issues", prefix)
# Adding the Satelite Table data to the database
        atl.IssueSatelites(issues_copy, project, engine, refresh_IDX)

        issue_lst = pd.concat([issue_lst,issues], axis=0)
      
      return issue_lst
