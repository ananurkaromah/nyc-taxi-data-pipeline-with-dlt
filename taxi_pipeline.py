import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONResponsePaginator

# Base URL for the Data Engineering Zoomcamp API
BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

@dlt.resource(name="taxi_data", write_disposition="merge", primary_key="id")
def taxi_resource():
    client = RESTClient(base_url=BASE_URL)
    # Using the simplified resource generator for the API
    for page in client.paginate("/", paginator=JSONResponsePaginator()):
        yield page

if __name__ == "__main__":
    # Create pipeline
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi",
    )

    # Load data
    load_info = pipeline.run(taxi_resource())
    print(load_info)