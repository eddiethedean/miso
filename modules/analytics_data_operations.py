import streamlit as st
from modules.constants import THREATS, MISO_PROGRAMS,DISSEM_MEANS, TSOCS, CLASSIFICATIONS,AUDIENCE,HPEM_PHASE

# Get all hpem for a given series
def get_hpem_for_series(all_assessments,series):
    toReturn = set()
    for assessment in all_assessments:
        if assessment["series_id"] == series["series_id"]:
            toReturn.add(assessment["current_hpem_phase"])
    return toReturn

# Get all dissemination means for a given series
def get_means_for_series(all_executions,series, check_for_social_media=False):
    toReturn = set()
    for execution in all_executions:
        if check_for_social_media:
            if execution["series_id"] == series["series_id"] and ("Social Media" in execution["dissemination_method"].replace("{", "").replace("}", "") or "RBR (social media)" in execution["dissemination_method"].replace("{", "").replace("}", "")):
                cleaned_list = execution["dissemination_means"].replace("{", "").replace("}", "").replace("\"", "")
                toReturn.update(cleaned_list.split(','))
        else:
            if execution["series_id"] == series["series_id"]:
                cleaned_list = execution["dissemination_means"].replace("{", "").replace("}", "").replace("\"", "")
                toReturn.update(cleaned_list.split(','))
    return toReturn

# Calculates how many series given a restriction exist in the system. Can optionally return names instead of counts
def how_many_of_type(arr, type, all_assessments, all_executions, is_tsoc_specific, other_category, return_names, check_for_social_media=False):
    if is_tsoc_specific:
        # Need to figure out which tsoc
        tsoc = type.split(" ")[-1]
        type = type[:-(len(tsoc) + 1)]
        arr = [obj for obj in arr if obj["tsoc"] == tsoc]
    if type == "Series":
        if return_names:
            return [obj["series_name"] for obj in arr]
        else:
            return len(arr)
    elif type in TSOCS:
        filtered_arr = [obj for obj in arr if obj["tsoc"] == type]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in ["In Support", "Not In Support"]:
        filtered_arr = [obj for obj in arr if obj["support_another_unit"] == (False if type == "Not In Support" else True)]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in CLASSIFICATIONS or other_category == "classification":
        filtered_arr = [obj for obj in arr if obj["classification"] == type]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)    
    elif type in THREATS or other_category == "threats":
        filtered_arr = [obj for obj in arr if obj["nds_threat"] == type]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in MISO_PROGRAMS or other_category == "miso_program":
        filtered_arr = [obj for obj in arr if obj["miso_program"] == type]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in AUDIENCE:
        filtered_arr = [obj for obj in arr if obj["target_audience_category"] == type]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in DISSEM_MEANS or other_category == "means":
        filtered_arr = [obj for obj in arr if type in get_means_for_series(all_executions, obj, check_for_social_media)]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    elif type in HPEM_PHASE:
        filtered_arr = [obj for obj in arr if type in get_hpem_for_series(all_assessments, obj)]
        if return_names:
            return [obj["series_name"] for obj in filtered_arr]
        else:
            return len(filtered_arr)
    else:
        if return_names:
            return []
        else:
            return 0

# Pulls classifications that were input by the user as "other"
def pull_other_classifications():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT classification
        FROM miso_series
        WHERE is_active = True
        """)
        classifications = cur.fetchall()
        other_class_set = set()
        for classification in classifications:
            if classification[0] not in CLASSIFICATIONS:
                other_class_set.add(classification[0])
    except Exception as e:
        st.warning(e)
    return other_class_set

# Pulls threats that were input by the user as "other"
def pull_other_threats():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT nds_threat
        FROM miso_series
        WHERE is_active = True
        """)
        threats = cur.fetchall()
        other_threat_set = set()
        for threat in threats:
            if threat[0] not in THREATS:
                other_threat_set.add(threat[0])

    except Exception as e:
        st.warning(e)
    return other_threat_set

# Pulls miso programs  that were input by the user as "other"
def pull_other_miso_program():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT miso_program
        FROM miso_series
        WHERE is_active = True
        """)
        other_programs = cur.fetchall()
        other_programs_set = set()
        for program in other_programs:
            if program[0] not in MISO_PROGRAMS:
                other_programs_set.add(program[0])

    except Exception as e:
        st.warning(e)
    return other_programs_set

# Pulls dissemination means that were input by the user as "other"
def pull_other_means():
    try:
        cur = st.session_state["conn"].cursor()
        cur.execute("""
        SELECT dissemination_means
        FROM miso_execution
        WHERE is_active = True
        """)
        other_means = cur.fetchall()
        other_means_set = set()
        for means in other_means:
            mean_list = means[0].lstrip(means[0][0]).rstrip(means[0][-1]).split(",")
            for actual_mean in mean_list:
                actual_mean = str(actual_mean.replace("\"", ""))
                if actual_mean not in DISSEM_MEANS:
                    other_means_set.add(actual_mean)
    except Exception as e:
        st.warning(e)
    # return other_programs_set
    return other_means_set

# Takes a category and adds "tsoc" lables to it based on the list of allowed tsocs
def add_tsocs_to_array(category, allowed_tsocs):
    toReturn = []
    for tsoc in allowed_tsocs:
        toReturn.append(category + " " + tsoc)
    return toReturn
