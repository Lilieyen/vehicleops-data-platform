import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATABASE_URL = (
    "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
)
engine = create_engine(DATABASE_URL)

# read the csv into a DataFrame
vehicles_df = pd.read_csv(
    RAW_DATA_DIR / "vehicles.csv"
)

trips_df = pd.read_csv(
    RAW_DATA_DIR / "trips.csv"
)

fuel_logs_df = pd.read_csv(
    RAW_DATA_DIR / "fuel_logs.csv"
)

sensor_readings_df = pd.read_csv(
    RAW_DATA_DIR / "sensor_readings.csv"
)

maintenance_df = pd.read_csv(
    RAW_DATA_DIR / "maintenance_records.csv"
)

# write the DataFrame into Postgresql as a table
vehicles_df.to_sql(
    "raw_vehicles",
    engine,
    if_exists="replace",
    index=False
)

trips_df.to_sql(
    "raw_trips",
    engine,
    if_exists="replace",
    index=False
)

fuel_logs_df.to_sql(
    "raw_fuel_logs",
    engine,
    if_exists="replace",
    index=False
)

sensor_readings_df.to_sql(
    "raw_sensor_readings",
    engine,
    if_exists="replace",
    index=False
)

maintenance_df.to_sql(
    "raw_maintenance",
    engine,
    if_exists="replace",
    index=False
)

print("All raw data sets loaded successfully.")