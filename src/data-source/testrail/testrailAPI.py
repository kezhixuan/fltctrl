from testrail import APIClient
from dotenv import load_dotenv
import os

load_dotenv()
testrail_url = os.getenv('TESTRAIL_URL')
clientAPI = APIClient(testrail_url)

class TestRailAPI(APIClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def getCase(case):
        return clientAPI.send_get(f'get_case/{case}')

    def getCases(project, suite=None):

        parameters = {}

        if suite:
            parameters['suite'] = suite

        if parameters:
            query_string = '&'.join([f'{key}={value}' for key, value in parameters.items()])
            url = f'get_cases/{project}&{query_string}'
        else:
            url = f'get_cases/{project}'

        return clientAPI.send_get(url)

    def getHistoryForCase(case):
        return clientAPI.send_get(f'get_history_for_case/{case}')

    def getProject(project):
        return clientAPI.send_get(f'get_project/{project}')

    def getProjects():
        return clientAPI.send_get(f'get_projects')

    def getSuite(suite):
        return clientAPI.send_get(f'get_suite/{suite}')

    def getResultsForRun(run):
        return clientAPI.send_get(f'get_results_for_run/{run}')