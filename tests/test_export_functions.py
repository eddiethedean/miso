"""
Tests for export functions in export module
"""
import pytest
import pandas as pd
import sqlite3
from io import BytesIO
from modules.export import (
    format_excel_sheet,
    get_available_fiscal_years,
    filter_table,
    close_preview_mode,
    reset_filters,
    refresh_export_data
)


class TestExportFunctions:
    """Test export utility functions"""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Sample DataFrame for testing"""
        return pd.DataFrame({
            "series_name": ["Operation Alpha", "Operation Bravo"],
            "tsoc": ["JSOC", "SOCAF"],
            "fiscal_year": [2023, 2024],
            "quarter": ["FYQ1", "FYQ2"],
            "start_year": [2023, 2024],
            "start_month": [1, 2],
            "fy_quarter_map": [
                {"2023": ["FYQ1", "FYQ2"]},
                {"2024": ["FYQ1", "FYQ2"]}
            ]
        })
    
    def test_format_excel_sheet(self, sample_dataframe):
        """Test format_excel_sheet function"""
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            sample_dataframe.to_excel(writer, sheet_name="Test", index=False, startrow=1)
            format_excel_sheet(writer, sample_dataframe, "Test")
        
        excel_buffer.seek(0)
        
        # Verify file was created
        assert excel_buffer.getvalue() is not None
        assert len(excel_buffer.getvalue()) > 0
    
    def test_format_excel_sheet_with_index(self, sample_dataframe):
        """Test format_excel_sheet with index=True"""
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            sample_dataframe.to_excel(writer, sheet_name="Test", index=True, startrow=1)
            format_excel_sheet(writer, sample_dataframe, "Test", index=True)
        
        excel_buffer.seek(0)
        assert len(excel_buffer.getvalue()) > 0
    
    def test_get_available_fiscal_years(self, sample_dataframe):
        """Test get_available_fiscal_years function"""
        years = get_available_fiscal_years(sample_dataframe)
        
        assert isinstance(years, list)
        assert 2023 in years
        assert 2024 in years
    
    def test_get_available_fiscal_years_empty(self):
        """Test get_available_fiscal_years with empty DataFrame"""
        empty_df = pd.DataFrame()
        years = get_available_fiscal_years(empty_df)
        
        assert isinstance(years, list)
        assert len(years) == 0
    
    def test_get_available_fiscal_years_no_column(self, sample_dataframe):
        """Test get_available_fiscal_years with missing column"""
        df_no_col = sample_dataframe.drop(columns=["fy_quarter_map"])
        years = get_available_fiscal_years(df_no_col)
        
        assert isinstance(years, list)
        assert len(years) == 0
    
    def test_filter_table_by_name(self, sample_dataframe):
        """Test filter_table filtering by series name"""
        import streamlit as st
        
        st.session_state["miso_export_name"] = "Alpha"
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        assert len(filtered) == 1
        assert "Alpha" in filtered["series_name"].iloc[0]
    
    def test_filter_table_by_tsoc(self, sample_dataframe):
        """Test filter_table filtering by TSOC"""
        import streamlit as st
        
        st.session_state["miso_export_tsoc"] = ["JSOC"]
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        assert len(filtered) == 1
        assert filtered["tsoc"].iloc[0] == "JSOC"
    
    def test_filter_table_by_fiscal_year(self, sample_dataframe):
        """Test filter_table filtering by fiscal year"""
        import streamlit as st
        
        st.session_state["miso_export_fiscal_year"] = [2023]
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        assert len(filtered) >= 1
        # Check that filtered data has the fiscal year
        for _, row in filtered.iterrows():
            fy_map = row["fy_quarter_map"]
            assert isinstance(fy_map, dict)
            assert "2023" in fy_map or any("2023" in str(k) for k in fy_map.keys())
    
    def test_filter_table_by_quarter(self, sample_dataframe):
        """Test filter_table filtering by quarter"""
        import streamlit as st
        
        st.session_state["miso_export_quarters"] = ["FYQ1"]
        st.session_state["miso_export_fiscal_year"] = [2023]
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        # Should filter to rows with FYQ1 in the specified year
        assert isinstance(filtered, pd.DataFrame)
    
    def test_filter_table_by_start_date(self, sample_dataframe):
        """Test filter_table filtering by start date"""
        import streamlit as st
        from datetime import date
        
        st.session_state["miso_export_start_date"] = date(2023, 1, 1)
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        # Should filter to rows with start date >= 2023-01-01
        assert isinstance(filtered, pd.DataFrame)
        if len(filtered) > 0:
            for _, row in filtered.iterrows():
                if pd.notnull(row["start_year"]) and pd.notnull(row["start_month"]):
                    row_date = date(int(row["start_year"]), int(row["start_month"]), 1)
                    assert row_date >= date(2023, 1, 1)
    
    def test_filter_table_by_end_date(self, sample_dataframe):
        """Test filter_table filtering by end date"""
        import streamlit as st
        from datetime import date
        
        st.session_state["miso_export_end_date"] = date(2023, 12, 31)
        
        filtered = filter_table(sample_dataframe.copy(), "miso")
        
        # Should filter to rows with start date <= 2023-12-31
        assert isinstance(filtered, pd.DataFrame)
    
    def test_close_preview_mode(self):
        """Test close_preview_mode function"""
        import streamlit as st
        
        st.session_state["show_export_preview"] = True
        st.session_state["show_cyber_export_preview"] = True
        
        close_preview_mode()
        
        assert st.session_state["show_export_preview"] == False
        assert st.session_state["show_cyber_export_preview"] == False
    
    def test_reset_filters(self, test_db, mock_session_state):
        """Test reset_filters function"""
        import streamlit as st
        from datetime import date
        
        # Set up session state
        for key, value in mock_session_state.items():
            st.session_state[key] = value
        
        # Set some filter values
        st.session_state["miso_export_start_date"] = date(2023, 1, 1)
        st.session_state["miso_export_end_date"] = date(2023, 12, 31)
        st.session_state["miso_export_name"] = "Test"
        st.session_state["miso_export_quarters"] = ["FYQ1"]
        st.session_state["miso_export_tsoc"] = ["JSOC"]
        st.session_state["miso_export_fiscal_year"] = [2023]
        
        reset_filters("miso")
        
        assert st.session_state["miso_export_start_date"] is None
        assert st.session_state["miso_export_end_date"] is None
        assert st.session_state["miso_export_name"] == ""
        assert st.session_state["miso_export_quarters"] == []
        assert st.session_state["miso_export_tsoc"] == []
        assert st.session_state["miso_export_fiscal_year"] == []

