"""
Comprehensive tests for export.py to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import sqlite3


class TestExportComprehensive:
    """Test export functionality comprehensively"""
    
    def test_refresh_export_data(self, test_db, mock_session_state):
        """Test refresh_export_data function"""
        import streamlit as st
        from modules.export import refresh_export_data
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        refresh_export_data()
        
        assert "all_export_miso" in st.session_state
        assert "all_export_cyber" in st.session_state
        assert "all_export_execution" in st.session_state
        assert "all_export_assessment" in st.session_state
    
    def test_render_export_filters(self):
        """Test render_export_filters component"""
        test_script = """
import streamlit as st
from modules.export import render_export_filters

st.session_state["miso_export_start_date"] = None
st.session_state["miso_export_end_date"] = None

render_export_filters("miso", [2023, 2024])
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render filter components
        assert len(at.date_input) > 0 or len(at.multiselect) > 0
    
    def test_filter_table_cyber_domain(self):
        """Test filter_table with cyber domain"""
        import streamlit as st
        from modules.export import filter_table
        
        df = pd.DataFrame({
            "cyber_name": ["Cyber Op 1", "Cyber Op 2"],
            "tsoc": ["JSOC", "SOCAF"],
            "start_year": [2023, 2024],
            "start_month": [1, 2],
            "fy_quarter_map": [
                {"2023": ["FYQ1"]},
                {"2024": ["FYQ1"]}
            ]
        })
        
        st.session_state["cyber_export_name"] = "Cyber Op 1"
        
        filtered = filter_table(df.copy(), "cyber")
        
        assert len(filtered) == 1
        assert "Cyber Op 1" in filtered["cyber_name"].iloc[0]
    
    def test_render_miso_tab_with_children(self, test_db, mock_session_state):
        """Test render_miso_tab with include children options"""
        import streamlit as st
        from modules.export import render_miso_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Set up export data
        st.session_state["all_export_miso"] = [
            {
                "series_id": 1,
                "series_name": "Test Series",
                "classification": "UNCLASS",
                "tsoc": "JSOC",
                "is_active": True
            }
        ]
        st.session_state["all_export_execution"] = [
            {
                "execution_id": 1,
                "series_id": 1,
                "miso_execution": "Test Execution",
                "is_active": True
            }
        ]
        st.session_state["all_export_assessment"] = [
            {
                "assessment_id": 1,
                "series_id": 1,
                "execution_id": 1,
                "is_active": True
            }
        ]
        st.session_state["active_miso"] = st.session_state["all_export_miso"]
        st.session_state["active_execution"] = st.session_state["all_export_execution"]
        st.session_state["active_assessment"] = st.session_state["all_export_assessment"]
        
        test_script = """
import streamlit as st
from modules.export import render_miso_tab

# Setup is done above
render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render MISO tab
        assert len(at.subheader) > 0 or len(at.checkbox) > 0
    
    def test_render_cyber_tab(self, test_db, mock_session_state):
        """Test render_cyber_tab"""
        import streamlit as st
        from modules.export import render_cyber_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        st.session_state["all_export_cyber"] = [
            {
                "cyber_id": 1,
                "cyber_name": "Test Cyber",
                "classification": "S//NF",
                "is_active": True
            }
        ]
        st.session_state["all_export_cyber_assessment"] = []
        st.session_state["active_cyber"] = st.session_state["all_export_cyber"]
        st.session_state["active_cyber_assessment"] = []
        
        test_script = """
import streamlit as st
from modules.export import render_cyber_tab

render_cyber_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0 or len(at.checkbox) > 0
    
    def test_render_ca_tab(self):
        """Test render_ca_tab"""
        test_script = """
import streamlit as st
from modules.export import render_ca_tab

render_ca_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # CA tab shows construction image
        assert len(at.subheader) > 0 or len(at.image) > 0
    
    def test_export_page_initialization(self, test_db, mock_session_state):
        """Test export_page initialization"""
        import streamlit as st
        from modules.export import export_page
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Set empty export data to trigger refresh
        st.session_state["all_export_miso"] = []
        st.session_state["all_export_cyber"] = []
        
        test_script = """
import streamlit as st
from modules.export import export_page

export_page()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.header) > 0

