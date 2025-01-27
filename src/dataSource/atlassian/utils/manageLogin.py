class manageLogin:

    def __init__(self):
        pass

    def getCreds(self, connectJira, instance):
        creds = []
        if instance == "jira_tsc":
            creds = {
                "url": connectJira.url,
                "username": connectJira.username,
                "api_token": connectJira.api_token,
            }
        elif instance == "jira_gilds":
            creds = {
                "url": connectJira.url,
                "username": connectJira.username,
                "api_token": connectJira.api_token,
            }
        return creds
