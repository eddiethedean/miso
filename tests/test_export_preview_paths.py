"""
Tests for export preview and selection paths
"""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd


class TestExportPreviewPaths:
    """Test export preview functionality"""
    
    def test_export_preview_with_series_only(self):
        """Test export preview with only series selected"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.export import render_miso_tab

# Setup minimal data
st.session_state["all_export_miso"] = [
    {
        "series_id": 1,
        "series_name": "Test",
        "is_active": True
    }
]
st.session_state["all_export_execution"] = []
st.session_state["all_export_assessment"] = []
st.session_state["active_miso"] = st.session_state["all_export_miso"]
st.session_state["active_execution"] = []
st.session_state["active_assessment"] = []
st.session_state["show_export_preview"] = True

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_export_preview_with_executions_only(self):
        """Test export preview with only executions"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.export import render_miso_tab

st.session_state["all_export_miso"] = [
    {
        "series_id": 1,
        "series_name": "Test",
        "is_active": True
    }
]
st.session_state["all_export_execution"] = [
    {
        "execution_id": 1,
        "series_id": 1,
        "miso_execution": "Exec1",
        "is_active": True
    }
]
st.session_state["all_export_assessment"] = []
st.session_state["active_miso"] = st.session_state["all_export_miso"]
st.session_state["active_execution"] = st.session_state["all_export_execution"]
st.session_state["active_assessment"] = []
st.session_state["show_export_preview"] = True

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_export_preview_with_assessments_only(self):
        """Test export preview with only assessments"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.export import render_miso_tab

st.session_state["all_export_miso"] = [
    {
        "series_id": 1,
        "series_name": "Test",
        "is_active": True
    }
]
st.session_state["all_export_execution"] = []
st.session_state["all_export_assessment"] = [
    {
        "assessment_id": 1,
        "series_id": 1,
        "execution_id": None,
        "is_active": True
    }
]
st.session_state["active_miso"] = st.session_state["all_export_miso"]
st.session_state["active_execution"] = []
st.session_state["active_assessment"] = st.session_state["all_export_assessment"]
st.session_state["show_export_preview"] = True

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_cyber_export_preview(self):
        """Test cyber export preview"""
        test_script = """
import streamlit as st
from modules.export import render_cyber_tab

st.session_state["all_export_cyber"] = [
    {
        "cyber_id": 1,
        "cyber_name": "Cyber Op",
        "is_active": True
    }
]
st.session_state["all_export_cyber_assessment"] = []
st.session_state["active_cyber"] = st.session_state["all_export_cyber"]
st.session_state["active_cyber_assessment"] = []
st.session_state["show_cyber_export_preview"] = True

render_cyber_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_filter_table_no_filters(self):
        """Test filter_table with no filters applied"""
        import streamlit as st
        from modules.export import filter_table
        
        df = pd.DataFrame({
            "series_name": ["Op1", "Op2"],
            "tsoc": ["JSOC", "SOCAF"],
            "start_year": [2023, 2024],
            "start_month": [1, 2],
            "fy_quarter_map": [
                {"2023": ["FYQ1"]},
                {"2024": ["FYQ1"]}
            ]
        })
        
        # Clear all filters
        if "miso_export_name" in st.session_state:
            del st.session_state["miso_export_name"]
        if "miso_export_tsoc" in st.session_state:
            del st.session_state["miso_export_tsoc"]
        if "miso_export_fiscal_year" in st.session_state:
            del st.session_state["miso_export_fiscal_year"]
        if "miso_export_quarters" in st.session_state:
            del st.session_state["miso_export_quarters"]
        if "miso_export_start_date" in st.session_state:
            del st.session_state["miso_export_start_date"]
        if "miso_export_end_date" in st.session_state:
            del st.session_state["miso_export_end_date"]
        
        filtered = filter_table(df.copy(), "miso")
        
        # Should return all rows when no filters
        assert len(filtered) == len(df)
    
    def test_filter_table_quarter_without_fiscal_year(self):
        """Test filter_table with quarters but no fiscal year"""
        import streamlit as st
        from modules.export import filter_table
        
        df = pd.DataFrame({
            "series_name": ["Op1"],
            "tsoc": ["JSOC"],
            "fy_quarter_map": [
                {"2023": ["FYQ1", "FYQ2"]}
            ]
        })
        
        st.session_state["miso_export_quarters"] = ["FYQ1"]
        # Don't set fiscal_year
        
        filtered = filter_table(df.copy(), "miso")
        
        assert isinstance(filtered, pd.DataFrame)

