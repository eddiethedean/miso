"""
Comprehensive tests for analytics_charts.py to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest


class TestAnalyticsChartsComprehensive:
    """Test chart functions with edge cases"""
    
    def test_means_chart_with_other_means(self):
        """Test means_chart with other means"""
        test_script = """
import streamlit as st
from modules.analytics_charts import means_chart

filtered_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC"}
]
other_means = {"Custom Mean"}
all_executions = [
    {
        "series_id": 1,
        "dissemination_means": '{"Custom Mean"}',
        "dissemination_method": '{"Other"}'
    }
]
allowed_tsocs = []

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_means_chart_percentages_expander(self):
        """Test means_chart percentages expander"""
        test_script = """
import streamlit as st
from modules.analytics_charts import means_chart

filtered_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC"}
]
other_means = set()
all_executions = [
    {
        "series_id": 1,
        "dissemination_means": '{"Internet"}',
        "dissemination_method": '{"Social Media"}'
    }
]
allowed_tsocs = []

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should have expander for percentages
        assert len(at.expander) > 0 or len(at.header) > 0
    
    def test_series_by_threat_chart_with_other_threats(self):
        """Test series_by_threat_chart with other threats"""
        test_script = """
import streamlit as st
from modules.analytics_charts import series_by_threat_chart

filtered_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC", "nds_threat": "Custom Threat"}
]
other_threats = {"Custom Threat"}
allowed_tsocs = []

series_by_threat_chart(filtered_data, other_threats, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_miso_program_chart_with_other_program(self):
        """Test miso_program_chart with other programs"""
        test_script = """
import streamlit as st
from modules.analytics_charts import miso_program_chart

other_miso_program = {"Custom Program"}
filtered_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC", "miso_program": "Custom Program"}
]
allowed_tsocs = []

miso_program_chart(other_miso_program, filtered_data, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0

