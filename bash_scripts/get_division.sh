#!/bin/bash

# Endpoint URL for division
URL="http://localhost:5000/divide"

# JSON payload for division
PAYLOAD='{"x": 20, "y": 5}'

# Send POST request to the division endpoint
curl -X POST "$URL" -H "Content-Type: application/json" -d "$PAYLOAD"
