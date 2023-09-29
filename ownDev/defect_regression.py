import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class defect_regression:

    def __init__(self):
      pass

    def SevMapping(self,row):
        if row['severity'] == 'Major':
            sev = 3
        elif row['severity'] == 'Blocker':
            sev = 4
        elif row['severity'] == 'Minor':
            sev = 2
        else:
            sev = 1
        return sev

    def PrioMapping(self,row):
        if row['priority'] == 'Major':
            sev = 3
        elif row['priority'] == 'Blocker':
            sev = 4
        elif row['priority'] == 'Minor':
            sev = 2
        else:
            sev = 1
        return sev

    def sevScore(self, row):
        if row['severity'] == 'Major':
            sev = 3
        elif row['severity'] == 'Blocker':
            sev = 4
        elif row['severity'] == 'Minor':
            sev = 2
        else:
            sev = 1

        if row['release phase'] == 'Functional Acceptance':
            rel = 2
        elif row['release phase'] == 'Production':
            rel = 4
        elif row['release phase'] == 'User Acceptance':
            rel = 3
        else:
            rel = 1

        return pow(sev * rel,2)

    def calculate_regression (self, regressAI):

        regressAI['year']= pd.to_datetime(regressAI['created'], utc=True).dt.year
        regressAI.to_excel("output.xlsx",sheet_name='Sheet_name_1') 
        
        projAvgSevSc = regressAI[['project','year','sevScore']].groupby(['project','year']).agg(sevScoreY=pd.NamedAgg(column="sevScore", aggfunc="mean"))
        projBugsY = regressAI[['project','year']].groupby(['project','year']).size().reset_index(name='bugs')

#        print(projAvgSevSc)
#        print(projBugsY)
        sb.set_style("darkgrid")
        sb.regplot(x=projAvgSevSc['sevScoreY'],y=projBugsY['bugs'])

     #   plt.show()

#        modelSevSc = LinearRegression()
#        modelSevSc.fit(projAvgSevSc,projBugsY)
#        r_sqS = modelSevSc.score(projAvgSevSc, projBugsY)

        severity = regressAI[['severityScore']]
        priority = regressAI[['priorityScore']]

        model = LinearRegression()

        model.fit(priority, severity)
        r_sq = model.score(priority, severity)
        print(f"coefficient of determination: {r_sq}")

        fiftyP = np.percentile(regressAI["sevScore"], 50)
        twenty5P = np.percentile(regressAI["sevScore"], 25)
        seventy5P = np.percentile(regressAI["sevScore"], 75)
        
        print(f"25% Percentile of Severity Score: {twenty5P}")
        print(f"50% Percentile of Severity Score: {fiftyP}")
        print(f"75% Percentile of Severity Score: {seventy5P}")
