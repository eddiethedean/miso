"""
Tests for data_operations module
"""
import pytest
import sqlite3
from modules.data_operations import (
    check_for_existing_data,
    parse_postgres_array,
    clean_strict_input,
    clean_lenient_input,
    clean_classification_input,
    month_name_from_any
)
from modules.constants import SERIES_SCHEMA, MONTH_MAP


class TestDataOperations:
    """Test data operation utilities"""
    
    def test_check_for_existing_data_new(self):
        """Test check_for_existing_data with new entry"""
        result = check_for_existing_data(SERIES_SCHEMA)
        assert isinstance(result, dict)
        assert len(result) == len(SERIES_SCHEMA)
        assert all(key in result for key in SERIES_SCHEMA)
    
    def test_check_for_existing_data_existing(self):
        """Test check_for_existing_data with existing data"""
        existing = {"series_name": "Test", "classification": "UNCLASS"}
        result = check_for_existing_data(SERIES_SCHEMA, existing)
        assert result == existing
    
    def test_parse_postgres_array_empty(self):
        """Test parsing empty PostgreSQL array"""
        assert parse_postgres_array("") == []
        assert parse_postgres_array(None) == []
        assert parse_postgres_array("{}") == []
    
    def test_parse_postgres_array_simple(self):
        """Test parsing simple PostgreSQL array"""
        result = parse_postgres_array('{value1,value2,value3}')
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_postgres_array_quoted(self):
        """Test parsing PostgreSQL array with quoted strings"""
        result = parse_postgres_array('{"value 1","value 2","value 3"}')
        assert result == ["value 1", "value 2", "value 3"]
    
    def test_parse_postgres_array_mixed(self):
        """Test parsing PostgreSQL array with mixed quoted/unquoted"""
        result = parse_postgres_array('{value1,"value 2",value3}')
        assert result == ["value1", "value 2", "value3"]
    
    def test_parse_postgres_array_list(self):
        """Test parsing when input is already a list"""
        input_list = ["value1", "value2"]
        result = parse_postgres_array(input_list)
        assert result == input_list
    
    def test_clean_strict_input_valid(self):
        """Test clean_strict_input with valid characters"""
        result = clean_strict_input("test_field", "Valid Text 123()")
        assert result == "Valid Text 123()"
    
    def test_clean_strict_input_invalid(self):
        """Test clean_strict_input removes invalid characters"""
        result = clean_strict_input("test_field", "Invalid@#$%Text")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
        assert "%" not in result
    
    def test_clean_strict_input_none(self):
        """Test clean_strict_input with None"""
        result = clean_strict_input("test_field", None)
        assert result == ""
    
    def test_clean_lenient_input_valid(self):
        """Test clean_lenient_input with valid characters"""
        result = clean_lenient_input("test_field", "Valid Text 123()%&")
        assert "Valid Text 123()%&" in result
    
    def test_clean_lenient_input_invalid(self):
        """Test clean_lenient_input removes invalid characters"""
        result = clean_lenient_input("test_field", "Invalid@#$Text")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
    
    def test_clean_classification_input(self):
        """Test clean_classification_input"""
        result = clean_classification_input("classification", "UNCLASS")
        assert result == "UNCLASS"
    
    def test_clean_classification_input_lowercase(self):
        """Test clean_classification_input converts to uppercase"""
        result = clean_classification_input("classification", "unclass")
        assert result == "UNCLASS"
    
    def test_clean_classification_input_invalid(self):
        """Test clean_classification_input removes invalid characters"""
        result = clean_classification_input("classification", "UNCLASS123")
        assert "123" not in result
    
    def test_month_name_from_any_numeric(self):
        """Test month_name_from_any with numeric input"""
        assert month_name_from_any("1") == "Jan"
        assert month_name_from_any("12") == "Dec"
        assert month_name_from_any("6") == "Jun"
    
    def test_month_name_from_any_empty(self):
        """Test month_name_from_any with empty input"""
        assert month_name_from_any("") == "None"
        assert month_name_from_any(None) == "None"
    
    def test_month_name_from_any_invalid(self):
        """Test month_name_from_any with invalid input"""
        result = month_name_from_any("99")
        assert result == ""

