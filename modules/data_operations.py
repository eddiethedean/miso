"""
For functions used by by multiple pages
"""
import streamlit as st
import pandas as pd
import sqlite3
import re
import requests
import logging
from dateutil import parser
from modules.constants import MONTH_MAP


def handle_radio_change(value):
    st.session_state["objective"] = value


# To cache the incoming data
@st.cache_data
def get_selected_data(data):
    selected_data = data
    return selected_data


# Check if create/update buttons are disabled or not
@st.cache_data
def submit_button_disabled(data):
    """
    Disable the submit button until all required fields are populated.
    Handles strings, lists, and None values.
    """
    # Check that every value is present and non-empty
    for key, value in data.items():
        if value is None:
            st.warning(
                f"The field '{key}' is required but has no value. "
                "Fields with (*NR) are NOT REQUIRED."
            )
            return True
        if isinstance(value, str) and value.strip() == "":
            st.warning(
                f"The field '{key}' is required but empty. "
                "Fields with (*NR) are NOT REQUIRED."
            )
            return True
        if isinstance(value, list) and not value:
            st.warning(
                f"The field '{key}' requires at least one selection. "
                "Fields with (*NR) are NOT REQUIRED."
            )
            return True

    # All validations passed
    st.success("Data is ready for submission")
    return False


# Checks whether we're creating a new entry or updating an entry
# Returns None if we're creating a new entry
def check_for_existing_data(schema, existing_data=None):
    if existing_data is None:
        index = dict.fromkeys(schema)
    else:
        index = existing_data
    return index


def parse_postgres_array(pg_array_str):
    """Parses a PostgreSQL array string into a list of strings."""
    if not pg_array_str:
        return []
    if isinstance(pg_array_str, list):
        return pg_array_str
    trimmed = pg_array_str.strip("{}")
    # Capture both quoted and unquoted strings
    raw_matches = re.findall(r'"(.*?)"|([^",]+)', trimmed)
    return [match[0] if match[0] else match[1] for match in raw_matches]


def manual_user_email(key: str):
    """
    Displays a validated SOCOM email input field in Streamlit.

    Args:
        key (str): Unique Streamlit key for the text input widget.

    Returns:
        str | None: A valid trimmed email address if valid, else None.
    """
    if "user_email" in st.session_state:
        return st.session_state.user_email
    email = st.text_input("Enter your SOCOM email", key=key)
    if email and not re.match(r"^[^@\s]+@socom\.mil$", email.strip(), re.IGNORECASE):
        st.error("Please enter a SOCOM email address.")
        return None
    if email:
        st.session_state.user_email = email.strip()
        st.rerun()

    return email.strip() if email else None


def get_user_email(session=None, connect_server=None, content_guid=None):
    """
    Attempts to retrieve the most recent Posit Connect user's email.
    """
    try:
        if not session or not connect_server or not content_guid:
            connect_server = st.secrets["database"]["CONNECT_SERVER"]
            api_key = st.secrets["database"]["CONNECT_API_KEY"]
            content_guid = st.secrets["database"]["TARGET_CONTENT_GUID"]
            session = requests.Session()
            session.headers.update({"Authorization": f"Key {api_key}"})

        # Get visits
        url = f"{connect_server}/__api__/v1/instrumentation/content/visits"
        response = session.get(url, params={"content_guid": content_guid}, verify=False)
        response.raise_for_status()
        data = response.json()
        visits = []
        visits.extend(data.get("results", []))
        next_page = data.get("paging", {}).get("next")
        while next_page:
            response = session.get(next_page, verify=False)
            response.raise_for_status()
            data = response.json()
            visits.extend(data.get("results", []))
            next_page = data.get("paging", {}).get("next")
        if not visits:
            raise ValueError("No visits found")
        df_visits = pd.DataFrame(visits)
        df_visits["time"] = pd.to_datetime(df_visits["time"])
        most_recent = df_visits.iloc[-1]
        user_guid = most_recent["user_guid"]
        if not user_guid:
            raise ValueError("No user GUID available")

        # Get user info
        user_url = f"{connect_server}/__api__/v1/users/{user_guid}"
        user_response = session.get(user_url, verify=False)
        if user_response.status_code != 200:
            raise ValueError("User info lookup failed")
        user_data = user_response.json()
        email = user_data.get("email")
        return email

    except Exception:
        return None


