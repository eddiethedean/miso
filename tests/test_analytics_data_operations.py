"""
Tests for analytics_data_operations module
"""
import pytest
from modules.analytics_data_operations import (
    how_many_of_type,
    add_tsocs_to_array,
    get_hpem_for_series,
    get_means_for_series
)
from modules.constants import TSOCS, THREATS, MISO_PROGRAMS, CLASSIFICATIONS, AUDIENCE, HPEM_PHASE


class TestAnalyticsDataOperations:
    """Test analytics data operations"""
    
    @pytest.fixture
    def sample_series_data(self):
        """Sample series data for testing"""
        return [
            {
                "series_id": 1,
                "series_name": "Operation Alpha",
                "tsoc": "JSOC",
                "support_another_unit": True,
                "classification": "UNCLASS",
                "nds_threat": "NDS-PRC",
                "miso_program": "CTWMP",
                "target_audience_category": "Citizens"
            },
            {
                "series_id": 2,
                "series_name": "Operation Bravo",
                "tsoc": "SOCAF",
                "support_another_unit": False,
                "classification": "S//NF",
                "nds_threat": "NDS-RUS",
                "miso_program": "DACMP",
                "target_audience_category": "Decision Makers"
            },
            {
                "series_id": 3,
                "series_name": "Operation Charlie",
                "tsoc": "JSOC",
                "support_another_unit": True,
                "classification": "UNCLASS",
                "nds_threat": "NDS-PRC",
                "miso_program": "CTWMP",
                "target_audience_category": "Citizens"
            }
        ]
    
    @pytest.fixture
    def sample_executions(self):
        """Sample execution data for testing"""
        return [
            {
                "series_id": 1,
                "dissemination_means": '{"Internet","Phone"}',
                "dissemination_method": '{"Social Media","SMS"}'
            },
            {
                "series_id": 2,
                "dissemination_means": '{"Radio"}',
                "dissemination_method": '{"Radio"}'
            }
        ]
    
    @pytest.fixture
    def sample_assessments(self):
        """Sample assessment data for testing"""
        return [
            {
                "series_id": 1,
                "current_hpem_phase": "Awareness"
            },
            {
                "series_id": 2,
                "current_hpem_phase": "Understanding"
            },
            {
                "series_id": 1,
                "current_hpem_phase": "Attitude"
            }
        ]
    
    def test_how_many_of_type_series(self, sample_series_data):
        """Test counting all series"""
        count = how_many_of_type(sample_series_data, "Series", [], [], False, "", False)
        assert count == 3
    
    def test_how_many_of_type_tsoc(self, sample_series_data):
        """Test counting by TSOC"""
        count = how_many_of_type(sample_series_data, "JSOC", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "SOCAF", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_support(self, sample_series_data):
        """Test counting by support status"""
        count = how_many_of_type(sample_series_data, "In Support", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "Not In Support", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_classification(self, sample_series_data):
        """Test counting by classification"""
        count = how_many_of_type(sample_series_data, "UNCLASS", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "S//NF", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_threat(self, sample_series_data):
        """Test counting by threat"""
        count = how_many_of_type(sample_series_data, "NDS-PRC", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "NDS-RUS", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_program(self, sample_series_data):
        """Test counting by MISO program"""
        count = how_many_of_type(sample_series_data, "CTWMP", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "DACMP", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_audience(self, sample_series_data):
        """Test counting by audience"""
        count = how_many_of_type(sample_series_data, "Citizens", [], [], False, "", False)
        assert count == 2
        
        count = how_many_of_type(sample_series_data, "Decision Makers", [], [], False, "", False)
        assert count == 1
    
    def test_how_many_of_type_return_names(self, sample_series_data):
        """Test returning names instead of count"""
        names = how_many_of_type(sample_series_data, "JSOC", [], [], False, "", True)
        assert isinstance(names, list)
        assert len(names) == 2
        assert "Operation Alpha" in names
        assert "Operation Charlie" in names
    
    def test_how_many_of_type_tsoc_specific(self, sample_series_data):
        """Test TSOC-specific filtering"""
        count = how_many_of_type(sample_series_data, "UNCLASS JSOC", [], [], True, "", False)
        assert count == 2  # Both JSOC series are UNCLASS
    
    def test_add_tsocs_to_array(self):
        """Test adding TSOCs to category array"""
        result = add_tsocs_to_array("CTWMP", ["JSOC", "SOCAF"])
        assert len(result) == 2
        assert "CTWMP JSOC" in result
        assert "CTWMP SOCAF" in result
    
    def test_add_tsocs_to_array_empty(self):
        """Test adding TSOCs with empty list"""
        result = add_tsocs_to_array("CTWMP", [])
        assert len(result) == 0
    
    def test_get_hpem_for_series(self, sample_assessments):
        """Test getting HPEM phases for a series"""
        phases = get_hpem_for_series(sample_assessments, {"series_id": 1})
        assert isinstance(phases, set)
        assert "Awareness" in phases
        assert "Attitude" in phases
        assert len(phases) == 2
    
    def test_get_means_for_series(self, sample_executions):
        """Test getting dissemination means for a series"""
        means = get_means_for_series(sample_executions, {"series_id": 1}, False)
        assert isinstance(means, set)
        assert "Internet" in means
        assert "Phone" in means
    
    def test_get_means_for_series_social_media(self, sample_executions):
        """Test getting means filtered for social media"""
        means = get_means_for_series(sample_executions, {"series_id": 1}, True)
        # Should only return means that have social media in method
        assert isinstance(means, set)

