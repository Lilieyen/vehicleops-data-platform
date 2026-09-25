# VehicleOps Data Platform

**An end-to-end fleet operations data platform built with Python, Apache Airflow, PostgreSQL, Docker, SQL, and Power BI.**

VehicleOps simulates the data environment of a fleet operation where information about vehicles, trips, fuel usage, maintenance, and engine conditions is generated across separate operational datasets.

The project takes **20,550 synthetic operational records** through a data pipeline, organizes them into a PostgreSQL warehouse, builds vehicle-level analytical views, and exposes the resulting metrics through an interactive Power BI dashboard.

### What the platform does

```text
Synthetic Fleet Data
        ↓
Generate → Validate → Load
        ↓
PostgreSQL Raw Layer
        ↓
Data Warehouse
        ↓
Analytics Views
        ↓
Power BI Fleet Dashboard
```

The current Airflow DAG orchestrates the **generation, validation, and loading** stages. PostgreSQL handles the downstream warehouse modeling and analytical views.

---

## The Problem

Fleet data is rarely contained in one dataset.

Vehicle information describes **what is in the fleet**, while trips describe **how vehicles are being used**, fuel logs capture **fuel consumption and cost**, maintenance records capture **maintenance activity and expenditure**, and sensor readings provide information about **vehicle operating conditions**.

Looking at these datasets independently makes it difficult to answer questions such as:

* Which vehicles are accumulating the most operational activity?
* How much fuel is each vehicle consuming?
* What is the fleet's fuel cost by vehicle type?
* Which vehicle types generate the highest maintenance costs?
* How frequently are vehicles undergoing maintenance?
* How does fuel efficiency vary across vehicles?

VehicleOps was built to bring these datasets together into a structured analytical platform where these questions can be answered from a common data model.

---

## The Data

The platform uses synthetic data generated specifically for the project.

| Dataset         | Records | Key information                                               |
| --------------- | ------: | ------------------------------------------------------------- |
| Vehicles        |      50 | Vehicle type, make, model, year, fuel type                    |
| Trips           |   5,000 | Distance, duration, fuel efficiency, fuel consumed, fuel cost |
| Fuel Logs       |   5,000 | Fuel date, fuel type, litres, price, cost, odometer           |
| Sensor Readings |  10,000 | Engine temperature, oil pressure, battery voltage, RPM        |
| Maintenance     |     500 | Maintenance type, date, cost, odometer, status                |

The datasets are deliberately separated at the raw layer to simulate the fragmented operational data that a fleet analytics system may need to integrate.

---

## The Approach

### 1. Generate

Python generates the five operational datasets as CSV files.

The generator creates relationships between records through identifiers such as `vehicle_id` and `trip_id`, allowing the datasets to be connected during warehouse modeling.

The generated files are stored under:

```text
data/raw/
├── vehicles.csv
├── trips.csv
├── fuel_logs.csv
├── sensor_readings.csv
└── maintenance_records.csv
```

### 2. Validate

Before loading the data into PostgreSQL, the pipeline runs a dedicated validation step.

This keeps validation separate from ingestion and provides a controlled point at which generated records can be checked before entering the database.

### 3. Load

The validated CSV files are loaded into PostgreSQL using Python and SQLAlchemy.

The raw layer contains:

```text
raw_vehicles
raw_trips
raw_fuel_logs
raw_sensor_readings
raw_maintenance
```

This layer preserves the source datasets before analytical transformations are applied.

### 4. Model

The raw datasets are transformed into a warehouse structure consisting of one vehicle dimension and four operational fact tables:

```text
warehouse
├── dim_vehicle
├── fact_trip
├── fact_fuel
├── fact_sensor
└── fact_maintenance
```

`dim_vehicle` provides the descriptive attributes used to identify and segment vehicles, while the fact tables store operational events.

One important modeling decision was made when building the fleet summary.

