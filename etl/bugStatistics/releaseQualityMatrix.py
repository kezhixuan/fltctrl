#import numpy as np
#import seaborn as sn
#import matplotlib.pyplot as plt
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
        if row['severity'] == 'Major':
            sev = 3
        elif row['severity'] == 'Blocker':
            sev = 4
        elif row['severity'] == 'Minor':
            sev = 2
        else:
            sev = 1
        return sev

    def RelPMapping(row):
        if row['release phase'] == 'Functional Acceptance':
            rel = 2
        elif row['release phase'] == 'Production':
            rel = 4
        elif row['release phase'] == 'User Acceptance':
            rel = 3
        else:
            rel = 1
        return rel

    def sevScore(row):
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


    def getAllBug(self):
        with self.engine.connect() as connection:
            lastCycle = str(pd.read_sql("select max(IDX) from sq.dim_refresh_history",connection).iat[0,0])
            print(lastCycle)
            min = int(lastCycle) -7
            sql_str = "select * from sq.fact_ji_issues iss,sq.fact_ji_versions vs where iss.project in ('SLS Agile', 'GRIP', 'WWSCL') and iss.Refresh_Cycle between " + lastCycle + " and " + str(min) + " and iss.issuekey_RC=vs.issuekey_RC"
            allBugs = pd.read_sql(sql_str ,connection)

            sql_squad = "select * from sq.fact_ji_squads squad where squad.Refresh_Cycle between " + lastCycle + " and " + str(min)
            allSquads = pd.read_sql(sql_squad,connection)


        aggBugs = allBugs[['issue_key','issuetype','bug classification','severity','priority','project','created','release phase','name','releaseDate','issueKey_RC']].copy()
        print(aggBugs.isnull().sum())
        print(aggBugs.head())

        print(allSquads.head())

        aggBugs['year'] = pd.to_datetime(aggBugs['created']).dt.year  
        aggBugs['sevScore'] = aggBugs.apply(loadIssuse4Release.sevScore, axis=1)
        aggBugs['severity_val'] = aggBugs.apply(loadIssuse4Release.SevMapping, axis=1)
        aggBugs['releaseP_val'] = aggBugs.apply(loadIssuse4Release.RelPMapping, axis=1)

        filt_gen_22 =( 
         (aggBugs['issuetype'] == 'Bug') &
         (aggBugs['year'] >= 2020)) 

        bugAgg = aggBugs.groupby(['project','issuetype','severity','name'], as_index=False).agg({'issuetype': 'count','severity': 'count'})

        print(bugAgg.head())
        
#        sn.displot(data=aggBugs[filt_gen_22], col='project', col_wrap=3, x ="sevScore", hue="year", fill=True, facet_kws={'sharey': False, 'sharex': False},kind="kde",  aspect=1.5, alpha=0.2)
#        print(aggBugs.head())
#        plt.xlabel('Severity Score')

#        plt.show()


xx = loadIssuse4Release()
xx.getAllBug()