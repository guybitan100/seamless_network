from influxdb_client import InfluxDBClient, Point, WritePrecision
import time


class InfluxDBWriter:
    """Handles writing test results to InfluxDB."""

    def __init__(self, influxdb_url, influxdb_token, influxdb_org, influxdb_bucket):
        self.influxdb_url = influxdb_url
        self.influxdb_token = influxdb_token
        self.influxdb_org = influxdb_org
        self.influxdb_bucket = influxdb_bucket

    def write_to_influxdb(self, results):
        """
        Write the stress test results to InfluxDB 2.x using Flux.

        Args:
            results (list): List of tuples containing elapsed time and errors for each request.
        """
        with InfluxDBClient(
            url=self.influxdb_url, token=self.influxdb_token, org=self.influxdb_org
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
                write_api.write(bucket=self.influxdb_bucket, record=point)
