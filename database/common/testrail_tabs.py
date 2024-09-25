from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, BIGINT, Boolean, DATETIME, PrimaryKeyConstraint, ForeignKeyConstraint
from connect import engine
from jira_tabs import dim_sq_config

m = MetaData()

dim_tr_case_types = Table('dim_case_type',m,
    Column('id', BIGINT, primary_key=True),
    Column('is_default', Boolean),
    Column('name', VARCHAR(None)),
    schema="SQ"
    )

dim_tr_cases = Table('dim_cases', m,
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
    ForeignKeyConstraint(["project_RC"],dim_sq_config.primary_key,use_alter=True,name="fk_tr_cases_sq_config"),
    ForeignKeyConstraint(["type_id"],dim_tr_case_types.primary_key,use_alter=True,name="fk_tr_case_type_sq_config"),
    schema="SQ")

fact_tr_run = Table('fact_run', m,
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
    ForeignKeyConstraint(["project_RC"],dim_sq_config.primary_key,use_alter=True,name="fk_tr_run_sq_config"),
    ForeignKeyConstraint(["Refresh_Cycle"],["SQ.dim_refresh_history.IDX"], use_alter=True, name="fk_index_refresh_hist" ),
    ForeignKeyConstraint(["case_id"],dim_tr_cases.primary_key,use_alter=True,name="fk_tr_case_sq_config"),
    schema="SQ")

fact_tr_result = Table('fact_result', m,
    Column('id', BIGINT) ,
    Column('runid_RC', BIGINT) ,
    Column('tester', VARCHAR(None)) ,
    Column('result', VARCHAR(None)) ,
    Column('run_date', DATETIME) ,
    Column('Refresh_Cycle', BIGINT),
    Column('project_RC', VARCHAR(200)),
    ForeignKeyConstraint(["runid_RC"],fact_tr_run.primary_key,use_alter=True,name="fk_tr_result_sq_config"),
    schema="SQ")

m.create_all(bind=engine)

