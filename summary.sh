#!/bin/bash
# summary.sh — Copy results from container to host and clean up

CONTAINER_NAME="customer-analytics-container"
RESULTS_DIR="./results"

mkdir -p "$RESULTS_DIR"

# Copy all generated outputs from the container
docker cp "$CONTAINER_NAME":/app/pipeline/data_raw.csv "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/data_preprocessed.csv "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight1.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight2.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/insight3.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/clusters.txt "$RESULTS_DIR/"
docker cp "$CONTAINER_NAME":/app/pipeline/summary_plot.png "$RESULTS_DIR/"

echo "All results copied to $RESULTS_DIR/"

# Stop and remove the container
docker stop "$CONTAINER_NAME"
docker rm "$CONTAINER_NAME"

echo "Container '$CONTAINER_NAME' stopped and removed."
