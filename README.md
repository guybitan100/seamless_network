# Reputation Service Stress Test Tool

This CLI tool simulates stress on the Reputation service by sending multiple concurrent requests to the service API. It allows you to specify the number of concurrent requests, the number of domains to test, and a timeout for the stress test.

## Features
- Send concurrent requests to the Reputation service API.
- Simulate stress on up to 5000 domains.
- Collect and report statistics on request times and error rates.
- Handle keyboard interrupts gracefully.
- Save detailed results to a CSV file.

## Requirements
- Python 3.x
- `requests influxdb_client pyyaml` library

## Installation
1. Clone this repository.
2. Install the required packages using:
   ```bash
   pip install -r requirements.txt
