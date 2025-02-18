import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import datetime as dt
import time
import numpy as np
import re
from openpyxl import Workbook
from database.common.connect import connectDB as connect
import src.dataSource.atlassian.utils.cleanDF as clDF
from datetime import datetime
from numpy import int64
import src.dataSource.atlassian.utils.loadConfig as conf



pd.options.mode.copy_on_write = True


class IssueSatelites:
    prefixFact = "dim_ji_"
    status = True

    def __init__(self, df, project, engine, refresh_IDX):

        success_aV = self.affectedVersion(df, project, engine, refresh_IDX)
        success_fV = self.fixVersions(df, project, engine, refresh_IDX)
        success_Co = self.jiraComponents(df, engine, refresh_IDX)
        success_Cf = self.jiraCustomfield(df, engine, refresh_IDX)
    #    success_La = self.jiraLabels(df, engine, refresh_IDX)
        success_Sq = self.jiraSquads(df, project, engine, refresh_IDX)

        if success_aV != True:
            self.status = False
        elif success_fV != True:
            self.status = False
        elif success_Co != True:
            self.status = False
        elif success_Cf != True:
            self.status = False
    #    elif success_La != True:
    #        self.status = False
        elif success_Sq != True:
            self.status = False
        else:
            self.status = True

        pass

    def customReleaseName(self, project, release):
        if project == "SIMS":
            majRelease = release.str.extract(r"(\d{1,2}.\d{1,2}.\d{1,2})")
        else:
            majRelease = release

        return majRelease
    
    def convertToDateTime(self, input):
        # function that reformats input string to datetime type
        try:
            
            return datetime.strptime(input, "%Y-%m-%d").date()
        except:
            try:
            
                return datetime.strptime(input, "%Y-%m-%dT%H:%M:%S.%f%z").date()
            except:
            
                return datetime.fromtimestamp(0)

    def fixVersions(self, df, project, engine, refresh_IDX):
        ### changing from nested structure to integrated harmonized json structure. e.g. versioons {self, id, ...} to versions.self; versions.id e.g.

        try:
            if "fixVersions" in df.columns:
                df_f = df["fixVersions"].explode().apply(pd.Series)
                df_f = df_f.drop_duplicates()
                if "id" in df_f:
                    df_f = df_f[df_f["id"].notnull()]
                    if not df_f.empty:
                        df_fixversions = pd.DataFrame()
                        df_fixversions["self"] = df_f["self"]
                        df_fixversions["fixversion_id"] = df_f["id"]
                        df_fixversions["name"] = self.customReleaseName(
                            project, df_f["name"]
                        )
                        df_fixversions["archived"] = df_f["archived"]
                        df_fixversions["released"] = df_f["released"]
                        if "releaseDate" in df_f:
                            df_fixversions["releaseDate"] = df_f["releaseDate"]
                        else:
                            df_fixversions["releaseDate"] = ""
                        df_fixversions["description"] = df_f["description"]
                        print(df_fixversions.columns)
                        df_f.drop(0, axis=1, inplace=True)
                        print(df_fixversions.columns)
                        df_fixversions["issueKey_RC"] = (
                            df["key"] + "-" + str(refresh_IDX)
                        )
                        df_fixversions["issue_key"] = df["key"]
                        df_fixversions["Refresh_Cycle"] = int(refresh_IDX)

                        df_fixversions = df_fixversions.drop_duplicates()
                        # df_fixversions.rename(columns={col:f'fields.fixVersions.{col}' for col in df_fixversions.columns}, inplace=True)
                        connect.write2DB(
                            self, engine, df_fixversions, "fixversions", self.prefixFact
                        )
            # df_fixversions.to_sql(self.prefixFact+'fixversions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
        except Exception as e:
            connect.getLogger().info(
                "FIXVERION: Project " + project + " failed" + " -- " + df["key"]
            )
            print(f"Unexpected {e=}, {type(e)=}" + project)
            return False
        except:
            print("Not found: fixVersion" + " - SateliteClass Exception")
            return False
        return True

    def affectedVersion(self, df, project, engine, refresh_IDX):
        # also known as "affectedVersion"
        try:
            if "versions" in df.columns:
                df_v = df["versions"].explode().apply(pd.Series)
                df_v = df_v.drop_duplicates()
                if "id" in df_v:
                    df_v = df_v[df_v["id"].notnull()]
                    if not df_v.empty:
                        df_versions = pd.DataFrame()
                        df_versions["version_id"] = df_v["id"]
                        df_versions["name"] = self.customReleaseName(
                            project, df_v["name"]
                        )
                        df_versions["archived"] = df_v["archived"]
                        df_versions["released"] = df_v["released"]
                        if "releaseDate" in df_v:
                            df_versions["releaseDate"] = df_v["releaseDate"]
                        else:
                            df_versions["releseDate"] = ""
                        df_versions["description"] = df_v["description"]
                        # print(df_versions.columns)
                        # df_v.drop(0, axis=1, inplace=True)
                        # print(df_versions.columns)
                        df_versions["issue_key"] = df["key"]
                        df_versions["Refresh_Cycle"] = int(refresh_IDX)
                        df_versions["issueKey_RC"] = df["key"] + "-" + str(refresh_IDX)
                        connect.write2DB(
                            self, engine, df_versions, "versions", self.prefixFact
                        )
                # df_versions.to_sql(self.prefixFact+'versions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
                # df_versions.rename(columns={col:f'fields.versions.{col}' for col in df_versions.columns}, inplace=True)
        except Exception as e:
            connect.getLogger().info(
                "VERSIONS: Project " + project + " failed" + " -- " + df["key"]
            )
            connect.getLogger().info(f"Unexpected {e=}, {type(e)=}" + project)
        except:
            connect.getLogger().info("Not found: versions in: " + project)
            return False
        return True

    def jiraComponents(self, df, engine, refresh_IDX):
        try:
            if "components" in df.columns:
                df_c = df["components"].explode().apply(pd.Series)
                df_c = df_c.drop_duplicates()
                if "id" in df_c:
                    df_c = df_c[df_c["id"].notna()]
                    if not df_c.empty:
                        df_components = pd.DataFrame()
                        df_components["self"] = df_c["self"]
                        df_components["component_id"] = df_c["id"]

                        df_components["name"] = df_c["name"]
                        df_components["issue_key"] = df["key"]
                        df_components["Refresh_Cycle"] = int(refresh_IDX)
                        df_components["issueKey_RC"] = (
                            df["key"] + "-" + str(refresh_IDX)
                        )
                        connect.write2DB(
                            self, engine, df_components, "components", self.prefixFact
                        )
                        # df_components.to_sql(self.prefixFact+'components', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
            # df_components.rename(columns={col:f'fields.components{col}' for col in df_components.columns}, inplace=True)
        except Exception as e:
            print("----> components --> " + df["key"])
            print(f"Unexpected {e=}, {type(e)=}")
        except:
            print("Not found: components")
            return False
        return True

    def jiraLabels(self, df, engine, refresh_IDX):
        try:
            if "labels" in df.columns:
                # df_l = df.assign(labels=df.labels.str.split(",")).explode("labels")
                df_l = df.explode("labels")
                df_l = df_l.drop_duplicates()
                if not df_l.empty:
                    df_labels = pd.DataFrame()
                    df_labels["label_id"] = df_l["id"]
                    df_labels["issueKey_RC"] = df_l["key"] + "-" + str(refresh_IDX)
                    df_labels["label"] = df_l["labels"]
                    df_labels["issue_key"] = df_l["key"]
                    df_labels["Refresh_Cycle"] = int(refresh_IDX)
                    # df_labels.to_sql(self.prefixFact+'labels', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
                    connect.write2DB(self, engine, df_labels, "labels", self.prefixFact)
            # df_labels.rename(columns={col:f'fields.labels.{col}' for col in df_labels.columns}, inplace=True)
        except Exception as e:
            print("----> labels --> " + df["key"])
            print(f"Unexpected {e=}, {type(e)=}")
        except:
            print("Not found: labels")
            return False
        return True

    # Squads are used in GILDS, special in SELS to organize the teams. Bugs must be assigned to one Squad.
    def jiraSquads(self, df, project, engine, refresh_IDX):
        try:
            if "squads" in df.columns:
                # df_l = df.assign(labels=df.labels.str.split(",")).explode("labels")
                df_l = df.explode("squads").apply(pd.Series)
                df_l = df_l.drop_duplicates()
                if "id" in df_l:
                    df_l = df_l[df_l["id"].notna()]
                    if not df_l.empty:
                        df_squads = pd.DataFrame()
                        df_squads["squad_id"] = df_l["id"]
                        df_squads["issueKey_RC"] = df_l["key"] + "-" + str(refresh_IDX)
                        if "squads" in df_l:
                            df_squads["squad"] = df_l["squads"].apply(pd.Series)[
                                "value"
                            ]
                        else:
                            df_squads["squad"] = ""
                        df_squads["issue_key"] = df_l["key"]
                        df_squads["Refresh_Cycle"] = int(refresh_IDX)
                        connect.write2DB(
                            self, engine, df_squads, "squads", self.prefixFact
                        )
                        # df_squads.to_sql(self.prefixFact+'squads', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')

        # df_labels.rename(columns={col:f'fields.labels.{col}' for col in df_labels.columns}, inplace=True)
        except Exception as e:
            print("Project: " + project + "----> squad --> " + df["key"])
            print(f"Unexpected {e=}, {type(e)=}")
        except:
            print("Not found: squad")
            return False
        return True

    def jiraCustomfield(self, df, engine, refresh_IDX):
        affected_version = {
            "customfield_20006.id",
            "customfield_20090.id",
            "customfield_20141.id",
            "customfield_14162.id",
        }
        if df.columns.isin(affected_version).any():
            for column in affected_version:
                if column in df:
                    colCheck = column.split(".")[0]
                    try:
                        dfr = df.loc[df[colCheck + ".id"].notna()]
                        print(dfr.columns)
                        if not dfr.empty:
                            df_affected_version = pd.DataFrame()
                          #  df_affected_version["issueKey_RC"] = (
                          #      df["key"] + "-" + str(refresh_IDX)
                          #  )
                            df_affected_version["version_id"] = dfr[colCheck + ".id"]
                            df_affected_version["name"] = dfr[colCheck + ".name"]
                            df_affected_version["archived"] = dfr[
                                colCheck + ".archived"
                            ]
                            df_affected_version["released"] = dfr[
                                colCheck + ".released"
                            ]
                            releaseDateField = colCheck + ".releasedate"
                            
                            if releaseDateField in dfr:
                                df_affected_version["releaseDate"] = dfr[releaseDateField].apply(lambda x: self.convertToDateTime(x))
                            else:
                                df_affected_version["releaseDate"] = ""
                            
                           # df_affected_version["issue_key"] = df["key"]
                            df_affected_version["Refresh_Cycle"] = int(refresh_IDX)
                            df_affected_version = df_affected_version.drop_duplicates()
                            connect.write2DB(
                                self,
                                engine,
                                df_affected_version,
                                "versions",
                                self.prefixFact,
                            )
                            # df_affected_version.to_sql(self.prefixFact+'versions', con=engine, schema='SQ',chunksize=2000, index=False, if_exists='append')

                    # df_affected_version.rename(columns={col:f'fields.customfield_14162.{col}' for col in df_affected_version.columns}, inplace=True)
                    except Exception as e:
                        print("----> affected_version --> " + df["key"])
                        print(f"Unexpected {e=}, {type(e)=}")
                    except:
                        print("Not found: 14162 (affected version)")
                        return False
        return True
