import streamlit as st
import pandas as pd
import io
import plotly.express as px
from datetime import datetime
from modules.data_operations import pull_series_and_cyber_data, pull_miso_assessments, pull_miso_executions
from modules.analytics_data_operations import pull_other_threats, add_tsocs_to_array, pull_other_miso_program, pull_other_means, how_many_of_type, pull_other_classifications
from modules.constants import TSOCS, QUARTERS
from modules.export import format_excel_sheet, get_available_fiscal_years
from modules.analytics_charts import miso_program_chart, active_miso_series_chart, series_by_audience_chart, series_by_threat_chart, hpem_phase_chart, means_chart

# def analytics_page():
#     st.image("images/construction.jpg")

def analytics_page():
    """
    Renders the Analytics page
    """
    with st.container(border=True):
        st.header(
            "Analytics",
            divider="grey")

        tab1, tab2, tab3 = st.tabs(["Tables", "Charts", "Metrics"])
        # Pull all series data and set that as master pull
        all_data = pull_series_and_cyber_data("Analytics")
        all_assessments = pull_miso_assessments()
        all_executions = pull_miso_executions()
        other_threats = pull_other_threats()
        other_miso_program = pull_other_miso_program()
        available_years = get_available_fiscal_years(pd.DataFrame(all_data[0]))

        with tab1:
            #This field is used for the filtering
            filtered_data = all_data

            # Construct a map object where the key is the FYQ and the value is an array of series that fall into that list
            series_map = {}
            # Need to get all of the "other" threats in the db
            other_class = pull_other_classifications()
            other_dissemination_means = pull_other_means()

            # Filter Container
            with st.container(border=True):
                st.write("Select data to include:")
                col1,col2,col3 = st.columns(3)
                with col1:
                    filter_years = st.multiselect("Reporting Fiscal Year(s)", available_years, key="analytics_fiscal_years")
                    include_support = st.checkbox("Include In Support of Another Unit", value=False)
                    if include_support:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_support_tsoc = st.checkbox("Include In Support by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                    include_no_support = st.checkbox("Include Not In Support of Another Unit", value=False)
                    if include_no_support:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_no_support_tsoc = st.checkbox("Include Not in Support by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                    include_classifications = st.checkbox("Include Classification", value=False)
                    if include_classifications:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_classifications_tsoc = st.checkbox("Include Classification by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                with col2:
                    filter_quarters = st.multiselect("Reporting Quarter(s)", QUARTERS, key="export_fiscal_quarter", help="If no quarters are selected; all will be included")
                    include_threats = st.checkbox("Include Threats", value=False)
                    if include_threats:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_threat_tsoc = st.checkbox("Include Threats by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                    include_miso_program = st.checkbox("Include PSYOP Program", value=False)
                    if include_miso_program:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_miso_program_tsoc = st.checkbox("Include PSYOP Program by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                    include_audience = st.checkbox("Include Target Audience Category", value=False)
                    if include_audience:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_audience_tsoc = st.checkbox("Include Target Audience Category by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                with col3:
                    filter_tsoc_list = st.multiselect(
                    "TSOC(s)",
                    TSOCS[1:],
                    key="export_tsoc"
                    )
                    include_means = st.checkbox("Include Dissemination Means", value=False)
                    if include_means:
                        col4, col5 = st.columns([1,8])
                        with col5:
                            include_means_tsoc = st.checkbox("Include Dissemination Means by TSOC", value=False, help="Only includes TSOC's selected in the TSOC selector")
                    include_hpem = st.checkbox("Include Current HPEM Phase", value=False)
           
            for series in filtered_data[0]: #0 because we are pulling cyber here too just because the current function does that

                # Need to get all of the fiscal years from each series and create a map of FYQ -> Array of series
                series_fy_quarter_map = series["fy_quarter_map"]
                years = list(series_fy_quarter_map.keys()) if series_fy_quarter_map else []
                for year in years:
                    # if (year in [str(x) for x in filter_years]) or (filter_years == []):
                    if (year in [str(x) for x in filter_years]):
                        for quarter in series_fy_quarter_map[year]:
                            if quarter in filter_quarters:
                                if series_map.get("FY" + year + "Q" + quarter[-1]):
                                    arr_to_append_to = series_map.get("FY" + year + "Q" + quarter[-1])
                                    arr_to_append_to.append(series)
                                    series_map["FY" + year + "Q" + quarter[-1]] = arr_to_append_to
                                else:
                                    series_map["FY" + year + "Q" + quarter[-1]] = [series]
                            elif filter_quarters == []: # Then just throw all quarters in
                                if series_map.get("FY" + year + "Q" + quarter[-1]):
                                    arr_to_append_to = series_map.get("FY" + year + "Q" + quarter[-1])
                                    arr_to_append_to.append(series)
                                    series_map["FY" + year + "Q" + quarter[-1]] = arr_to_append_to
                                else:
                                    series_map["FY" + year + "Q" + quarter[-1]] = [series]

            # These are the 4 buckets of DataTypes that will be on the left side of the table
            regular_types = ['Series'] # Series count is always in the table
            regular_types.extend([obj for obj in filter_tsoc_list])
            types_with_tsoc = []
            others = []

            # Apply the filter values to the data type list
            if include_support:
                regular_types.append('In Support')
                if include_support_tsoc:
                    types_with_tsoc.extend([*add_tsocs_to_array('In Support', filter_tsoc_list)])
            if include_no_support:
                regular_types.append('Not In Support')
                if include_no_support_tsoc:
                    types_with_tsoc.extend([*add_tsocs_to_array('Not In Support', filter_tsoc_list)])
            if include_classifications:
                regular_types.extend(['UNCLASS', 'S//NF', 'S//REL FVEY'])
                others.extend([*other_class])
                if include_classifications_tsoc:
                    types_with_tsoc.extend([
                        *add_tsocs_to_array('UNCLASS', filter_tsoc_list),
                        *add_tsocs_to_array('S//NF', filter_tsoc_list),
                        *add_tsocs_to_array('S//REL FVEY', filter_tsoc_list),
                        ])
            if include_threats:
                regular_types.extend(['NDS-DPRK', 'NDS-IRAN/ITN','NDS-PRC','NDS-RUS','NDS-VEO'])
                others.extend([*other_threats])
                if include_threat_tsoc:
                    types_with_tsoc.extend([
                        *add_tsocs_to_array('NDS-DPRK', filter_tsoc_list),
                        *add_tsocs_to_array('NDS-IRAN/ITN', filter_tsoc_list),
                        *add_tsocs_to_array('NDS-PRC', filter_tsoc_list),
                        *add_tsocs_to_array('NDS-RUS', filter_tsoc_list),
                        *add_tsocs_to_array('NDS-VEO', filter_tsoc_list),
                        ])
            if include_miso_program:
                regular_types.extend(['CTWMP','DACMP'])
                others.extend([*other_miso_program])
                if include_miso_program_tsoc:
                    types_with_tsoc.extend([
                        *add_tsocs_to_array('CTWMP', filter_tsoc_list),
                        *add_tsocs_to_array('DACMP', filter_tsoc_list),
                    ])
            if include_audience:
                regular_types.extend(['Citizens', 'Decision Makers', 'Defense Personnel', 'Influencers', 'Social Media Users'])
                if include_audience_tsoc:
                    types_with_tsoc.extend([
                        *add_tsocs_to_array('Citizens', filter_tsoc_list),
                        *add_tsocs_to_array('Decision Makers', filter_tsoc_list),
                        *add_tsocs_to_array('Defense Personnel', filter_tsoc_list),
                        *add_tsocs_to_array('Influencers', filter_tsoc_list),
                        *add_tsocs_to_array('Social Media Users', filter_tsoc_list),
                        ])
            if include_means:
                regular_types.extend(['Internet', 'Phone', 'Physical Event', 'Physical Product', 'Radio', 'Television Products'])
                others.extend([*other_dissemination_means])
                if include_means_tsoc:
                    types_with_tsoc.extend([
                        *add_tsocs_to_array('Internet', filter_tsoc_list),
                        *add_tsocs_to_array('Phone', filter_tsoc_list),
                        *add_tsocs_to_array('Physical Event', filter_tsoc_list),
                        *add_tsocs_to_array('Radio', filter_tsoc_list),
                        *add_tsocs_to_array('Television Products', filter_tsoc_list),
                        ])

            if include_hpem:
                regular_types.extend(['Data Not Available','Too Early','Awareness','Understanding','Attitude','Preference','Intention','Behavior Change'])

            # Need to loop through the "other" categories and add them to the data types list potentially with tsoc variants
            other_class_with_tsocs = []
            other_threats_with_tsocs = []
            other_miso_program_with_tsocs = []
            other_means_with_tsocs = []
            if include_classifications_tsoc:
                for classification in other_class:
                    other_class_with_tsocs.extend(add_tsocs_to_array(classification, filter_tsoc_list))
            if include_threat_tsoc:
                for threat in other_threats:
                    other_threats_with_tsocs.extend(add_tsocs_to_array(threat, filter_tsoc_list))
            if include_miso_program_tsoc:
                for program in other_miso_program:
                    other_miso_program_with_tsocs.extend(add_tsocs_to_array(program, filter_tsoc_list))
            if include_means_tsoc:
                for mean in other_dissemination_means:
                    other_means_with_tsocs.extend(add_tsocs_to_array(mean, filter_tsoc_list))

            others_with_tsoc = [
                 *other_class_with_tsocs,
                 *other_threats_with_tsocs,
                 *other_miso_program_with_tsocs,
                 *other_means_with_tsocs
            ]    
         
            # Now we start building the table
            table1Data = {
                "Data Types" : [*regular_types, *types_with_tsoc, *others,*others_with_tsoc ]
            }
            table1NamesData = {
                "Data Types" : [*regular_types, *types_with_tsoc, *others,*others_with_tsoc ]
            }

            series_set = [] # This will hold unique series that appear in the map after filters have been applied. To be used in the sum column
            seen_series_ids = set() # Track seen series IDs for O(1) lookup instead of O(n)
            for key in sorted(series_map.keys()):
                # Populate the series_set array to be used for sum column
                for series in series_map.get(key):
                    series_id_str = str(series["series_id"])
                    if series_id_str not in seen_series_ids:
                        seen_series_ids.add(series_id_str)
                        series_set.append(series)

                # Populate all of the other columns based on FY and quarter
                table1Data[key] = []
                table1NamesData[key] = []
                for type in regular_types:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "", True))
                for type in types_with_tsoc:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "", True))
                if include_classifications:
                    for type in other_class:
                        table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "classification", False))
                        table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "classification", True))
                if include_threats:
                    for type in other_threats:
                        table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "threats", False))
                        table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "threats", True))
                if include_miso_program:
                    for type in other_miso_program:
                        table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "miso_program", False))
                        table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "miso_program", True))
                if include_means:
                    for type in other_dissemination_means:
                        table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "means", False))
                        table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, False, "means", True))
                for type in other_class_with_tsocs:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "classification", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "classification", True))
                for type in other_threats_with_tsocs:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "threats", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "threats", True))
                for type in other_miso_program_with_tsocs:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "miso_program", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "miso_program", True))
                for type in other_means_with_tsocs:
                    table1Data[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "means", False))
                    table1NamesData[key].append(how_many_of_type(series_map.get(key), type, all_assessments, all_executions, True, "means", True))

            # Now we properly build the sum column
            sumArray = []
            sumNamesArray = []
            for type in regular_types:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "", True))
            for type in types_with_tsoc:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "", True))
            if include_classifications:
                for type in other_class:
                    sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "classification", False))
                    sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "classification", True))
            if include_threats:
                for type in other_threats:
                    sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "threats", False))
                    sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "threats", True))
            if include_miso_program:
                for type in other_miso_program:
                    sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "miso_program", False))
                    sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "miso_program", True))
            if include_means:
                for type in other_dissemination_means:
                    sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "means", False))
                    sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, False, "means", True))
            for type in other_class_with_tsocs:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "classification", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "classification", True))
            for type in other_threats_with_tsocs:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "threats", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "threats", True))
            for type in other_miso_program_with_tsocs:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "miso_program", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "miso_program", True))
            for type in other_means_with_tsocs:
                sumArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "means", False))
                sumNamesArray.append(how_many_of_type((filtered_data[0] if len(series_set) == 0 else series_set), type, all_assessments, all_executions, True, "means", True))

            table1Data["Sum"] = sumArray
            table1NamesData["Sum"] = sumNamesArray

            df1 = pd.DataFrame(table1Data)
            df1Names = pd.DataFrame(table1NamesData)

            st.title("Series Counts", help="Cells in this table represent the number of series that fall into the specified [fiscal year + quarter + data type]. The first column displays the data types that have been included in the selectors above. The sum column shows the number of unique series that are represented in that row of the table.")
           
            st.dataframe(df1, hide_index=True)

            excel_buffer = io.BytesIO()
         
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df1.to_excel(writer, sheet_name="Series Counts", index=False, startrow=1)
                format_excel_sheet(writer, df1, "Series Counts")
                df1Names.to_excel(writer, sheet_name="Series Names", index=False, startrow=1)
                format_excel_sheet(writer, df1Names, "Series Names")

            excel_buffer.seek(0)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            st.download_button(
                label="Download Counts with Sources",
                type="secondary",
                data=excel_buffer,
                file_name=f"exported_data_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download an excel sheet with two tabs. The first tab displays the counts in the above table. The second tab displays the series names that are represented by the counts in tab 1."
            )

            table2Data = {
                 "Data Types" : [*regular_types, *types_with_tsoc, *others,*others_with_tsoc ]
            }

            table2NamesData = {
                "Data Types" : [*regular_types, *types_with_tsoc, *others,*others_with_tsoc ]
            }

            # Table one needs names and then counts changes to produce numerical second table
            # Loop through all the FYQ, for the first ones, leave the values in, otherwise take the difference from the last value
            lastKey = ""
            sumArr = []
            sumNameArr = []
            for key in table1NamesData.keys():
                if key != "Data Types" and key != "Sum":
                    newArr = []
                    nameArr = [] # used to store added and removed names
                    if lastKey == "":
                        lastKey = key
                        nameIndex = 0
                        for dataType in table1NamesData["Data Types"]:
                            nameArr.append("Added: " + str(table1NamesData[key][nameIndex]))
                            sumNameArr.append(table1NamesData[key][nameIndex])
                            newArr.append(0)
                            sumArr.append(0)
                            nameIndex = nameIndex + 1
                        table2Data[key] = newArr
                        table2NamesData[key] = nameArr
                    else:
                        pastSeriesArr = table1NamesData[lastKey]
                        currentSeriesArr = table1NamesData[key]
               
                        index = 0
                        for dataType in table1NamesData["Data Types"]:
                            pastSeries = set(pastSeriesArr[index])
                            currentSeries = set(currentSeriesArr[index])
                            dropped = pastSeries - currentSeries
                            added = currentSeries - pastSeries
                            newArr.append(len(dropped) + len(added))
                            nameArr.append("Added: " + str(list(added)) + "\r\n\r\n" + "Dropped: " + str(list(dropped)))
                            sumArr[index] = sumArr[index] + len(dropped) + len(added)
                            sumNameArr[index].extend(currentSeriesArr[index])
                            sumNameArr[index] = list(set(sumNameArr[index]))
                            index = index + 1
                        table2Data[key] = newArr
                        table2NamesData[key] = nameArr
                        lastKey = key
            if lastKey == "":
                nameIndex = 0
                for dataType in table1NamesData["Data Types"]:
                    sumArr.append(0)
                    sumNameArr.append([])
                    nameIndex = nameIndex + 1
            table2Data["Sum"] = sumArr
            table2NamesData["All Series Affected"] = sumNameArr

            df2 = pd.DataFrame(table2Data)
            df2Names = pd.DataFrame(table2NamesData)
            st.title("Changes by Quarter",  help="Cells in this table represent the total count of changes in series count for a data type from the previous [fiscal year + quarter] to the current [fiscal year + quarter], taking into account series that have been added or dropped. A series that is in both (or not in both) the current column and the previous column for a given row will not be counted towards the 'Changes' count. The first column displays the data types that have been included in the selectors above. The sum column shows the number of changes for that row's data type across the time period specified. The first time period represented in the chart will always show 0 changes for all data types.")
            st.dataframe(df2, hide_index=True)

            excel_buffer2 = io.BytesIO()
         
            with pd.ExcelWriter(excel_buffer2, engine='xlsxwriter') as writer:
                df2.to_excel(writer, sheet_name="Changes by Quarter", index=False, startrow=1)
                format_excel_sheet(writer, df2, "Changes by Quarter")
                df2Names.to_excel(writer, sheet_name="Changes by Quarter (Names)", index=False, startrow=1)
                format_excel_sheet(writer, df2Names, "Changes by Quarter (Names)")

            excel_buffer2.seek(0)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            st.download_button(
                label="Download Changes with Sources",
                type="secondary",
                data=excel_buffer2,
                file_name=f"exported_data_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download an excel sheet with two tabs. The first tab displays the counts in the above table. The second tab displays the series names that are represented by the counts in tab 1, dictating which series were 'added' or 'dropped' from the previous time period."
            )

        with tab2:
            # Adjust this later when we start filtering to update the charts
            filtered_data = all_data[0]
   
            with st.container(border=True):
                st.write("Filters:")
                col1,col2,col3 = st.columns(3)
                with col1:
                    filter_years = st.multiselect("Reporting Fiscal Year(s)", available_years, key="analytics_fiscal_years_charts")

                with col2:
                    filter_quarters = []
                    if filter_years != []:
                        filter_quarters = st.multiselect("Reporting Quarter(s)", QUARTERS, key="charts_fiscal_quarter")
                   
                with col3:
                    filter_tsoc_list = st.multiselect(
                    "TSOC(s)",
                    TSOCS[1:],
                    key="charts_tsoc"
                    )

            if filter_years != []:
                included_series = []
                for series in filtered_data:
                    added = False
                    series_fy_quarter_map = series["fy_quarter_map"]
                    years = series_fy_quarter_map.keys()
                    for year in years:
                        if (year in [str(x) for x in filter_years]) and added is False:
                            if filter_quarters:
                                for quarter in series_fy_quarter_map[year]:
                                    if quarter in filter_quarters and added is False:
                                        included_series.append(series)
                                        added = True
                                        break
                            else:
                                included_series.append(series)
                                added = True
                                break

                filtered_data = included_series

            if filter_tsoc_list:
                included_series = []
                for tsoc in filter_tsoc_list:
                    for series in filtered_data:
                        if series["tsoc"] == tsoc:
                            included_series.append(series)
                filtered_data = included_series
 
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    active_miso_series_chart(filtered_data, filter_tsoc_list)

                with st.container(border=True):
                    series_by_audience_chart(filtered_data, filter_tsoc_list)

                with st.container(border=True):
                    hpem_phase_chart(filtered_data, all_assessments)
     
            with col2:
                with st.container(border=True):
                    series_by_threat_chart(filtered_data, other_threats, filter_tsoc_list)
                   
                with st.container(border=True):
                    miso_program_chart(other_miso_program, filtered_data, filter_tsoc_list)

                with st.container(border=True):
                    means_chart(filtered_data, other_dissemination_means, all_executions, filter_tsoc_list)
             
        with tab3:
            webTab, clickTab, EngagementsTab, EngagementRateTab = st.tabs(["Web Metrics", "Click Through Rate", "Engagements", "Engagement Rate"])