def country_city_selector(
    label_prefix,
    countries_df,
    cities_df,
    country_key,
    city_key,
    selected_countries_arr=None,
    selected_cities_arr=None
):
    """
    Streamlit component to select countries and cities from worldcities.csv data.

    Args:
        label_prefix (str): Prefix label for Streamlit widgets (e.g., "Series").
        countries_df (pd.DataFrame): DataFrame with unique ['iso3', 'country'] columns.
        cities_df (pd.DataFrame): Full DataFrame from worldcities.csv.
        country_key (str): Streamlit key for storing selected countries.
        city_key (str): Streamlit key for storing selected city display strings.

    Returns:
        Tuple[List[str], List[str]]: selected_countries (ISO3 codes), selected_locations (display strings)
    """
    # Sort countries for dropdown
    countries_df = countries_df.dropna(subset=["iso3", "country"]).drop_duplicates()
    iso3_to_country = dict(zip(countries_df["iso3"], countries_df["country"]))
    country_options = sorted(iso3_to_country.keys())
    # Sanitize defaults: only keep those that are in options
    selected_countries_arr = [c for c in (selected_countries_arr or []) if c in country_options]
    # The following 3 if statements ensure that we clear the cities from the options when the countries are cleared
    if "Createseries_country" in st.session_state and st.session_state["active_page"] == "createseries":
        if st.session_state["Createseries_country"] == [] or st.session_state["Createseries_country"] != st.session_state["selected_countries"]:
            st.session_state["selected_cities"] = []
       

    if "Updateseries_country" in st.session_state and st.session_state["active_page"] == "updateseries":
        # if st.session_state["Updateseries_country"] == [] or st.session_state["Updateseries_country"] != st.session_state["selected_cities"]:
        if st.session_state["Updateseries_country"] == [] or st.session_state["Updateseries_country"] != st.session_state["selected_countries"]:
            st.session_state["selected_cities"] = []
   
    if (country_key == "Createseries_country" and st.session_state["active_page"] == "createseries") or (country_key == "Updateseries_country" and st.session_state["active_page"] == "updateseries"):
        st.session_state["selected_countries"] = selected_countries_arr
        st.session_state["selected_cities"] = selected_cities_arr

    if len(selected_countries_arr) > 0:
        selected_countries = st.multiselect(
            f"**{label_prefix} Countries:**",
            options=country_options,
            default=selected_countries_arr,
            format_func=lambda iso3: f"{iso3_to_country.get(iso3, iso3)} ({iso3})",
            key=country_key
        )
    else:
        selected_countries = st.multiselect(
            f"**{label_prefix} Countries:**",
            options=country_options,
            format_func=lambda iso3: f"{iso3_to_country.get(iso3, iso3)} ({iso3})",
            key=country_key
        )
# Build city options based on selected countries
    if selected_countries:
        filtered = cities_df[cities_df["iso3"].isin(selected_countries)].copy()
    else:
        filtered = cities_df.iloc[0:0].copy()  # empty options when no country selected

    # Ensure admin_name exists (fallback to empty if missing)
    if "admin_name" not in filtered.columns:
        filtered["admin_name"] = ""

    # Display format must match what you use everywhere else
    # "City, Admin (Country Name, ISO3)"
    filtered["display"] = filtered.apply(
        lambda r: f"{r['city_ascii']}, {r['admin_name'] or ''} ({r['country']}, {r['iso3']})",
        axis=1
    )
    city_options = sorted(set(filtered["display"].tolist()))

    # Sanitize city defaults to those in options
    selected_cities_arr = [d for d in (selected_cities_arr or []) if d in city_options]

    if len(selected_cities_arr) > 0:
        selected_city_displays = st.multiselect(
            f"{label_prefix} Cities(*NR):",
            options=city_options,
            default=selected_cities_arr,
            help="Select one or more cities (or leave empty to apply to entire country).",
            key=city_key
        )
    else:
        selected_city_displays = st.multiselect(
            f"{label_prefix} Cities(*NR):",
            options=city_options,
            help="Select one or more cities (or leave empty to apply to entire country).",
            key=city_key
        )
    return selected_countries, selected_city_displays


