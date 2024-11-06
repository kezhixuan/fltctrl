import pandas as pd
import pytest
from sqlalchemy import text

from database.common.connect import connectDB

# Unit Test Class for the Database connection handling.
class TestconnectDB():
    env = "FC_Test"
    localTest = "fc_db"
    jira = "jira_gilds"

    def test_connection(self):
        # Configure Database connnection
        ############## end Database Connection Configuration ##################
        # create and establish a database session
        db =connectDB(self.env, self.localTest)

        query = f'select 1'
        with db.engine.connect() as conn:
            try:
                conn.execute(text(query))
                conn.commit()
                success = True
            except Exception as e:
                print(e)
        assert success is True

#tc = TestconnectDB()
#tc.test_connection()