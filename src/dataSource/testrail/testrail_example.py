from testrailAPI import TestRailAPI


class clientTestRail(TestRailAPI):
    pass


example = clientTestRail
response = example.getProject(134)
print(f"Project:\n {response} \n\n")

response = example.getSuite(20778)
print(f"Suite:\n {response} \n\n")

response = example.getResultsForRun(55085)
print(f"Results for Run:\n {response} \n\n")

response = example.getCases(134, 20778)
print(f"Results for Cases:\n {response} \n\n")

response = example.getProjects()
print(f"Results for Projects:\n {response} \n\n")
