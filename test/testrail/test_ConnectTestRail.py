import pytest
import pandas as pd
from unittest.mock import Mock, patch
from unittest import mock
import Connect2Sqlserver as c2s
import src.dataSource.testrail.ConnectTestRail as testr
import sys



class TestConnectTestRail():

    def setUp(self):
        self.monkeypatch = mock.MonkeyPatch()
        self.monkeypatch.setattr(sys.argv[1], 'FC_Test')
        self.monkeypatch.setattr(sys.argv[2], 'fc_db')
        self.monkeypatch.setattr(sys.argv[3], 'jira_tsc')
    
    def test_getTestRailData(self):
#        testargs = ["FC_Test", "jira_tsc"]
#        with mock.patch('sys.argv') as mock_sys:
#            print(mock_sys)
           

            with mock.patch('database.common.connect.connectDB.write2DB') as mock_create_engine:
                # Mock für die Session
                mock_engine = mock_create_engine.return_value
                mock_session = mock.MagicMock()
                mock_engine.connect.return_value = mock_session

                        # Beispiel-Daten
                mock_proj = mock.MagicMock()
                mock_proj = 4
                mock_session.query.return_value.filter_by.return_value.first.return_value = mock_proj
                
                con2 =  c2s.Connect2Sqlserver()
                con2.getTestRailData(self)
                
                
            assert testr.empty is False
        
        

        