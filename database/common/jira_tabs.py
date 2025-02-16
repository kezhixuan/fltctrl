from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    VARCHAR,
    BIGINT,
    Boolean,
    DATETIME,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
)
from database.common.connect import connectDB


class jira_tabs(connectDB):
    m = MetaData()

    def __init__(self, env, db):
        m = self.m
        super().__init__(env, db)

        m.create_all(bind=self.engine)

    dim_refresh_history = Table(
        "dim_refresh_history",
        m,
        Column("index", BIGINT),
        Column("IDX", BIGINT, primary_key=True),
        Column("SysJi1", VARCHAR(None)),
        Column("SysJi2", VARCHAR(None)),
        Column("SysJi3", VARCHAR(None)),
        Column("SysTr1", VARCHAR(None)),
        Column("RefreshDate", DATETIME),
        schema="SQ",
    )

    dim_sq_config = Table(
        "dim_sq_config",
        m,
        Column("refresh_active", VARCHAR(None)),
        Column("jira_system", VARCHAR(None)),
        Column("jira_id", VARCHAR(None)),
        Column("jira_project", VARCHAR(200)),
        Column("jira_project_name", VARCHAR(None)),
        Column("project_name", VARCHAR(200)),
        Column("issue_types", VARCHAR(None)),
        Column("report_start_date", VARCHAR(None)),
        Column("topic_id", VARCHAR(None)),
        Column("issues_system", BIGINT),
        Column("itdomain", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        Column("project_RC", VARCHAR(200), primary_key=True),
        schema="SQ",
    )

    dim_releases = Table(
        "dim_ji_releases",
        m,
        Column("self", VARCHAR(None)),
        Column("id", VARCHAR(50)),
        Column("name", VARCHAR(None)),
        Column("archived", Boolean),
        Column("released", Boolean),
        Column("releaseDate", DATETIME),
        Column("userReleaseDate", VARCHAR(None)),
        Column("projectId", BIGINT),
        Column("description", VARCHAR(None)),
        Column("startDate", DATETIME),
        Column("userStartDate", VARCHAR(None)),
        Column("project", VARCHAR(200)),
        Column("overdue", Boolean),
        Column("Refresh_Cycle", BIGINT),
        Column("project_RC", VARCHAR(200)),
        ForeignKeyConstraint(
            ["project_RC"],
            ["SQ.dim_sq_config.project_RC"],
            use_alter=True,
            name="fk_release_sq_config",
        ),
        schema="SQ",
    )

    fact_issues = Table(
        "fact_ji_issues",
        m,
        Column("index", BIGINT),
        Column("id", VARCHAR(50)),
        Column("issue_key", VARCHAR(None)),
        Column("summary", VARCHAR(None)),
        Column("statuscategorychangedate", DATETIME),
        Column("issuetype", VARCHAR(None)),
        Column("creator", VARCHAR(None)),
        Column("severity", VARCHAR(None)),
        Column("created", DATETIME),
        Column("bug classification", VARCHAR(None)),
        Column("project", VARCHAR(50)),
        Column("jira_key", VARCHAR(200)),
        Column("priority", VARCHAR(200)),
        Column("release phase", VARCHAR(None)),
        Column("duedate", DATETIME),
        Column("updated", DATETIME),
        Column("status", VARCHAR(None)),
        Column("defect_age", VARCHAR(None)),
        Column("affected version", VARCHAR(None)),
        Column("issueKey_RC",VARCHAR(50)),
        Column("project_RC", VARCHAR(200)),
        Column("fixVersions", VARCHAR(50)),
        Column("labels", VARCHAR(None)),
        Column("versions", VARCHAR(50)),
        Column("components", VARCHAR(50)),
        Column("squads", VARCHAR(50)),
        Column("sims_demand_category", VARCHAR(None)),
        Column("affected versions", VARCHAR(None)),
        Column("environment", VARCHAR(None)),
        Column("parent", VARCHAR(None)),
        Column("resolution", VARCHAR(None)),
        Column("assignee", VARCHAR(None)),
        Column("reporter", VARCHAR(None)),
        Column("security", VARCHAR(None)),
        Column("progress", VARCHAR(None)),
        Column("resolutiondate", DATETIME),
        Column("timeoriginalestimate", VARCHAR(None)),
        Column("description", VARCHAR(None)),
        Column("timeestimate", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        ForeignKeyConstraint(
            ["Refresh_Cycle"],
            ["SQ.dim_refresh_history.IDX"],
            use_alter=True,
            name="fk_index_refresh_hist",
        ),
        ForeignKeyConstraint(
            ["project_RC"],
            ["SQ.dim_sq_config.project_RC"],
            use_alter=True,
            name="fk_issues_sq_config",
        ),
        ForeignKeyConstraint(
            ["components"],
            ["SQ.dim_ji_components.component_id"],
            use_alter=True,
            name="fk_issues_components",
        ),
        ForeignKeyConstraint(
            ["fixVersions"],
            ["SQ.dim_ji_fixversions.fixversion_id"],
            use_alter=True,
            name="fk_issues_fixversions",
        ),
        ForeignKeyConstraint(
            ["versions"],
            ["SQ.dim_ji_versions.version_id"],
            use_alter=True,
            name="fk_issues_versions",
        ),
        ForeignKeyConstraint(
            ["squads"],
            ["SQ.dim_ji_squads.squad_id"],
            use_alter=True,
            name="fk_issues_squads",
        ),
        schema="SQ",
    )

    dim_ji_versions = Table(
        "dim_ji_versions",
        m,
        Column("version_id", VARCHAR(50), primary_key=True),
        Column("self", VARCHAR(None)),
        Column("description", VARCHAR(None)),
        Column("name", VARCHAR(None)),
        Column("archived", Boolean),
        Column("released", Boolean),
        Column("releaseDate", DATETIME),
        Column("issue_key", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        Column("issueKey_RC", VARCHAR(50)),
        schema="SQ",
    )

    dim_ji_fixversions = Table(
        "dim_ji_fixversions",
        m,
        Column("fixversion_id", VARCHAR(50), primary_key=True),
        Column("self", VARCHAR(None)),
        Column("description", VARCHAR(None)),
        Column("name", VARCHAR(None)),
        Column("archived", Boolean),
        Column("released", Boolean),
        Column("releaseDate", DATETIME),
        Column("issue_key", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        Column("issueKey_RC", VARCHAR(50)),
        schema="SQ",
    )

    dim_ji_components = Table(
        "dim_ji_components",
        m,
        Column("self", VARCHAR(None)),
        Column("component_id", VARCHAR(50), primary_key=True),
        Column("name", VARCHAR(None)),
        Column("issue_key", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        Column("issueKey_RC", VARCHAR(50)),
        schema="SQ",
    )

    dim_ji_squads = Table(
        "dim_ji_squads",
        m,
        Column("squad_id", VARCHAR(50), primary_key=True),
        Column("issueKey_RC", VARCHAR(50)),
        Column("squad", VARCHAR(None)),
        Column("issue_key", VARCHAR(None)),
        Column("Refresh_Cycle", BIGINT),
        schema="SQ",
    )
