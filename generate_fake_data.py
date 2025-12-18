"""
Generate fake data for MISO application using Faker
"""
import sqlite3
import random
import json
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import lorem, date_time
from modules.constants import (
    TSOCS, THREATS, MISO_PROGRAMS, CLASSIFICATIONS, AUDIENCE,
    DISSEM_MEANS, DISSEM_METHODS_BY_MEANS, ATTRIBUTION, HPEM_PHASE,
    QUARTERS, MONTH_MAP
)

# Initialize Faker
fake = Faker()
fake.add_provider(lorem)
fake.add_provider(date_time)

def generate_military_unit():
    """Generate a realistic military unit name"""
    unit_types = ["Battalion", "Group", "Brigade", "Regiment", "Squadron", "Company"]
    numbers = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
    specialties = ["PSYOP", "Special Forces", "Ranger", "Airborne", "Marine", "Navy"]
    return f"{random.choice(numbers)} {random.choice(specialties)} {random.choice(unit_types)}"

# Sample data
SAMPLE_SERVICES = ["USA", "USAF", "USN", "USMC", "USSF"]

# Common country codes for operations
SAMPLE_COUNTRIES = ["AFG", "IRQ", "SYR", "YEM", "SOM", "NGA", "MLI", "PHL", "IDN", "THA", "PAK", "LBY", "SDN", "KEN", "UGA"]

def generate_fy_quarter_map(start_year, num_quarters=4):
    """Generate fiscal year quarter map"""
    fy_map = {}
    current_year = start_year
    for i in range(num_quarters):
        quarter = QUARTERS[i % 4]
        year_key = str(current_year)
        if year_key not in fy_map:
            fy_map[year_key] = []
        fy_map[year_key].append(quarter)
        if (i + 1) % 4 == 0:
            current_year += 1
    return json.dumps(fy_map)

def generate_fake_miso_series(conn, num_series=20):
    """Generate fake MISO series data"""
    cur = conn.cursor()
    current_year = datetime.now().year
    
    for i in range(num_series):
        start_year = random.randint(current_year - 2, current_year)
        start_month = random.randint(1, 12)
        end_year = random.randint(start_year, current_year + 1)
        end_month = random.randint(1, 12)
        
        fiscal_year = start_year
        quarter = random.choice(QUARTERS[1:])  # Skip empty string
        
        # Generate realistic operation name using Faker
        operation_codename = fake.word().capitalize()
        series_name = f"Operation {operation_codename}-{fake.random_int(min=100, max=999)}"
        
        cur.execute("""
            INSERT INTO miso_series (
                series_name, classification, support_another_unit, executing_unit,
                executing_unit_service, series_actively_disseminating, miso_program,
                miso_objective, supporting_miso_objective, start_month, start_year,
                end_month, end_year, fiscal_year, calendar_year, quarter, tsoc,
                nds_threat, gcp_threat, target_audience, target_audience_category,
                susceptibility_score, accessiblity_score, desired_behavior,
                threshold_percentage, fy_quarter_map, is_active, changed_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            series_name,
            random.choice(CLASSIFICATIONS[1:]),  # Skip empty
            random.choice([True, False]),
            generate_military_unit(),
            random.choice(SAMPLE_SERVICES),
            random.choice([True, False]),
            random.choice(MISO_PROGRAMS),
            fake.sentence(nb_words=6).rstrip('.'),
            fake.sentence(nb_words=4).rstrip('.'),
            start_month,
            start_year,
            end_month,
            end_year,
            fiscal_year,
            start_year,
            quarter,
            random.choice(TSOCS[1:]),  # Skip empty
            random.choice(THREATS[1:]),  # Skip empty
            random.choice(THREATS[1:]),  # gcp_threat
            fake.sentence(nb_words=3).rstrip('.'),
            random.choice(AUDIENCE),
            str(random.randint(1, 5)),
            str(random.randint(1, 5)),
            fake.sentence(nb_words=5).rstrip('.'),
            random.uniform(50.0, 100.0),
            generate_fy_quarter_map(start_year),
            1,
            fake.email(domain="socom.mil")
        ))
    
    conn.commit()
    print(f"Generated {num_series} MISO series")

def generate_fake_miso_executions(conn, num_executions=30):
    """Generate fake MISO execution data"""
    cur = conn.cursor()
    
    # Get all series IDs
    cur.execute("SELECT series_id FROM miso_series WHERE is_active = 1")
    series_ids = [row[0] for row in cur.fetchall()]
    
    if not series_ids:
        print("No series found, skipping executions")
        return
    
    for i in range(num_executions):
        series_id = random.choice(series_ids)
        start_date = datetime.now() - timedelta(days=random.randint(0, 365))
        end_date = start_date + timedelta(days=random.randint(1, 90))
        
        means = random.sample(DISSEM_MEANS[1:], random.randint(1, 3))  # Skip empty
        means_str = json.dumps(means)
        
        method = random.choice(DISSEM_METHODS_BY_MEANS.get(means[0] if means else "Internet", ["Other"]))
        method_vol_map = json.dumps({method: random.randint(1000, 100000)})
        
        cur.execute("""
            INSERT INTO miso_execution (
                series_id, miso_execution, dissemination_start, dissemination_end,
                dissemination_means, dissemination_method, volume, method_vol_map,
                participation_based_on_incentive, attribution, collection_data_gathering_plan,
                notes, is_active, changed_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            series_id,
            f"Execution {fake.word().capitalize()}-{fake.random_int(min=1, max=100)}",
            start_date.date(),
            end_date.date(),
            means_str,
            json.dumps([method]),
            random.randint(1000, 1000000),
            method_vol_map,
            random.choice([True, False, None]),
            random.choice(ATTRIBUTION[1:]),  # Skip empty
            fake.sentence(nb_words=8).rstrip('.'),
            fake.text(max_nb_chars=200),
            1,
            fake.email(domain="socom.mil")
        ))
    
    conn.commit()
    print(f"Generated {num_executions} MISO executions")

