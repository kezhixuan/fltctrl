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

    def getCases(project, suite=None, custom_regressiontype=None):

        parameters = {}

        if suite:
            parameters['suite'] = suite
        if custom_regressiontype:
            parameters['custom_regressiontype'] = custom_regressiontype

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

    def getUser(usrId):
        return clientAPI.send_get(f'get_user/{usrId}')

    #TODO: Add and consider this as valid use case also for storing users in the DB
    #this way we could see who is working on what
    #Note: since TR 6.6 TR admins can call get_users with no parameter
    def getUsers(projectId=None):

        parameters = {}

        if projectId:
            parameters['projectId'] = projectId

        if parameters:
            query_string = '&'.join([f'{key}={value}' for key, value in parameters.items()])
            url = f'get_users/{query_string}'
        else:
            url = f'get_users/'

        return clientAPI.send_get(url)

    ##TODO add this
    def get_results_for_case():
        return print('fTODO')
