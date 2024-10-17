from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, BIGINT, Boolean, DATETIME, PrimaryKeyConstraint, ForeignKeyConstraint
from connect import connectDB
from jira_tabs import jira_tabs



class testrail_tabs (connectDB):
        m = MetaData()
        
        def __init__(self,env, db):
            m = self.m
            super().__init__(env, db)

            dim_tr_case_types = Table('dim_tr_case_type',m,
                Column('id', BIGINT, primary_key=True),
                Column('is_default', Boolean),
                Column('name', VARCHAR(None)),
                schema="SQ"
                )

            dim_tr_cases = Table('dim_tr_cases', m,
                Column('id', BIGINT) ,
                Column('title', VARCHAR(None)) ,
                Column('section_id', BIGINT) ,
                Column('template_id', BIGINT) ,
                Column('type_id', BIGINT) ,
                Column('priority_id', BIGINT) ,
                Column('milestone_id', BIGINT) ,
                Column('refs', VARCHAR(None)) ,
                Column('created_by', BIGINT) ,
                Column('created_on', DATETIME) ,
                Column('updated_by', BIGINT) ,
                Column('updated_on', DATETIME),
                Column('estimate', BIGINT) ,
                Column('estimate_forecast', VARCHAR(None)),
                Column('suite_id', BIGINT) ,
                Column('display_order', BIGINT) ,
                Column('is_deleted', Boolean) ,
                Column('custom_automation_type', BIGINT) ,
                Column('custom_preconds', VARCHAR(None)) ,
                Column('custom_steps', VARCHAR(None)) ,
                Column('custom_expected', VARCHAR(None)) ,
                Column('custom_steps_separated', VARCHAR(None)) ,
                Column('custom_mission', VARCHAR(None)) ,
                Column('custom_goals', VARCHAR(None)) ,
                Column('Refresh_Cycle', BIGINT),
                Column('project_RC', VARCHAR(200)),
                Column('caseId_RC', BIGINT, primary_key=True),
                ForeignKeyConstraint(["project_RC"],jira_tabs.dim_sq_config.primary_key,use_alter=True,name="fk_tr_cases_sq_config"),
                ForeignKeyConstraint(["type_id"],dim_tr_case_types.primary_key,use_alter=True,name="fk_tr_case_type_sq_config"),
                schema="SQ")

            fact_tr_run = Table('fact_tr_run', m,
                Column('id', BIGINT) ,
                Column('runid_RC', BIGINT, primary_key=True) ,
                Column('case_id', BIGINT) ,
                Column('milestone_id', BIGINT) ,
                Column('submilestone_id', BIGINT) ,
                Column('run_name', VARCHAR(None)) ,
                Column('created_by', BIGINT) ,
                Column('created_on', DATETIME) ,
                Column('status', VARCHAR(200)),
                Column('Refresh_Cycle', BIGINT),
                Column('project_RC', VARCHAR(200)),
                Column('caseId_RC', BIGINT),
                ForeignKeyConstraint(["project_RC"],jira_tabs.dim_sq_config.primary_key,use_alter=True,name="fk_tr_run_sq_config"),
                ForeignKeyConstraint(["Refresh_Cycle"],jira_tabs.dim_refresh_history.primary_key, use_alter=True, name="fk_tr_run_index_refresh_hist" ),
                ForeignKeyConstraint(["caseId_RC"],dim_tr_cases.primary_key,use_alter=True,name="fk_tr_case_sq_config"),
                schema="SQ")

            fact_tr_result = Table('fact_tr_result', m,
                Column('id', BIGINT) ,
                Column('runid_RC', BIGINT) ,
                Column('tester', VARCHAR(None)) ,
                Column('result', VARCHAR(None)) ,
                Column('run_date', DATETIME) ,
                Column('Refresh_Cycle', BIGINT),
                Column('project_RC', VARCHAR(200)),
                ForeignKeyConstraint(["runid_RC"],fact_tr_run.primary_key,use_alter=True,name="fk_tr_result_sq_config"),
                schema="SQ")

            m.create_all(bind=self.engine)

