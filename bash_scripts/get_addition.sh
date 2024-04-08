#!/bin/bash

# Endpoint URL
URL="http://localhost:8000/add"

# JSON payload
PAYLOAD='{"x": 25, "y": 10}'

# Send POST request
curl -X POST "$URL" -H "Content-Type: application/json" -d "$PAYLOAD"
