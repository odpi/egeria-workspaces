import psycopg2
import csv
import random
import os
import sys
from datetime import datetime, timedelta

def generate_data():
    print("Starting synthetic sales forecast data generation...")
    
    # 3-year date range: July 2023 to June 2026
    start_date = datetime(2023, 7, 1)
    end_date = datetime(2026, 6, 30)
    
    # Base configuration
    product_lines = ["Therapeutics", "Diagnostics", "Vaccines", "Devices"]
    stages = ["Pipeline", "Upside", "Commit", "Closed Won", "Closed Lost"]
    
    us_reps = [f"US_REP_{i:02d}" for i in range(1, 11)]
    eu_reps = [f"EU_REP_{i:02d}" for i in range(1, 8)]
    uk_reps = [f"UK_REP_{i:02d}" for i in range(1, 5)]
    
    # Output file paths
    uk_csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uk_sales_forecast.csv")
    os.makedirs(os.path.dirname(uk_csv_path), exist_ok=True)
    
    # Connect to PostgreSQL
    # NOTE: We connect as egeria_user (user4egeria) for demonstration simplicity so that the schemas 
    # and tables are owned by the same user Egeria's Surveyor uses to crawl. 
    # In production, data owners and metadata surveyors would run with separate, restricted credentials.
    try:
        conn = psycopg2.connect(
            host="host.docker.internal",
            port=5442,
            dbname="coco_pharma",
            user="egeria_user",
            password="user4egeria"
        )
        cur = conn.cursor()
        print("Connected to PostgreSQL successfully.")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        sys.exit(1)
        
    try:
        # Create schemas
        print("Creating schemas...")
        cur.execute("CREATE SCHEMA IF NOT EXISTS us_sales;")
        cur.execute("CREATE SCHEMA IF NOT EXISTS eu_sales;")
        cur.execute("CREATE SCHEMA IF NOT EXISTS target_sales;")
        
        # Create tables
        print("Creating tables...")
        cur.execute("""
            DROP TABLE IF EXISTS us_sales.us_sales_forecast;
            CREATE TABLE us_sales.us_sales_forecast (
                RecordID VARCHAR(50) PRIMARY KEY,
                Date DATE,
                RepID VARCHAR(50),
                ProductLine VARCHAR(100),
                ForecastAmount NUMERIC(15, 2),
                ConfidenceLevel INTEGER,
                OpportunityID VARCHAR(50),
                SalesStage VARCHAR(50),
                CloseDate DATE,
                Currency VARCHAR(10),
                CreatedDate DATE
            );
        """)
        
        cur.execute("""
            DROP TABLE IF EXISTS eu_sales.eu_sales_forecast;
            CREATE TABLE eu_sales.eu_sales_forecast (
                uid VARCHAR(50) PRIMARY KEY,
                datum DATE,
                mitarbeiter VARCHAR(50),
                kategorie VARCHAR(100),
                wert_eur NUMERIC(15, 2),
                status INTEGER,
                deal_id VARCHAR(50),
                stage VARCHAR(50),
                expected_close_date DATE,
                currency VARCHAR(10),
                creation_date DATE
            );
        """)
        
        cur.execute("""
            DROP TABLE IF EXISTS target_sales.consolidated_forecast;
            CREATE TABLE target_sales.consolidated_forecast (
                ConsolidatedID VARCHAR(50) PRIMARY KEY,
                Region VARCHAR(20),
                Date DATE,
                ProductLine VARCHAR(100),
                AmountUSD NUMERIC(15, 2),
                ConfidencePercent INTEGER,
                OpportunityID VARCHAR(50),
                SalesStage VARCHAR(50),
                CloseDate DATE,
                CreatedDate DATE
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating schemas/tables: {e}")
        conn.rollback()
        sys.exit(1)
        
    # Generate data loop
    current_date = start_date
    us_records = []
    eu_records = []
    uk_records = []
    
    us_id_counter = 1
    eu_id_counter = 1
    uk_id_counter = 1
    
    print("Generating records...")
    while current_date <= end_date:
        # Determine growth factor (12% YoY)
        years_since_start = (current_date - start_date).days / 365.25
        growth_factor = 1.0 + (0.12 * years_since_start)
        
        # Seasonality: Q4 (Oct, Nov, Dec) has 1.5x deal volume and amount
        is_q4 = current_date.month in [10, 11, 12]
        season_volume_factor = 1.5 if is_q4 else 1.0
        season_amount_factor = 1.3 if is_q4 else 1.0
        
        # Daily deal count based on volume factors
        num_deals_us = int(random.choices([0, 1, 2, 3], weights=[40, 40, 15, 5])[0] * season_volume_factor)
        num_deals_eu = int(random.choices([0, 1, 2], weights=[50, 40, 10])[0] * season_volume_factor)
        num_deals_uk = int(random.choices([0, 1, 2], weights=[60, 30, 10])[0] * season_volume_factor)
        
        # 1. US Deals
        for _ in range(num_deals_us):
            opp_id = f"US-OPP-{us_id_counter:05d}"
            rep = random.choice(us_reps)
            prod = random.choice(product_lines)
            stage = random.choices(stages, weights=[30, 20, 20, 20, 10])[0]
            
            # Base amount
            amount = random.uniform(10000, 150000) * growth_factor * season_amount_factor
            
            # Confidence Level
            if stage == "Closed Won":
                conf = 100
            elif stage == "Closed Lost":
                conf = 0
            elif stage == "Commit":
                conf = random.randint(80, 95)
            elif stage == "Upside":
                conf = random.randint(50, 75)
            else:
                conf = random.randint(10, 45)
                
            # Close Date is usually 1 to 4 months after creation date
            close_date = current_date + timedelta(days=random.randint(30, 120))
            
            us_records.append((
                f"US-REC-{us_id_counter:05d}",
                current_date.strftime("%Y-%m-%d"),
                rep,
                prod,
                round(amount, 2),
                conf,
                opp_id,
                stage,
                close_date.strftime("%Y-%m-%d"),
                "USD",
                current_date.strftime("%Y-%m-%d")
            ))
            us_id_counter += 1
            
        # 2. EU Deals
        for _ in range(num_deals_eu):
            opp_id = f"EU-OPP-{eu_id_counter:05d}"
            rep = random.choice(eu_reps)
            prod = random.choice(product_lines)
            stage = random.choices(stages, weights=[35, 15, 20, 20, 10])[0]
            
            # Base amount
            amount_eur = random.uniform(8000, 120000) * growth_factor * season_amount_factor
            
            if stage == "Closed Won":
                conf = 100
            elif stage == "Closed Lost":
                conf = 0
            elif stage == "Commit":
                conf = random.randint(80, 95)
            elif stage == "Upside":
                conf = random.randint(50, 75)
            else:
                conf = random.randint(10, 45)
                
            close_date = current_date + timedelta(days=random.randint(30, 120))
            
            eu_records.append((
                f"EU-REC-{eu_id_counter:05d}",
                current_date.strftime("%Y-%m-%d"),
                rep,
                prod,
                round(amount_eur, 2),
                conf,
                opp_id,
                stage,
                close_date.strftime("%Y-%m-%d"),
                "EUR",
                current_date.strftime("%Y-%m-%d")
            ))
            eu_id_counter += 1
            
        # 3. UK Deals (CSV)
        for _ in range(num_deals_uk):
            opp_id = f"UK-OPP-{uk_id_counter:05d}"
            rep = random.choice(uk_reps)
            prod = random.choice(product_lines)
            stage = random.choices(stages, weights=[30, 20, 20, 20, 10])[0]
            
            # Base amount
            amount_gbp = random.uniform(7000, 95000) * growth_factor * season_amount_factor
            
            if stage == "Closed Won":
                prob = 1.00
            elif stage == "Closed Lost":
                prob = 0.00
            elif stage == "Commit":
                prob = round(random.uniform(0.80, 0.95), 2)
            elif stage == "Upside":
                prob = round(random.uniform(0.50, 0.75), 2)
            else:
                prob = round(random.uniform(0.10, 0.45), 2)
                
            close_date = current_date + timedelta(days=random.randint(30, 120))
            
            uk_records.append({
                "id": f"UK-REC-{uk_id_counter:05d}",
                "forecast_date": current_date.strftime("%Y-%m-%d"),
                "sales_rep": rep,
                "segment": prod,
                "value_gbp": round(amount_gbp, 2),
                "probability": prob,
                "deal_id": opp_id,
                "stage": stage,
                "close_date": close_date.strftime("%Y-%m-%d"),
                "currency": "GBP",
                "creation_date": current_date.strftime("%Y-%m-%d")
            })
            uk_id_counter += 1
            
        current_date += timedelta(days=1)
        
    print(f"Generated {len(us_records)} US records, {len(eu_records)} EU records, and {len(uk_records)} UK records.")
    
    # Insert US records into postgres
    print("Inserting US records into PostgreSQL...")
    try:
        cur.executemany("""
            INSERT INTO us_sales.us_sales_forecast 
            (RecordID, Date, RepID, ProductLine, ForecastAmount, ConfidenceLevel, OpportunityID, SalesStage, CloseDate, Currency, CreatedDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, us_records)
        conn.commit()
    except Exception as e:
        print(f"Error inserting US records: {e}")
        conn.rollback()
        sys.exit(1)
        
    # Insert EU records into postgres
    print("Inserting EU records into PostgreSQL...")
    try:
        cur.executemany("""
            INSERT INTO eu_sales.eu_sales_forecast 
            (uid, datum, mitarbeiter, kategorie, wert_eur, status, deal_id, stage, expected_close_date, currency, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, eu_records)
        conn.commit()
    except Exception as e:
        print(f"Error inserting EU records: {e}")
        conn.rollback()
        sys.exit(1)
        
    # Write UK records to CSV
    print(f"Writing UK records to CSV: {uk_csv_path}")
    try:
        with open(uk_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "forecast_date", "sales_rep", "segment", "value_gbp", "probability", "deal_id", "stage", "close_date", "currency", "creation_date"
            ])
            writer.writeheader()
            writer.writerows(uk_records)
        print("UK CSV file written successfully.")
    except Exception as e:
        print(f"Error writing UK CSV file: {e}")
        sys.exit(1)
        
    # Close Postgres
    cur.close()
    conn.close()
    print("Data generation complete.")

if __name__ == "__main__":
    generate_data()
