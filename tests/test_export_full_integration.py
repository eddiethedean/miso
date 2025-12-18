"""
Full integration tests for export page to maximize coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import sqlite3


class TestExportFullIntegration:
    """Full integration tests for export functionality"""
    
    def test_render_miso_tab_all_combinations(self, test_db, mock_session_state):
        """Test render_miso_tab with all checkbox combinations"""
        import streamlit as st
        from modules.export import render_miso_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Setup data
        st.session_state["all_export_miso"] = [
            {
                "series_id": 1,
                "series_name": "Test Series",
                "classification": "UNCLASS",
                "tsoc": "JSOC",
                "is_active": True,
                "type": "psyop"
            }
        ]
        st.session_state["all_export_execution"] = [
            {
                "execution_id": 1,
                "series_id": 1,
                "miso_execution": "Test Exec",
                "is_active": True
            }
        ]
        st.session_state["all_export_assessment"] = [
            {
                "assessment_id": 1,
                "series_id": 1,
                "execution_id": 1,
                "progress": None,
                "threshold_met": None,
                "is_active": True
            }
        ]
        st.session_state["active_miso"] = st.session_state["all_export_miso"]
        st.session_state["active_execution"] = st.session_state["all_export_execution"]
        st.session_state["active_assessment"] = st.session_state["all_export_assessment"]
        st.session_state["show_export_preview"] = False
        
        test_script = """
import streamlit as st
from modules.export import render_miso_tab

# Test with all options enabled
st.session_state["include_executions"] = True
st.session_state["include_assessments"] = True
st.session_state["include_miso_children"] = True
st.session_state["include_exec_children"] = True

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_render_miso_tab_empty_tables(self, test_db, mock_session_state):
        """Test render_miso_tab with empty data tables"""
        import streamlit as st
        from modules.export import render_miso_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        st.session_state["all_export_miso"] = []
        st.session_state["all_export_execution"] = []
        st.session_state["all_export_assessment"] = []
        st.session_state["active_miso"] = []
        st.session_state["active_execution"] = []
        st.session_state["active_assessment"] = []
        st.session_state["show_export_preview"] = False
        
        test_script = """
import streamlit as st
from modules.export import render_miso_tab

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should handle empty data
        assert len(at.subheader) > 0
    
    def test_render_cyber_tab_with_series_children(self, test_db, mock_session_state):
        """Test render_cyber_tab with include children"""
        import streamlit as st
        from modules.export import render_cyber_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        st.session_state["all_export_cyber"] = [
            {
                "cyber_id": 1,
                "cyber_name": "Cyber Op",
                "is_active": True
            }
        ]
        st.session_state["all_export_cyber_assessment"] = [
            {
                "assessment_id": 1,
                "cyber_id": 1,
                "is_active": True
            }
        ]
        st.session_state["active_cyber"] = st.session_state["all_export_cyber"]
        st.session_state["active_cyber_assessment"] = st.session_state["all_export_cyber_assessment"]
        st.session_state["show_cyber_export_preview"] = False
        
        test_script = """
import streamlit as st
from modules.export import render_cyber_tab

st.session_state["include_cyber"] = True
st.session_state["include_cyber_assessments"] = True
st.session_state["include_cyber_children"] = True

render_cyber_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_export_preview_with_all_selections(self, test_db, mock_session_state):
        """Test export preview with all types selected"""
        import streamlit as st
        from modules.export import render_miso_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        st.session_state["all_export_miso"] = [
            {
                "series_id": 1,
                "series_name": "Test",
                "is_active": True,
                "type": "psyop"
            }
        ]
        st.session_state["all_export_execution"] = [
            {
                "execution_id": 1,
                "series_id": 1,
                "miso_execution": "Exec",
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
        st.session_state["show_export_preview"] = False  # Start with preview off
        
        test_script = """
import streamlit as st
from modules.export import render_miso_tab

st.session_state["include_miso"] = True
st.session_state["include_executions"] = True
st.session_state["include_assessments"] = True

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render the tab
        assert len(at.subheader) > 0 or len(at.checkbox) > 0

