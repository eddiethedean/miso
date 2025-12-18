"""
Tests for specific code paths in analytics.py
"""
import pytest
from streamlit.testing.v1 import AppTest
import json


class TestAnalyticsPaths:
    """Test specific code paths in analytics.py"""
    
    def test_analytics_with_all_filter_options(self):
        """Test analytics page with all filter checkboxes enabled"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.analytics import analytics_page
from unittest.mock import patch

# Mock data
test_series = [
    {
        "series_id": 1,
        "series_name": "Test Op",
        "tsoc": "JSOC",
        "support_another_unit": True,
        "classification": "UNCLASS",
        "nds_threat": "NDS-PRC",
        "miso_program": "CTWMP",
        "target_audience_category": "Citizens",
        "fy_quarter_map": {"2023": ["FYQ1"]}
    }
]

with patch('modules.analytics.pull_series_and_cyber_data', return_value=[test_series, []]):
    with patch('modules.analytics.pull_miso_assessments', return_value=[]):
        with patch('modules.analytics.pull_miso_executions', return_value=[]):
            with patch('modules.analytics.pull_other_threats', return_value=set()):
                with patch('modules.analytics.pull_other_miso_program', return_value=set()):
                    with patch('modules.analytics.pull_other_classifications', return_value=set()):
                        with patch('modules.analytics.pull_other_means', return_value=set()):
                            # Set filter options
                            st.session_state["analytics_fiscal_years"] = [2023]
                            st.session_state["export_fiscal_quarter"] = ["FYQ1"]
                            st.session_state["export_tsoc"] = ["JSOC"]
                            
                            analytics_page()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.tabs) > 0
    
    def test_analytics_table_with_empty_quarters(self):
        """Test analytics table when no quarters selected"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test the quarter filtering logic
series_data = [
    {
        "series_id": 1,
        "series_name": "Op1",
        "tsoc": "JSOC",
        "fy_quarter_map": {"2023": ["FYQ1", "FYQ2"]}
    }
]

# Simulate empty quarters filter
count = how_many_of_type(series_data, "Series", [], [], False, "", False)
st.write(f"Count: {count}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0
    
    def test_analytics_charts_tab_with_filters(self):
        """Test charts tab with year and quarter filters"""
        test_script = """
import streamlit as st
from modules.analytics_charts import active_miso_series_chart

filtered_data = [
    {
        "series_id": 1,
        "series_name": "Op1",
        "tsoc": "JSOC",
        "fy_quarter_map": {"2023": ["FYQ1"]}
    }
]

# Test with TSOC filter
active_miso_series_chart(filtered_data, ["JSOC"])
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.plotly_chart) > 0
    
    def test_analytics_charts_tab_no_year_filter(self):
        """Test charts tab without year filter"""
        test_script = """
import streamlit as st
from modules.analytics_charts import series_by_audience_chart

filtered_data = [
    {
        "series_id": 1,
        "series_name": "Op1",
        "tsoc": "JSOC",
        "target_audience_category": "Citizens"
    }
]

series_by_audience_chart(filtered_data, [])
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0
    
    def test_analytics_metrics_tab(self):
        """Test metrics tab (even though empty)"""
        test_script = """
import streamlit as st
from modules.analytics import analytics_page
from unittest.mock import patch

with patch('modules.analytics.pull_series_and_cyber_data', return_value=[[], []]):
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
        
        # Should have tabs including Metrics
        assert len(at.tabs) >= 3

