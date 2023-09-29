import pandas as pd

class dashboard_config:

    def __init__ (self):
        pass

    def read_config(self):
        config = pd.read_excel('system_config.xlsx', sheet_name='projList')

        return config
    
    def get_issue_projects(self, instance):
        jiraInstance = instance.split('_',1)[1]

        jiraProjects = pd.DataFrame(self.read_config())
        jiraProjects.query("Active == 'y' & Jira_System == '" + jiraInstance.upper() + "'" , inplace=True)
        return jiraProjects