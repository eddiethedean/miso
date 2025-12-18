"""
Initialize SQLite database with schema for MISO application
"""
import sqlite3
import json
from datetime import datetime
import random

def create_database(db_path='miso.db'):
    """Create database and all tables"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create miso_series table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS miso_series (
            series_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT NOT NULL,
            classification TEXT,
            support_another_unit BOOLEAN,
            executing_unit TEXT,
            executing_unit_service TEXT,
            series_actively_disseminating BOOLEAN,
            miso_program TEXT,
            miso_objective TEXT,
            supporting_miso_objective TEXT,
            start_month INTEGER,
            start_year INTEGER,
            end_month INTEGER,
            end_year INTEGER,
            fiscal_year INTEGER,
            calendar_year INTEGER,
            quarter TEXT,
            tsoc TEXT,
            nds_threat TEXT,
            gcp_threat TEXT,
            target_audience TEXT,
            target_audience_category TEXT,
            susceptibility_score TEXT,
            accessiblity_score TEXT,
            desired_behavior TEXT,
            threshold_percentage REAL,
            fy_quarter_map TEXT,
            is_active BOOLEAN DEFAULT 1,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT
        )
    """)
    
    # Create miso_execution table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS miso_execution (
            execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER,
            miso_execution TEXT,
            dissemination_start DATE,
            dissemination_end DATE,
            dissemination_means TEXT,
            dissemination_method TEXT,
            volume INTEGER,
            method_vol_map TEXT,
            participation_based_on_incentive BOOLEAN,
            attribution TEXT,
            collection_data_gathering_plan TEXT,
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT,
            FOREIGN KEY (series_id) REFERENCES miso_series(series_id)
        )
    """)
    
    # Create miso_assessment table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS miso_assessment (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER,
            execution_id INTEGER,
            baseline_data TEXT,
            moe_planned TEXT,
            moe_observed TEXT,
            threshold_met BOOLEAN,
            progress BOOLEAN,
            active_summary TEXT,
            list_integrated_information_forces TEXT,
            causation_correlation_supporting_data TEXT,
            planned_adjustments TEXT,
            current_hpem_phase TEXT,
            fiscal_year INTEGER,
            quarter TEXT,
            calendar_year INTEGER,
            is_active BOOLEAN DEFAULT 1,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT,
            FOREIGN KEY (series_id) REFERENCES miso_series(series_id),
            FOREIGN KEY (execution_id) REFERENCES miso_execution(execution_id)
        )
    """)
    
    # Create miso_location table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS miso_location (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER,
            country_code TEXT,
            city TEXT,
            FOREIGN KEY (series_id) REFERENCES miso_series(series_id)
        )
    """)
    
    # Create cyber_series table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cyber_series (
            cyber_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cyber_name TEXT NOT NULL,
            classification TEXT,
            cyber_objective TEXT,
            start_month INTEGER,
            start_year INTEGER,
            end_month INTEGER,
            end_year INTEGER,
            fiscal_year INTEGER,
            calendar_year INTEGER,
            quarter TEXT,
            tsoc TEXT,
            nds_threat TEXT,
            gcp_threat TEXT,
            key_activities TEXT,
            component TEXT,
            operators_enablers TEXT,
            equipment TEXT,
            training TEXT,
            education TEXT,
            target_audience TEXT,
            intelligence TEXT,
            authority TEXT,
            fy_quarter_map TEXT,
            is_active BOOLEAN DEFAULT 1,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT
        )
    """)
    
    # Create cyber_assessment table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cyber_assessment (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cyber_id INTEGER,
            success_indicators TEXT,
            success_measure TEXT,
            partners TEXT,
            challenges TEXT,
            way_forward TEXT,
            forward_comments TEXT,
            is_active BOOLEAN DEFAULT 1,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT,
            FOREIGN KEY (cyber_id) REFERENCES cyber_series(cyber_id)
        )
    """)
    
    # Create cyber_location table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cyber_location (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cyber_id INTEGER,
            country_code TEXT,
            city TEXT,
            FOREIGN KEY (cyber_id) REFERENCES cyber_series(cyber_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database created successfully at {db_path}")

if __name__ == "__main__":
    create_database()

