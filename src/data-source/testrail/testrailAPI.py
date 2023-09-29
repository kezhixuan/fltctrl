from testrail import APIClient

##TODO: read url from configuration
clientAPI = APIClient("https://dbschenker.testrail.io")

class TestRailAPI(APIClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def getCase(case):
        return clientAPI.send_get(f'get_case/{case}')

    def getCases(project, suite):
        return clientAPI.send_get(f'get_cases/{project}&suite_id={suite}')

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