import streamlit as st
import io
import pandas as pd
import plotly.express as px
from datetime import datetime
from modules.export import format_excel_sheet
from modules.analytics_data_operations import how_many_of_type

def means_chart(filtered_data, other_means, all_executions, allowed_tsocs):
    st.header("Dissemination Means")
    dfObj = {}
    if allowed_tsocs == []:
        dfObj = {
                        "JSOC": [
                            how_many_of_type(filtered_data, 'Internet JSOC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone JSOC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event JSOC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product JSOC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio JSOC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products JSOC', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " JSOC", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCAF": [
                            how_many_of_type(filtered_data, 'Internet SOCAF', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCAF', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCAF', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCAF', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCAF', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCAF', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCAF", [], all_executions, True, "means", False) for obj in other_means]
                        ],
                        "SOCCENT": [
                            how_many_of_type(filtered_data, 'Internet SOCCENT', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCCENT', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCCENT', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCCENT', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCCENT', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCCENT', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCCENT", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCEUR": [
                            how_many_of_type(filtered_data, 'Internet SOCEUR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCEUR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCEUR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCEUR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCEUR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCEUR', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCEUR", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCKOR": [
                            how_many_of_type(filtered_data, 'Internet SOCKOR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCKOR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCKOR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCKOR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCKOR', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCKOR', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCKOR", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCNORTH": [
                            how_many_of_type(filtered_data, 'Internet SOCNORTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCNORTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCNORTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCNORTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCNORTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCNORTH', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCNORTH", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCPAC": [
                            how_many_of_type(filtered_data, 'Internet SOCPAC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCPAC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCPAC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCPAC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCPAC', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCPAC', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCPAC", [], all_executions, True, "means", False) for obj in other_means]
                            ],
                        "SOCSOUTH": [
                            how_many_of_type(filtered_data, 'Internet SOCSOUTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Phone SOCSOUTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Event SOCSOUTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Physical Product SOCSOUTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Radio SOCSOUTH', [], all_executions, True, "", False),
                            how_many_of_type(filtered_data, 'Television Products SOCSOUTH', [], all_executions, True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCSOUTH", [], all_executions, True, "means", False) for obj in other_means]
                            ]
                    }
    else:
        for tsoc in allowed_tsocs:
            dfObj[tsoc] = [
                how_many_of_type(filtered_data, 'Internet ' + tsoc, [], all_executions, True, "", False),
                how_many_of_type(filtered_data, 'Phone ' + tsoc, [], all_executions, True, "", False),
                how_many_of_type(filtered_data, 'Physical Event ' + tsoc, [], all_executions, True, "", False),
                how_many_of_type(filtered_data, 'Physical Product ' + tsoc, [], all_executions, True, "", False),
                how_many_of_type(filtered_data, 'Radio ' + tsoc, [], all_executions, True, "", False),
                how_many_of_type(filtered_data, 'Television Products ' + tsoc, [], all_executions, True, "", False),
                *[how_many_of_type(filtered_data, obj + " " + tsoc, [], all_executions, True, "means", False) for obj in other_means]
            ]
    means_df = pd.DataFrame(dfObj, index=['Internet','Phone','Physical Event','Physical Product','Radio', 'Television Products', *other_means])

    st.bar_chart(means_df, stack=True, horizontal=True)

    with st.expander("Chart Data"):
        st.table(means_df)
        means_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(means_excel_buffer, engine='xlsxwriter') as writer:
            means_df.to_excel(writer, sheet_name="Dissemination Means", index=True, startrow=1)
            format_excel_sheet(writer, means_df, "Dissemination Means", index=True)
            means_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
                        label="Download",
                        type="secondary",
                        key="means_table_download",
                        data=means_excel_buffer,
                        file_name=f"exported_data_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

    with st.expander("Percentages"):
        sum_series_with_internet = how_many_of_type(filtered_data, 'Internet', [], all_executions, False, "", False)
        sum_series_with_social_media = how_many_of_type(filtered_data, 'Internet', [], all_executions, False, "", False, True)
        sum_series_with_physical_products = how_many_of_type(filtered_data, 'Physical Product', [], all_executions, False, "", False)
        sum_series_with_radio = how_many_of_type(filtered_data, 'Radio', [], all_executions, False, "", False)
        sum_series_with_phone = how_many_of_type(filtered_data, 'Phone', [], all_executions, False, "", False)
        sum_series_with_tv = how_many_of_type(filtered_data, 'Television', [], all_executions, False, "", False)
        sum_series_with_physical_event = how_many_of_type(filtered_data, 'Physical Event', [], all_executions, False, "", False)
        sum_series_with_means = (sum_series_with_internet +
                                 sum_series_with_phone +
                                 sum_series_with_physical_event +
                                 sum_series_with_physical_products +
                                 sum_series_with_radio +
                                 sum_series_with_tv)
        for mean in other_means:
            sum_series_with_means = sum_series_with_means + how_many_of_type(filtered_data, mean, [], all_executions, False, "means", False)

        if sum_series_with_means > 0:
            internet_ratio = sum_series_with_internet / sum_series_with_means
            if sum_series_with_internet > 0:
                social_media_ratio = sum_series_with_social_media / sum_series_with_internet
            else:
                social_media_ratio = -1
            products_ratio = sum_series_with_physical_products / sum_series_with_means
            radio_ratio = sum_series_with_radio / sum_series_with_means
            phone_ratio = sum_series_with_phone / sum_series_with_means
            tv_ratio = sum_series_with_tv / sum_series_with_means
            event_ratio = sum_series_with_physical_event / sum_series_with_means
       

            st.write(str(sum_series_with_internet) + "/" + str(sum_series_with_means) + "(" + f"{internet_ratio:.0%}" + ")" + " used Internet")
            if social_media_ratio != -1:
                st.write(str(sum_series_with_social_media) + "/" + str(sum_series_with_internet) + "(" + f"{social_media_ratio:.0%}" + ")" + " used Internet and Social Media")
            st.write(str(sum_series_with_physical_products) + "/" + str(sum_series_with_means) + "(" + f"{products_ratio:.0%}" + ")" + " used Physical Products")
            st.write(str(sum_series_with_physical_event) + "/" + str(sum_series_with_means) + "(" + f"{event_ratio:.0%}" + ")" + " used Physical Events")
            st.write(str(sum_series_with_radio) + "/" + str(sum_series_with_means) + "(" + f"{radio_ratio:.0%}" + ")" + " used Radio")
            st.write(str(sum_series_with_phone) + "/" + str(sum_series_with_means) + "(" + f"{phone_ratio:.0%}" + ")" + " used Phone")
            st.write(str(sum_series_with_tv) + "/" + str(sum_series_with_means) + "(" + f"{tv_ratio:.0%}" + ")" + " used TV")


        else:
            st.write("No Series Found")
       

def hpem_phase_chart(filtered_data, all_assessments):
    st.header("Series by HPEM Phase")

    hpem_df = pd.DataFrame(
                    {
                    "Phase": ['Data Not Available','Too Early','Awareness','Understanding','Attitude','Preference','Intention','Behavior Change'],
                    "Series Count": [
                    how_many_of_type(filtered_data, 'Data Not Available', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Too Early', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Awareness', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Understanding', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Attitude', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Preference', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Intention', all_assessments, [], False, "", False),
                    how_many_of_type(filtered_data, 'Behavior Change', all_assessments, [], False, "", False)],
                    }
                    )

    fig = px.bar(hpem_df, x="Series Count", y="Phase", orientation="h")
    st.plotly_chart(fig)
    with st.expander("Chart Data"):
        st.dataframe(hpem_df, hide_index=True)
        hpem_df_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(hpem_df_excel_buffer, engine='xlsxwriter') as writer:
            hpem_df.to_excel(writer, sheet_name="Series by HPEM Phase", index=False, startrow=1)
            format_excel_sheet(writer, hpem_df, "Series by HPEM Phase")
            hpem_df_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="Download",
            type="secondary",
            key="hpem_phase_chart_data",
            data=hpem_df_excel_buffer,
            file_name=f"exported_data_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def series_by_threat_chart(filtered_data, other_threats, allowed_tsocs):
    st.header("PSYOP Series by GCP Threat")
    dfObj = {}
    if allowed_tsocs == []:
        dfObj = {
            "JSOC": [
                            how_many_of_type(filtered_data, 'NDS-DPRK JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-IRAN/ITN JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-PRC JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-RUS JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-VEO JSOC', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " JSOC", [], [], True, "threats", False) for obj in other_threats]
                            ],
                        "SOCAF": [
                            how_many_of_type(filtered_data, 'NDS-DPRK SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-PRC SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-RUS SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-VEO SOCAF', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCAF", [], [], True, "threats", False) for obj in other_threats]

                        ],
                        "SOCCENT": [
                            how_many_of_type(filtered_data, 'NDS-DPRK SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-PRC SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-RUS SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-VEO SOCCENT', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCCENT", [], [], True, "threats", False) for obj in other_threats]

                            ],
                        "SOCEUR": [
                            how_many_of_type(filtered_data, 'NDS-DPRK SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-PRC SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-RUS SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-VEO SOCEUR', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCEUR", [], [], True, "threats", False) for obj in other_threats]

                            ],
                            "SOCKOR": [
                                how_many_of_type(filtered_data, 'NDS-DPRK SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-PRC SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-RUS SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-VEO SOCKOR', [], [], True, "", False),
                                *[how_many_of_type(filtered_data, obj + " SOCKOR", [], [], True, "threats", False) for obj in other_threats]

                            ],
                            "SOCNORTH": [
                                how_many_of_type(filtered_data, 'NDS-DPRK SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-PRC SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-RUS SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-VEO SOCNORTH', [], [], True, "", False),
                                *[how_many_of_type(filtered_data, obj + " SOCNORTH", [], [], True, "threats", False) for obj in other_threats]

                            ],
                            "SOCPAC": [
                                how_many_of_type(filtered_data, 'NDS-DPRK SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-PRC SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-RUS SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-VEO SOCPAC', [], [], True, "", False),
                                *[how_many_of_type(filtered_data, obj + " SOCPAC", [], [], True, "threats", False) for obj in other_threats]

                            ],
                            "SOCSOUTH": [
                                how_many_of_type(filtered_data, 'NDS-DPRK SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-IRAN/ITN SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-PRC SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-RUS SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'NDS-VEO SOCSOUTH', [], [], True, "", False),
                                *[how_many_of_type(filtered_data, obj + " SOCSOUTH", [], [], True, "threats", False) for obj in other_threats]
                            ]
        }
    else:
        for tsoc in allowed_tsocs:
            dfObj[tsoc] = [
                          how_many_of_type(filtered_data, 'NDS-DPRK ' + tsoc, [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-IRAN/ITN ' + tsoc, [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-PRC ' + tsoc, [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-RUS ' + tsoc, [], [], True, "", False),
                            how_many_of_type(filtered_data, 'NDS-VEO ' + tsoc, [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " " + tsoc, [], [], True, "threats", False) for obj in other_threats]
            ]
    series_by_threat_df = pd.DataFrame(dfObj, index=['NDS-DPRK','NDS-IRAN/ITN','NDS-PRC','NDS-RUS','NDS-VEO', *other_threats])


    st.bar_chart(series_by_threat_df, stack=True, horizontal=True)

    with st.expander("Chart Data"):
        st.table(series_by_threat_df)
        series_by_threat_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(series_by_threat_excel_buffer, engine='xlsxwriter') as writer:
            series_by_threat_df.to_excel(writer, sheet_name="PSYOP Series by GCP Threat", index=True, startrow=1)
            format_excel_sheet(writer, series_by_threat_df, "PSYOP Series by GCP Threat", index=True)
            series_by_threat_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
                            label="Download",
                            type="secondary",
                            key="series_by_threat_table_download",
                            data=series_by_threat_excel_buffer,
                            file_name=f"exported_data_{timestamp}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

def series_by_audience_chart(filtered_data, allowed_tsocs):
    st.header("PSYOP Series by Target Audience")
    dfObj = {}
    if allowed_tsocs == []:
        dfObj = {
                        "JSOC": [
                            how_many_of_type(filtered_data, 'Citizens JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Decision Makers JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Defense Personnel JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Influencers JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Social Media Users JSOC', [], [], True, "", False),
                            ],
                        "SOCAF": [
                            how_many_of_type(filtered_data, 'Citizens SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Decision Makers SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Defense Personnel SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Influencers SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Social Media Users SOCAF', [], [], True, "", False),
                        ],
                        "SOCCENT": [
                            how_many_of_type(filtered_data, 'Citizens SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Decision Makers SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Defense Personnel SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Influencers SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Social Media Users SOCCENT', [], [], True, "", False),
                            ],
                        "SOCEUR": [
                            how_many_of_type(filtered_data, 'Citizens SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Decision Makers SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Defense Personnel SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Influencers SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'Social Media Users SOCEUR', [], [], True, "", False),
                            ],
                            "SOCKOR": [
                                how_many_of_type(filtered_data, 'Citizens SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Decision Makers SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Defense Personnel SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Influencers SOCKOR', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Social Media Users SOCKOR', [], [], True, "", False),
                            ],
                            "SOCNORTH": [
                                how_many_of_type(filtered_data, 'Citizens SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Decision Makers SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Defense Personnel SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Influencers SOCNORTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Social Media Users SOCNORTH', [], [], True, "", False),
                            ],
                            "SOCPAC": [
                                how_many_of_type(filtered_data, 'Citizens SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Decision Makers SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Defense Personnel SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Influencers SOCPAC', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Social Media Users SOCPAC', [], [], True, "", False),
                            ],
                            "SOCSOUTH": [
                                how_many_of_type(filtered_data, 'Citizens SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Decision Makers SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Defense Personnel SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Influencers SOCSOUTH', [], [], True, "", False),
                                how_many_of_type(filtered_data, 'Social Media Users SOCSOUTH', [], [], True, "", False),
                            ]
                    }
    else:
        for tsoc in allowed_tsocs:
            dfObj[tsoc] = [
                how_many_of_type(filtered_data, 'Citizens ' + tsoc, [], [], True, "", False),
                how_many_of_type(filtered_data, 'Decision Makers ' + tsoc, [], [], True, "", False),
                how_many_of_type(filtered_data, 'Defense Personnel ' + tsoc, [], [], True, "", False),
                how_many_of_type(filtered_data, 'Influencers ' + tsoc, [], [], True, "", False),
                how_many_of_type(filtered_data, 'Social Media Users ' + tsoc, [], [], True, "", False),
            ]

    series_by_audience_df = pd.DataFrame(dfObj, index=['Citizens','Decision Makers','Defense Personnel','Influencers','Social Media Users'])

    st.bar_chart(series_by_audience_df, stack=True, horizontal=True)

    with st.expander("Chart Data"):
        st.table(series_by_audience_df)
        series_by_audience_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(series_by_audience_excel_buffer, engine='xlsxwriter') as writer:
            series_by_audience_df.to_excel(writer, sheet_name="PSYOP Series by Target Audience", index=True, startrow=1)
            format_excel_sheet(writer, series_by_audience_df, "PSYOP Series by Target Audience", index=True)
            series_by_audience_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
                        label="Download",
                        type="secondary",
                        key="series_by_audience_table_download",
                        data=series_by_audience_excel_buffer,
                        file_name=f"exported_data_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

def active_miso_series_chart(filtered_data, allowed_tsocs ):
    st.header("Active PSYOP Series")
    dfObj = {}
    if allowed_tsocs == []:
        dfObj["TSOC"] =  ['JSOC','SOCAF','SOCCENT','SOCEUR','SOCKOR','SOCNORTH','SOCPAC','SOCSOUTH']
        dfObj["Series Count"] =  [
                    how_many_of_type(filtered_data, 'JSOC', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCAF', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCCENT', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCEUR', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCKOR', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCNORTH', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCPAC', [], [], False, "", False),
                    how_many_of_type(filtered_data, 'SOCSOUTH', [], [], False, "", False)]

    else:
        dfObj["TSOC"] = allowed_tsocs
        dfObj["Series Count"] = []
        for tsoc in allowed_tsocs:
            dfObj["Series Count"].append(how_many_of_type(filtered_data, tsoc, [], [], False, "", False))

    active_miso_df = pd.DataFrame(dfObj)

    fig = px.bar(active_miso_df, x="Series Count", y="TSOC", orientation="h")
    st.plotly_chart(fig)
    with st.expander("Chart Data"):
        st.dataframe(active_miso_df, hide_index=True)
        active_miso_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(active_miso_excel_buffer, engine='xlsxwriter') as writer:
            active_miso_df.to_excel(writer, sheet_name="Active PSYOP Series", index=False, startrow=1)
            format_excel_sheet(writer, active_miso_df, "Active PSYOP Series")
            active_miso_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="Download",
            type="secondary",
            data=active_miso_excel_buffer,
            file_name=f"exported_data_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def miso_program_chart(other_miso_program, filtered_data, allowed_tsocs):
    st.header("PSYOP Series by PSYOP Program")
    dfObj = {}
    if allowed_tsocs == []:
        dfObj = {
                        "JSOC": [
                            how_many_of_type(filtered_data, 'CTWMP JSOC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP JSOC', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " JSOC", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCAF": [
                            how_many_of_type(filtered_data, 'CTWMP SOCAF', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCAF', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCAF", [], [], True, "miso_program", False) for obj in other_miso_program]
                        ],
                        "SOCCENT": [
                            how_many_of_type(filtered_data, 'CTWMP SOCCENT', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCCENT', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCCENT", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCEUR": [
                            how_many_of_type(filtered_data, 'CTWMP SOCEUR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCEUR', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCEUR", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCKOR": [
                            how_many_of_type(filtered_data, 'CTWMP SOCKOR', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCKOR', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCKOR", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCNORTH": [
                            how_many_of_type(filtered_data, 'CTWMP SOCNORTH', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCNORTH', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCNORTH", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCPAC": [
                            how_many_of_type(filtered_data, 'CTWMP SOCPAC', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCPAC', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCPAC", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ],
                        "SOCSOUTH": [
                            how_many_of_type(filtered_data, 'CTWMP SOCSOUTH', [], [], True, "", False),
                            how_many_of_type(filtered_data, 'DACMP SOCSOUTH', [], [], True, "", False),
                            *[how_many_of_type(filtered_data, obj + " SOCSOUTH", [], [], True, "miso_program", False) for obj in other_miso_program]
                            ]
                    }
    else:
        for tsoc in allowed_tsocs:
            dfObj[tsoc] = [
                how_many_of_type(filtered_data, 'CTWMP ' + tsoc, [], [], True, "", False),
                how_many_of_type(filtered_data, 'DACMP ' + tsoc, [], [], True, "", False),
                *[how_many_of_type(filtered_data, obj + " " + tsoc, [], [], True, "miso_program", False) for obj in other_miso_program]
            ]
    series_by_program_df = pd.DataFrame(dfObj, index=['CTWMP', 'DACMP', *other_miso_program])

    st.bar_chart(series_by_program_df, stack=True, horizontal=True)

    with st.expander("Chart Data"):
        st.table(series_by_program_df)
        series_by_program_excel_buffer = io.BytesIO()
        with pd.ExcelWriter(series_by_program_excel_buffer, engine='xlsxwriter') as writer:
            series_by_program_df.to_excel(writer, sheet_name="PSYOP Series by PSYOP Program", index=True, startrow=1)
            format_excel_sheet(writer, series_by_program_df, "PSYOP Series by PSYOP Program", index=True)
            series_by_program_excel_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
                            label="Download",
                            type="secondary",
                            key="series_by_program_table_download",
                            data=series_by_program_excel_buffer,
                            file_name=f"exported_data_{timestamp}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )