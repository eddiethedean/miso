import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
from modules.constants import TSOCS, QUARTERS
from modules.data_operations import (
    pull_series_and_cyber_data,
    pull_miso_executions,
    pull_miso_assessments,
    pull_cyber_assessments
)


def close_preview_mode():
    st.session_state["show_export_preview"] = False
    st.session_state["show_cyber_export_preview"] = False


def format_excel_sheet(writer, df, sheet_name, index=False):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    num_cols = len(df.columns) + (1 if index else 0)

    class_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#FF0000',
        'font_color': '#000000'
    })

    worksheet.merge_range(0, 0, 0, num_cols - 1, "SECRET//NOFORN", class_format)
    bottom_row = len(df) + 1
    worksheet.merge_range(bottom_row + 1, 0, bottom_row + 1, num_cols - 1, "SECRET//NOFORN", class_format)
    for col in range(num_cols):
        worksheet.set_column(col, col, 17)

def reset_filters(domain):
    st.session_state[f"{domain}_export_start_date"] = None
    st.session_state[f"{domain}_export_end_date"] = None
    st.session_state[f"{domain}_export_name"] = ""
    st.session_state[f"{domain}_export_quarters"] = []
    st.session_state[f"{domain}_export_tsoc"] = []
    st.session_state[f"{domain}_export_fiscal_year"] = []
    refresh_export_data()


def get_available_fiscal_years(df, year_col="fy_quarter_map"):
    if df.empty or year_col not in df.columns:
        return []

    years = set()
    for row in df[year_col].dropna():
        if isinstance(row, dict):
            years.update(int(y) for y in row.keys())

    return sorted(years)


def refresh_export_data():
    miso_and_cyber = pull_series_and_cyber_data("Export")
    st.session_state["all_export_miso"] = miso_and_cyber[0]
    st.session_state["all_export_cyber"] = miso_and_cyber[1]
    st.session_state["all_export_execution"] = pull_miso_executions()
    st.session_state["all_export_assessment"] = pull_miso_assessments()
    st.session_state["all_export_cyber_assessment"] = pull_cyber_assessments()
    st.session_state["active_miso"] = st.session_state["all_export_miso"]
    st.session_state["active_cyber"] = st.session_state["all_export_cyber"]
    st.session_state["active_execution"] = st.session_state["all_export_execution"]
    st.session_state["active_assessment"] = st.session_state["all_export_assessment"]
    st.session_state["active_cyber_assessment"] = st.session_state["all_export_cyber_assessment"]


def render_export_filters(domain, available_years):
    if f"{domain}_export_start_date" not in st.session_state:
        st.session_state[f"{domain}_export_start_date"] = None
    if f"{domain}_export_end_date" not in st.session_state:
        st.session_state[f"{domain}_export_end_date"] = None
    with st.container(border=True):
        st.markdown("Filters:")
        col1, col2, col3, col4 = st.columns([2,2,2,1])
        with col1:
            start_date = st.date_input(
                "Series Start Date (AFTER)",
                value=st.session_state[f"{domain}_export_start_date"],
                key=f"{domain}_export_start_date",
            )
            st.text_input("Series Name", key=f"{domain}_export_name")
        with col2:
            end_date = st.date_input(
                "Series Start Date (BEFORE)",
                value=st.session_state[f"{domain}_export_end_date"],
                key=f"{domain}_export_end_date",
            )
            st.multiselect("Reporting Fiscal Year(s)", available_years, key=f"{domain}_export_fiscal_year")
        with col3:
            st.multiselect("TSOC(s)", TSOCS, key=f"{domain}_export_tsoc")
            st.multiselect("Reporting Quarter(s)", QUARTERS, key=f"{domain}_export_quarters")
        with col4:
            st.button("Reset Filters", on_click=reset_filters, args=(domain,), key=f"{domain}_reset_filter_btn")
            st.button("Refresh Data", on_click=refresh_export_data, key=f"{domain}_refresh_btn")


