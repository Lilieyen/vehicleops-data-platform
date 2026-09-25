import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# load the csv files
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

# validate that the datasets are not empty
assert not vehicles_df.empty
assert not trips_df.empty
assert not fuel_logs_df.empty
assert not sensor_readings_df.empty
assert not maintenance_df.empty

# validate unique record iDS
assert vehicles_df["vehicle_id"].is_unique
assert trips_df["trip_id"].is_unique
assert fuel_logs_df["fuel_log_id"].is_unique
assert sensor_readings_df["sensor_reading_id"].is_unique
assert maintenance_df["maintenance_id"].is_unique

# validate vehicle references
assert trips_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert fuel_logs_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert sensor_readings_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert maintenance_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()

assert fuel_logs_df["trip_id"].isin(trips_df["trip_id"]).all()

# validate numeric fields
assert (trips_df["distance_km"] > 0).all()
assert (trips_df["duration_hours"] > 0).all()
assert (trips_df["fuel_consumed_litres"] > 0).all()
assert (trips_df["fuel_cost"] > 0).all()

assert (fuel_logs_df["fuel_litres"] > 0).all()
assert (fuel_logs_df["fuel_price_per_litre"] > 0).all()
assert (fuel_logs_df["fuel_cost"] > 0).all()
assert (fuel_logs_df["odometer_km"] > 0).all()

assert (maintenance_df["maintenance_cost"] > 0).all()
assert (maintenance_df["odometer_km"] > 0).all()

# validate sensor ranges
assert sensor_readings_df["engine_temperature_c"].between(60, 110).all()
assert sensor_readings_df["oil_pressure_psi"].between(20, 70).all()
assert sensor_readings_df["battery_voltage_v"].between(11.5, 14.8).all()
assert sensor_readings_df["engine_rpm"].between(600, 3500).all()

# validating values in cateegories
assert vehicles_df["fuel_type"].isin(["Diesel", "Petrol"]).all()
assert maintenance_df["maintenance_type"].isin(
    [
        "Oil Change",
        "Brake Service",
        "Tire Replacement",
        "Engine Repair",
        "Battery Replacement",
        "Routine Inspection"
    ]
).all()

assert maintenance_df["status"].isin(["Completed", "Pending"]).all()

print("Raw data validation passed")
