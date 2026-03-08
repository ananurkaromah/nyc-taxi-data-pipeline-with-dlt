# NYC Taxi Data Pipeline with dlt 

- This project demonstrates a **simple data pipeline** built using **Python** and **dlt (data load tool)** to ingest data from a REST API and load it into a **DuckDB** database.

- The pipeline extracts **NYC Taxi data** from the Data Engineering Zoomcamp API and stores it locally for analysis

- The course material can be found on GitHub here: [DataTalksClub/data-engineering-zoomcamp: Free Data Engineering course!](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main)


## Project Overview

This pipeline performs the following steps:

1. Connects to a REST API that provides NYC taxi data
2. Retrieves the data using **incremental pagination**
3. Loads the data into a **DuckDB** database
4. Stores the dataset under the schema **`nyc_taxi`**

The project is a simple example of building an **EL (Extract–Load) pipeline** using modern data engineering tools.



## 🛠 Tech Stack

* **Python**
* **dlt (data load tool)**
* **DuckDB**
* **REST API**


## 📂 Project Structure

```
project-folder/
│
├── taxi_pipeline.py            # Main pipeline script
└── taxi_pipeline_pipeline.py   # A more flexible and configurable pipeline template using rest_api_resources
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies (optional)
```



**Description**

- **taxi_pipeline.py**
    
    A minimal pipeline that extracts data from a REST API and loads it into DuckDB.
    
- **taxi_pipeline_pipeline.py**
    
    A configurable pipeline template designed for production-style REST API ingestion.
    
---

## Requirements

Make sure Python is installed (Python 3.9+ recommended).

Install dependencies:

```bash
pip install dlt duckdb
```

---

## Data Source

The data is fetched from the following API endpoint:

```
https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
```

This API provides sample **NYC taxi datasets** used for data engineering practice.

---

### 1. Simple Taxi Pipeline

File: `taxi_pipeline.py`

This script demonstrates the **simplest way to load REST API data into DuckDB using dlt**.

#### Pipeline Steps

1. Define the API base URL
2. Create a REST API source
3. Configure the dlt pipeline
4. Load the data into DuckDB

#### Code Example

```python
import dlt
from dlt.sources.rest import RESTSource

# Base URL API
BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

# Create REST API source
def taxi_source():
    source = RESTSource(
        url=BASE_URL,
        pagination={"type": "incremental", "page_size": 1000},
    )
    return source

# Create pipeline
pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi",
)

# Load data
data = taxi_source().load()
pipeline.run(data)

print("Pipeline finished running!")
```

#### Run the Pipeline

```bash
python taxi_pipeline.py
```

After running the script, the taxi data will be loaded into a **DuckDB database**.

---

### 2. REST API Template Pipeline

File: `taxi_pipeline_pipeline.py`

This script is a **template pipeline** that allows more advanced configuration for REST APIs.

It supports:

- authentication
- multiple endpoints
- resource configuration
- scalable ingestion pipelines

#### Example Code

```python
import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig

@dlt.source
def taxi_pipeline_rest_api_source(access_token: str = dlt.secrets.value):
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://example.com/v1/",
            "auth": {"type": "bearer", "token": access_token},
        },
        "resources": [],
    }

    yield from rest_api_resources(config)

pipeline = dlt.pipeline(
    pipeline_name='taxi_pipeline_pipeline',
    destination='duckdb',
    refresh="drop_sources",
    progress="log",
)

if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)
```

#### Run the Template Pipeline

```bash
python taxi_pipeline_pipeline.py
```

---

### Differences Between the Two Pipelines

| Feature | Simple Pipeline | Template Pipeline |
| --- | --- | --- |
| Complexity | Very simple | More advanced |
| API configuration | Minimal | Fully configurable |
| Authentication support | No | Yes |
| Multiple endpoints | No | Yes |
| Scalability | Learning / small projects | Production pipelines |

---

### Output

After running the pipeline, the data will be stored in a **DuckDB database**.

Dataset name:

```
nyc_taxi
```

You can query the data using SQL.

Example query:

```sql
SELECT * FROM nyc_taxi LIMIT 10;
```

---

## Learning Goals

This project demonstrates:

- Building a simple **data ingestion pipeline**
- Extracting data from a **REST API**
- Loading data into **DuckDB**
- Using **dlt for ELT pipelines**
- Understanding the difference between **simple pipelines and configurable templates**
