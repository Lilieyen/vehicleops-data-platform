import numpy as np 
import pandas as pd
from pathlib import Path

# for reproducibility
np.random.seed(42)

# project folders
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# creates the raw data directory if it doesn't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# VEHICLE DATA GENERATION  
NUM_VEHICLES = 50

vehicle_ids = [
    f"VH{str(i).zfill(3)}"
    for i in range(1, NUM_VEHICLES + 1)
]

# vehicle type, make and model
vehicle_specs = {
    "Truck": [
        ("Isuzu", "NPR"),
        ("Mitsubishi", "Canter")
    ],
    "Pickup": [
        ("Toyota", "Hilux")
    ],
    "Van": [
        ("Toyota", "Hiace")
    ]
}

vehicle_types = np.random.choice(
    list(vehicle_specs.keys()),
    size=NUM_VEHICLES
)

makes = []
models = []

for vehicle_type in vehicle_types:
    make, model = vehicle_specs[vehicle_type][
        np.random.randint(len(vehicle_specs[vehicle_type]))
    ]
    makes.append(make)
    models.append(model)

# manufacturing year between 2018 and 2024
years = np.random.randint(
    2018,
    2025,
    size=NUM_VEHICLES 
)

# fuel type
fuel_types = np.random.choice(
    ["Diesel", "Petrol"],
    size=NUM_VEHICLES,
)

# combining all the arrays into a DataFrame
vehicles_df = pd.DataFrame({
    "vehicle_id": vehicle_ids,
    "vehicle_type": vehicle_types,
    "make": makes,
    "model": models,
    "year": years,
    "fuel_type": fuel_types
})

# saving the DataFrame to a CSV file
vehicles_df.to_csv(RAW_DATA_DIR / "vehicles.csv", index=False)

print(f"Generated {len(vehicles_df)} vehicle records.")


# TRIP VOLUME AND DATES
NUM_TRIPS = 5000

trip_ids = [
    f"TR{str(i).zfill(5)}"
    for i in range(1, NUM_TRIPS + 1)
]

trip_dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    periods=NUM_TRIPS  
)

trip_vehicles = np.random.choice(
    vehicles_df["vehicle_id"],
    size=NUM_TRIPS
)

locations = [
    "Nairobi",
    "Mombasa",
    "Nakuru",
    "Kisumu",
    "Eldoret",
    "Thika",
    "Naivasha",
    "Machakos"
]

origins = np.random.choice(
    locations,
    size=NUM_TRIPS
)

destinations = [
    np.random.choice(
        [location for location in locations if location != origin]
    )
    for origin in origins
]

route_distances = {
    ("Nairobi", "Mombasa"): 480,
    ("Nairobi", "Nakuru"): 155,
    ("Nairobi", "Kisumu"): 350,
    ("Nairobi", "Eldoret"): 310,
    ("Nairobi", "Thika"): 45,
    ("Nairobi", "Naivasha"): 95,
    ("Nairobi", "Machakos"): 115,

    ("Mombasa", "Nakuru"): 630,
    ("Mombasa", "Kisumu"): 850,
    ("Mombasa", "Eldoret"): 750,
    ("Mombasa", "Thika"): 520,
    ("Mombasa", "Naivasha"): 620,
    ("Mombasa", "Machakos"): 420,

    ("Nakuru", "Kisumu"): 190,
    ("Nakuru", "Eldoret"): 160,
    ("Nakuru", "Thika"): 200,
    ("Nakuru", "Naivasha"): 75,
    ("Nakuru", "Machakos"): 270,

    ("Kisumu", "Eldoret"): 120,
    ("Kisumu", "Thika"): 370,
    ("Kisumu", "Naivasha"): 270,
    ("Kisumu", "Machakos"): 465,

    ("Eldoret", "Thika"): 350,
    ("Eldoret", "Naivasha"): 235,
    ("Eldoret", "Machakos"): 430,

    ("Thika", "Naivasha"): 145,
    ("Thika", "Machakos"): 80,

    ("Naivasha", "Machakos"): 190,
}

# reverse route
def get_route_distance(origin, destination):
    if(origin, destination) in route_distances:
        return route_distances[(origin, destination)]
    return route_distances[(destination, origin)]

distances = [
    get_route_distance(origin, destination)
    for origin, destination in zip(origins, destinations)
]

# trip durations in hours, assuming average speed of 50km/h
average_speed = np.clip(
    np.random.normal(
    loc=50,
    scale=8,
    size=NUM_TRIPS
),
25,
80
)

trip_duration_hours = distances / average_speed

trip_vehicle_types =(
    vehicles_df.set_index("vehicle_id").loc[trip_vehicles, "vehicle_type"].values
)

# FUEL EFFICIENCY
fuel_efficiency_ranges = {
    "Truck": (18, 25),
    "Pickup": (9, 14),
    "Van": (10, 15)
}

