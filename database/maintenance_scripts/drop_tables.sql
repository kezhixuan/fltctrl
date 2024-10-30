-- Delete all jira tables --
drop table sq.fact_ji_squads
drop table sq.fact_ji_fixversions
drop table sq.fact_ji_labels
drop table sq.fact_ji_components
drop table sq.fact_ji_versions
drop table sq.fact_ji_issues
drop table sq.dim_ji_releases

-- Delete TestRail Tables --
drop table sq.fact_tr_result
drop table sq.fact_tr_run
drop table sq.dim_tr_case_type
drop table sq.dim_tr_cases

-- Delete config tables
drop table sq.dim_refresh_history
drop table sq.dim_sq_config