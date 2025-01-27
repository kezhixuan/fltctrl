from testrailAPI import TestRailAPI


class clientTestRail(TestRailAPI):
    pass


## The purpose is to get data from the test rail instance
## Client should read json files from the folder: TestRailProjects
## Projects defined there should be iterated and expected data should
## be obtained

##TODO: read json
## read project_definition_carrierManager.json
## map to dict, so it will end up like below
theDictionary = {"project": "134", "suite": "20778"}

##TODO: get expected data
client = clientTestRail
data = client.getCases(theDictionary["project"], theDictionary["suite"])

##TODO: push to the data base?
print(data)
