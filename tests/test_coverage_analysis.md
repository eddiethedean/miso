# Test Coverage Analysis

## Functions by Module

### modules/data_operations.py (17 functions)
- ✅ `check_for_existing_data` - TESTED
- ✅ `parse_postgres_array` - TESTED
- ✅ `month_name_from_any` - TESTED
- ✅ `clean_strict_input` - TESTED
- ✅ `clean_lenient_input` - TESTED
- ✅ `clean_classification_input` - TESTED
- ❌ `handle_radio_change` - NOT TESTED (Streamlit callback)
- ❌ `get_selected_data` - NOT TESTED (Streamlit cached function)
- ❌ `submit_button_disabled` - NOT TESTED (Streamlit function)
- ❌ `manual_user_email` - NOT TESTED (Streamlit function)
- ❌ `get_user_email` - NOT TESTED (API function)
- ❌ `country_city_selector` - NOT TESTED (Streamlit component)
- ❌ `render_select_with_other` - NOT TESTED (Streamlit component)
- ❌ `pull_cyber_assessments` - NOT TESTED (Database function)
- ❌ `pull_miso_assessments` - NOT TESTED (Database function)
- ❌ `pull_miso_executions` - NOT TESTED (Database function)
- ❌ `pull_series_and_cyber_data` - NOT TESTED (Database function)

**Coverage: 6/17 (35%)**

### modules/analytics_data_operations.py (8 functions)
- ✅ `get_hpem_for_series` - TESTED
- ✅ `get_means_for_series` - TESTED
- ✅ `how_many_of_type` - TESTED (comprehensive)
- ✅ `add_tsocs_to_array` - TESTED
- ❌ `pull_other_classifications` - NOT TESTED (Database function)
- ❌ `pull_other_threats` - NOT TESTED (Database function)
- ❌ `pull_other_miso_program` - NOT TESTED (Database function)
- ❌ `pull_other_means` - NOT TESTED (Database function)

**Coverage: 4/8 (50%)**

### modules/analytics_charts.py (6 functions)
- ❌ `means_chart` - NOT TESTED (Streamlit chart function)
- ❌ `hpem_phase_chart` - NOT TESTED (Streamlit chart function)
- ❌ `series_by_threat_chart` - NOT TESTED (Streamlit chart function)
- ❌ `series_by_audience_chart` - NOT TESTED (Streamlit chart function)
- ❌ `active_miso_series_chart` - NOT TESTED (Streamlit chart function)
- ❌ `miso_program_chart` - NOT TESTED (Streamlit chart function)

**Coverage: 0/6 (0%)**

### modules/export.py (13 functions)
- ❌ `close_preview_mode` - NOT TESTED (Streamlit function)
- ❌ `format_excel_sheet` - NOT TESTED (Excel formatting)
- ❌ `reset_filters` - NOT TESTED (Streamlit function)
- ❌ `get_available_fiscal_years` - NOT TESTED
- ❌ `refresh_export_data` - NOT TESTED (Database function)
- ❌ `render_export_filters` - NOT TESTED (Streamlit component)
- ❌ `filter_table` - NOT TESTED
- ❌ `export_page` - NOT TESTED (Streamlit page)
- ❌ `render_miso_tab` - NOT TESTED (Streamlit component)
- ❌ `render_cyber_tab` - NOT TESTED (Streamlit component)
- ❌ `render_ca_tab` - NOT TESTED (Streamlit component)

**Coverage: 0/13 (0%)**

### modules/analytics.py (1 function)
- ❌ `analytics_page` - NOT TESTED (Streamlit page - partially tested via AppTest)

**Coverage: 0/1 (0%)**

## Summary

**Total Functions: 45**
**Tested Functions: 10**
**Untested Functions: 35**

**Overall Coverage: ~22%**

## Missing Test Categories

1. **Database Functions** (11 functions) - Need database fixtures
2. **Streamlit UI Components** (18 functions) - Need AppTest integration
3. **Chart Functions** (6 functions) - Need AppTest with data fixtures

## Recommendations

1. Add tests for database functions using test database fixtures
2. Add AppTest tests for Streamlit components
3. Add tests for chart generation functions
4. Add tests for export functionality
5. Add tests for filter and data transformation functions

