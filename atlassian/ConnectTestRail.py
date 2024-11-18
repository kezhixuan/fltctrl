import requests
import json
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine
from database.common.testrail_tabs import testrail_tabs

class ConnectTestRail:
    
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, api_key)
    
    def get_test_cases(self, project_id=None):
        # Construct the URL for fetching test cases
        url = f"{self.base_url}/index.php?/api/v2/get_cases/{project_id}" if project_id else f"{self.base_url}/index.php?/api/v2/get_cases"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, auth=self.auth)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching test cases: {response.status_code} - {response.text}")
    
    def create_dataframe(self, test_cases):
        # Normalize the JSON response into a Pandas DataFrame
        df = pd.json_normalize(test_cases)
        return df
    
    def convert_to_datetime(self, input):
        # Convert string to datetime object
        try:
            return datetime.strptime(input, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return datetime.strptime("1970-01-01", "%Y-%m-%d")
    
    def transform_data(self, df):
        # Example field mapping and transformation
        df['created_on'] = df['created_on'].apply(lambda x: self.convert_to_datetime(x))
        df.rename(columns={
            'id': 'caseID_RC',
            'title': 'title',
            'section_id': 'section_id',
            'template_id': 'template_id',
            'type_id': 'type_id',
            'priority_id': 'priority_id',
            'milestone_id': 'milestone_id',
            'refs': 'refs',
            'created_by': 'created_by',
            'created_on': 'created_on',
            'updated_by': 'updated_by',
            'updated_on': 'updated_on',
            'estimate': 'estimate',
            'estimate_forecast': 'estimate_forecast',
            'suite_id': 'suite_id',
            'display_order': 'display_order',
            'is_deleted': 'is_deleted',
            'custom_automation_type': 'custom_automation_type',
            'custom_preconds': 'custom_preconds',
            'custom_steps': 'custom_steps',
            'custom_expected': 'custom_expected',
            'custom_steps_separated': 'custom_steps_separated',
            'custom_mission': 'custom_mission',
            'custom_goals': 'custom_goals'
        }, inplace=True)
        # Add more field transformation logic as needed
        return df
    
    def store_test_cases(self, df, engine, load_id):
        # Add load_id to the DataFrame and store it in the database
        df['load_id'] = load_id
        df.to_sql('dim_cases', con=engine, if_exists='append', index=False)
        print("Test cases stored successfully")

    def load_data(self, project_id=None):
        # Generate a unique load ID for the entire load process
        load_id = datetime.now().strftime("%Y%m%d%H%M%S")
        test_cases = self.get_test_cases(project_id)
        df = self.create_dataframe(test_cases)
        df = self.transform_data(df)
        
        engine = create_engine('sqlite:///testrail.db')
        self.store_test_cases(df, engine, load_id)

# Usage example
if __name__ == "__main__":
    base_url = "https://yourtestrailurl.testrail.io"
    username = "your_username"
    api_key = "your_api_key"
    
    connect_testrail = ConnectTestRail(base_url, username, api_key)
    
    # Load data for all projects
    connect_testrail.load_data()
    
    # Load data for a specific project
    project_id = 1
    connect_testrail.load_data(project_id)