def filter_table(table, domain):
    if st.session_state.get(f"{domain}_export_start_date"):
        start_date = st.session_state[f"{domain}_export_start_date"]

        table = table[
            (table["start_year"].notnull()) & (table["start_month"].notnull())
        ]

        table = table[
            table.apply(
                lambda row: date(int(row["start_year"]), int(row["start_month"]), 1) >=
                            date(start_date.year, start_date.month, 1),
                axis=1
            )
        ]

    if st.session_state.get(f"{domain}_export_end_date"):
        end_date = st.session_state[f"{domain}_export_end_date"]

        table = table[
            (table["start_year"].notnull()) & (table["start_month"].notnull())
        ]

        table = table[
            table.apply(
                lambda row: date(int(row["start_year"]), int(row["start_month"]), 1) <= date(end_date.year, end_date.month, 1),
                axis=1
            )
        ]

    if st.session_state.get(f"{domain}_export_name"):
        name_filter = st.session_state[f"{domain}_export_name"].lower()
        if domain == "miso":
            table = table[table["series_name"].str.lower().str.contains(name_filter)]
        else:
            table = table[table[f"{domain}_name"].str.lower().str.contains(name_filter)]

    if st.session_state.get(f"{domain}_export_fiscal_year"):
        fiscal_years = st.session_state[f"{domain}_export_fiscal_year"]

        table = table[
            table["fy_quarter_map"].apply(
                lambda fy_map: any(str(year) in fy_map for year in fiscal_years) if isinstance(fy_map, dict) else False
            )
        ]

    if st.session_state.get(f"{domain}_export_quarters"):
        quarters = st.session_state[f"{domain}_export_quarters"]

        if st.session_state.get(f"{domain}_export_fiscal_year"):
            table = table[
                table["fy_quarter_map"].apply(
                    lambda fy_map: any(
                        quarter in quarters
                        for year in fiscal_years if str(year) in fy_map
                        for quarter in fy_map[str(year)]
                    ) if isinstance(fy_map, dict) else False
                )
            ]
        else:
            table = table[
                table["fy_quarter_map"].apply(
                    lambda fy_map: any(
                        quarter in quarters
                        for quarter_list in fy_map.values() for quarter in quarter_list
                    ) if isinstance(fy_map, dict) else False
                )
            ]

    if st.session_state.get(f"{domain}_export_tsoc"):
        tsocs = st.session_state[f"{domain}_export_tsoc"]
        table = table[table["tsoc"].isin(tsocs)]

    return table


def export_page():
    st.header("Export", help="Export PSYOP, Cyber, and Civil Affairs data.", divider="grey")

    # Initialize if needed
    if st.session_state["all_export_miso"] == [] or st.session_state["all_export_cyber"] == []:
    # if st.session_state["all_export_miso"] == [] or st.session_state["all_export_cyber"] == [] or st.session_state["all_export_ca"] == []:
        refresh_export_data()

    if "active_export_tab" not in st.session_state:
        st.session_state["active_export_tab"] = "miso"

    def set_active_tab(tab):
        st.session_state["active_export_tab"] = tab

    # miso_tab, cyber_tab = st.tabs(["PSYOP Export", "Cyber Export"])
    miso_tab, cyber_tab, ca_tab = st.tabs(["PSYOP Export", "Cyber Export", "Civil Affairs Export"])

    if st.session_state["active_export_tab"] == "miso":
        with miso_tab:
            set_active_tab("miso")
            render_miso_tab()
        with cyber_tab:
            set_active_tab("cyber")
            render_cyber_tab()
        with ca_tab:
            set_active_tab("ca")
            render_ca_tab()
    elif st.session_state["active_export_tab"] == "cyber":
        with miso_tab:
            set_active_tab("miso")
            render_miso_tab()
        with cyber_tab:
            set_active_tab("cyber")
            render_cyber_tab()
        with ca_tab:
            set_active_tab("ca")
            render_ca_tab()
    elif st.session_state["active_export_tab"] == "ca":
        with miso_tab:
            set_active_tab("miso")
            render_miso_tab()
        with cyber_tab:
            set_active_tab("cyber")
            render_cyber_tab()
        with ca_tab:
            set_active_tab("ca")
            render_ca_tab()


