import pytest
import pandas as pd

from src.dataSource.atlassian.utils.loadConfig import loadConfig as conf


class TestloadConfig():
    
    def test_getIssueProjects(self):

        jiraProjects = conf.readConfig(self)
        #check = jiraProjects[jiraProjects['jira_id']=='ODM']
        #print(check['jira_id'])
        assert jiraProjects.empty is False
        #assert ( jiraProjects[(jiraProjects["jira_id"] == "ODM")].size == 1)

#tr = TestloadConfig()
#tr.test_getIssueProjects()