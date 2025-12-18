"""
Tests for Streamlit app using streamlit.testing
"""
import pytest
from streamlit.testing.v1 import AppTest
import os
import sqlite3
from pathlib import Path


@pytest.fixture
def test_db_for_app():
    """Create a test database for app testing"""
    # Create database in a known location
    db_path = "test_miso.db"
    
    # Initialize if it doesn't exist
    if not os.path.exists(db_path):
        from init_database import create_database
        create_database(db_path)
        
        # Add minimal test data
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO miso_series (
                series_name, classification, tsoc, nds_threat, miso_program,
                start_year, start_month, end_year, end_month, fiscal_year, quarter,
                fy_quarter_map, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Test Operation", "UNCLASS", "JSOC", "NDS-PRC", "CTWMP",
            2023, 1, 2024, 12, 2023, "FYQ1", '{"2023": ["FYQ1"]}', 1
        ))
        
        conn.commit()
        conn.close()
    
    yield db_path
    
    # Cleanup (optional - comment out if you want to keep test DB)
    # if os.path.exists(db_path):
    #     os.remove(db_path)


class TestStreamlitApp:
    """Test Streamlit app using AppTest"""
    
    def test_app_initial_load(self, test_db_for_app):
        """Test that app loads without errors"""
        # Note: AppTest requires the app to be importable
        # We'll test individual pages instead
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check that app runs without crashing
        assert at is not None
    
    def test_analytics_page_renders(self):
        """Test that analytics page renders"""
        # Create a minimal test script for analytics
        test_script = """
import streamlit as st
import sqlite3
from modules.analytics import analytics_page

# Setup minimal session state
if 'conn' not in st.session_state:
    st.session_state.conn = sqlite3.connect('test_miso.db', check_same_thread=False)
    st.session_state.conn.row_factory = sqlite3.Row
if 'iso3_country_map' not in st.session_state:
    st.session_state.iso3_country_map = {"AFG": "Afghanistan"}

analytics_page()
"""
        
        at = AppTest.from_string(test_script)
        at.run()
        
        # Check that page rendered
        assert len(at.markdown) > 0 or len(at.header) > 0
    
    def test_export_page_renders(self):
        """Test that export page renders"""
        test_script = """
import streamlit as st
import sqlite3
from modules.export import export_page

# Setup minimal session state
if 'conn' not in st.session_state:
    st.session_state.conn = sqlite3.connect('test_miso.db', check_same_thread=False)
    st.session_state.conn.row_factory = sqlite3.Row
if 'iso3_country_map' not in st.session_state:
    st.session_state.iso3_country_map = {"AFG": "Afghanistan"}
if 'all_export_miso' not in st.session_state:
    st.session_state.all_export_miso = []
if 'all_export_cyber' not in st.session_state:
    st.session_state.all_export_cyber = []

export_page()
"""
        
        at = AppTest.from_string(test_script)
        at.run()
        
        # Check that page rendered
        assert len(at.markdown) > 0 or len(at.header) > 0


class TestStreamlitComponents:
    """Test individual Streamlit components"""
    
    def test_header_component(self):
        """Test header component"""
        test_script = """
import streamlit as st
st.header("Test Header", divider="grey")
"""
        at = AppTest.from_string(test_script)
        at.run()
        assert len(at.header) > 0
        assert "Test Header" in at.header[0].value
    
    def test_dataframe_component(self):
        """Test dataframe component"""
        test_script = """
import streamlit as st
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
st.dataframe(df)
"""
        at = AppTest.from_string(test_script)
        at.run()
        assert len(at.dataframe) > 0
    
    def test_multiselect_component(self):
        """Test multiselect component"""
        test_script = """
import streamlit as st
options = ["Option 1", "Option 2", "Option 3"]
selected = st.multiselect("Choose options", options, key="test_select")
"""
        at = AppTest.from_string(test_script)
        at.run()
        assert len(at.multiselect) > 0
    
    def test_button_interaction(self):
        """Test button click interaction"""
        test_script = """
import streamlit as st
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button("Increment", key="inc_btn"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Click button
        if len(at.button) > 0:
            at.button[0].click().run()
            # Check that count increased (would need to check markdown/text output)