def render_miso_tab():
    st.subheader("PSYOP Export")
    include_series_children = None
    include_exec_children = None
    # Initialize editable tables as empty DataFrames to avoid NameError
    editable_miso = pd.DataFrame()
    editable_execution_table = pd.DataFrame()
    editable_assessment_table = pd.DataFrame()
    original_assessment_df = pd.DataFrame()
    miso_table = pd.DataFrame()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        include_miso = st.checkbox("Include PSYOP Series", value=True)
    with col2:
        include_executions = st.checkbox(
            "Include PSYOP Executions",
            value=False if not include_miso else st.session_state.get("include_executions", False),
            disabled=not include_miso,
            key="include_executions"
        )
    with col3:
        include_assessments = st.checkbox(
            "Include PSYOP Assessments",
            value=False if not include_miso else st.session_state.get("include_assessments", False),
            disabled=not include_miso,
            key="include_assessments"
        )

    # Filters
    fiscal_years = get_available_fiscal_years(pd.DataFrame(st.session_state["all_export_miso"]))
    render_export_filters(domain="miso", available_years=fiscal_years)

    st.markdown("Make Selections:")
    with st.container(border=True):
        # Render MISO Series Table
        if include_miso:
            col1, col2, col3, col4 = st.columns([1, 1, 3, 1])
            with col1:
                st.markdown("PSYOP Series")
            with col3:
                include_series_children = st.checkbox(
                    "Include All Associated Reports",
                    key="include_miso_children",
                    help="Includes the PSYOP executions/assessments \
                        associated with the selected PSYOP series \
                        in the export (if included above in the \
                        top checkboxes). These will not appear \
                        in the selection tables but will appear \
                        in the preview tables."
                    )
            with col4:
                select_all_miso = st.checkbox("Select All", key="export_select_all_miso")
            miso_table = pd.DataFrame(st.session_state["active_miso"])
            if len(miso_table) > 0:
                miso_table = miso_table.drop(columns=["is_active"])
                miso_table = filter_table(miso_table, "miso")
                cols_to_convert = ['start_year', 'end_year', 'calendar_year']
                for col in cols_to_convert:
                    if col in miso_table.columns:
                        miso_table[col] = miso_table[col].astype('Int64').astype(str).replace('<NA>', '')

            column_configuration = {}
            for col in miso_table.columns:
                column_configuration[col] = st.column_config.Column(disabled=True)

            if select_all_miso:
                miso_table["Select"] = True
            else:
                miso_table["Select"] = False

            desired_order = [
                # "series_id",
                "series_name",
                "classification",
                "support_another_unit",
                "executing_unit",
                "executing_unit_service",
                "series_actively_disseminating",
                "miso_program",
                "miso_objective",
                "supporting_miso_objective",
            ]

            final_columns = ["Select"] + desired_order

            # Identify all other columns, except for updated last_cols
            last_cols = ["fy_quarter_map", "date_updated", "changed_by", "series_id"]
            additional_fields = [col for col in miso_table.columns if col not in final_columns + last_cols]

            # Final column order with updated/changed_by at the end
            final_order = final_columns + additional_fields + [col for col in last_cols if col in miso_table.columns]

            # Reorder the DataFrame
            miso_table = miso_table[[col for col in final_order if col in miso_table.columns]]

            column_configuration["Select"] = st.column_config.CheckboxColumn(
                "",
                help="Select this entry",
                default=False,
                required=False
            )
            editable_miso = st.data_editor(
                miso_table, column_config=column_configuration,
                hide_index=True, key="export_miso_editable",
                on_change=close_preview_mode()
            )

        # Render MISO Executions Table
        if include_executions:
            col1, col2, col3, col4 = st.columns([1, 1, 3, 1])
            with col1:
                st.markdown("PSYOP Executions")
            with col3:
                include_exec_children = st.checkbox(
                    "Include All Associated Reports",
                    key="include_exec_children",
                    help="Includes the PSYOP assessments associated \
                        with the selected PSYOP execution in the export \
                        (if included above in the top checkboxes). \
                        These will not appear in the selection tables \
                        but will appear in the preview tables.")
            with col4:
                select_all_execution = st.checkbox("Select All", key="export_select_all_execution")
            execution_table = pd.DataFrame(st.session_state["active_execution"])
            if len(execution_table) > 0:
                execution_table = execution_table.drop(columns=["is_active"])

            # Add the `series_name` column by mapping `series_id` to `series_name` from `miso_table`
            if "series_id" in execution_table.columns and "series_id" in miso_table.columns and "series_name" in miso_table.columns:
                valid_series_ids = miso_table["series_id"].dropna().unique()
                execution_table = execution_table[execution_table["series_id"].isin(valid_series_ids)]
                series_mapping = miso_table.set_index("series_id")["series_name"].to_dict()
                execution_table["series_name"] = execution_table["series_id"].map(series_mapping)

            execution_configuration = {}
            for col in execution_table.columns:
                execution_configuration[col] = st.column_config.Column(disabled=True)

            if select_all_execution:
                execution_table["Select"] = True
            else:
                execution_table["Select"] = False

            # Define the desired column order
            desired_order = [
                "series_name",
                "miso_execution",
                "dissemination_start",
                "dissemination_end",
                "dissemination_means",
                "dissemination_method",
                "method_vol_map",
            ]
            final_columns = ["Select"] + desired_order

            # Identify all other columns, except for updated last_cols
            last_cols = ["date_updated", "changed_by", "execution_id", "series_id"]
            additional_fields = [col for col in execution_table.columns if col not in final_columns + last_cols]

            # Final column order with updated/changed_by at the end
            final_order = final_columns + additional_fields + [col for col in last_cols if col in execution_table.columns]

            # Reorder the DataFrame
            execution_table = execution_table[[col for col in final_order if col in execution_table.columns]]

            # Add configuration for the "Select" column                
            execution_configuration["Select"] = st.column_config.CheckboxColumn(
                "",
                help="Select this entry",
                default=False,
                required=False
            )
            editable_execution_table = st.data_editor(
                execution_table, column_config=execution_configuration,
                hide_index=True, key="export_execution_editable",
                on_change=close_preview_mode()
            )

        # Render MISO Assessments Table
        if include_assessments:
            reference_execution_table = pd.DataFrame(st.session_state["active_execution"])
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown("PSYOP Assessments")
            with col3:
                select_all_assessment = st.checkbox("Select All", key="export_select_all_assessment")

            assessment_table = pd.DataFrame(st.session_state["active_assessment"])
            original_assessment_df = assessment_table.copy()
            if len(assessment_table) > 0:
                assessment_table = assessment_table.drop(columns=["is_active"], errors="ignore")

            # Create display-only versions of nullable boolean columns
            boolean_cols = ["progress", "threshold_met"]

            for col in boolean_cols:
                if col in assessment_table.columns:
                    assessment_table[f"{col}_display"] = assessment_table[col].fillna("—")

            # Map series_name and execution_name to assessments_table
            if ("series_id" in assessment_table.columns and "series_id" in miso_table.columns and "series_name" in miso_table.columns):
                valid_series_ids = miso_table["series_id"].dropna().unique()
                assessment_table = assessment_table[assessment_table["series_id"].isin(valid_series_ids)]
                series_mapping = miso_table.set_index("series_id")["series_name"].to_dict()
                assessment_table["series_name"] = assessment_table["series_id"].map(series_mapping)

            if ("execution_id" in assessment_table.columns and "execution_id" in reference_execution_table.columns and "miso_execution" in reference_execution_table.columns):
                exec_mapping = reference_execution_table.set_index("execution_id")["miso_execution"].to_dict()
                assessment_table["miso_execution"] = assessment_table["execution_id"].map(exec_mapping)

            # Apply the same mapping to the original_assessment_df for export
            if "series_id" in original_assessment_df.columns and "series_id" in miso_table.columns:
                original_assessment_df["series_name"] = original_assessment_df["series_id"].map(series_mapping)

            if "execution_id" in original_assessment_df.columns and "execution_id" in reference_execution_table.columns:
                original_assessment_df["miso_execution"] = original_assessment_df["execution_id"].map(exec_mapping)

            # Build visible table (drop real boolean columns from UI)
            visible_table = assessment_table.drop(columns=boolean_cols, errors="ignore")

            # Build column configuration
            assessment_configuration = {}
            for col in visible_table.columns:
                if col.endswith("_display"):
                    # Display-only text column
                    assessment_configuration[col] = st.column_config.TextColumn(
                        col.replace("_display", "").replace("_", " ").title(),
                        disabled=True
                    )
                else:
                    assessment_configuration[col] = st.column_config.Column(disabled=True)

            # Handle the "Select All" checkbox
            visible_table["Select"] = True if select_all_assessment else False

            # Add configuration for the "Select" column
            assessment_configuration["Select"] = st.column_config.CheckboxColumn(
                "",
                help="Select this entry",
                default=False,
                required=False
            )

            # Define the desired column order
            desired_order = [
                "series_name",
                "miso_execution",
                "progress_display",
                "threshold_met_display",
            ]

            # Always start with Select + desired order
            final_columns = ["Select"] + desired_order

            # Identify all other columns, except for updated last_cols
            last_cols = ["fiscal_year", "quarter", "calendar_year", "date_updated", "changed_by", "assessment_id", "execution_id", "series_id"]
            remaining_cols = [col for col in visible_table.columns if col not in final_columns + last_cols]

            final_order = final_columns + remaining_cols + last_cols

            visible_table = visible_table[[col for col in final_order if col in visible_table.columns]]

            # Render the editable assessment table
            editable_assessment_table = st.data_editor(
                visible_table,
                column_config=assessment_configuration,
                hide_index=True,
                key="export_assessment_editable",
                on_change=close_preview_mode()
            )

    preview_btn = st.button("Preview export", type="primary")
    if preview_btn or st.session_state["show_export_preview"]:
        if include_miso and not editable_miso.empty:
            selected_series = editable_miso[editable_miso["Select"]]
        else:
            selected_series = pd.DataFrame()

        if include_series_children and (include_executions or include_assessments) and not editable_miso.empty:
            selected_series_ids = editable_miso[editable_miso["Select"]]["series_id"]
            if include_executions and not editable_execution_table.empty and "series_id" in editable_execution_table.columns:
                editable_execution_table.loc[
                    editable_execution_table["series_id"].isin(selected_series_ids), 
                    "Select"
                ] = True
            if include_assessments and not editable_assessment_table.empty and "series_id" in editable_assessment_table.columns:
                editable_assessment_table.loc[
                    editable_assessment_table["series_id"].isin(selected_series_ids), 
                    "Select"
                ] = True

        if include_exec_children and include_assessments and not editable_execution_table.empty:
            selected_execution_ids = editable_execution_table[editable_execution_table["Select"]]["execution_id"]
            if not editable_assessment_table.empty and "execution_id" in editable_assessment_table.columns:
                editable_assessment_table.loc[
                    editable_assessment_table["execution_id"].isin(selected_execution_ids), 
                    "Select"
                ] = True

        if include_executions and not editable_execution_table.empty:
            selected_execution = editable_execution_table[editable_execution_table["Select"]]
        else:
            selected_execution = pd.DataFrame()
        if include_assessments and not editable_assessment_table.empty:
            selected_ids = editable_assessment_table.loc[editable_assessment_table["Select"], "assessment_id"].tolist()
            selected_assessment = original_assessment_df[original_assessment_df["assessment_id"].isin(selected_ids)]
            export_desired_order = ["series_name","miso_execution","progress","threshold_met"]
            export_last_cols = ["fiscal_year", "quarter", "calendar_year", "date_updated","changed_by","assessment_id","execution_id","series_id"]
            export_final_columns = [col for col in export_desired_order if col in selected_assessment.columns]
            export_remaining_cols = [col for col in selected_assessment.columns if col not in export_final_columns + export_last_cols]
            export_final_order = (export_final_columns + export_remaining_cols + [col for col in export_last_cols if col in selected_assessment.columns])
            selected_assessment = selected_assessment[export_final_order]
        else:
            selected_assessment = pd.DataFrame()

        st.session_state["show_export_preview"] = True

    # ---- Export Preview and Excel Download ----
    if st.session_state["show_export_preview"]:
        st.markdown("Tables to export:")
        with st.container(border=True):
            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                if not selected_series.empty:
                    st.markdown("PSYOP Series")
                    series_out = selected_series.drop(columns=["Select", "type"], errors="ignore")
                    st.dataframe(series_out, hide_index=True, key="export_series_table")
                    series_out.to_excel(writer, sheet_name="PSYOP", index=False, startrow=1)
                    format_excel_sheet(writer, series_out, "PSYOP")

                if not selected_execution.empty:
                    st.markdown("PSYOP Execution")
                    execution_out = selected_execution.drop(columns=["Select"], errors="ignore").copy()
                    st.dataframe(execution_out, hide_index=True)
                    execution_out.to_excel(writer, sheet_name="PSYOP Execution", index=False, startrow=1)
                    format_excel_sheet(writer, execution_out, "PSYOP Execution")

                if not selected_assessment.empty:
                    st.markdown("PSYOP Assessment")
                    assessment_out = selected_assessment.drop(columns=["Select"], errors="ignore").copy()
                    st.dataframe(assessment_out, hide_index=True)
                    assessment_out.to_excel(writer, sheet_name="PSYOP Assessment", index=False, startrow=1)
                    format_excel_sheet(writer, assessment_out, "PSYOP Assessment")

            excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download Excel File",
                type="primary",
                data=excel_buffer,
                file_name=f"exported_MISO_data_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# ---- Cyber Tab ----
