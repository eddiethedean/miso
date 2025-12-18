"""
Integration tests for analytics page to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import json
import sqlite3


class TestAnalyticsIntegration:
    """Integration tests for analytics page"""
    
    def test_analytics_full_flow_with_filters(self, test_db, mock_session_state):
        """Test full analytics page flow with various filter combinations"""
        import streamlit as st
        from modules.analytics import analytics_page
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Create test data with proper structure
        test_series = [
            {
                "series_id": 1,
                "series_name": "Test Operation",
                "tsoc": "JSOC",
                "support_another_unit": True,
                "classification": "UNCLASS",
                "nds_threat": "NDS-PRC",
                "miso_program": "CTWMP",
                "target_audience_category": "Citizens",
                "fy_quarter_map": {"2023": ["FYQ1", "FYQ2"]}
            }
        ]
        
        test_script = f"""
import streamlit as st
import pandas as pd
import sqlite3
from modules.analytics import analytics_page
from unittest.mock import patch

# Setup
st.session_state.conn = sqlite3.connect('test_miso.db', check_same_thread=False)
st.session_state.conn.row_factory = sqlite3.Row
st.session_state.iso3_country_map = {{"AFG": "Afghanistan"}}

test_series = {test_series}

with patch('modules.analytics.pull_series_and_cyber_data', return_value=[test_series, []]):
    with patch('modules.analytics.pull_miso_assessments', return_value=[]):
        with patch('modules.analytics.pull_miso_executions', return_value=[]):
            with patch('modules.analytics.pull_other_threats', return_value=set()):
                with patch('modules.analytics.pull_other_miso_program', return_value=set()):
                    with patch('modules.analytics.pull_other_classifications', return_value=set()):
                        with patch('modules.analytics.pull_other_means', return_value=set()):
                            # Set various filter states
                            st.session_state["analytics_fiscal_years"] = [2023]
                            st.session_state["export_fiscal_quarter"] = ["FYQ1"]
                            st.session_state["export_tsoc"] = ["JSOC"]
                            st.session_state["include_support"] = True
                            st.session_state["include_support_tsoc"] = True
                            st.session_state["include_no_support"] = True
                            st.session_state["include_classifications"] = True
                            st.session_state["include_classifications_tsoc"] = True
                            st.session_state["include_threats"] = True
                            st.session_state["include_threat_tsoc"] = True
                            st.session_state["include_miso_program"] = True
                            st.session_state["include_miso_program_tsoc"] = True
                            st.session_state["include_audience"] = True
                            st.session_state["include_audience_tsoc"] = True
                            st.session_state["include_means"] = True
                            st.session_state["include_means_tsoc"] = True
                            st.session_state["include_hpem"] = True
                            
                            analytics_page()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render analytics page
        assert len(at.tabs) > 0 or len(at.header) > 0
    
    def test_analytics_changes_table_calculation(self):
        """Test changes table calculation logic"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Simulate changes calculation
series_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC"},
    {"series_id": 2, "series_name": "Op2", "tsoc": "JSOC"}
]

# Get names for changes table
names1 = how_many_of_type(series_data, "JSOC", [], [], False, "", True)
names2 = how_many_of_type(series_data[:1], "JSOC", [], [], False, "", True)

# Simulate changes: added and dropped
added = set(names1) - set(names2)
dropped = set(names2) - set(names1)

st.write(f"Added: {added}, Dropped: {dropped}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0

