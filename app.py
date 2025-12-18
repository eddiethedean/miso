"""
Main Streamlit application for MISO
"""
import streamlit as st
import sqlite3
import os
from modules.analytics import analytics_page
from modules.export import export_page
from modules.constants import TSOCS

# Page configuration
st.set_page_config(
    page_title="MISO Management System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Country code to name mapping (simplified)
COUNTRY_MAP = {
    "AFG": "Afghanistan",
    "IRQ": "Iraq",
    "SYR": "Syria",
    "YEM": "Yemen",
    "SOM": "Somalia",
    "NGA": "Nigeria",
    "MLI": "Mali",
    "PHL": "Philippines",
    "IDN": "Indonesia",
    "THA": "Thailand"
}

def init_session_state():
    """Initialize session state variables"""
    if "conn" not in st.session_state:
        db_path = "miso.db"
        if not os.path.exists(db_path):
            st.error(f"Database not found at {db_path}. Please run init_database.py and generate_fake_data.py first.")
            st.stop()
        
        st.session_state["conn"] = sqlite3.connect(db_path, check_same_thread=False)
        st.session_state["conn"].row_factory = sqlite3.Row
    
    if "iso3_country_map" not in st.session_state:
        st.session_state["iso3_country_map"] = COUNTRY_MAP
    
    if "all_export_miso" not in st.session_state:
        st.session_state["all_export_miso"] = []
    
    if "all_export_cyber" not in st.session_state:
        st.session_state["all_export_cyber"] = []
    
    if "all_export_execution" not in st.session_state:
        st.session_state["all_export_execution"] = []
    
    if "all_export_assessment" not in st.session_state:
        st.session_state["all_export_assessment"] = []
    
    if "all_export_cyber_assessment" not in st.session_state:
        st.session_state["all_export_cyber_assessment"] = []
    
    if "active_miso" not in st.session_state:
        st.session_state["active_miso"] = []
    
    if "active_cyber" not in st.session_state:
        st.session_state["active_cyber"] = []
    
    if "active_execution" not in st.session_state:
        st.session_state["active_execution"] = []
    
    if "active_assessment" not in st.session_state:
        st.session_state["active_assessment"] = []
    
    if "active_cyber_assessment" not in st.session_state:
        st.session_state["active_cyber_assessment"] = []
    
    if "show_export_preview" not in st.session_state:
        st.session_state["show_export_preview"] = False
    
    if "show_cyber_export_preview" not in st.session_state:
        st.session_state["show_cyber_export_preview"] = False
    
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "analytics"

def main():
    """Main application"""
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("MISO Management System")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Analytics", "Export"],
        index=0 if st.session_state["active_page"] == "analytics" else 1
    )
    
    if page == "Analytics":
        st.session_state["active_page"] = "analytics"
        analytics_page()
    elif page == "Export":
        st.session_state["active_page"] = "export"
        export_page()
    
    # Close connection on app close (though SQLite handles this automatically)
    # We'll keep it open for the session

if __name__ == "__main__":
    main()