def generate_fake_miso_assessments(conn, num_assessments=25):
    """Generate fake MISO assessment data"""
    cur = conn.cursor()
    
    # Get all series IDs
    cur.execute("SELECT series_id FROM miso_series WHERE is_active = 1")
    series_ids = [row[0] for row in cur.fetchall()]
    
    # Get execution IDs
    cur.execute("SELECT execution_id, series_id FROM miso_execution WHERE is_active = 1")
    executions = cur.fetchall()
    
    if not series_ids:
        print("No series found, skipping assessments")
        return
    
    current_year = datetime.now().year
    
    for i in range(num_assessments):
        series_id = random.choice(series_ids)
        execution_id = None
        if executions:
            matching_execs = [e[0] for e in executions if e[1] == series_id]
            if matching_execs:
                execution_id = random.choice(matching_execs)
        
        cur.execute("""
            INSERT INTO miso_assessment (
                series_id, execution_id, baseline_data, moe_planned, moe_observed,
                threshold_met, progress, active_summary, list_integrated_information_forces,
                causation_correlation_supporting_data, planned_adjustments,
                current_hpem_phase, fiscal_year, quarter, calendar_year, is_active, changed_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            series_id,
            execution_id,
            fake.sentence(nb_words=10).rstrip('.'),
            fake.sentence(nb_words=8).rstrip('.'),
            fake.sentence(nb_words=8).rstrip('.'),
            random.choice([True, False, None]),
            random.choice([True, False, None]),
            fake.paragraph(nb_sentences=3),
            random.choice(["CA", "Cyber", "JMWC", "PA", "None"]),
            fake.sentence(nb_words=12).rstrip('.'),
            fake.sentence(nb_words=6).rstrip('.'),
            random.choice(HPEM_PHASE[1:]),  # Skip empty
            current_year - 1,
            random.choice(QUARTERS[1:]),
            current_year - 1,
            1,
            fake.email(domain="socom.mil")
        ))
    
    conn.commit()
    print(f"Generated {num_assessments} MISO assessments")

def generate_fake_miso_locations(conn):
    """Generate fake location data for MISO series"""
    cur = conn.cursor()
    
    cur.execute("SELECT series_id FROM miso_series WHERE is_active = 1")
    series_ids = [row[0] for row in cur.fetchall()]
    
    for series_id in series_ids:
        num_locations = random.randint(1, 3)
        countries = random.sample(SAMPLE_COUNTRIES, num_locations)
        
        for country in countries:
            # Use Faker to generate city names, or None for country-level operations
            city = fake.city() if random.random() > 0.3 else None
            
            cur.execute("""
                INSERT INTO miso_location (series_id, country_code, city)
                VALUES (?, ?, ?)
            """, (series_id, country, city))
    
    conn.commit()
    print(f"Generated locations for {len(series_ids)} MISO series")

def generate_fake_cyber_series(conn, num_series=15):
    """Generate fake cyber series data"""
    cur = conn.cursor()
    current_year = datetime.now().year
    
    for i in range(num_series):
        start_year = random.randint(current_year - 2, current_year)
        start_month = random.randint(1, 12)
        end_year = random.randint(start_year, current_year + 1)
        end_month = random.randint(1, 12)
        
        fiscal_year = start_year
        quarter = random.choice(QUARTERS[1:])
        
        # Generate realistic cyber operation name
        cyber_codename = fake.word().capitalize()
        cyber_name = f"Cyber Operation {cyber_codename}-{fake.random_int(min=100, max=999)}"
        
        cur.execute("""
            INSERT INTO cyber_series (
                cyber_name, classification, cyber_objective, start_month, start_year,
                end_month, end_year, fiscal_year, calendar_year, quarter, tsoc,
                nds_threat, gcp_threat, key_activities, component, operators_enablers,
                equipment, training, education, target_audience, intelligence, authority,
                fy_quarter_map, is_active, changed_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cyber_name,
            random.choice(CLASSIFICATIONS[1:]),
            fake.sentence(nb_words=7).rstrip('.'),
            start_month,
            start_year,
            end_month,
            end_year,
            fiscal_year,
            start_year,
            quarter,
            random.choice(TSOCS[1:]),
            random.choice(THREATS[1:]),
            random.choice(THREATS[1:]),
            fake.sentence(nb_words=10).rstrip('.'),
            random.choice(["Offensive", "Defensive", "Intelligence Gathering"]),
            fake.sentence(nb_words=5).rstrip('.'),
            fake.sentence(nb_words=4).rstrip('.'),
            fake.sentence(nb_words=4).rstrip('.'),
            fake.sentence(nb_words=4).rstrip('.'),
            fake.sentence(nb_words=3).rstrip('.'),
            fake.sentence(nb_words=6).rstrip('.'),
            random.choice(["GCC", "SOCOM", "Other"]),
            generate_fy_quarter_map(start_year),
            1,
            fake.email(domain="socom.mil")
        ))
    
    conn.commit()
    print(f"Generated {num_series} cyber series")

