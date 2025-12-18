import datetime


SERIES_SCHEMA = [
    'series_name',
    'classification',
    'support_another_unit',
    'executing_unit',
    'executing_unit_service',
    'series_actively_disseminating',
    'miso_program',
    'miso_objective'
    'supporting_miso_objective',
    'start_month',
    'start_year',
    'end_month',
    'end_year',
    'fiscal_year',
    'calendar_year',
    'quarter',
    'tsoc',
    'gcp_threat',
    'target_audience',
    'target_audience_category',
    'susceptibility_score',
    'accessiblity_score',
    'desired_behavior',
    'threshold_percentage',
]

EXECUTION_SCHEMA = [
    'miso_execution',
    'dissemination_start',
    'dissemination_end',
    'dissemination_means',
    'dissemination_method',
    'volume',
    'participation_based_on_incentive',
    'attribution',
    'collection_data_gathering_plan',
    'notes',
]

ASSESSMENT_SCHEMA = [
    'baseline_data',
    'moe_planned',
    'moe_observed',
    'threshold_met',
    'active_summary',
    'list_integrated_information_forces',
    'causation_correlation_supporting_data',
    'planned_adjustments',
    'current_hpem_phase',
]


CYBER_SCHEMA = [
    'cyber_name',
    'classification',
    'cyber_objective',
    'start_month',
    'start_year',
    'end_month',
    'end_year',
    'fiscal_year',
    'calendar_year',
    'quarter',
    'tsoc',
    'key_activities',
    'component',
    'operators_enablers',
    'equipment',
    'training',
    'education',
    'target_audience',
    'gcp_threat',
    'intelligence',
    'authority',
]

CYBER_ASSESS_SCHEMA = [
    'success_indicators',
    'success_measure',
    'partners',
    'challenges',
    'way_forward',
    'forward_comments',
]

CYBER_OP_TYPE = [
    '',
    'Offensive',
    'Defensive',
    'Intelligence Gathering',
    'Force Protection',
    'Other'
]

CYBER_AGENCIES = [
    '',
    'CYBERCOM',
    'JFHQ-C',
    'Services',
    'Other',
]

CYBER_AUTHORITY = [
    '',
    'GCC',
    'SOCOM',
    'Other',
]

CLASSIFICATIONS = [
 "", "UNCLASS", "S//NF", "S//REL FVEY", "OTHER"
]

BOOLEAN = {
    '': None,
    'Yes': True,
    'No': False,
}

QUERY_BY = [
    'All Entries',
    'TSOC',
    'Quarter',
]

MISO_PROGRAMS = [
    # '',
    'CTWMP',
    'DACMP',
    'Other',
]

MONTH_MAP = {
    '': None,
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

QUARTERS = [
    # '',
    'FYQ1',
    'FYQ2',
    'FYQ3',
    'FYQ4',
]

FISCAL_YEARS = list(range(datetime.datetime.now().year - 3, datetime.datetime.now().year + 2))

TSOCS = [
    '',
    'JSOC',
    'SOCAF',
    'SOCCENT',
    'SOCEUR',
    'SOCKOR',
    'SOCNORTH',
    'SOCPAC',
    'SOCSOUTH',
]

THREATS = [
    '',
    'NDS-DPRK',
    'NDS-IRAN/ITN',
    'NDS-PRC',
    'NDS-RUS',
    'NDS-VEO',
    'Other',
]

AUDIENCE = [
    # '',
    'Citizens',
    'Decision Makers',
    'Defense Personnel',
    'Influencers',
    'Social Media Users',
]

SCORE = [
    '',
    '1',
    '2',
    '3',
    '4',
    '5',
]

DISSEM_MEANS = [
    # '',
    'Internet',
    'Phone',
    'Physical Event',
    'Physical Product',
    'Radio',
    'Television Products',
    'Other',
]

DISSEM_METHODS_BY_MEANS = {
    "Internet": [
        "AdTech", "Social Media", "PAI (ads)", "PAO (online)",
        "RBR (social media)", "YouTube", "Google", "Other"
    ],
    "Phone": ["FABS-L (text)", "PULSE", "SMS", "Other"],
    "Physical Event": [
        "Face to Face", "Key Leader Engagement (KLE)",
        "Technical Exchange (TE)", "Workshop", "Other"
    ],
    "Physical Product": [
        "Brochure", "Comic Items", "Handbills",
        "Leaflets", "Newspaper Ad", "Poster", "Other"
    ],
    "Radio": ["Radio", "FABS-L (radio)", "Other"],
    "Television Products": ["TV", "Other"],
    "Other": ["Other"]
}

ATTRIBUTION = [
    '',
    'United States',
    'Partner',
    'None'
]

INFO_FORCES = [
    # '',
    'Civil Affairs (CA)',
    'Cyber',
    'JMWC',
    'Public Affairs (PA)',
    'None',
    'Other',
]

HPEM_PHASE = [
    '',
    'Data Not Available',
    'Too Early',
    'Awareness',
    'Understanding',
    'Attitude',
    'Preference',
    'Intention',
    'Behavior Change',
]

CITIES_FILE_PATH = "geojson_data/worldcities.csv"

CYBER_PARTNERS = [
    '',
    'US Joint Cyber',
    'US Joint MISO',
    'US Joint PA',
    'Foreign Partners',
    'Department of State',
    'No Collaboration',
    'Other',
]

SERVICES = [
    'Unknown',
    'USA',
    'USA CIV(Perm)',
    'USA CIV(Term)',
    'USA CTR(Perm)',
    'USA CTR(Term)',
    'USAF',
    'USCG',
    'USMC',
    'USN',
    'USSF',
]