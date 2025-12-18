"""
Tests for chart edge cases to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest


class TestChartsEdgeCases:
    """Test edge cases in chart functions"""
    
    def test_means_chart_percentages_no_series(self):
        """Test means_chart percentages with no series"""
        test_script = """
import streamlit as st
from modules.analytics_charts import means_chart

filtered_data = []
other_means = set()
all_executions = []
allowed_tsocs = []

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should handle empty data gracefully
        assert len(at.header) > 0 or len(at.expander) > 0
    
    def test_means_chart_percentages_with_data(self):
        """Test means_chart percentages calculation"""
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
        "dissemination_means": '{"Internet","Radio"}',
        "dissemination_method": '{"Social Media","Radio"}'
    }
]
allowed_tsocs = []

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should show percentages expander
        assert len(at.expander) > 0 or len(at.header) > 0
    
    def test_means_chart_social_media_percentage(self):
        """Test means_chart with social media percentage calculation"""
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
        
        # Should calculate social media ratio
        assert len(at.expander) > 0

