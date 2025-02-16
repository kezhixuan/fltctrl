import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from unittest import mock
from sqlalchemy import engine
import codecs
import src.dataSource.testrail.ConnectTestRail as testr


class TestConnectTestRail:

    #  def setUp(self):
    #      self.monkeypatch = mock.MonkeyPatch()
    #      self.monkeypatch.setattr(sys.argv[1], 'FC_Test')
    #      self.monkeypatch.setattr(sys.argv[2], 'fc_db')
    #      self.monkeypatch.setattr(sys.argv[3], 'jira_tsc')

    # def test_getTestRailData(self):
    #        testargs = ["FC_Test", "jira_tsc"]
    #        with mock.patch('sys.argv') as mock_sys:
    #            print(mock_sys)

    #       with mock.patch('database.common.connect.connectDB.write2DB') as mock_create_engine:
    #           # Mock für die Session
    #           mock_engine = mock_create_engine.return_value
    #           mock_session = mock.MagicMock()
    #          mock_engine.connect.return_value = mock_session

    # Beispiel-Daten
    #         mock_proj = mock.MagicMock()
    #         mock_proj = 4
    #         mock_session.query.return_value.filter_by.return_value.first.return_value = mock_proj

    #         con2 =  c2s.Connect2Sqlserver()
    #         con2.getTestRailData(self)

    #    assert testr.empty is False

    def getData(self):
        data = {
            "caseID_RC": ["12334-4"],
            "id": [123],
            "refs": [
                "GCT-3424, GCT-3426, GCT-3485, GCT-3455, GCT-3603, GCT-3604, GCT-3629, GCT-3696, GCT-3697, GCT-3782, GCT-3816, GCT-3888, GCT-3889, GCT-3891, GCT-3938, GCT-4027, GCT-4028, GCT-4095, GCT-4107, GCT-4163, GCT-4233, GCT-4234, GCT-4236, GCT-4284, GCT-4285, GCT-4307, GCT-4286"
            ],
        }
        testData = pd.DataFrame(data)

        return testData

    # Testfall mit unittest.mock
    def test_store_case_refs(self):
        connData = pd.read_json(codecs.open("FC_Test" + ".json", "r", "utf-8"))
        self.testrailCon = connData["testrail"]
        # Mock für create_engine
        # with mock.patch('sqlalchemy.create_engine') as mock_create_engine:
        # Beispiel-Daten
        mock_refs = mock.MagicMock()
        mock_refs = self.getData()

        ctr = testr.ConnectTestRail(self.testrailCon)
        print(mock_refs)

        result = ctr.extract_case_refs(mock_refs)

        # print(result)
        # Überprüfen, ob das Ergebnis korrekt ist
        assert True == True
