import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import datetime as dt
import time
import numpy as np
import re
from openpyxl import Workbook
import atlassian.utils.cleanDF as clDF
import atlassian.utils.loadConfig as conf
from atlassian.utils import manageLogin as mgl

class issuesReleases:
  
  def __init__(self, connectJira, instance):
    print(connectJira)
    login = mgl.manageLogin()
    self.creds = login.getCreds(connectJira, instance)
    self.instance = instance

    pass

  def connect2jira(self, creds, project):
    start_at = 0
    end_of_stream = False
    release_lst = []
    retries = 0

    # read configuration from excel


    # prepare jira jql to query releases for a project

    # request releases from jira

    # cleanup release data

    # store result in mssql database

    while (not end_of_stream) and (retries < 4):

      url = f"{creds['url']}rest/api/3/project/{project}/version?startAt={start_at}&maxResults=100"

      headers = {
        "Accept": "application/json"
      }

      auth = HTTPBasicAuth(self.creds["username"], self.creds["api_token"])

      response = requests.request(
        "GET",
        url,
        headers=headers,
      #  params=query,
        auth=auth
      )
      
      releases = response.json()

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
        if response.json()['values'] == []:
          end_of_stream = True
        else:
          release_lst.extend(response.json()['values'])
          start_at = response.json()['startAt'] + response.json()['maxResults']
        #  print(start_at)
        #  print(end_of_stream)
          total_releases = response.json()['total'] 
          time.sleep(0.2)
      
      else:
        raise Exception(f"Error code {response.status_code}: {response.json()}")
        end_of_stream = True

    return release_lst

  def get_releases(self):
    release_lst =  pd.DataFrame()
    projects = conf.loadConfig().getProjectsByInstance(self.instance)
    print(projects.head())
    for index, row in projects.iterrows():
      proj_release=pd.DataFrame(self.connect2jira(self.creds, row['jira_project']))
      proj_release["project"]=row['jira_project']
      release_lst = pd.concat([release_lst,proj_release], axis=0)    
    
#    releases = pd.json_normalize(release_lst)

    release_lst["startDate"] = pd.to_datetime(release_lst["startDate"])
    release_lst["releaseDate"] = pd.to_datetime(release_lst["releaseDate"])
    release_lst["id"] = pd.to_numeric(release_lst["id"])
    print(release_lst)
    return release_lst

#or Testing only
#isr = issuesReleases()
#isr.get_releases()