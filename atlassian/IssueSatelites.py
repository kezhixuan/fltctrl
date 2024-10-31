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
from datetime import datetime
from numpy import int64
import atlassian.utils.loadConfig as conf


class IssueSatelites:
  prefixFact = "fact_ji_"
  
  def __init__(self, df, project, engine, refresh_IDX, credentials):
    self.creds = credentials

    self.affectedVersion(df, project, engine, refresh_IDX)
    self.fixVersions(df, project, engine, refresh_IDX)
    self.jiraComponents(df, engine, refresh_IDX)
    self.jiraCustomfield(df, engine, refresh_IDX)
    self.jiraLabels(df, engine, refresh_IDX)
    self.jiraSquads(df, engine, project, refresh_IDX)
    
    pass
  
  def customReleaseName(self,project, release):
    if project == 'SIMS':
      majRelease = release.str.extract(r'(\d{1,2}.\d{1,2}.\d{1,2})')
    else:
      majRelease = release

    return majRelease
  
  def fixVersions(self, df, project, engine, refresh_IDX):
    ### changing from nested structure to integrated harmonized json structure. e.g. versioons {self, id, ...} to versions.self; versions.id e.g.
   
    try:
      if 'fixVersions' in df.columns:
        df_f = df['fixVersions'].explode().apply(pd.Series)
        if 'id' in df_f:
          df_f = df_f[df_f['id'].notnull()]
          if not df_f.empty:
            df_fixversions = pd.DataFrame()
            df_fixversions["self"] = df_f["self"]
            df_fixversions["id"] =df_f["id"]
            df_fixversions["name"] = self.customReleaseName(project, df_f["name"])
            df_fixversions["archived"] = df_f["archived"]
            df_fixversions["released"] = df_f['released']
            df_fixversions["releaseDate"] = df_f['releaseDate']
            df_fixversions["description"] = df_f['description']
            print(df_fixversions.columns)
            df_f.drop(0, axis=1, inplace=True)
            print(df_fixversions.columns)
            df_fixversions["issueKey_RC"] = df["key"] + "-" + str(refresh_IDX)
            df_fixversions['issue_key'] = df['key']
            df_fixversions["Refresh_Cycle"] = int(refresh_IDX)
     # df_fixversions.rename(columns={col:f'fields.fixVersions.{col}' for col in df_fixversions.columns}, inplace=True)
      df_fixversions.to_sql(self.prefixFact+'fixversions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
    except Exception as e:
        print("----> fixVersions --> " + df["key"])
        print(f"Unexpected {e=}, {type(e)=}")
    except:
      print("Not found: fixVersion" + " - SateliteClass Exception")
    return

  def affectedVersion(self, df, project, engine, refresh_IDX):
    # also known as "affectedVersion"
    try:  
        if 'versions' in df.columns:
            df_v = df["versions"].explode().apply(pd.Series)
            if 'id' in df_v:
                df_v = df_v[df_v['id'].notnull()]
                if not df_v.empty:
                  df_versions = pd.DataFrame()
                  df_versions["id"] =df_v["id"]
                  df_versions["name"] = self.customReleaseName(project, df_v["name"])
                  df_versions["archived"] = df_v["archived"]
                  df_versions["released"] = df_v['released']
                  df_versions["releaseDate"] = df_v['releaseDate']
                  df_versions["description"] = df_v['description']
                  print(df_versions.columns)
                  df_v.drop(0, axis=1, inplace=True)
                  print(df_versions.columns)
                  df_versions['issue_key'] = df['key']
                  df_versions["Refresh_Cycle"] = int(refresh_IDX)
                  df_versions["issueKey_RC"] = df["key"] + "-" + str(refresh_IDX)
            df_versions.to_sql(self.prefixFact+'versions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
            #df_versions.rename(columns={col:f'fields.versions.{col}' for col in df_versions.columns}, inplace=True)
    except Exception as e:
        print("----> versions --> " + df["key"])
        print(f"Unexpected {e=}, {type(e)=}")
    except:
        print("Not found: versions") 
    return
  
  
  def jiraComponents(self, df, engine, refresh_IDX):
    try:  
      if 'components' in df.columns:
        df_c= df['components'].explode().apply(pd.Series)
        if 'id' in df_c:
          df_c= df_c[df_c['id'].notna()]
          if not df_c.empty:
            df_components = pd.DataFrame()
            df_components["self"] = df_c["self"]
            df_components["id"] =df_c["id"]
            
            df_components['name'] = df_c['name']
            df_components["issue_key"] = df["key"]
            df_components["Refresh_Cycle"] = int(refresh_IDX)
            df_components["issueKey_RC"] = df["key"] + "-" + str(refresh_IDX)
            df_components.to_sql(self.prefixFact+'components', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
      #df_components.rename(columns={col:f'fields.components{col}' for col in df_components.columns}, inplace=True)
    except Exception as e:
      print("----> components --> " + df["key"])
      print(f"Unexpected {e=}, {type(e)=}")
    except:
      print("Not found: components")  
    
    return

  def jiraLabels(self, df, engine, refresh_IDX):
    try: 
     if 'labels' in df.columns:
        #df_l = df.assign(labels=df.labels.str.split(",")).explode("labels")
        df_l = df.explode("labels")
        if not df_l.empty:
          df_labels = pd.DataFrame()
          df_labels["issueKey_RC"] = df_l["key"] + "-" + str(refresh_IDX)
          df_labels["label"] = df_l["labels"]        
          df_labels["issue_key"] = df_l["key"]
          df_labels["Refresh_Cycle"] = int(refresh_IDX)
          df_labels.to_sql(self.prefixFact+'labels', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
      
      #df_labels.rename(columns={col:f'fields.labels.{col}' for col in df_labels.columns}, inplace=True)
    except Exception as e:
      print("----> labels --> " + df["key"])
      print(f"Unexpected {e=}, {type(e)=}")
    except:
      print("Not found: labels")
    return

# Squads are used in GILDS, special in SELS to organize the teams. Bugs must be assigned to one Squad.
  def jiraSquads(self, df, project, engine, refresh_IDX):
      try: 
          if 'squads' in df.columns:
            #df_l = df.assign(labels=df.labels.str.split(",")).explode("labels")
            df_l = df.explode("squads").apply(pd.Series)
            if 'id' in df_l:
              df_l= df_l[df_l['id'].notna()]
              if not df_l.empty:
                df_squads = pd.DataFrame()
                df_squads["issueKey_RC"] = df_l["key"] + "-" + str(refresh_IDX)
                df_squads["squad"] = df_l["squads"].apply(pd.Series)["value"]
                df_squads["issue_key"] = df_l["key"]
                df_squads["Refresh_Cycle"] = int(refresh_IDX)
                df_squads.to_sql(self.prefixFact+'squads', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
          
        #df_labels.rename(columns={col:f'fields.labels.{col}' for col in df_labels.columns}, inplace=True)
      except Exception as e:
        print("----> squad --> " + df["key"])
        print("Project: " + project  + f"Unexpected {e=}, {type(e)=}")
      except:
        print("Not found: squad")
      return


  def jiraCustomfield(self, df, engine, refresh_IDX):
    affected_version = {"customfield_20006.id","customfield_20090.id","customfield_20141.id","customfield_14162.id"}
    if df.columns.isin(affected_version).any():
      for column in affected_version:
        if column in df:
          colCheck = column.split('.')[0]
          try:
            dfr = df.loc[df[colCheck +'.id'].notna()]
            print(dfr.columns)
            if not dfr.empty:
              df_affected_version = pd.DataFrame()
              df_affected_version["issueKey_RC"] = df["key"] + "-" + str(refresh_IDX)
              df_affected_version["id"] = dfr[colCheck + ".id"]
              df_affected_version["name"] = dfr[colCheck +".name"]
              df_affected_version["archived"] = dfr[colCheck + ".archived"]
              df_affected_version["released"] = dfr[colCheck + '.released']
              df_affected_version["releaseDate"] = dfr[colCheck + '.releasedate']
              df_affected_version["issue_key"] = df["key"]
              df_affected_version["Refresh_Cycle"] = int(refresh_IDX)
              df_affected_version.to_sql(self.prefixFact+'versions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
          
          # df_affected_version.rename(columns={col:f'fields.customfield_14162.{col}' for col in df_affected_version.columns}, inplace=True)
          except Exception as e:
            print("----> affected_version --> " + df["key"])
            print(f"Unexpected {e=}, {type(e)=}")
          except:
            print("Not found: 14162 (affected version)") 

    return "Alll gooood !"
      