import codecs
import json
import pandas as pd

class columnHandling:

    def __init__ (self):
        pass
#                "Defect Age",
#                "sls_squad
#"customfield_14455",
#"customfield_11095"
    def consolidateCutomFields(self,dfCore):
        # fields.customfield_19890 --> severity
        # fields.customfield_20083 --> severity_IRE
        # fields.customfield_20005 --> severity_ATD
        # fields.customfield_20118 --> severity_GPIS
        # fields.customfield_11106 --> seveirty_GILDS
        if 'severity' not in dfCore.columns:
            if("fields.customfield_19890.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_19890.value': 'severity'}, inplace= True )                
            elif("fields.customfield_20083.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20083.value': 'severity'}, inplace= True )
            elif("fields.customfield_20118.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20118.value': 'severity'}, inplace= True )
            elif("fields.customfield_20005.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20005.value': 'severity'}, inplace= True )
            elif("fields.customfield_11106.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_11106.value': 'severity'}, inplace= True )
        # fields.customfield_19900 --> release_phase
        # fields.customfield_20081 --> release_phase_IRE
        # fields.customfield_20003 --> release_phase_ATD
        # fields.customfield_20128 --> release_phase_GPIS
        # fields.customfield_11107 --> release_phase_GILDS
        if 'release phase' not in dfCore.columns:
            if("fields.customfield_19900.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_19900.value': 'release phase'}, inplace= True )
            elif("fields.customfield_20081.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20081.value': 'release phase'}, inplace= True )
            elif("fields.customfield_20003.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20003.value': 'release phase'}, inplace= True )
            elif("fields.customfield_20128.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20128.value': 'release phase'}, inplace= True )
            elif("fields.customfield_11107.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_11107.value': 'release phase'}, inplace= True )
        # fields.customfield_19901 --> bug_classification
        # fields.customfield_20080 --> bug_classification_IRE
        # fields.customfield_20004 --> bug_classification_ATD
        # fields.customfield_20129 --> bug_classification_GPIS
        # fields.customfield_11487 --> bug_classification_GILDS
        if 'bug classification' not in dfCore.columns:
            if("fields.customfield_19901.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_19901.value': 'bug classification'}, inplace= True )                
            elif("fields.customfield_20080.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20080.value': 'bug classification'}, inplace= True )
            elif("fields.customfield_2004.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20004.value': 'bug classification'}, inplace= True )
            elif("fields.customfield_2129.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_20129.value': 'bug classification'}, inplace= True )
            elif("fields.customfield_11487.value" in dfCore.columns):
                dfCore.rename(columns= {'fields.customfield_11487.value': 'bug classification'}, inplace= True )
        return dfCore
    
    def cleanColumnNames(self, project, dfCore, dfSatelite):

        dfCore.rename(columns= {'key': 'issue_key'}, inplace= True )
        dfCore.rename(columns= {'fields.issuetype.name': 'issuetype'}, inplace= True )
        dfCore.rename(columns= {'fields.project.name': 'project'}, inplace= True )
        dfCore.rename(columns= {'fields.project.key': 'jira_key'}, inplace= True )
        dfCore.rename(columns= {'fields.priority.name': 'priority'}, inplace= True )
        dfCore.rename(columns= {'fields.status.name': 'status'}, inplace= True )
        dfCore.rename(columns= {'fields.creator.displayName': 'creator'}, inplace= True )
        dfCore.rename(columns= {'fields.created': 'created'}, inplace= True )
        dfCore.rename(columns= {'fields.summary': 'summary'}, inplace= True )
        dfCore.rename(columns= {'fields.statuscategorychangedate': 'statuscategorychangedate'}, inplace= True )
        dfCore.rename(columns= {'fields.duedate': 'duedate'}, inplace= True )
        dfCore.rename(columns= {'fields.updated': 'updated'}, inplace= True )
        
        dfSatelite.rename(columns={'fields.labels': 'labels'}, inplace = True )
        dfSatelite.rename(columns={'fields.components': 'components'}, inplace = True )
        dfSatelite.rename(columns={'fields.fixVersions': 'fixVersions'}, inplace = True )
        dfSatelite.rename(columns={'fields.versions': 'versions'}, inplace = True )
        dfSatelite.rename(columns={'fields.project.name':'project'}, inplace = True )
        dfSatelite.rename(columns={'fields.customfield_11095':'squads'}, inplace = True)
        #dfSatelite.rename(columns={'fields.customfield_14162.id': 'customfield_14162.id'}, inplace = True )
        #dfSatelite.rename(columns={'fields.customfield_14162.name': 'customfield_14162.name'}, inplace = True )
        #dfSatelite.rename(columns={'fields.customfield_14162.archived': 'customfield_14162.archived'}, inplace = True )
        #dfSatelite.rename(columns={'fields.customfield_14162.released': 'customfield_14162.released'}, inplace = True )    
        #dfSatelite.rename(columns={'fields.customfield_14162.releaseDate': 'customfield_14162.releaseDate'}, inplace = True ) 

        if project == 'IRE':
            # IRE project has used costomfield 19900 and 20081 for release phase attribute.
            # latest use was 20081, and 19900 has been droped
            dfCore.drop('fields.customfield_19900.value', axis=1, inplace = True)
          

        for col in dfSatelite.filter(like="customfield").columns:
            try:
                dfSatelite.rename(columns= {col : str(col.lower().replace('fields.',''))}, inplace = True)
            except:
                print(f'field: ' + col + ' not found')
        
        dfCore = self.consolidateCutomFields(dfCore)
        
        return dfCore, dfSatelite
    
    