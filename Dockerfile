# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install "dlt[duckdb]" pandas

# Copy your scripts into the container
COPY taxi_pipeline.py .

# Command to run the pipeline
CMD ["python", "taxi_pipeline.py"]

COPY requirements.txt .
RUN pip install -r requirements.txt