Trip, fuel, and maintenance records were **aggregated independently before being joined to the vehicle dimension**. This prevents the multiplication of records that can occur when several fact tables are joined together at their transaction level.

### 5. Analyze

Three PostgreSQL views form the analytics layer.

**`v_fleet_summary`**

Combines vehicle-level trip, fuel, and maintenance metrics, including:

* Total trips
* Total distance
* Total duration
* Average fuel efficiency
* Total fuel consumed
* Total fuel cost
* Total maintenance cost

**`v_fuel_analytics`**

Focuses on fuel activity and cost by vehicle and fuel type.

**`v_maintenance_analytics`**

Focuses on maintenance frequency, expenditure, completion status, and the most recent maintenance timestamp.

These views provide the datasets consumed by the Power BI dashboard rather than connecting the dashboard directly to the raw operational tables.

### 6. Visualize

Power BI connects to the analytics views and presents the resulting fleet metrics through a single dashboard.

The dashboard contains six headline KPIs:

* Total Fleet
* Total Trips
* Total Distance
* Total Fuel Consumed
* Total Fuel Cost
* Total Maintenance Cost

It also includes:

* **Fuel Cost by Vehicle Type**
* **Maintenance Cost by Vehicle Type**
* **Average Fuel Efficiency by Vehicle**
* **Vehicle Performance Overview**

Slicers allow the dashboard to be explored by:

* Vehicle Type
* Fuel Type
* Vehicle Make
* Vehicle Year


## The Outcome

The project resulted in a working fleet analytics platform that takes synthetic operational data from generation through to an interactive dashboard.

The completed platform includes:

* **5 datasets** containing 20,550 synthetic records
* An **Airflow pipeline** for generation, validation, and ingestion
* A PostgreSQL **raw data layer**
* A structured **warehouse with fact and dimension tables**
* **3 analytical SQL views**
* An interactive **Power BI fleet performance dashboard**

The dashboard provides a consolidated view of fleet activity, fuel consumption, fuel costs, maintenance costs, and vehicle-level performance.

### Dashboard

<img width="1435" height="798" alt="powerbi-dashboard png" src="https://github.com/user-attachments/assets/28ba24ed-f3eb-4f81-9ff8-c98d308fba99" />


### Airflow Pipeline

<img width="1600" height="645" alt="airflow-dag png" src="https://github.com/user-attachments/assets/ffacbb00-b96d-4116-9f86-67c87790bdec" />


---

## Technology Stack

| Technology     | Role                                    |
| -------------- | --------------------------------------- |
| Python         | Data generation, validation & ingestion |
| Apache Airflow | Pipeline orchestration                  |
| PostgreSQL     | Raw layer, warehouse & analytics        |
| SQL            | Data modeling & analytical views        |
| Docker         | Environment & service management        |
| Power BI       | Dashboard & visualization               |

---

## Project Structure

```text
vehicleops-data-platform/
├── dags/
├── data/raw/
├── scripts/
├── powerbi/
├── docs/images/
├── docker-compose.yaml
└── README.md
```

---

## Running the Project

### Prerequisites

* Docker Desktop
* Git
* Power BI Desktop *(for the dashboard)*

### Start the platform

```bash
docker compose up -d
```

Open Airflow, trigger `vehicleops_pipeline`, and allow the pipeline to complete.

The generated data is then available in PostgreSQL for the warehouse and analytics layers.

The Power BI dashboard is available at:

```text
powerbi/VehicleOps_Fleet_Performance_Dashboard.pbix
```

> The `.env` file contains local configuration and credentials and is excluded from version control.

---

## Future Improvements

* Orchestrate warehouse transformations through Airflow
* Add automated data quality tests
* Introduce incremental data loading
* Add historical fleet performance tracking
* Extend the platform with predictive maintenance and logistics analytics

---


## Portfolio

This project is part of my data engineering portfolio.

[https://github.com/Lilieyen/data-engineering-portfolio]
