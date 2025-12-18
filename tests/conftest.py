"""
Pytest configuration and fixtures
"""
import pytest
import sqlite3
import os
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def test_db_path():
    """Create a temporary database for testing"""
    # Use a temporary file
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture(scope="function")
def test_db(test_db_path):
    """Create and populate a test database"""
    # Initialize database schema
    from init_database import create_database
    create_database(test_db_path)
    
    # Generate minimal test data
    conn = sqlite3.connect(test_db_path)
    cur = conn.cursor()
    
    # Insert test MISO series
    cur.execute("""
        INSERT INTO miso_series (
            series_name, classification, support_another_unit, executing_unit,
            executing_unit_service, series_actively_disseminating, miso_program,
            miso_objective, tsoc, nds_threat, target_audience_category,
            start_year, start_month, end_year, end_month, fiscal_year, quarter,
            fy_quarter_map, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Test Operation Alpha-001", "UNCLASS", False, "1st PSYOP Battalion",
        "USA", True, "CTWMP", "Test objective", "JSOC", "NDS-PRC",
        "Citizens", 2023, 1, 2024, 12, 2023, "FYQ1",
        '{"2023": ["FYQ1", "FYQ2"]}', 1
    ))
    
    series_id = cur.lastrowid
    
    # Insert test execution
    cur.execute("""
        INSERT INTO miso_execution (
            series_id, miso_execution, dissemination_start, dissemination_end,
            dissemination_means, dissemination_method, volume, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        series_id, "Test Execution 1", "2023-01-15", "2023-02-15",
        '["Internet"]', '["Social Media"]', 10000, 1
    ))
    
    execution_id = cur.lastrowid
    
    # Insert test assessment
    cur.execute("""
        INSERT INTO miso_assessment (
            series_id, execution_id, baseline_data, moe_planned, moe_observed,
            current_hpem_phase, fiscal_year, quarter, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        series_id, execution_id, "Baseline test data", "MOE planned",
        "MOE observed", "Awareness", 2023, "FYQ1", 1
    ))
    
    # Insert test location
    cur.execute("""
        INSERT INTO miso_location (series_id, country_code, city)
        VALUES (?, ?, ?)
    """, (series_id, "AFG", "Kabul"))
    
    # Insert test cyber series
    cur.execute("""
        INSERT INTO cyber_series (
            cyber_name, classification, cyber_objective, tsoc, nds_threat,
            start_year, start_month, end_year, end_month, fiscal_year, quarter,
            fy_quarter_map, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Test Cyber Operation-001", "S//NF", "Cyber test objective",
        "SOCAF", "NDS-RUS", 2023, 1, 2024, 12, 2023, "FYQ1",
        '{"2023": ["FYQ1"]}', 1
    ))
    
    cyber_id = cur.lastrowid
    
    # Insert test cyber assessment
    cur.execute("""
        INSERT INTO cyber_assessment (
            cyber_id, success_indicators, success_measure, is_active
        ) VALUES (?, ?, ?, ?)
    """, (cyber_id, "Success indicator 1", "Measure 1", 1))
    
    conn.commit()
    conn.close()
    
    return test_db_path


@pytest.fixture
def mock_session_state(test_db):
    """Mock Streamlit session state with test database connection"""
    import streamlit as st
    
    # Create a mock connection
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    
    # Store in a dict that mimics session_state
    state = {
        "conn": conn,
        "iso3_country_map": {
            "AFG": "Afghanistan",
            "IRQ": "Iraq",
            "SYR": "Syria"
        },
        "all_export_miso": [],
        "all_export_cyber": [],
        "all_export_execution": [],
        "all_export_assessment": [],
        "all_export_cyber_assessment": [],
        "active_miso": [],
        "active_cyber": [],
        "active_execution": [],
        "active_assessment": [],
        "active_cyber_assessment": [],
        "show_export_preview": False,
        "show_cyber_export_preview": False,
        "active_page": "analytics"
    }
    
    yield state
    
    # Cleanup
    conn.close()