def render_cyber_tab():
    st.subheader("Cyber Export")
    # Initialize editable tables as empty DataFrames to avoid NameError
    editable_cyber = pd.DataFrame()
    editable_cyber_assessment_table = pd.DataFrame()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        include_cyber = st.checkbox("Include Cyber Series", value=True)
    with col2:
        include_cyber_assessments = st.checkbox(
            "Include Cyber Assessments",
            value=False if not include_cyber else st.session_state.get("include_cyber_assessments", False),
            disabled=not include_cyber,
            key="include_cyber_assessments"
        )

    # Filters
    fiscal_years = get_available_fiscal_years(pd.DataFrame(st.session_state["all_export_cyber"]))
    render_export_filters(domain="cyber", available_years=fiscal_years)

    st.markdown("Make Selections:")
    with st.container(border=True):
        if include_cyber:
            col1, col2, col3, col4 = st.columns([1, 1, 3, 1])
            with col1:
                st.markdown("Cyber Series")
            with col3:
                include_cyber_series_children = st.checkbox(
                    "Include All Associated Reports",
                    key="include_cyber_children",
                    help="Includes the Cyber assessments \
                        associated with the selected Cyber series \
                        in the export (if included above in the \
                        top checkboxes). These will not appear \
                        in the selection tables but will appear \
                        in the preview tables."
                    )
            with col4:
                select_all_cyber = st.checkbox("Select All", key="export_select_all_cyber")
            cyber_table = pd.DataFrame(st.session_state["active_cyber"])
            if len(cyber_table) > 0:
                cyber_table = cyber_table.drop(columns=["is_active"], errors="ignore")
                cyber_table = filter_table(cyber_table, "cyber")
                cols_to_convert = ['start_year', 'end_year', 'calendar_year']
                for col in cols_to_convert:
                    if col in cyber_table.columns:
                        cyber_table[col] = cyber_table[col].astype('Int64').astype(str).replace('<NA>', '')

            column_configuration = {}
            for col in cyber_table.columns:
                column_configuration[col] = st.column_config.Column(disabled=True)

            if select_all_cyber:
                cyber_table["Select"] = True
            else:
                cyber_table["Select"] = False

            # Define column ordering
            desired_order = [
                "cyber_name",
                "classification",
            ]
            final_columns = ["Select"] + desired_order

            # Identify additional fields and reorder columns
            last_cols = ["fy_quarter_map", "date_updated", "changed_by", "cyber_id"]
            additional_fields = [col for col in cyber_table.columns if col not in final_columns + last_cols]
            final_order = final_columns + additional_fields + [col for col in last_cols if col in cyber_table.columns]
            cyber_table = cyber_table[[col for col in final_order if col in cyber_table.columns]]

            # Add "Select" column configuration
            column_configuration = {col: st.column_config.Column(disabled=True) for col in cyber_table.columns}
            column_configuration["Select"] = st.column_config.CheckboxColumn(
                "",
                help="Select this entry",
                default=False,
                required=False
            )

            # Render editable table
            editable_cyber = st.data_editor(
                cyber_table,
                column_config=column_configuration,
                hide_index=True,
                key="export_cyber_editable",
                on_change=close_preview_mode()
            )

        if include_cyber_assessments:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown("Cyber Assessments")
            with col3:
                select_all_cyber_assessment = st.checkbox("Select All", key="export_select_all_cyber_assessment")
            cyber_assessment_table = pd.DataFrame(st.session_state["active_cyber_assessment"])
            if len(cyber_assessment_table) > 0:
                cyber_assessment_table = cyber_assessment_table.drop(columns=["is_active"], errors="ignore")

            # Map series_name and execution_name to assessments
            if "cyber_id" in cyber_assessment_table.columns and "cyber_id" in cyber_table.columns:
                valid_cyber_ids = cyber_table["cyber_id"].dropna().unique()
                cyber_assessment_table = cyber_assessment_table[cyber_assessment_table["cyber_id"].isin(valid_cyber_ids)]
                cyber_series_mapping = cyber_table.set_index("cyber_id")["cyber_name"].to_dict()
                cyber_assessment_table["cyber_name"] = cyber_assessment_table["cyber_id"].map(cyber_series_mapping)

            cyber_assessment_configuration = {}
            for col in cyber_assessment_table.columns:
                cyber_assessment_configuration[col] = st.column_config.Column(disabled=True)

            # Handle the "Select All" checkbox
            if select_all_cyber_assessment:
                cyber_assessment_table["Select"] = True
            else:
                cyber_assessment_table["Select"] = False

            # Define the desired column order
            desired_order = [
                "cyber_name",
            ]

            final_columns = ["Select"] + desired_order

            # Identify all other columns, except for updated last_cols
            last_cols = ["date_updated", "changed_by", "assessment_id", "series_id"]
            additional_fields = [col for col in cyber_assessment_table.columns if col not in final_columns + last_cols]

            # Final column order with updated/changed_by at the end
            final_order = final_columns + additional_fields + [col for col in last_cols if col in cyber_assessment_table.columns]

            # Reorder the DataFrame
            cyber_assessment_table = cyber_assessment_table[[col for col in final_order if col in cyber_assessment_table.columns]]

            # Add configuration for the "Select" column
            cyber_assessment_configuration["Select"] = st.column_config.CheckboxColumn(
                "",
                help="Select this entry",
                default=False,
                required=False
            )

            # Render the editable assessment table
            editable_cyber_assessment_table = st.data_editor(
                cyber_assessment_table,
                column_config=cyber_assessment_configuration,
                hide_index=True,
                key="export_cyber_assessment_editable",
                on_change=close_preview_mode()
            )

    cyber_preview_btn = st.button("Preview export", type="primary", key="cyber_preview_export")
    if cyber_preview_btn or st.session_state["show_cyber_export_preview"]:
        if include_cyber and not editable_cyber.empty:
            selected_cyber = editable_cyber[editable_cyber["Select"]]
        else:
            selected_cyber = pd.DataFrame()

        if include_cyber_series_children and include_cyber_assessments and not editable_cyber.empty:
            selected_cyber_ids = editable_cyber[editable_cyber["Select"]]["cyber_id"]
            if not editable_cyber_assessment_table.empty and "cyber_id" in editable_cyber_assessment_table.columns:
                editable_cyber_assessment_table.loc[
                    editable_cyber_assessment_table["cyber_id"].isin(selected_cyber_ids), 
                    "Select"
                ] = True

        if include_cyber_assessments and not editable_cyber_assessment_table.empty:
            selected_cyber_assessment = editable_cyber_assessment_table[editable_cyber_assessment_table["Select"]]
        else:
            selected_cyber_assessment = pd.DataFrame()
        st.session_state["show_cyber_export_preview"] = True

    # ---- Export Preview and Excel Download ----
    if st.session_state["show_cyber_export_preview"]:
        st.markdown("Tables to export:")
        with st.container(border=True):
            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                if not selected_cyber.empty:
                    st.markdown("Cyber Series")
                    cyber_series_out = selected_cyber.drop(columns=["Select", "type"], errors="ignore")
                    st.dataframe(cyber_series_out, hide_index=True, key="export_cyber_series_table")
                    cyber_series_out.to_excel(writer, sheet_name="Cyber", index=False, startrow=1)
                    format_excel_sheet(writer, cyber_series_out, "Cyber")

                if not selected_cyber_assessment.empty:
                    st.markdown("Cyber Assessment")
                    cyber_assessment_out = selected_cyber_assessment.drop(columns=["Select"], errors="ignore").copy()
                    st.dataframe(cyber_assessment_out, hide_index=True)
                    cyber_assessment_out.to_excel(writer, sheet_name="Cyber Assessment", index=False, startrow=1)
                    format_excel_sheet(writer, cyber_assessment_out, "Cyber Assessment")

            excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download Excel File",
                type="primary",
                data=excel_buffer,
                key="cyber_download_excel_file",
                file_name=f"exported_MISO_data_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def render_ca_tab():
    st.subheader("Civil Affairs Export")
    st.image("images/construction.jpg")