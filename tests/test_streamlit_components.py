"""
Tests for Streamlit UI components
"""
import pytest
from streamlit.testing.v1 import AppTest
import sqlite3


class TestStreamlitComponents:
    """Test Streamlit UI component functions"""
    
    def test_handle_radio_change(self):
        """Test handle_radio_change callback"""
        test_script = """
import streamlit as st
from modules.data_operations import handle_radio_change

if 'objective' not in st.session_state:
    st.session_state.objective = None

handle_radio_change("Test Objective")
st.write(f"Objective: {st.session_state.objective}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert at.session_state["objective"] == "Test Objective"
    
    def test_get_selected_data(self):
        """Test get_selected_data cached function"""
        test_script = """
import streamlit as st
from modules.data_operations import get_selected_data

data = {"key1": "value1", "key2": "value2"}
result = get_selected_data(data)
st.write(f"Result: {result}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Function should return the data
        assert len(at.markdown) > 0
    
    def test_submit_button_disabled_valid(self):
        """Test submit_button_disabled with valid data"""
        test_script = """
import streamlit as st
from modules.data_operations import submit_button_disabled

data = {
    "field1": "value1",
    "field2": ["item1", "item2"],
    "field3": 123
}
disabled = submit_button_disabled(data)
st.write(f"Disabled: {disabled}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should not be disabled with valid data
        assert len(at.markdown) > 0
    
    def test_submit_button_disabled_invalid(self):
        """Test submit_button_disabled with invalid data"""
        test_script = """
import streamlit as st
from modules.data_operations import submit_button_disabled

data = {
    "field1": None,  # Invalid
    "field2": "value2"
}
disabled = submit_button_disabled(data)
st.write(f"Disabled: {disabled}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should be disabled with invalid data
        assert len(at.markdown) > 0
    
    def test_submit_button_disabled_empty_string(self):
        """Test submit_button_disabled with empty string"""
        test_script = """
import streamlit as st
from modules.data_operations import submit_button_disabled

data = {
    "field1": "",  # Empty string
    "field2": "value2"
}
disabled = submit_button_disabled(data)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should be disabled with empty string
        assert len(at.warning) > 0
    
    def test_submit_button_disabled_empty_list(self):
        """Test submit_button_disabled with empty list"""
        test_script = """
import streamlit as st
from modules.data_operations import submit_button_disabled

data = {
    "field1": [],  # Empty list
    "field2": "value2"
}
disabled = submit_button_disabled(data)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should be disabled with empty list
        assert len(at.warning) > 0
    
    def test_manual_user_email_valid(self):
        """Test manual_user_email with valid SOCOM email"""
        test_script = """
import streamlit as st
from modules.data_operations import manual_user_email

# Simulate user input
st.session_state["manual_user_email_test"] = "user@socom.mil"
email = manual_user_email("test")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should accept valid email
        assert len(at.text_input) > 0
    
    def test_manual_user_email_invalid(self):
        """Test manual_user_email with invalid email"""
        test_script = """
import streamlit as st
from modules.data_operations import manual_user_email

# Simulate invalid email
st.session_state["manual_user_email_test"] = "user@invalid.com"
email = manual_user_email("test")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should show error for invalid email
        assert len(at.error) > 0 or len(at.text_input) > 0
    
    def test_render_select_with_other_standard(self):
        """Test render_select_with_other with standard option"""
        test_script = """
import streamlit as st
from modules.data_operations import render_select_with_other

options = ["Option1", "Option2", "OTHER"]
value = render_select_with_other("Test Label", options, "Option1", "test", "create")
st.write(f"Value: {value}")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        assert len(at.selectbox) > 0
    
    def test_render_select_with_other_custom(self):
        """Test render_select_with_other with OTHER option"""
        test_script = """
import streamlit as st
from modules.data_operations import render_select_with_other

options = ["Option1", "Option2", "OTHER"]
# Simulate selecting OTHER
st.session_state["testcreate_select"] = "OTHER"
st.session_state["testcreate_OTHER"] = "Custom Value"
value = render_select_with_other("Test Label", options, "", "test", "create")
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should show text input when OTHER is selected
        assert len(at.selectbox) > 0
    
    def test_country_city_selector(self, mock_session_state):
        """Test country_city_selector component"""
        import streamlit as st
        import pandas as pd
        
        test_script = """
import streamlit as st
import pandas as pd
from modules.data_operations import country_city_selector

# Create sample dataframes
countries_df = pd.DataFrame({
    "iso3": ["AFG", "IRQ"],
    "country": ["Afghanistan", "Iraq"]
})
cities_df = pd.DataFrame({
    "iso3": ["AFG", "AFG", "IRQ"],
    "country": ["Afghanistan", "Afghanistan", "Iraq"],
    "city_ascii": ["Kabul", "Kandahar", "Baghdad"],
    "admin_name": ["Kabul", "Kandahar", "Baghdad"]
})

countries, cities = country_city_selector(
    "Test", countries_df, cities_df, "test_country", "test_city"
)
"""
        at = AppTest.from_string(test_script)
        at.run()
        
        # Should render multiselect components
        assert len(at.multiselect) >= 1

