from .columnHandling import columnHandling


class columnHandlingCustom(columnHandling):

    def __init__(self):
        pass

    def getMajorRelease(self, project, dfCore, dfSatelite):

        if project == "SIMS":
            dfSatelite.loc[
                dfSatelite["fields.project"] == "SIMS", "fields.versions"
            ] = "".join(
                dfSatelite["fields.versions"].split(" ")[1:][0]
            )  # .join(["fields.versions"].split('-')[0])
        #  print("Maj: " + majRelease_num)
        #  majRelease = ''.join(majRelease_num.split('-')[0])
        #  dfCore["fields.version"] = ''.join(release.split('')[1:][0])
        return self.cleanColumnNames(project, dfCore, dfSatelite)


# t = columnHandlingCustom()
# majR = t.getMajorRelease('core 2.3.4-asödlf')
# t.cleanColumnNames
# print(majR)