fuel_efficiency = [
    np.random.uniform(
        fuel_efficiency_ranges[vehicle_type][0],
        fuel_efficiency_ranges[vehicle_type][1]
    )
    for vehicle_type in trip_vehicle_types  
]

# fuel_consumption
fuel_consumed_litres = (
    np.array(distances) / 100) * np.array(fuel_efficiency
)

# fuel cost per litre
fuel_prices = {
    "Diesel": 190,
    "Petrol": 200
}

# trip fuel types look up
trip_fuel_types = (
    vehicles_df.set_index("vehicle_id").loc[trip_vehicles, "fuel_type"].values
)

fuel_cost = [
    fuel_consumed * fuel_prices[fuel_type]
    for fuel_consumed, fuel_type in zip(fuel_consumed_litres, trip_fuel_types)
]

trips_df = pd.DataFrame({
    "trip_id": trip_ids,
    "vehicle_id": trip_vehicles,
    "trip_date": trip_dates,
    "origin": origins,
    "destination": destinations,
    "distance_km": distances,
    "duration_hours": trip_duration_hours,
    "fuel_type": trip_fuel_types,
    "fuel_efficiency_1_per_100km": fuel_efficiency,
    "fuel_consumed_litres": fuel_consumed_litres,
    "fuel_cost": fuel_cost,
    
})

trips_df.to_csv(RAW_DATA_DIR / "trips.csv", index=False)

print(f"Generated {len(trips_df)} trip records.")


#TRIP DATA VALIDATION
assert trips_df["trip_id"].is_unique
assert trips_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert (trips_df["origin"] != trips_df["destination"]).all()
assert (trips_df["distance_km"] > 0).all()
assert (trips_df["duration_hours"] > 0).all()
assert (trips_df["fuel_consumed_litres"] > 0).all()
assert (trips_df["fuel_cost"] > 0).all()

print("All trip data validation checks passed.")


# FUEL LOG DATA GENERATION
NUM_FUEL_LOGS = 5000

fuel_log_ids = [
    f"FL{str(i).zfill(5)}"
    for i in range(1, NUM_FUEL_LOGS + 1)
]

fuel_dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    periods=NUM_FUEL_LOGS
)


fuel_log_trips = np.random.choice(
    trips_df["trip_id"],
    size=NUM_FUEL_LOGS  
)

fuel_log_vehicles = (
    trips_df.set_index("trip_id").loc[fuel_log_trips, "vehicle_id"].values
)

fuel_litres = np.random.uniform(
    10,
    150,
    size=NUM_FUEL_LOGS 
)

fuel_log_types = (
    vehicles_df.set_index("vehicle_id").loc[fuel_log_vehicles, "fuel_type"].values
)

fuel_log_prices = [
    fuel_prices[fuel_type]
    for fuel_type in fuel_log_types
]

fuel_costs = [
    litres * price
    for litres, price in zip(fuel_litres, fuel_log_prices)
]

#odometer readings
odometer_readings = np.random.uniform(
    10000,
    250000,
    size=NUM_FUEL_LOGS
)

fuel_logs_df = pd.DataFrame({
    "fuel_log_id": fuel_log_ids,
    "vehicle_id": fuel_log_vehicles,
    "trip_id": fuel_log_trips,
    "fuel_date": fuel_dates,
    "fuel_type": fuel_log_types,
    "fuel_litres": fuel_litres,
    "fuel_price_per_litre": fuel_log_prices,
    "fuel_cost": fuel_costs,
    "odometer_km": odometer_readings
})

fuel_logs_df.to_csv(RAW_DATA_DIR / "fuel_logs.csv", index=False)

print(f"Generated {len(fuel_logs_df)} fuel log records.")

# fuel log validation
assert fuel_logs_df["fuel_log_id"].is_unique
assert fuel_logs_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert fuel_logs_df["trip_id"].isin(trips_df["trip_id"]).all()
assert (fuel_logs_df["fuel_litres"] > 0).all()
assert (fuel_logs_df["fuel_price_per_litre"] > 0).all()
assert (fuel_logs_df["fuel_cost"] > 0).all()
assert (fuel_logs_df["odometer_km"] > 0).all()

print("All fuel log data validation checks passed.")

#verifying that the vehicle_id in fuel_logs_df matches the vehicle_id in trips_df for the corresponding trip_id
trip_vehicle_lookup = trips_df.set_index("trip_id")["vehicle_id"]

assert(fuel_logs_df["vehicle_id"] == fuel_logs_df["trip_id"].map(trip_vehicle_lookup)).all()

print("All fuel log trip-relationships validated.")


# SENSOR READING IDS AND DATES
NUM_SENSOR_READINGS = 10000

# generate sensor readings
sensor_reading_ids = [
    f"SR{str(i).zfill(5)}"
    for i in range(1, NUM_SENSOR_READINGS + 1)
]

