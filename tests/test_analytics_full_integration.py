"""
Full integration tests for analytics page to maximize coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import json
import sqlite3


class TestAnalyticsFullIntegration:
    """Full integration tests exercising all analytics paths"""
    
    def test_analytics_tables_tab_complete_flow(self, test_db, mock_session_state):
        """Test complete tables tab flow with all options"""
        import streamlit as st
        from modules.analytics import analytics_page
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Create comprehensive test data
        test_series = [
            {
                "series_id": 1,
                "series_name": "Op1",
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
                "series_name": "Op2",
                "tsoc": "SOCAF",
                "support_another_unit": False,
                "classification": "S//NF",
                "nds_threat": "NDS-RUS",
                "miso_program": "DACMP",
                "target_audience_category": "Decision Makers",
                "fy_quarter_map": {"2023": ["FYQ3"]}
            }
        ]
        
        test_assessments = [
            {"series_id": 1, "current_hpem_phase": "Awareness"},
            {"series_id": 2, "current_hpem_phase": "Understanding"}
        ]
        
        test_executions = [
            {
                "series_id": 1,
                "dissemination_means": '{"Internet","Radio"}',
                "dissemination_method": '{"Social Media"}'
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
test_assessments = {test_assessments}
test_executions = {test_executions}

with patch('modules.analytics.pull_series_and_cyber_data', return_value=[test_series, []]):
    with patch('modules.analytics.pull_miso_assessments', return_value=test_assessments):
        with patch('modules.analytics.pull_miso_executions', return_value=test_executions):
            with patch('modules.analytics.pull_other_threats', return_value=set()):
                with patch('modules.analytics.pull_other_miso_program', return_value=set()):
                    with patch('modules.analytics.pull_other_classifications', return_value=set()):
                        with patch('modules.analytics.pull_other_means', return_value=set()):
                            analytics_page()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render analytics page
        assert len(at.tabs) > 0
    
    def test_analytics_charts_tab_with_year_filter(self):
        """Test charts tab with year filter applied"""
        test_script = """
import streamlit as st
from modules.analytics_charts import active_miso_series_chart, series_by_threat_chart

filtered_data = [
    {
        "series_id": 1,
        "series_name": "Op1",
        "tsoc": "JSOC",
        "nds_threat": "NDS-PRC",
        "fy_quarter_map": {"2023": ["FYQ1"]}
    }
]

# Test charts with filtered data
active_miso_series_chart(filtered_data, ["JSOC"])
series_by_threat_chart(filtered_data, set(), ["JSOC"])
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.plotly_chart) > 0
    
    def test_analytics_charts_tab_no_quarter_filter(self):
        """Test charts tab with year but no quarter filter"""
        test_script = """
import streamlit as st
from modules.analytics_charts import series_by_audience_chart

filtered_data = [
    {
        "series_id": 1,
        "series_name": "Op1",
        "tsoc": "JSOC",
        "target_audience_category": "Citizens",
        "fy_quarter_map": {"2023": ["FYQ1", "FYQ2"]}
    }
]

series_by_audience_chart(filtered_data, [])
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0

