# stress_tester.py
import concurrent.futures
import time
import random
import csv
from infra.api_requester import APIRequester
from infra.influxdb_writer import InfluxDBWriter


class StressTester:

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.api_requester = APIRequester(
            api_url=config_loader.get("api_url"),
            auth_token=config_loader.get("auth_token"),
        )
        influxdb_config = config_loader.get("influxdb")
        self.influxdb_writer = InfluxDBWriter(
            influxdb_url=influxdb_config["url"],
            influxdb_token=influxdb_config["token"],
            influxdb_org=influxdb_config["org"],
            influxdb_bucket=influxdb_config["bucket"],
        )

    def stress_test(self, concurrent_requests, num_domains, timeout):
        """
        Perform a stress test by making concurrent requests to the API with a list of domains.

        Args:
            concurrent_requests (int): Number of concurrent requests to make.
            num_domains (int): Number of domains to test.
            timeout (int): Timeout in seconds for the stress test process.
        """
        # Generate a list of domains for testing
        domains = [
            f"example{i}.com" for i in range(num_domains)
        ]  # Replace with actual domains fetching logic
        results = []

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=concurrent_requests
        ) as executor:
            futures = {
                executor.submit(
                    self.api_requester.fetch_reputation, random.choice(domains)
                ): i
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
        self.process_results(results, start_time)

    def process_results(self, results, start_time):
        """
        Process and print the results of the stress test.

        Args:
            results (list): List of tuples containing elapsed time and errors for each request.
            start_time (float): The start time of the stress test.
        """
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
        self.write_results_to_csv(results)

        # Write results to InfluxDB
        self.influxdb_writer.write_to_influxdb(results)

    @staticmethod
    def write_results_to_csv(results):
        """
        Write the results of the stress test to a CSV file.

        Args:
            results (list): List of tuples containing elapsed time and errors for each request.
        """
        with open("stress_test_results.csv", "w", newline="") as csvfile:
            fieldnames = ["elapsed_time", "error"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for elapsed_time, error in results:
                writer.writerow({"elapsed_time": elapsed_time, "error": error})
