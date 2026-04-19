import dlt
from dlt.sources.rest_api import rest_api_resources

def taxi_pipeline_rest_api_source():
    config = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
            # Removed the 'auth' section since you don't have a token
        },
        "resources": [
            {
                "name": "taxi_rides",
                "endpoint": {
                    "path": "/", # The base URL already points to the data
                },
            }
        ],
    }
    yield from rest_api_resources(config)

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name='taxi_pipeline_advanced',
        destination='duckdb',
        dataset_name='nyc_taxi'
    )
    
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)