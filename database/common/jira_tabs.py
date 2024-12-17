from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, BIGINT, Boolean, DATETIME, PrimaryKeyConstraint, ForeignKeyConstraint
from database.common.connect import connectDB


class jira_tabs(connectDB):
        m = MetaData()
        


        def __init__(self, env, db):
                m = self.m
                super().__init__(env, db)

                m.create_all(bind=self.engine)

        dim_refresh_history = Table('dim_refresh_history', m,
                        Column('index', BIGINT),
                        Column('IDX', BIGINT, primary_key=True),
                        Column('SysJi1', VARCHAR(None)),
                        Column('SysJi2', VARCHAR(None)),
                        Column('SysJi3', VARCHAR(None)),
                        Column('SysTr1', VARCHAR(None)),
                        Column('RefreshDate', DATETIME),
                        schema="SQ")

                

        dim_sq_config = Table('dim_sq_config', m,
                        Column('refresh_active', VARCHAR(None)),
                        Column('jira_system', VARCHAR(None)),
                        Column('jira_id', VARCHAR(None)),
                        Column('jira_project', VARCHAR(200)),
                        Column('jira_project_name', VARCHAR(None)),
                        Column('project_name', VARCHAR(200)),
                        Column('issue_types', VARCHAR(None)),
                        Column('report_start_date', VARCHAR(None)),
                        Column('topic_id', VARCHAR(None)) ,
                        Column('issues_system', BIGINT), 
                        Column('itdomain', VARCHAR(None)),
                        Column('Refresh_Cycle', BIGINT), 
                        Column('project_RC', VARCHAR(200), primary_key=True),
                        schema="SQ")
               

        dim_releases = Table('dim_ji_releases', m,
                Column('self', VARCHAR(None)) ,
                Column('id', BIGINT) ,
                Column('name', VARCHAR(None)),
                Column('archived', Boolean) ,
                Column('released', Boolean) ,
                Column('releaseDate', DATETIME) ,
                Column('userReleaseDate', VARCHAR(None)) ,
                Column('projectId', BIGINT), 
                Column('description', VARCHAR(None)),
                Column('startDate', DATETIME),
                Column('userStartDate', VARCHAR(None)) ,
                Column('project', VARCHAR(200)) ,
                Column('overdue', Boolean) ,
                Column('Refresh_Cycle', BIGINT),
                Column('project_RC', VARCHAR(200)),
                ForeignKeyConstraint(["project_RC"],["SQ.dim_sq_config.project_RC"],use_alter=True,name="fk_release_sq_config"),
                schema="SQ")

        fact_issues = Table('fact_ji_issues', m,
                Column('index', BIGINT),
                Column('id', BIGINT),
                Column('issue_key', VARCHAR(None) ),
                Column('summary', VARCHAR(None) ),
                Column('statuscategorychangedate', DATETIME),
                Column('issuetype', VARCHAR(None) ),
                Column('creator', VARCHAR(None) ),
                Column('severity', VARCHAR(None) ),
                Column('created', DATETIME),
                Column('bug classification', VARCHAR(None) ),
                Column('project', VARCHAR(50)),
                Column('jira_key', VARCHAR(200)),
                Column('priority', VARCHAR(200) ),
                Column('release phase', VARCHAR(None) ),
                Column('duedate', DATETIME),
                Column('updated', DATETIME),
                Column('status', VARCHAR(None) ),
                Column('defect_age', VARCHAR(None) ),
                Column('affected version', VARCHAR(None) ),
                Column('issueKey_RC', VARCHAR(50), primary_key=True),
                Column('project_RC', VARCHAR(200)),
                Column('fixed versions', VARCHAR(None) ),
                Column('sims_demand_category', VARCHAR(None) ),
                Column('affected versions', VARCHAR(None) ),
                Column('environment', VARCHAR(None) ),
                Column('parent', VARCHAR(None) ),
                Column('resolution', VARCHAR(None) ),
                Column('assignee', VARCHAR(None) ),
                Column('reporter', VARCHAR(None) ),
                Column('security', VARCHAR(None) ),
                Column('progress', VARCHAR(None) ),
                Column('resolutiondate', DATETIME),
                Column('timeoriginalestimate', VARCHAR(None) ),
                Column('description', VARCHAR(None) ),
                Column('timeestimate', VARCHAR(None) ),
                Column('Refresh_Cycle', BIGINT),
                ForeignKeyConstraint(["Refresh_Cycle"],["SQ.dim_refresh_history.IDX"], use_alter=True, name="fk_index_refresh_hist" ),
                ForeignKeyConstraint(["project_RC"],["SQ.dim_sq_config.project_RC"],use_alter=True,name="fk_issues_sq_config"),
                schema="SQ")

        fact_versions = Table('fact_ji_versions', m,
                Column('self', VARCHAR(None)),
                Column('id', BIGINT),
                Column('description', VARCHAR(None)),
                Column('name', VARCHAR(None)),
                Column('archived', Boolean),
                Column('released', Boolean),
                Column('releaseDate', DATETIME),
                Column('issue_key', VARCHAR(None)),
                Column('Refresh_Cycle', BIGINT),
                Column('issueKey_RC', VARCHAR(50)),
                ForeignKeyConstraint(["issueKey_RC"],["SQ.fact_ji_issues.issueKey_RC"], use_alter=True, name="fk_versions_issues"),
                schema="SQ")

        fact_fixversions = Table('fact_ji_fixversions', m,
                Column('self', VARCHAR(None)),
                Column('id', BIGINT),
                Column('description', VARCHAR(None)),
                Column('name', VARCHAR(None)),
                Column('archived', Boolean),
                Column('released', Boolean),
                Column('releaseDate', DATETIME),
                Column('issue_key', VARCHAR(None)),
                Column('Refresh_Cycle', BIGINT),
                Column('issueKey_RC', VARCHAR(50)),
                ForeignKeyConstraint(["issueKey_RC"],["SQ.fact_ji_issues.issueKey_RC"], use_alter=True, name="fk_fixversions_issues"),
                schema="SQ")


        fact_components = Table('fact_ji_components', m,
                Column('self', VARCHAR(None)),
                Column('id', BIGINT),
                Column('name', VARCHAR(None)),
                Column('issue_key', VARCHAR(None)),
                Column('Refresh_Cycle', BIGINT),
                Column('issueKey_RC', VARCHAR(50)),
                ForeignKeyConstraint(["issueKey_RC"],["SQ.fact_ji_issues.issueKey_RC"], use_alter=True, name="fk_components_issues"),
                schema="SQ")

        fact_squads = Table('fact_ji_squads', m,
                Column('issueKey_RC', VARCHAR(50)),
                Column('squad', VARCHAR(None)),
                Column('issue_key', VARCHAR(None)),
                Column('Refresh_Cycle', BIGINT),
                ForeignKeyConstraint(["issueKey_RC"],["SQ.fact_ji_issues.issueKey_RC"], use_alter=True, name="fk_squads_issues"),
                schema="SQ")
        
        fact_labels = Table('fact_ji_labels', m,
                Column('issueKey_RC', VARCHAR(50)),
                Column('label', VARCHAR(None)),
                Column('issue_key', VARCHAR(None)),
                Column('Refresh_Cycle', BIGINT),
                ForeignKeyConstraint(["issueKey_RC"],["SQ.fact_ji_issues.issueKey_RC"], use_alter=True, name="fk_labels_issues"),
                schema="SQ")

        
