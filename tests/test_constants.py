"""
Tests for constants module
"""
import pytest
from modules.constants import (
    SERIES_SCHEMA,
    EXECUTION_SCHEMA,
    ASSESSMENT_SCHEMA,
    CYBER_SCHEMA,
    TSOCS,
    THREATS,
    MISO_PROGRAMS,
    CLASSIFICATIONS,
    QUARTERS,
    MONTH_MAP,
    DISSEM_MEANS,
    AUDIENCE,
    HPEM_PHASE
)


class TestConstants:
    """Test constants are properly defined"""
    
    def test_series_schema_not_empty(self):
        """Test SERIES_SCHEMA is not empty"""
        assert len(SERIES_SCHEMA) > 0
        assert isinstance(SERIES_SCHEMA, list)
    
    def test_execution_schema_not_empty(self):
        """Test EXECUTION_SCHEMA is not empty"""
        assert len(EXECUTION_SCHEMA) > 0
        assert isinstance(EXECUTION_SCHEMA, list)
    
    def test_assessment_schema_not_empty(self):
        """Test ASSESSMENT_SCHEMA is not empty"""
        assert len(ASSESSMENT_SCHEMA) > 0
        assert isinstance(ASSESSMENT_SCHEMA, list)
    
    def test_cyber_schema_not_empty(self):
        """Test CYBER_SCHEMA is not empty"""
        assert len(CYBER_SCHEMA) > 0
        assert isinstance(CYBER_SCHEMA, list)
    
    def test_tsocs_list(self):
        """Test TSOCS list"""
        assert isinstance(TSOCS, list)
        assert len(TSOCS) > 0
        assert "JSOC" in TSOCS
        assert "SOCAF" in TSOCS
    
    def test_threats_list(self):
        """Test THREATS list"""
        assert isinstance(THREATS, list)
        assert len(THREATS) > 0
        assert "NDS-PRC" in THREATS
        assert "NDS-RUS" in THREATS
    
    def test_miso_programs_list(self):
        """Test MISO_PROGRAMS list"""
        assert isinstance(MISO_PROGRAMS, list)
        assert len(MISO_PROGRAMS) > 0
        assert "CTWMP" in MISO_PROGRAMS
        assert "DACMP" in MISO_PROGRAMS
    
    def test_classifications_list(self):
        """Test CLASSIFICATIONS list"""
        assert isinstance(CLASSIFICATIONS, list)
        assert len(CLASSIFICATIONS) > 0
        assert "UNCLASS" in CLASSIFICATIONS
        assert "S//NF" in CLASSIFICATIONS
    
    def test_quarters_list(self):
        """Test QUARTERS list"""
        assert isinstance(QUARTERS, list)
        assert len(QUARTERS) == 4
        assert "FYQ1" in QUARTERS
        assert "FYQ4" in QUARTERS
    
    def test_month_map(self):
        """Test MONTH_MAP"""
        assert isinstance(MONTH_MAP, dict)
        assert MONTH_MAP["Jan"] == 1
        assert MONTH_MAP["Dec"] == 12
        assert len(MONTH_MAP) == 13  # 12 months + empty string
    
    def test_dissem_means_list(self):
        """Test DISSEM_MEANS list"""
        assert isinstance(DISSEM_MEANS, list)
        assert "Internet" in DISSEM_MEANS
        assert "Radio" in DISSEM_MEANS
    
    def test_audience_list(self):
        """Test AUDIENCE list"""
        assert isinstance(AUDIENCE, list)
        assert "Citizens" in AUDIENCE
        assert "Decision Makers" in AUDIENCE
    
    def test_hpem_phase_list(self):
        """Test HPEM_PHASE list"""
        assert isinstance(HPEM_PHASE, list)
        assert "Awareness" in HPEM_PHASE
        assert "Behavior Change" in HPEM_PHASE

