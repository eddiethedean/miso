"""
Integration tests for export page to increase coverage
"""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import sqlite3


class TestExportIntegration:
    """Integration tests for export page"""
    
    def test_render_miso_tab_full_flow(self, test_db, mock_session_state):
        """Test full render_miso_tab flow"""
        import streamlit as st
        from modules.export import render_miso_tab
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Setup comprehensive data
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
                "progress": True,
                "threshold_met": False,
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

render_miso_tab()
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.subheader) > 0
    
    def test_export_page_all_tabs(self, test_db, mock_session_state):
        """Test export page with all tab scenarios"""
        import streamlit as st
        from modules.export import export_page
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Test each tab
        for tab in ["miso", "cyber", "ca"]:
            st.session_state["active_export_tab"] = tab
            st.session_state["all_export_miso"] = []
            st.session_state["all_export_cyber"] = []
            
            test_script = f"""
import streamlit as st
from modules.export import export_page

st.session_state["active_export_tab"] = "{tab}"
export_page()
"""
            at = AppTest.from_string(test_script)
            at.run()
            
            assert len(at.header) > 0 or len(at.tabs) > 0

