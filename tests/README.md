# Test Suite for MISO Management System

This directory contains the test suite for the MISO Management System using pytest and Streamlit's built-in testing framework.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Pytest fixtures and configuration
├── test_constants.py             # Tests for constants module
├── test_data_operations.py       # Tests for data operations utilities
├── test_analytics_data_operations.py  # Tests for analytics data operations
└── test_streamlit_app.py         # Tests using Streamlit's AppTest
```

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_constants.py
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=modules --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_data_operations.py::TestDataOperations::test_parse_postgres_array_simple
```

## Test Categories

### Unit Tests
- **test_constants.py**: Tests that all constants are properly defined
- **test_data_operations.py**: Tests utility functions like input cleaning, array parsing
- **test_analytics_data_operations.py**: Tests analytics calculation functions

### Integration Tests (Streamlit)
- **test_streamlit_app.py**: Tests using Streamlit's `AppTest` framework to test UI components

## Test Fixtures

The `conftest.py` file provides several fixtures:

- `test_db_path`: Creates a temporary database file
- `test_db`: Creates and populates a test database with sample data
- `mock_session_state`: Provides a mock Streamlit session state

## Writing New Tests

### For Non-Streamlit Functions

```python
import pytest
from modules.your_module import your_function

def test_your_function():
    result = your_function(input_data)
    assert result == expected_output
```

### For Streamlit Components

```python
from streamlit.testing.v1 import AppTest

def test_streamlit_component():
    test_script = """
import streamlit as st
from modules.your_module import your_page_function

your_page_function()
"""
    at = AppTest.from_string(test_script)
    at.run()
    # Assert on components
    assert len(at.markdown) > 0
```

## Test Coverage

To generate a coverage report:

```bash
pytest tests/ --cov=modules --cov-report=term-missing
```

For HTML report:

```bash
pytest tests/ --cov=modules --cov-report=html
open htmlcov/index.html
```

## Notes

- Tests use a temporary database to avoid affecting the main database
- Streamlit tests use `AppTest.from_string()` for isolated component testing
- All tests should be independent and not rely on execution order
- Use fixtures from `conftest.py` for database setup

