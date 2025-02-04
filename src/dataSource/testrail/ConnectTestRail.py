import requests
import json
import time
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine,text
from sqlalchemy.exc import IntegrityError
from database.common.testrail_tabs import testrail_tabs
from database.common.connect import connectDB as connect
from src.dataSource.atlassian.utils.loadConfig import loadConfig


class ConnectTestRail:

    def __init__(self, testRail):
        self.testRail = testRail
        self.base_url = testRail.url
        self.auth = HTTPBasicAuth(testRail.username, testRail.api_token)
        self.trCaseAttrs = loadConfig.readTRAttributes(self)

    def get_test_case_type(self):
        # Construct the URL for fetching test cases
        url = f"{self.base_url}/index.php?/api/v2/get_case_types"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers, auth=self.auth)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error fetching test cases: {response.status_code} - {response.text}"
            )

    def create_case_type_df(self, dfct):
        # Normalize the JSON response into a Pandas DataFrame
        return pd.json_normalize(dfct)

    def transform_case_type_df(self, df, refresh_IDX):
        # Example field mapping and transformation
        dfct = self.create_case_type_df(df)
        dfct.rename(
            columns={"id": "id", "is_default": "is_default", "name": "name"},
            inplace=True,
        )
        dfct["Refresh_Cycle"] = int(refresh_IDX)
        dfct["typeID_RC"] = dfct.apply(
            lambda row: str(row["id"]) + "-" + str(refresh_IDX), axis=1
        )
        # Add more field transformation logic as needed
        return dfct

    def store_test_case_types(self, df, engine, refresh_ID):
        # Add load_id to the DataFrame and store it in the database
        connect.write2DB(self, engine, df, "case_types", "dim_tr_")
        print("Test case_types stored successfully")

    def get_testrail_items(self, endpoint, object, param):
        end_of_stream = False
        items = []
        retries = 0
        offset = 0
        # Construct the URL for fetching test cases
        while (not end_of_stream) and (retries < 4):
            url = (
                f"{self.base_url}/index.php?/api/v2/{endpoint}/{param}&offset={offset}"
            )
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers, auth=self.auth)
            if response.status_code == 429:  # rate limit hit
                print("Rate limited. Waiting 60 seconds...")
                retries += 1
                time.sleep(60)

            elif response.status_code == 401:  # unauthorized:
                print("Unathorized. Please update credentials")
                end_of_stream = True

            elif response.status_code == 403:  # forbidden:
                print("Forbidden")
                end_of_stream = True

            elif response.status_code == 200:

                if response.json()[f"{object}"] == []:
                    end_of_stream = True
                else:
                    items += response.json()[f"{object}"]
                    offset = response.json()["size"] + offset
                    time.sleep(0.2)
            else:
                raise Exception(f"Error code {response.status_code}: {response.json()}")
                end_of_stream = True

        return items

    def process_test_runs(self, projConfig, engine, refresh_IDX):
        # 1.get test run
        startdate = int(datetime(2024, 1, 1, 0, 0).timestamp())
        param = str(projConfig["testrail_id"]) + "&created_after=" + str(startdate)
        runs = self.get_testrail_items("get_runs", "runs", param)
        # 2.create data_frame

        df = pd.json_normalize(runs)
        if not df.empty:
            # 3.convert some column values
            df["created_on"] = df["created_on"].apply(
                lambda x: self.convert_to_datetime(x)
            )
            df["updated_on"] = df["updated_on"].apply(
                lambda x: self.convert_to_datetime(x)
            )
            df["completed_on"] = df["completed_on"].apply(
                lambda x: self.convert_to_datetime(x)
            )
            df["Refresh_Cycle"] = int(refresh_IDX)
            df["runID_RC"] = df.apply(
                lambda row: str(row["id"]) + "-" + str(refresh_IDX), axis=1
            )
            # Add more field transformation logic as needed
            attGroup = self.trCaseAttrs["general"]
            columns = attGroup["standard"]
            print(projConfig.itDomain + "----" + projConfig.jira_id)

            # 4.store test run data
            connect.write2DB(self, engine, df, "runs", "fact_tr_")
            print("Test runs stored successfully")
        return runs

    def process_tests(self, projConfig, engine, refresh_IDX, runs):
        all_tests = []
        runs = pd.json_normalize(runs)
        runs["created_on"] = runs["created_on"].apply(
            lambda x: self.convert_to_datetime(x)
        )
        runs["created_on"] = pd.to_datetime(runs["created_on"])
        runs = runs[runs["created_on"] > "2024-01-01 00:00:00"]
        for index, run in runs.iterrows():
            tests = self.get_testrail_items("get_tests", "tests", run["id"])
            print("-- " + str(index) + " --- Searched run_id :" + str(run["id"]))
            all_tests += tests
        # 2.create data_frame
        df = pd.json_normalize(all_tests)
        columns = [
            "id",
            "case_id",
            "status_id",
            "run_id",
            "title",
            "refs",
            "type_id",
            "custom_automated",
        ]
        df = df[columns]
        # 3.convert some column values
        df["Refresh_Cycle"] = int(refresh_IDX)
        df["testID_RC"] = df.apply(
            lambda row: str(row["id"]) + "-" + str(refresh_IDX), axis=1
        )
        # Add more field transformation logic as needed

        print(projConfig.itDomain + "----" + projConfig.jira_id)

        # 4.store test run data
        connect.write2DB(self, engine, df, "tests", "fact_tr_")
        print("Tests stored successfully")
        return runs

    def get_test_cases(self, projConfig, suite):
        end_of_stream = False
        case_lst = []
        retries = 0
        total_cases = 0
        offset = 0
        # Construct the URL for fetching test cases
        while (not end_of_stream) and (retries < 4):
            id = projConfig["testrail_id"]
            url = f"{self.base_url}/index.php?/api/v2/get_cases/{id}&suite_id={suite}&offset={offset}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers, auth=self.auth)
            if response.status_code == 429:  # rate limit hit
                print("Rate limited. Waiting 60 seconds...")
                retries += 1
                time.sleep(60)

            elif response.status_code == 401:  # unauthorized:
                print("Unathorized. Please update credentials")
                end_of_stream = True

            elif response.status_code == 403:  # forbidden:
                print("Forbidden")
                end_of_stream = True

            elif response.status_code == 200:

                if response.json()["cases"] == []:
                    end_of_stream = True
                else:
                    case_lst.extend(response.json()["cases"])
                    offset = response.json()["size"] + offset
                    # print(start_at)
                    # print(end_of_stream)
                    total_cases = total_cases + offset
                    time.sleep(0.2)
            else:
                raise Exception(f"Error code {response.status_code}: {response.json()}")
                end_of_stream = True

        return case_lst

    def create_dataframe(self, test_cases):
        # Normalize the JSON response into a Pandas DataFrame
        df = pd.json_normalize(test_cases,max_level=1)
        return df

    def convert_to_datetime(self, input):
        # Convert string to datetime object
        try:
            date = datetime.fromtimestamp(input)
            # return datetime.strptime(input, "%Y-%m-%dT%H:%M:%S%z")
        except (ValueError, TypeError):
            date = datetime.strptime("2024-01-01", "%Y-%m-%d")

        return date

    def extract_case_refs(self, refs):
        #parsing the references to jira issues
        refs['refs'] = refs['refs'].str.split(',')
        refs = refs.explode('refs').reset_index(drop=True)
        return refs


    def create_project_RC(self, id, refresh_IDX, trConfig):
        return trConfig["jira_project"] + str(refresh_IDX)

    def transform_data(self, df, refresh_IDX, projConfig, engine):
        # Example field mapping and transformation
        df["created_on"] = df["created_on"].apply(lambda x: self.convert_to_datetime(x))
        df["updated_on"] = df["updated_on"].apply(lambda x: self.convert_to_datetime(x))
        df["Refresh_Cycle"] = int(refresh_IDX)
        df["projectTR"] = projConfig["testrail_id"]
        df["projectJI"] = projConfig["jira_id"]
        df["project_RC"] = df["suite_id"].apply(
            lambda x: self.create_project_RC(x, refresh_IDX, projConfig)
        )
        df["typeID_RC"] = df.apply(
            lambda row: str(row["type_id"]) + "-" + str(refresh_IDX), axis=1
        )
        df["caseID_RC"] = df.apply(
            lambda row: str(row["id"]) + "-" + str(refresh_IDX), axis=1
        )
        # Add more field transformation logic as needed
        attGroup = self.trCaseAttrs["general"]
        columns = attGroup["standard"]
        print(projConfig.itDomain + "----" + projConfig.jira_id)

 

        if projConfig.regType == "y":
            columns = columns + attGroup["regFlag"]
        if projConfig.testrail_id == 162:
            try:
                columns.remove("custom_steps")
                columns.remove("custom_security")
                columns.append("custom_robot")
                df["custom_automated"] = df["custom_robot"]
                #df.rename(columns={'custom_robot':'custom_automated'}, inplace=True)
            except ValueError:
                pass
        if projConfig.testrail_id == 170:
            try:
                columns.remove("custom_steps")
                columns.remove("custom_automated")
                columns.remove("custom_security")
            except ValueError:
                pass
        return df[columns]

    def store_test_cases(self, df, refs, engine, refresh_ID):
        # Add load_id to the DataFrame and store it in the database
        connect.write2DB(self, engine, df, "cases", "dim_tr_")
        print("Test cases stored successfully")
        
        connect.write2DB(self, engine, refs, "refs", "fact_tr_")
        print("Test cases refs stored successfully")

    def load_data(self, project_id, testRail, engine, refresh_IDX, config):
        # Generate a unique load ID for the entire load process
        # load_id = datetime.now().strftime("%Y%m%d%H%M%S")

        if config['jira_system'].iloc[0] == "TSC":
            try:
                case_types = self.transform_case_type_df(self.get_test_case_type(), refresh_IDX)
                self.store_test_case_types(case_types, engine, refresh_IDX)
            except IntegrityError as e:
                print(f'Integrity error: {e}')

        for index, projectConf in config.iterrows():
            suits = projectConf.suite_id
            if projectConf.testrail_id != "15":
                if projectConf.testrail_id < 900000:
                    if projectConf.refresh_active == "y":
                        for index, suite in enumerate(projectConf.suite_id):

                            print(suite)
                            test_cases = self.get_test_cases(projectConf, suite)
                            df = self.create_dataframe(test_cases)
                            df = self.transform_data(df, refresh_IDX, projectConf, engine)

                            df_refs = df[["caseID_RC", "refs","id"]]
                            df_refs = self.extract_case_refs(df_refs)
                            df_refs["refresh_cycle"] = refresh_IDX

                            self.store_test_cases(
                                df,
                                df_refs,
                                engine,
                                refresh_IDX,
                            )
                        runs = self.process_test_runs(projectConf, engine, refresh_IDX)
                       # self.process_tests(projectConf, engine, refresh_IDX, runs)


# class testRail:
#     def __init__(self):
#         print("hahhah")

# Usage example
# if __name__ == "__main__":
#    base_url = "https://yourtestrailurl.testrail.io"
#    username = "your_username"
#    api_key = "your_api_key"

#    connect_testrail = ConnectTestRail(base_url, username, api_key)

#    # Load data for all projects
#    connect_testrail.load_data()

#    # Load data for a specific project
#    project_id = 1
#    connect_testrail.load_data(project_id)


