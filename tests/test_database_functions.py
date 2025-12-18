"""
Tests for database functions in data_operations module
"""
import pytest
import sqlite3
from modules.data_operations import (
    pull_cyber_assessments,
    pull_miso_assessments,
    pull_miso_executions,
    pull_series_and_cyber_data
)
from modules.analytics_data_operations import (
    pull_other_classifications,
    pull_other_threats,
    pull_other_miso_program,
    pull_other_means
)


class TestDatabaseFunctions:
    """Test database query functions"""
    
    def test_pull_miso_assessments(self, test_db, mock_session_state):
        """Test pulling MISO assessments from database"""
        import streamlit as st
        
        # Set up session state with test database
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        assessments = pull_miso_assessments()
        
        assert isinstance(assessments, list)
        assert len(assessments) > 0
        assert "assessment_id" in assessments[0] or "series_id" in assessments[0]
    
    def test_pull_miso_executions(self, test_db, mock_session_state):
        """Test pulling MISO executions from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        executions = pull_miso_executions()
        
        assert isinstance(executions, list)
        assert len(executions) > 0
        assert "execution_id" in executions[0] or "series_id" in executions[0]
    
    def test_pull_cyber_assessments(self, test_db, mock_session_state):
        """Test pulling cyber assessments from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        assessments = pull_cyber_assessments()
        
        assert isinstance(assessments, list)
        # May be empty if no cyber assessments in test DB
        if len(assessments) > 0:
            assert "assessment_id" in assessments[0] or "cyber_id" in assessments[0]
    
    def test_pull_series_and_cyber_data_home(self, test_db, mock_session_state):
        """Test pulling series and cyber data for Home page"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        data = pull_series_and_cyber_data("Home")
        
        assert isinstance(data, list)
        # May be empty if no data, but should be a list
        if len(data) > 0:
            # Home type returns dicts with specific fields
            assert "series_id" in data[0] or "name" in data[0] or "cyber_id" in data[0]
    
    def test_pull_series_and_cyber_data_export(self, test_db, mock_session_state):
        """Test pulling series and cyber data for Export page"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        data = pull_series_and_cyber_data("Export")
        
        assert isinstance(data, list)
        assert len(data) == 2  # Returns [miso_data, cyber_data]
        assert isinstance(data[0], list)  # MISO data
        assert isinstance(data[1], list)  # Cyber data
    
    def test_pull_series_and_cyber_data_analytics(self, test_db, mock_session_state):
        """Test pulling series and cyber data for Analytics page"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        data = pull_series_and_cyber_data("Analytics")
        
        assert isinstance(data, list)
        assert len(data) == 2  # Returns [miso_data, cyber_data]
    
    def test_pull_other_classifications(self, test_db, mock_session_state):
        """Test pulling other classifications from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        other_class = pull_other_classifications()
        
        assert isinstance(other_class, set)
        # Should not include standard classifications
        from modules.constants import CLASSIFICATIONS
        for cls in other_class:
            assert cls not in CLASSIFICATIONS or cls == ""
    
    def test_pull_other_threats(self, test_db, mock_session_state):
        """Test pulling other threats from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        other_threats = pull_other_threats()
        
        assert isinstance(other_threats, set)
        # Should not include standard threats
        from modules.constants import THREATS
        for threat in other_threats:
            assert threat not in THREATS or threat == ""
    
    def test_pull_other_miso_program(self, test_db, mock_session_state):
        """Test pulling other MISO programs from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        other_programs = pull_other_miso_program()
        
        assert isinstance(other_programs, set)
        # Should not include standard programs
        from modules.constants import MISO_PROGRAMS
        for program in other_programs:
            assert program not in MISO_PROGRAMS
    
    def test_pull_other_means(self, test_db, mock_session_state):
        """Test pulling other dissemination means from database"""
        import streamlit as st
        
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        other_means = pull_other_means()
        
        assert isinstance(other_means, set)
        # Should not include standard means
        from modules.constants import DISSEM_MEANS
        for mean in other_means:
            assert mean not in DISSEM_MEANS