def generate_fake_cyber_assessments(conn, num_assessments=15):
    """Generate fake cyber assessment data"""
    cur = conn.cursor()
    
    cur.execute("SELECT cyber_id FROM cyber_series WHERE is_active = 1")
    cyber_ids = [row[0] for row in cur.fetchall()]
    
    if not cyber_ids:
        print("No cyber series found, skipping assessments")
        return
    
    for i in range(num_assessments):
        cyber_id = random.choice(cyber_ids)
        
        cur.execute("""
            INSERT INTO cyber_assessment (
                cyber_id, success_indicators, success_measure, partners,
                challenges, way_forward, forward_comments, is_active, changed_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cyber_id,
            fake.sentence(nb_words=6).rstrip('.'),
            fake.sentence(nb_words=5).rstrip('.'),
            random.choice(["US Joint Cyber", "US Joint MISO", "Foreign Partners", "No Collaboration"]),
            fake.sentence(nb_words=8).rstrip('.'),
            fake.sentence(nb_words=6).rstrip('.'),
            fake.text(max_nb_chars=150),
            1,
            fake.email(domain="socom.mil")
        ))
    
    conn.commit()
    print(f"Generated {num_assessments} cyber assessments")

def generate_fake_cyber_locations(conn):
    """Generate fake location data for cyber series"""
    cur = conn.cursor()
    
    cur.execute("SELECT cyber_id FROM cyber_series WHERE is_active = 1")
    cyber_ids = [row[0] for row in cur.fetchall()]
    
    for cyber_id in cyber_ids:
        num_locations = random.randint(1, 2)
        countries = random.sample(SAMPLE_COUNTRIES, num_locations)
        
        for country in countries:
            # Use Faker to generate city names, or None for country-level operations
            city = fake.city() if random.random() > 0.4 else None
            
            cur.execute("""
                INSERT INTO cyber_location (cyber_id, country_code, city)
                VALUES (?, ?, ?)
            """, (cyber_id, country, city))
    
    conn.commit()
    print(f"Generated locations for {len(cyber_ids)} cyber series")

def main():
    """Generate all fake data"""
    db_path = 'miso.db'
    conn = sqlite3.connect(db_path)
    
    print("Generating fake data...")
    generate_fake_miso_series(conn, num_series=25)
    generate_fake_miso_executions(conn, num_executions=40)
    generate_fake_miso_assessments(conn, num_assessments=30)
    generate_fake_miso_locations(conn)
    generate_fake_cyber_series(conn, num_series=15)
    generate_fake_cyber_assessments(conn, num_assessments=20)
    generate_fake_cyber_locations(conn)
    
    conn.close()
    print("Fake data generation complete!")

if __name__ == "__main__":
    main()

