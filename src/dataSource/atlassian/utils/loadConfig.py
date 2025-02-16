import pandas as pd
import codecs


class loadConfig:

    def __init__(self):
        pass

    ##get all jira configurations
    def readConfig(self):
        config = pd.read_json(codecs.open("config/jira.json", "r", "utf-8"))

        return config

    def readTRConfig(self):
        config = pd.read_json(codecs.open("config/testrail.json", "r", "utf-8"))
        testRails = pd.DataFrame(config)
        return testRails

    def readTRAttributes(self):
        config = pd.read_json(
            codecs.open("src/dataSource/testrail/config/TestRail.json", "r", "utf-8")
        )
        trAttr = pd.DataFrame(config)
        return trAttr

    ##get testrail info by jira id
    def getTestRail(self, jiraId):
        config = pd.read_json(codecs.open("config/testrail.json", "r", "utf-8"))
        testRails = pd.DataFrame(config)
        testRails.query(f"jira_id == '{jiraId}'", inplace=True)

        return testRails

    ##get jira projects by jira service
    def getProjectsByInstance(self, jiraService):
        jiraInstance = jiraService.split("_", 1)[1]
        jiraProjects = pd.DataFrame(self.readConfig())
        jiraProjects.query(
            "refresh_active == 'y' & jira_system == '" + jiraInstance.upper() + "'",
            inplace=True,
        )
        print(jiraProjects)
        return jiraProjects

    ##get specific jira project by jira service and project
    def getIssueProjects(self, testProj, jiraService):
        jiraProjects = pd.DataFrame(self.readConfig())
        if jiraService == "jira_tsc":
            if testProj != "":
                jiraProjects.query(
                    "refresh_active == 'y' & jira_system == 'TSC' & jira_project == '"
                    + testProj
                    + "'",
                    inplace=True,
                )
            else:
                jiraProjects.query(
                    "refresh_active == 'y' & jira_system == 'TSC'", inplace=True
                )
        elif jiraService == "jira_tsc1":
            jiraProjects.query(
                "refresh_active == 'y' & jira_system == 'TSC1'", inplace=True
            )
        elif jiraService == "jira_gilds":
            jiraProjects.query(
                "refresh_active == 'y' & jira_system == 'GILDS'", inplace=True
            )
        print(jiraProjects)
        return jiraProjects


# loadConfig().getIssueProjects('MDMADM','jira_tsc')
