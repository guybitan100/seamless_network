import requests
import concurrent.futures
import time
import random
import csv
import argparse
import signal
import sys
from influxdb_client import InfluxDBClient, Point, WritePrecision

API_URL = "https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/{}"
AUTH_TOKEN = "I_am_under_stress_when_I_test"
HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}

# InfluxDB 2.x configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your_influxdb_token"
INFLUXDB_ORG = "your_org_name"
INFLUXDB_BUCKET = "stress_test_bucket"


def fetch_reputation(domain):
    """
    Perform a single API request to fetch the reputation of a domain.

    Args:
        domain (str): The domain name to check.

    Returns:
        tuple: A tuple containing the elapsed time for the request and an error message or code if applicable.
               (elapsed_time, None) if the request was successful, or
               (elapsed_time, response.status_code) if the request returned an error status code, or
               (None, str(e)) if an exception occurred during the request.
    """
    try:
        start_time = time.time()
        response = requests.get(API_URL.format(domain), headers=HEADERS)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            return elapsed_time, None  # Return time taken and no error
        else:
            return (
                elapsed_time,
                response.status_code,
            )  # Return time taken and error code
    except Exception as e:
        return None, str(e)


def signal_handler(signum, frame):
    """
    Handle signal interrupts (e.g., KeyboardInterrupt) to exit the script gracefully.
    Args:
        signum: Signal number.
        frame: Current stack frame.
    """
    print("KeyboardInterrupt detected. Ending stress test early.")
    sys.exit(1)


def write_to_influxdb(results):
    """
    Write the stress test results to InfluxDB 2.x using Flux.

    Args:
        results (list): List of tuples containing elapsed time and errors for each request.
    """
    with InfluxDBClient(
        url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG
    ) as client:
        write_api = client.write_api(write_options=WritePrecision.NS)

        for elapsed_time, error in results:
            point = (
                Point("reputation_api_test")
                .field(
                    "elapsed_time",
                    float(elapsed_time) if elapsed_time is not None else 0,
                )
                .field("error", str(error) if error is not None else "None")
                .time(time.time(), WritePrecision.NS)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)


def stress_test(concurrent_requests, num_domains, timeout):
    """
    Perform a stress test by making concurrent requests to the API with a list of domains.
    Args:
        concurrent_requests (int): Number of concurrent requests to make.
        num_domains (int): Number of domains to test.
        timeout (int): Timeout in seconds for the stress test process.
    Returns:
        None
    """
    # Generate a list of domains for testing
    domains = [
        "example{}.com".format(i) for i in range(num_domains)
    ]  # Replace with actual domains fetching logic
    results = []

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=concurrent_requests
    ) as executor:
        futures = {
            executor.submit(fetch_reputation, random.choice(domains)): i
            for i in range(concurrent_requests)
        }

        try:
            for future in concurrent.futures.as_completed(futures, timeout=timeout):
                elapsed_time, error = future.result()
                if elapsed_time is not None:
                    results.append((elapsed_time, error))
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Ending stress test early.")
        except concurrent.futures.TimeoutError:
            print("Timeout reached. Ending stress test.")

    # Calculate and print results
    total_requests = len(results)
    errors = [res for res in results if res[1] is not None]
    error_rate = len(errors) / total_requests * 100 if total_requests else 0
    total_time = time.time() - start_time
    times = [res[0] for res in results if res[0] is not None]

    average_time = sum(times) / len(times) if times else 0
    max_time = max(times) if times else 0
    p90_time = sorted(times)[int(len(times) * 0.9)] if times else 0

    print(f"Test is over!")
    print(f"Time in total: {total_time:.2f} seconds")
    print(f"Requests in total: {total_requests}")
    print(f"Error rate: {error_rate:.2f}% ({len(errors)} / {total_requests})")
    print(f"Average time for one request: {average_time:.2f} ms")
    print(f"Max time for one request: {max_time:.2f} seconds")
    print(f"p90 time for requests: {p90_time:.2f} seconds")

    # Write results to CSV
    with open("stress_test_results.csv", "w", newline="") as csvfile:
        fieldnames = ["elapsed_time", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for elapsed_time, error in results:
            writer.writerow({"elapsed_time": elapsed_time, "error": error})

    # Write results to InfluxDB
    # write_to_influxdb(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reputation Service Stress Test")
    parser.add_argument(
        "--concurrent_requests",
        type=int,
        default=10,
        help="Number of concurrent requests",
    )
    parser.add_argument(
        "--num_domains",
        type=int,
        default=100,
        help="Number of domains to test (max: 5000)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout in seconds to finish the stress process",
    )
    args = parser.parse_args()
    # Set up signal handler for graceful exit on KeyboardInterrupt
    signal.signal(signal.SIGINT, signal_handler)
    stress_test(args.concurrent_requests, args.num_domains, args.timeout)
