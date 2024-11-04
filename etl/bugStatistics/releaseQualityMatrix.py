#import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import sys
import pandas as pd
from database.common.connect import connectDB
from sqlalchemy import create_engine, text


#conn = connectDB(sys.argv[1], sys.argv[2])


class loadIssuse4Release(connectDB):
    env=[]
    localTest=[]
    conDB=[]
    

    def __init__(self):
        super().__init__(sys.argv[1], sys.argv[2])
        pass

    def SevMapping(row):
        if row['Severity'] == 'Major':
            sev = 3
        elif row['Severity'] == 'Blocker':
            sev = 4
        elif row['Severity'] == 'Minor':
            sev = 2
        else:
            sev = 1
        return sev

    def RelPMapping(row):
        if row['ReleasePhase'] == 'Functional Acceptance':
            rel = 2
        elif row['ReleasePhase'] == 'Production':
            rel = 4
        elif row['ReleasePhase'] == 'User Acceptance':
            rel = 3
        else:
            rel = 1
        return rel

    def sevScore(row):
        if row['Severity'] == 'Major':
            sev = 3
        elif row['Severity'] == 'Blocker':
            sev = 4
        elif row['Severity'] == 'Minor':
            sev = 2
        else:
            sev = 1

        if row['ReleasePhase'] == 'Functional Acceptance':
            rel = 2
        elif row['ReleasePhase'] == 'Production':
            rel = 4
        elif row['ReleasePhase'] == 'User Acceptance':
            rel = 3
        else:
            rel = 1

        return pow(sev * rel,2)


    def getAllBug(self):
        with self.engine.connect() as connection:
            lastCycle = str(pd.read_sql("select max(IDX) from sq.dim_refresh_history",connection).iat[0,0])
            print(lastCycle)
            min = int(lastCycle) -2
            sql_str = ("select iss.project Project, iss.issueKey_RC, iss.issuetype IssueType, iss.issue_key IssueKey, iss.\"bug classification\" BugClassification," +
                " iss.\"release phase\" ReleasePhase, iss.created Created, " +
                " iss.severity Severity, vs.name ReleaseName, vs.releaseDate ReleaseDate, " +
                " sq.squad Squad " +
                " from sq.fact_ji_issues iss " +
                " LEFT OUTER JOIN sq.fact_ji_squads sq  on sq.issueKey_RC = iss.issueKey_RC " +
                " LEFT JOIN sq.fact_ji_versions vs on vs.issueKey_RC = iss.issueKey_RC " +
                " where iss.project in ('SLS Agile', 'STAR Platform', 'WebClaims', 'MDM ADM') " +
                " and iss.Refresh_Cycle between " + str(min) + " and "  + lastCycle + " ")
            print(sql_str)
            
            
            allBugs = pd.read_sql(sql_str ,connection)
        
        # adding further statistic fields to simplify reporting.
        allBugs['year'] = pd.to_datetime(allBugs['Created']).dt.year  
        allBugs['sevScore'] = allBugs.apply(loadIssuse4Release.sevScore, axis=1)
        allBugs['severity_val'] = allBugs.apply(loadIssuse4Release.SevMapping, axis=1)
        allBugs['releaseP_val'] = allBugs.apply(loadIssuse4Release.RelPMapping, axis=1)

        allBugs.to_sql('etl_bugs_stats', con=self.engine, schema='SQ',chunksize=2000, index=False, if_exists='append')

        print(allBugs.isnull().sum())
        print(allBugs.head())


        filt_gen_22 =( 
         (allBugs['IssueType'] == 'Bug') &
         (allBugs['year'] >= 2020)) 

        bugAgg = allBugs.groupby(['Project','IssueType','ReleasePhase','Squad','Severity','ReleaseName'], as_index=False).agg({'IssueType': 'count','Severity': 'count'})
        bugAgg.to_sql('etl_bugs_agg', con=self.engine, schema='SQ',chunksize=2000, index=False, if_exists='append')
        print(bugAgg.head())
        
        sn.displot(data=allBugs[filt_gen_22], col='Project', col_wrap=4, x ="sevScore", hue="year", fill=True, facet_kws={'sharey': False, 'sharex': False},kind="kde",  aspect=1.5, alpha=0.2)
        print(allBugs.head())
        plt.xlabel('Severity Score')

        plt.show()


xx = loadIssuse4Release()
xx.getAllBug()