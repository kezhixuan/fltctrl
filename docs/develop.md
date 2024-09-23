****1.loadConfig.py****

There are configuration files defined in config folder which defined projects information.
There are following files:
1. **jira.json**: define jira related information

```
{
        "refresh_active": "y",
        "jira_system": "TSC",
        "jira_id": "CISCOSLC",
        "jira_project": "CISCOSLC",
        "jira_project_name": "CiscoSLC",
        "project_name": "CiscoSLC",
        "issue_types": "",
        "report_start_date": "",
        "topic_id": "",
        "issues_system": ""
}
```

2. **testrail.json**: define testrail ralated information and jira id

```
{
      "testrail_id": 12,
      "jira_id": "GXD",
      "suite_id": [622,703],
      "refresh_active": "y",
      "automation_flag": "n"
}
```


File loadConfig.py will read these json files and get necessary informations.
