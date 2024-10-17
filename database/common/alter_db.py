from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, BIGINT, Boolean, DATETIME, PrimaryKeyConstraint, ForeignKeyConstraint, exc, text
from connect import connectDB
from jira_tabs import jira_tabs


class alter_db(connectDB):
    m = MetaData()
    
    def __init__(self, env, db):
        m = self.m
        super().__init__(env, db)

        query = f'ALTER TABLE sq.fact_ji_issues add squad VARCHAR(100);'

        with self.engine.connect() as conn:
            try:
                conn.execute(text(query))
                conn.commit()
            except Exception as e:
                print(e)

