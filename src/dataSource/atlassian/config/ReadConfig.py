import pandas as pd

class ReadConfig:

    def __init__ (self):
        pass

    def readConfig(self):
        config = pd.read_excel('system_config.xlsx', sheet_name='projList')

        return config
    
    def getIssueProjects(self, testProj, jiraService):
        jiraProjects = pd.DataFrame(self.readConfig())     
        if jiraService == "jira_tsc":
            if testProj != "":
                jiraProjects.query("Active == 'y' & Jira_System == 'TSC' & jira_project == '" + testProj + "'", inplace=True)
            else:
                jiraProjects.query("Active == 'y' & Jira_System == 'TSC'", inplace=True)
        elif jiraService == "jira_gilds":
            jiraProjects.query("Active == 'y' & Jira_System == 'GILDS'", inplace=True)
        return jiraProjects