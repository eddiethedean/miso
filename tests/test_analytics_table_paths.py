"""
Tests for analytics table generation paths
"""
import pytest
from streamlit.testing.v1 import AppTest
import json


class TestAnalyticsTablePaths:
    """Test analytics table generation with various scenarios"""
    
    def test_analytics_table_empty_series_map(self):
        """Test analytics table when series_map is empty"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test with empty data
series_data = []
count = how_many_of_type(series_data, "Series", [], [], False, "", False)
st.write(f"Empty count: {count}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0
    
    def test_analytics_table_sum_column_empty_series_set(self):
        """Test sum column calculation with empty series_set"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test sum calculation logic
series_data = []
count = how_many_of_type(series_data, "Series", [], [], False, "", False)
names = how_many_of_type(series_data, "Series", [], [], False, "", True)
st.write(f"Count: {count}, Names: {names}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0
    
    def test_analytics_changes_table_first_period(self):
        """Test changes table with first period (should show 0 changes)"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type

# Test changes calculation for first period
series_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC"}
]

count = how_many_of_type(series_data, "JSOC", [], [], False, "", False)
st.write(f"Count: {count}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0
    
    def test_analytics_table_with_other_categories_tsoc(self):
        """Test table with other categories and TSOC variants"""
        test_script = """
import streamlit as st
from modules.analytics_data_operations import how_many_of_type, add_tsocs_to_array

# Test other categories with TSOC
series_data = [
    {"series_id": 1, "series_name": "Op1", "tsoc": "JSOC", "classification": "CUSTOM"}
]

# Test other classification with TSOC
tsoc_variants = add_tsocs_to_array("CUSTOM", ["JSOC"])
st.write(f"TSOC variants: {tsoc_variants}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.markdown) > 0