def render_select_with_other(
    label, options, stored_value,
    key_prefix, action, help_text=None
):
    """
    - options: list of allowed options (include "OTHER" in options)
    - stored_value: string from DB
    """
    # If the stored value isn't in options and isn't empty, show "OTHER" and prefill the text input.
    if stored_value and stored_value not in options:
        default_index = options.index("OTHER") if "OTHER" in options else 0
        other_prefill = stored_value
    else:
        default_index = options.index(stored_value) if stored_value in options else 0
        other_prefill = ""

    selected = st.selectbox(
        label,
        options=options,
        index=default_index,
        key=f"{key_prefix}{action}_select",
        help=help_text
    )

    if selected == "OTHER":
        custom = st.text_input(
            "Please specify:",
            value=other_prefill,
            key=f"{key_prefix}{action}_OTHER",
            max_chars=50
        )
        final_value = custom.strip()
    else:
        final_value = selected

    return final_value


def month_name_from_any(val):
    MONTH_NUM_TO_NAME = {v: k for k, v in MONTH_MAP.items() if v is not None}
    if val in ("", None):
        return "None"
    try:
        n = int(val)
    except Exception:
        return ""
    return MONTH_NUM_TO_NAME.get(n, "")

def pull_cyber_assessments():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT *
        FROM cyber_assessment
        WHERE is_active = True
        """)
        cyber_assessments = cur.fetchall()
        columns =  [desc[0] for desc in cur.description]

        result_dicts = [dict(zip(columns, row)) for row in cyber_assessments]

    except Exception as e:
                st.warning(e)
    return result_dicts

def pull_miso_assessments():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT *
        FROM miso_assessment
        WHERE is_active = True
        """)
        assessments = cur.fetchall()
        columns =  [desc[0] for desc in cur.description]

        result_dicts = [dict(zip(columns, row)) for row in assessments]

    except Exception as e:
                st.warning(e)
    return result_dicts


