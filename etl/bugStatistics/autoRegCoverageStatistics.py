import seaborn as sn
import matplotlib.pyplot as plt
import sys
import pandas as pd
from database.common.connect import connectDB
from sqlalchemy import create_engine, text, MetaData, schema, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base


class regressionCoverage(connectDB):
    env = []
    localTest = []
    conDB = []

    def __init__(self):
        super().__init__(sys.argv[1], sys.argv[2])
        pass

    def getRegressionCases(self):
        with self.engine.connect() as connection:
            lastCycle = str(
                pd.read_sql(
                    "select max(IDX) from sq.dim_refresh_history", connection
                ).iat[0, 0]
            )
            print(lastCycle)
            sql_str = (
                "select count(tc.id), tc.projectJI, tc.custom_automated, tc.custom_regressiontype  "
                + " from sq.dim_tr_cases tc where tc.custom_automated in (1) "
                + " and tc.custom_regressiontype = 1 "
                + " and tc.Refresh_Cycle = "
                + lastCycle
                + ""
                + " group by tc.projectJI, tc.custom_regressiontype, tc.custom_automated "
            )
            print(sql_str)
            sql_all = (
                "select tc.projectJI, tc.custom_automated, tc.custom_regressiontype, tc.id"
                + " from sq.dim_tr_cases tc "
                + " where tc.Refresh_Cycle = "
                + lastCycle
            )

            RegressAutomate = pd.read_sql(sql_str, connection)

            allRegressAutomate = pd.read_sql(sql_all, connection)
            print(allRegressAutomate)

            print(allRegressAutomate.groupby(["projectJI", "custom_automated"]).count())


if __name__ == "__main__":
    reg = regressionCoverage()
    reg.getRegressionCases()
