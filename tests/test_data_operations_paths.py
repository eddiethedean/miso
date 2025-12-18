"""
Tests for specific paths in data_operations.py
"""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd


class TestDataOperationsPaths:
    """Test specific code paths in data_operations.py"""
    
    def test_country_city_selector_updateseries_page(self):
        """Test country_city_selector on updateseries page"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.data_operations import country_city_selector

countries_df = pd.DataFrame({
    "iso3": ["AFG"],
    "country": ["Afghanistan"]
})
cities_df = pd.DataFrame({
    "iso3": ["AFG"],
    "country": ["Afghanistan"],
    "city_ascii": ["Kabul"],
    "admin_name": ["Kabul"]
})

st.session_state["active_page"] = "updateseries"
st.session_state["Updateseries_country"] = ["AFG"]
st.session_state["selected_countries"] = ["AFG"]
st.session_state["selected_cities"] = []

countries, cities = country_city_selector(
    "Test", countries_df, cities_df, "Updateseries_country", "Updateseries_city",
    selected_countries_arr=["AFG"], selected_cities_arr=[]
)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.multiselect) >= 1
    
    def test_country_city_selector_country_cleared(self):
        """Test country_city_selector when country is cleared"""
        test_script = """
import streamlit as st
import pandas as pd
from modules.data_operations import country_city_selector

countries_df = pd.DataFrame({
    "iso3": ["AFG"],
    "country": ["Afghanistan"]
})
cities_df = pd.DataFrame({
    "iso3": ["AFG"],
    "country": ["Afghanistan"],
    "city_ascii": ["Kabul"],
    "admin_name": ["Kabul"]
})

st.session_state["active_page"] = "createseries"
st.session_state["Createseries_country"] = []
st.session_state["selected_countries"] = []
st.session_state["selected_cities"] = []

countries, cities = country_city_selector(
    "Test", countries_df, cities_df, "Createseries_country", "Createseries_city"
)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.multiselect) >= 1
    
    def test_render_select_with_other_no_stored_value(self):
        """Test render_select_with_other with no stored value"""
        test_script = """
import streamlit as st
from modules.data_operations import render_select_with_other

options = ["Option1", "Option2", "OTHER"]
value = render_select_with_other("Test", options, None, "test", "create")
st.write(f"Value: {value}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.selectbox) > 0
    
    def test_render_select_with_other_empty_stored(self):
        """Test render_select_with_other with empty stored value"""
        test_script = """
import streamlit as st
from modules.data_operations import render_select_with_other

options = ["Option1", "Option2", "OTHER"]
value = render_select_with_other("Test", options, "", "test", "create")
st.write(f"Value: {value}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.selectbox) > 0
    
    def test_pull_series_and_cyber_data_no_locations(self, test_db, mock_session_state):
        """Test pull_series_and_cyber_data with no location data"""
        import streamlit as st
        from modules.data_operations import pull_series_and_cyber_data
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Clear location data
        conn = st.session_state["conn"]
        cur = conn.cursor()
        cur.execute("DELETE FROM miso_location")
        cur.execute("DELETE FROM cyber_location")
        conn.commit()
        
        data = pull_series_and_cyber_data("Export")
        
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_pull_series_and_cyber_data_multiple_locations(self, test_db, mock_session_state):
        """Test pull_series_and_cyber_data with multiple locations per series"""
        import streamlit as st
        from modules.data_operations import pull_series_and_cyber_data
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Add multiple locations
        conn = st.session_state["conn"]
        cur = conn.cursor()
        cur.execute("SELECT series_id FROM miso_series LIMIT 1")
        result = cur.fetchone()
        if result:
            series_id = result[0]
            cur.execute("DELETE FROM miso_location WHERE series_id = ?", (series_id,))
            cur.execute("""
                INSERT INTO miso_location (series_id, country_code, city)
                VALUES (?, ?, ?), (?, ?, ?)
            """, (series_id, "AFG", "Kabul", series_id, "IRQ", "Baghdad"))
            conn.commit()
        
        data = pull_series_and_cyber_data("Export")
        
        assert isinstance(data, list)

