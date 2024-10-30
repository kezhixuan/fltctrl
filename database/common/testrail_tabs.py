from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, BIGINT, Boolean, DATETIME, PrimaryKeyConstraint, ForeignKeyConstraint
from connect import connectDB
from jira_tabs import jira_tabs



class testrail_tabs (connectDB):
        m = MetaData()
        


        def __init__(self, env, db):
                m = self.m
                super().__init__(env, db)

                m.create_all(bind=self.engine)
        
        dim_tr_case_types = Table('dim_tr_case_types', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('caseID_RC', VARCHAR(200), primary_key=True),
            Column('type', VARCHAR(255)),
            Column('regression', Boolean),
            schema="SQ"
        )

        dim_tr_cases = Table('dim_cases', m,
            Column('id', BIGINT) ,
            Column('caseID_RC', VARCHAR(200), primary_key=True),
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
            ForeignKeyConstraint(["project_RC"],jira_tabs.dim_sq_config.primary_key,use_alter=True,name="fk_tr_cases_sq_config"),
            ForeignKeyConstraint(["caseID_RC"],dim_tr_case_types.primary_key,use_alter=True,name="fk_tr_case_type_sq_config"),
            schema="SQ")

        fact_tr_run = Table('fact_tr_run', m,
            Column('self', VARCHAR(None)),
            Column('id', BIGINT) ,
            Column('runid_RC', VARCHAR(200), primary_key=True) ,
            Column('caseID_RC', VARCHAR(200)) ,
            Column('milestone_id', BIGINT) ,
            Column('submilestone_id', BIGINT) ,
            Column('run_name', VARCHAR(None)) ,
            Column('created_by', BIGINT) ,
            Column('created_on', DATETIME) ,
            Column('status', VARCHAR(200)),
            Column('Refresh_Cycle', BIGINT),
            Column('project_RC', VARCHAR(200)),
            ForeignKeyConstraint(["project_RC"],jira_tabs.dim_sq_config.primary_key,use_alter=True,name="fk_tr_run_sq_config"),
            ForeignKeyConstraint(["Refresh_Cycle"],jira_tabs.dim_refresh_history.primary_key, use_alter=True, name="fk_tr_run_index_refresh_hist" ),
            ForeignKeyConstraint(["caseID_RC"],dim_tr_cases.primary_key,use_alter=True,name="fk_tr_case_id_run"),
            schema="SQ")

        fact_tr_results = Table('fact_results', m,
            Column('self', VARCHAR(None)),
            Column('id', BIGINT) ,
            Column('runid_RC', VARCHAR(200)) ,
            Column('caseID_RC', VARCHAR(200)),
            Column('tester', VARCHAR(None)) ,
            Column('result', VARCHAR(None)) ,
            Column('defect_id', VARCHAR(None)) ,
            Column('version', VARCHAR(None)) ,
            Column('run_date', DATETIME) ,
            Column('Refresh_Cycle', BIGINT),
            Column('project_RC', VARCHAR(200)),
            ForeignKeyConstraint(["runid_RC"], fact_tr_run.primary_key, use_alter=True, name="fk_tr_results_run"),
            ForeignKeyConstraint(["caseID_RC"], dim_tr_cases.primary_key, use_alter=True, name="fk_tr_results_case"),
            schema="SQ")

        # Create in 24/10/23 by Ken
        dim_tr_projects = Table('dim_projects', m,
            Column('id', BIGINT),
            Column('name', VARCHAR(200)),
            Column('projectID_RC', VARCHAR(200), primary_key=True),
            Column('project_RC', VARCHAR(200)),
            ForeignKeyConstraint(["project_RC"], jira_tabs.dim_sq_config.primary_key, use_alter=True, name="fk_tr_projects_sq_config"),
            schema="SQ"
        )

        fact_tr_case_fields = Table('fact_case_fields', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('caseID_RC', VARCHAR(200)),
            Column('priority', VARCHAR(255)),
            Column('automated', VARCHAR(255)),
            Column('security', VARCHAR(255)),
            Column('regression', VARCHAR(255)),
            # below is for ITDAO
            Column('test_data', VARCHAR(255)),
            Column('robot', VARCHAR(255)),
            Column('execution_type', VARCHAR(255)),
            Column('project_RC', VARCHAR(200)),
            ForeignKeyConstraint(["caseID_RC"], dim_tr_cases.primary_key, use_alter=True, name="fk_tr_case_fields_cases"),
            schema="SQ"
        )

        fact_tr_groups = Table('fact_groups', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('name', VARCHAR(255)),
            Column('role', VARCHAR(255)),
            Column('projectID_RC', VARCHAR(200)),
            ForeignKeyConstraint(["projectID_RC"], dim_tr_projects.primary_key, use_alter=True, name="fk_tr_groups_projects"),
            schema="SQ"
        )

        fact_tr_users = Table('fact_users', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('name', VARCHAR(255)),
            Column('group', VARCHAR(255)),
            Column('projectID_RC', VARCHAR(200)),
            ForeignKeyConstraint(["projectID_RC"], dim_tr_projects.primary_key, use_alter=True, name="fk_tr_users_projects"),
            schema="SQ"
        )

        fact_tr_suites = Table('fact_suites', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('name', VARCHAR(255)),
            Column('caseID_RC', VARCHAR(200)),
            Column('projectID_RC', VARCHAR(200)),
            ForeignKeyConstraint(["projectID_RC"], dim_tr_projects.primary_key, use_alter=True, name="fk_tr_suites_projects"),
            ForeignKeyConstraint(["caseID_RC"], dim_tr_cases.primary_key, use_alter=True, name="fk_tr_suites_cases"),
            schema="SQ"
        )

        fact_tr_section = Table('fact_section', m,
            Column('self', VARCHAR(255)),
            Column('id', BIGINT),
            Column('name', VARCHAR(255)),
            Column('caseID_RC', VARCHAR(200)),
            Column('projectID_RC', VARCHAR(200)),
            ForeignKeyConstraint(["projectID_RC"], dim_tr_projects.primary_key, use_alter=True, name="fk_tr_section_projects"),
            ForeignKeyConstraint(["caseID_RC"], dim_tr_cases.primary_key, use_alter=True, name="fk_tr_section_cases"),
            schema="SQ"
        )