sensor_dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    periods=NUM_SENSOR_READINGS
)

# assign sensor readings
sensor_vehicles = np.random.choice(
    vehicles_df["vehicle_id"],
    size=NUM_SENSOR_READINGS    
)

engine_temperature = np.clip(
    np.random.normal(
        loc=85,
        scale=8,
        size=NUM_SENSOR_READINGS    
    ),
    60,
    110
)

oil_pressure = np.clip(
    np.random.normal(
        loc=45,
        scale=7,
        size=NUM_SENSOR_READINGS
    ),
    20,
    70
)

battery_voltage = np.clip(
    np.random.normal(
        loc=13.5,
        scale=0.6,
        size=NUM_SENSOR_READINGS
    ),
    11.5,
    14.8
)

# engine revolutions per minute (rpm)
engine_rpm = np.clip(
    np.random.normal(
        loc=1800,
        scale=400,
        size=NUM_SENSOR_READINGS
    ),
    600,
    3500
)

sensor_readings_df = pd.DataFrame({
    "sensor_reading_id": sensor_reading_ids,
    "vehicle_id": sensor_vehicles,
    "reading_date": sensor_dates,
    "engine_temperature_c": engine_temperature,
    "oil_pressure_psi": oil_pressure,
    "battery_voltage_v": battery_voltage,
    "engine_rpm": engine_rpm
})

sensor_readings_df.to_csv(RAW_DATA_DIR / "sensor_readings.csv", index=False)

print(f"Generated {len(sensor_readings_df)} sensor reading records.")

# ssensor data validation
assert sensor_readings_df["sensor_reading_id"].is_unique
assert sensor_readings_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert (sensor_readings_df["engine_temperature_c"] >= 60).all()
assert (sensor_readings_df["engine_temperature_c"] <= 110).all()
assert (sensor_readings_df["oil_pressure_psi"] >= 20).all()
assert (sensor_readings_df["oil_pressure_psi"] <= 70).all()
assert (sensor_readings_df["battery_voltage_v"] >= 11.5).all()
assert (sensor_readings_df["battery_voltage_v"] <= 14.8).all()
assert (sensor_readings_df["engine_rpm"] >= 600).all()
assert (sensor_readings_df["engine_rpm"] <= 3500).all()

print("All sensor reading data validation checks passed.")

# MAINTENANCEE RECORDS
NUM_MAINTENANCE_RECORDS = 500

maintenance_ids = [
    f"MT{str(i).zfill(5)}"
    for i in range(1, NUM_MAINTENANCE_RECORDS + 1)
]

maintenance_dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    periods=NUM_MAINTENANCE_RECORDS
)

maintenance_vehicles = np.random.choice(
    vehicles_df["vehicle_id"],
    size=NUM_MAINTENANCE_RECORDS
)

maintenance_types = np.random.choice(
    ["Oil Change",
     "Brake Service",
     "Tire Replacement",
     "Engine Repair",
     "Battery Replacement",
     "Routine Inspection"],
    size=NUM_MAINTENANCE_RECORDS
)

maintenance_cost_ranges = {
    "Oil Change": (3000, 8000),
    "Brake Service": (5000, 20000),
    "Tire Replacement": (10000, 40000),
    "Engine Repair": (20000, 100000),
    "Battery Replacement": (8000, 25000),
    "Routine Inspection": (2000, 5000)  
}

maintenance_costs = [
    np.random.uniform(
        maintenance_cost_ranges[maintenance_type][0],
        maintenance_cost_ranges[maintenance_type][1]
    )
    for maintenance_type in maintenance_types
]

maintenance_odometer = np.random.uniform(
    10000,
    250000,
    size=NUM_MAINTENANCE_RECORDS
)

maintenance_status = np.random.choice(
    [
        "Completed",
        "Pending"
    ],
    size=NUM_MAINTENANCE_RECORDS
)

maintenance_df = pd.DataFrame({
    "maintenance_id": maintenance_ids,
    "vehicle_id": maintenance_vehicles,
    "maintenance_date": maintenance_dates,
    "maintenance_type": maintenance_types,
    "maintenance_cost": maintenance_costs,
    "odometer_km": maintenance_odometer,
    "status": maintenance_status
})

maintenance_df.to_csv(RAW_DATA_DIR / "maintenance_records.csv", index=False)

print(f"Generated {len(maintenance_df)} maintenance records.")

# maintenance records validation
assert maintenance_df["maintenance_id"].is_unique
assert maintenance_df["vehicle_id"].isin(vehicles_df["vehicle_id"]).all()
assert maintenance_df["maintenance_type"].isin(maintenance_cost_ranges.keys()).all()
assert (maintenance_df["maintenance_cost"] > 0).all()
assert (maintenance_df["odometer_km"] > 0).all()
assert maintenance_df["status"].isin(["Completed", "Pending"]).all()

print("All maintenance data validation checks passed.")