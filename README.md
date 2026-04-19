# NYC Taxi Data Pipeline: End-to-End ELT with dlt, DuckDB, and Metabase

## 1. Project Overview
This project demonstrates a robust, containerized data pipeline built to ingest NYC Taxi data from a REST API and load it into a DuckDB database for analytical processing. It serves as a practical implementation of modern **ELT (Extract-Load-Transform)** patterns, utilizing `dlt` (Data Load Tool) for automated schema evolution and Docker for local workflow orchestration.

## 2. Dataset Description
The pipeline consumes the **NYC Taxi Trip Dataset** provided via the DataTalksClub Data Engineering Zoomcamp API. This dataset includes trip records from New York City’s yellow taxis, capturing pickup/dropoff times, locations, trip distances, itemized fares, and passenger counts.

### Data Dictionary
| Column | Description |
| :--- | :--- |
| `vendor_name` | TPEP provider (e.g., Creative Mobile, VeriFone) |
| `trip_pickup_date_time` | Date and time when the meter was engaged |
| `trip_dropoff_date_time` | Date and time when the meter was disengaged |
| `passenger_count` | Number of passengers in the vehicle |
| `trip_distance` | Elapsed trip distance in miles |
| `fare_amt` | Time-and-distance fare calculated by the meter |
| `tip_amt` | Tip amount (automatically populated for credit card trips) |
| `tolls_amt` | Total amount of all tolls paid in trip |
| `total_amt` | The total amount charged to passengers |
| `payment_type` | Numeric code signifying how the passenger paid |

## 3. Problem Statement
Manual data ingestion from REST APIs often leads to schema breakage and data type inconsistencies. This project addresses the need for a **resilient and scalable ingestion layer** that can handle semi-structured JSON data, map it to a structured relational format, and provide a foundation for business intelligence without manual intervention.

## 4. Key Research 
![alt text](<NYC-taxi pipeline.png>)
<br>

http://localhost:3000/public/dashboard/3ffc394f-1a27-4e65-bed0-93ddccc1b350

### 1. Profitability: Highest Revenue per Mile

- **Peak Efficiency:** The absolute highest `revenue_per_mile` on the chart is approximately **$4.65**. Tracing this point to the Y-axis, it aligns with a `pickup_hour` of **12 (Noon)**.
- **High-Value Clusters:** There is another strong cluster of high revenue efficiency between **$4.30 and $4.50 per mile**.
- **Data Quality Observation:** The Y-axis for `pickup_hour` shows values reaching up to 40. Since a 24-hour clock maxes out at 23, this indicates a minor configuration issue. Metabase might be automatically summing the hours instead of treating them as categories, or the X and Y axes are swapped in the visualization settings. Changing the chart settings from a line chart to a scatter plot, or ensuring the X-axis is set to `pickup_hour` (Ordinal/Category) and Y-axis to `revenue_per_mile` (Numeric), will clear this up!

### 2. Operational Efficiency: Tolls & Surcharges vs. Base Fare

- **Time-Series Focus:** Note that this specific chart is grouped by `trip_date` (June 2009) rather than by vendor, so the insights reflect daily operational trends across the entire fleet.
- **Low Non-Fare Impact:** The `non_fare_percentage` (the light blue bars measured on the right-hand axis) remains consistently low throughout the month. It generally fluctuates between **5% and 15%**. This means the base fare is highly dominant, making up 85% to 95% of total trip costs.
- **Surcharges vs. Tolls:** On most standard days, `total_surcharges` (light purple bars) outpace `total_tolls` (coral bars). However, there are notable anomalies—such as the spike around June 14, 2009—where total tolls briefly exceed surcharges, likely indicating a high volume of airport or bridge/tunnel trips on that specific weekend.


## 5. Pipeline Architecture & Lineage
The architecture follows a modular, containerized approach:
1. **Source:** Data Engineering Zoomcamp REST API (JSON).
2. **Ingestion (dlt):** Python-based extraction using `dlt` for schema inference and incremental loading.
3. **Storage (DuckDB):** An embedded OLAP database for high-performance analytical queries.
4. **Orchestration:** Docker Compose managing the Python pipeline and Metabase BI tool.
5. **Visualization:** Metabase for strategic dashboards.

**Data Lineage:** `API (JSON)` -> `dlt (Python)` -> `DuckDB (Relational)` -> `Metabase (SQL/Charts)`

## 6. Data Ingestion & Orchestration
- **Tooling:** `dlt` (Data Load Tool)
- **Method:** Incremental loading with schema evolution.
- **Workflow:** Docker Compose orchestrates two services:
    - `pipeline`: Executes the Python script to sync data.
    - `metabase`: Serves the BI dashboard with custom DuckDB drivers.

## 7. Data Warehouse & Transformation
While this project uses **DuckDB** as a local analytical warehouse, the data is structured into a clean `nyc_taxi` schema. Transformations are handled **at the query level (View-based)** within Metabase to maintain a "Lean ELT" approach.

## 8. Strategic Business Insights & Recommendations

### Insight 1: Revenue per Mile Efficiency
**Query:** Identifying trip profitability by hour.
- *Strategic Recommendation:* Implement dynamic surge pricing during hours where `total_trips` are high but `revenue_per_mile` is low (due to congestion).

### Insight 2: Tipping Optimization
**Query:** Correlation between payment types and tip amounts.
- *Strategic Recommendation:* If specific vendors show higher tip averages, analyze their POS (Point of Sale) UI to implement "Suggested Tip" best practices across the fleet.

## 9. Project Folder Structure
```text
.
├── .dlt/                   # dlt credentials and metadata
├── plugins/                # Custom DuckDB drivers for Metabase
├── taxi_pipeline.py        # Main ingestion script
├── Dockerfile              # Pipeline image configuration
├── Dockerfile.metabase     # Custom Metabase image for DuckDB support
├── docker-compose.yaml     # Orchestration file
├── taxi_pipeline.duckdb    # Local analytical database
└── README.md               # Project documentation

```

## 10. Execution Steps
Prepare Drivers:
Ensure the DuckDB driver is in plugins/duckdb.metabase-driver.jar.

Build and Run:

Bash
```
docker compose build
docker compose up -d
```

Execute Pipeline:

Bash
```
docker compose run pipeline
```

Access Dashboard:
Open http://localhost:3000 and connect to /database/taxi_pipeline.duckdb.


## 11. Final Configuration
- Metabase Version: v0.49.13 (Debian-based for native library support).

- Python Version: 3.9-slim.

- Database Engine: DuckDB 1.x.

## 12. Future Work & Scalability
- Cloud Migration: Transition DuckDB to MotherDuck for cloud-based persistence.

- Automation: Integrate GitHub Actions to trigger the pipeline on a daily schedule.

- Advanced Transformation: Introduce dbt (data build tool) for complex modeling within DuckDB.

## 13. Acknowledgements
DataTalksClub: For providing the Data Engineering Zoomcamp curriculum and API.

dltHub: For the simplified ingestion framework.

Metabase Community: For the DuckDB driver support.