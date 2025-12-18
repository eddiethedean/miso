"""
Comprehensive tests for analytics.py to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import json


class TestAnalyticsComprehensive:
    """Test analytics page with various filter combinations"""
    
    @pytest.fixture
    def sample_series_with_fy_quarter_map(self):
        """Sample series with fiscal year quarter map"""
        return [
            {
                "series_id": 1,
                "series_name": "Operation Alpha",
                "tsoc": "JSOC",
                "support_another_unit": True,
                "classification": "UNCLASS",
                "nds_threat": "NDS-PRC",
                "miso_program": "CTWMP",
                "target_audience_category": "Citizens",
                "fy_quarter_map": {"2023": ["FYQ1", "FYQ2"], "2024": ["FYQ1"]}
            },
            {
                "series_id": 2,
                "series_name": "Operation Bravo",
                "tsoc": "SOCAF",
                "support_another_unit": False,
                "classification": "S//NF",
                "nds_threat": "NDS-RUS",
                "miso_program": "DACMP",
                "target_audience_category": "Decision Makers",
                "fy_quarter_map": {"2023": ["FYQ3", "FYQ4"]}
            }
        ]
    
    def test_analytics_page_with_all_filters(self, test_db, mock_session_state):
        """Test analytics page with all filter options enabled"""
        import streamlit as st
        import pandas as pd
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        test_script = """
import streamlit as st
import pandas as pd
import sqlite3
from modules.analytics import analytics_page

# Setup session state
st.session_state.conn = sqlite3.connect('test_miso.db', check_same_thread=False)
st.session_state.conn.row_factory = sqlite3.Row
st.session_state.iso3_country_map = {"AFG": "Afghanistan"}

# Mock the data pull functions to return test data
from unittest.mock import patch
import json

test_data = [
    {
        "series_id": 1,
        "series_name": "Test Operation",
        "tsoc": "JSOC",
        "support_another_unit": True,
        "classification": "UNCLASS",
        "nds_threat": "NDS-PRC",
        "miso_program": "CTWMP",
        "target_audience_category": "Citizens",
        "fy_quarter_map": {"2023": ["FYQ1"]}
    }
]

with patch('modules.analytics.pull_series_and_cyber_data', return_value=[test_data, []]):
    with patch('modules.analytics.pull_miso_assessments', return_value=[]):
        with patch('modules.analytics.pull_miso_executions', return_value=[]):
            with patch('modules.analytics.pull_other_threats', return_value=set()):
                with patch('modules.analytics.pull_other_miso_program', return_value=set()):
                    with patch('modules.analytics.pull_other_classifications', return_value=set()):
                        with patch('modules.analytics.pull_other_means', return_value=set()):
                            analytics_page()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render analytics page
        assert len(at.header) > 0 or len(at.tabs) > 0
    
    def test_analytics_table_with_filters(self):
        """Test analytics table generation with various filter combinations"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test with different filter combinations
series_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC", "support_another_unit": True},
    {"series_id": 2, "series_name": "Op2", "tsoc": "SOCAF", "support_another_unit": False}
]

# Test various filter types
count1 = how_many_of_type(series_data, "In Support", [], [], False, "", False)
count2 = how_many_of_type(series_data, "Not In Support", [], [], False, "", False)
count3 = how_many_of_type(series_data, "JSOC", [], [], False, "", False)

st.write(f"In Support: {count1}, Not In Support: {count2}, JSOC: {count3}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0
    
    def test_analytics_changes_table(self):
        """Test changes by quarter table generation"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test series name collection for changes table
series_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC"},
    {"series_id": 2, "series_name": "Op2", "tsoc": "JSOC"}
]

names = how_many_of_type(series_data, "JSOC", [], [], False, "", True)
st.write(f"Names: {names}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0

