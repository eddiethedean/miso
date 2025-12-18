"""
Tests for chart functions in analytics_charts module
"""
import pytest
from streamlit.testing.v1 import AppTest
from modules.analytics_charts import (
    means_chart,
    hpem_phase_chart,
    series_by_threat_chart,
    series_by_audience_chart,
    active_miso_series_chart,
    miso_program_chart
)


class TestChartFunctions:
    """Test chart generation functions"""
    
    @pytest.fixture
    def sample_series_data(self):
        """Sample series data for charts"""
        return [
            {
                "series_id": 1,
                "series_name": "Operation Alpha",
                "tsoc": "JSOC",
                "nds_threat": "NDS-PRC",
                "miso_program": "CTWMP",
                "target_audience_category": "Citizens"
            },
            {
                "series_id": 2,
                "series_name": "Operation Bravo",
                "tsoc": "SOCAF",
                "nds_threat": "NDS-RUS",
                "miso_program": "DACMP",
                "target_audience_category": "Decision Makers"
            }
        ]
    
    @pytest.fixture
    def sample_executions(self):
        """Sample execution data"""
        return [
            {
                "series_id": 1,
                "dissemination_means": '{"Internet","Phone"}',
                "dissemination_method": '{"Social Media","SMS"}'
            },
            {
                "series_id": 2,
                "dissemination_means": '{"Radio"}',
                "dissemination_method": '{"Radio"}'
            }
        ]
    
    @pytest.fixture
    def sample_assessments(self):
        """Sample assessment data"""
        return [
            {
                "series_id": 1,
                "current_hpem_phase": "Awareness"
            },
            {
                "series_id": 2,
                "current_hpem_phase": "Understanding"
            }
        ]
    
    def test_means_chart_renders(self, sample_series_data, sample_executions):
        """Test that means_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import means_chart

filtered_data = {sample_series_data}
all_executions = {sample_executions}
other_means = set()
allowed_tsocs = []

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Chart should render (check for header or chart component)
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_hpem_phase_chart_renders(self, sample_series_data, sample_assessments):
        """Test that hpem_phase_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import hpem_phase_chart

filtered_data = {sample_series_data}
all_assessments = {sample_assessments}

hpem_phase_chart(filtered_data, all_assessments)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.plotly_chart) > 0
    
    def test_series_by_threat_chart_renders(self, sample_series_data):
        """Test that series_by_threat_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import series_by_threat_chart

filtered_data = {sample_series_data}
other_threats = set()
allowed_tsocs = []

series_by_threat_chart(filtered_data, other_threats, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_series_by_audience_chart_renders(self, sample_series_data):
        """Test that series_by_audience_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import series_by_audience_chart

filtered_data = {sample_series_data}
allowed_tsocs = []

series_by_audience_chart(filtered_data, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_active_miso_series_chart_renders(self, sample_series_data):
        """Test that active_miso_series_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import active_miso_series_chart

filtered_data = {sample_series_data}
allowed_tsocs = []

active_miso_series_chart(filtered_data, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.plotly_chart) > 0
    
    def test_miso_program_chart_renders(self, sample_series_data):
        """Test that miso_program_chart renders without errors"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import miso_program_chart

other_miso_program = set()
filtered_data = {sample_series_data}
allowed_tsocs = []

miso_program_chart(other_miso_program, filtered_data, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0
    
    def test_means_chart_with_tsoc_filter(self, sample_series_data, sample_executions):
        """Test means_chart with TSOC filtering"""
        test_script = f"""
import streamlit as st
from modules.analytics_charts import means_chart

filtered_data = {sample_series_data}
all_executions = {sample_executions}
other_means = set()
allowed_tsocs = ["JSOC"]

means_chart(filtered_data, other_means, all_executions, allowed_tsocs)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0 or len(at.bar_chart) > 0