def pull_miso_executions():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT *
        FROM miso_execution
        WHERE is_active = True
        """)
        executions = cur.fetchall()
        columns =  [desc[0] for desc in cur.description]

        result_dicts = [dict(zip(columns, row)) for row in executions]

    except Exception as e:
                st.warning(e)
    return result_dicts
# home or export
def pull_series_and_cyber_data(type):
    try:
        cur = st.session_state["conn"].cursor()
        if type == "Home":
            cur.execute("""
                SELECT series_id, series_name, executing_unit, start_month, start_year, end_month, end_year, tsoc, nds_threat, is_active, fiscal_year, quarter, fy_quarter_map
                FROM miso_series
                WHERE is_active = True
                """)
        else:
            cur.execute("""
                SELECT *
                FROM miso_series
                WHERE is_active = True
                """)
        all_series = cur.fetchall()  
        columns =  [desc[0] for desc in cur.description]
        if type == "Home":
            columns[1] = "name"
        cur.execute("""
                SELECT *
                FROM miso_location
                """)
        all_locations = cur.fetchall()
        location_map = {}
        country_map = {}
        country_code_map = {}
        for item in all_locations:
     
            if item[3] != None: # if city is not none
                if location_map.get(item[1]) == None: # if seriesId is not none
                    location_map[item[1]] = [item[3]] # store array of cities as value to seriesId as key
                else:
                    location_map[item[1]].append(item[3])
                   
            if country_map.get(item[1]) == None:
                country_map[item[1]] = [st.session_state["iso3_country_map"].get(item[2])]
         
                country_code_map[item[1]] = [item[2]]
            else:
                country_map[item[1]].append(st.session_state["iso3_country_map"].get(item[2]))
                country_code_map[item[1]].append(item[2])
        columns.append("city(s)")
        columns.append("country(s)")
        columns.append("type")      
        columns.append("country_code")    
        updated_all_series = []
        for row in all_series:
            if location_map.get(row[0]) != None:
                row = row + (",".join(location_map.get(row[0])),)
            else:
                row = row + (None,)
            if country_map.get(row[0]) != None:          
                row = row + (",".join(list(set(country_map.get(row[0])))),)
            else:
                row = row + (None,)
            row = row + ("psyop",)
            row = row + (",".join(list(set(country_code_map.get(row[0])))),)

            updated_all_series.append(row)

            # Now to pull cyber data and add it to the list
        if type == "Home":
            cur.execute("""
                SELECT cyber_id, cyber_name, component, start_month, start_year, end_month, end_year, tsoc, nds_threat, is_active, fiscal_year, quarter, fy_quarter_map
                FROM cyber_series
                WHERE is_active = True
                """)
        else:
            cur.execute("""
                SELECT *
                FROM cyber_series
                WHERE is_active = True
                """)
        cyber_series = cur.fetchall()  
        cyber_columns =  [desc[0] for desc in cur.description]
        if type == "Export":
            cyber_columns.append("city(s)")
            cyber_columns.append("country(s)")
            cyber_columns.append("type")
            cyber_columns.append("country_code")
        cur.execute("""
                SELECT *
                FROM cyber_location
                """)
        cyber_locations = cur.fetchall()
        location_map = {}
        country_map = {}
        country_code_map = {}
        for item in cyber_locations:
            if item[3] != None: # if city is not none
                if location_map.get(item[1]) == None: # if seriesId is not none
                    location_map[item[1]] = [item[3]] # store array of cities as value to seriesId as key
                else:
                    location_map[item[1]].append(item[3])
            if country_map.get(item[1]) == None:
                country_map[item[1]] = [st.session_state["iso3_country_map"].get(item[2])]
                country_code_map[item[1]] = [item[2]]
            else:
                country_map[item[1]].append(st.session_state["iso3_country_map"].get(item[2]))
                country_code_map[item[1]].append(item[2])

        for row in cyber_series:
            if location_map.get(row[0]) != None:
                row = row + (",".join(location_map.get(row[0])),)
            else:
                row = row + (None,)
            if country_map.get(row[0]) != None:
                row = row + (",".join(list(set(country_map.get(row[0])))),)
            else:
                row = row + (None,)
            row = row + ("cyber",)
            row = row + (",".join(list(set(country_code_map.get(row[0])))),)

            updated_all_series.append(row)
        result_dicts = [dict(zip(columns, row)) for row in updated_all_series]
    except Exception as e:
        st.warning(e)
        result_dicts = []
        updated_all_series = []
        columns = []
        cyber_columns = []
    if type == "Home":
        return result_dicts if 'result_dicts' in locals() else []
    else:
        if 'updated_all_series' in locals() and len(updated_all_series) > 0:
            result_dict_miso = [dict(zip(columns, row)) for row in updated_all_series if row[-2] == "psyop"]
            result_dict_cyber = [dict(zip(cyber_columns, row)) for row in updated_all_series if row[-2] =="cyber"]
            return [result_dict_miso, result_dict_cyber]
        else:
            return [[], []]


def clean_strict_input(field_name, raw_value):
    if raw_value is None:
        return ""
    original = raw_value.strip()
    improved = re.sub(r"[^a-zA-Z0-9\s(),\"']", "", original)
    cleaned = improved.strip()
    if improved != original:
        st.warning(
            f"Some characters were removed from '{field_name}'. "
            """Only a-z A-Z 0-9 () , " ' are allowed."""
        )
    return cleaned


def clean_lenient_input(field_name, raw_value):
    if raw_value is None:
        return ""
    original = raw_value.strip()
    # regex [^\s1-՚] adds a-zA-Z1-9'`=[];~@^_{}|:<>?
    improved = re.sub(r"[^a-zA-Z0-9\s.,;:+%&\-_/—(՚)\"\'\\]", "", original)
    cleaned = improved.strip()
    if raw_value != cleaned:
        st.warning(
            f"Some characters were removed from '{field_name}'. "
            r"""Only a-z A-Z 0-9 - % & () _ + ; ' : " , . \\\/ ՚ are allowed."""
        )

    return cleaned


def clean_classification_input(field_name, raw_value):
    if raw_value is None:
        return ""
    original = raw_value.strip().upper()
    cleaned = re.sub(r"[^A-Z\s/]", "", original)
    if original != cleaned:
        st.warning(
            f"Some characters were removed from '{field_name}'. "
            "Only uppercase letters and forward slashes are allowed."
        )

    return cleaned