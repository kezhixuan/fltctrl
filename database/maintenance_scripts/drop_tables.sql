-- Delete all jira tables --
drop table sq.fact_ji_squads
drop table sq.fact_ji_fixversions
drop table sq.fact_ji_labels
drop table sq.fact_ji_components
drop table sq.fact_ji_versions
drop table sq.fact_ji_issues
drop table sq.dim_ji_releases

-- Delete TestRail Tables --
drop table sq.fact_tr_tests
drop table sq.fact_tr_runs

drop table sq.dim_tr_cases
drop table sq.dim_tr_case_types
drop table sq.fact_case_fields
drop table sq.fact_groups
drop table sq.fact_results
drop table sq.fact_tr_section
drop table sq.fact_suites
drop table sq.fact_users
drop table sq.dim_tr_projects
DROP TABLE sq.fact_tr_suites
drop table sq.fact_tr_users

drop table sq.fact_tr_groups
drop table sq.fact_tr_case_fields
drop table sq.dim_tr_case_types
drop table sq.dim_tr_cases
drop table sq.dim_tr_projects

-- Delete ETL Tables
drop table sq.etl_bugs_agg
drop table sq.etl_bugs_stats

-- Delete config tables
drop table sq.dim_refresh_history
drop table sq.dim_sq_config