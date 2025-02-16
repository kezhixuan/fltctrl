from unittest.mock import Mock, patch
from unittest import mock
import pandas as pd
import numpy as np
from src.dataSource.atlassian import IssueSatelites as atl
from database.common.connect import connectDB
from sqlalchemy import engine

# Unit Test Class for the Database connection handling.


class TestconnectDB:

    def getData(self):
        testData = [
            [
                "280463",
                "LIN-10048",
                "LiNeS",
                [
                    {
                        "self": "vvvv",
                        "id": "17003",
                        "description": "",
                        "name": "2024-123 Release",
                        "archived": False,
                        "released": False,
                    }
                ],
            ]
        ]
        Data_type = object

        np_array = np.array(testData, dtype=Data_type)
        return pd.DataFrame(np_array, columns=["id", "key", "components", "versions"])

        # Testfall mit unittest.mock

    def test_IssueSatelites(self):
        # Mock für create_engine
        # with mock.patch('sqlalchemy.create_engine') as mock_create_engine:
        with mock.patch(
            "database.common.connect.connectDB.write2DB"
        ) as mock_create_engine:
            # Mock für die Session
            mock_engine = mock_create_engine.return_value
            mock_session = mock.MagicMock()
            mock_engine.connect.return_value = mock_session

            # Beispiel-Daten
            mock_issue = mock.MagicMock()
            mock_issue = self.getData()
            mock_session.query.return_value.filter_by.return_value.first.return_value = (
                mock_issue
            )

            # Aufruf der zu testenden Funktion

            res = atl.IssueSatelites(mock_issue, "project", engine, 600)

            # print(result)
            # Überprüfen, ob das Ergebnis korrekt ist
            assert res.status == True
