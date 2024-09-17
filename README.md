
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
- Required libraries: `requests`, `influxdb_client`, `pyyaml`

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd seamless_network
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.yaml` file to set up the necessary configuration parameters, including API endpoints, request parameters, and InfluxDB settings.

## Usage

To run the stress test, use the following command:

```bash
python main.py --config_file <path_to_config_file> --concurrent_requests <number> --num_domains <number>
```

- `--config_file`: Path to the YAML configuration file (default: `config.yaml`).
- `--concurrent_requests`: Number of concurrent requests to send (default: 10).
- `--num_domains`: Number of domains to test, with a maximum limit of 5000 (default: 100).

Example:

```bash
python main.py --config_file config.yaml --concurrent_requests 100 --num_domains 500
```

## Project Structure

- **`infra/`**: Contains the core infrastructure scripts.
  - `api_requester.py`: Handles API request operations.
  - `config_loader.py`: Loads and parses the configuration from `config.yaml`.
  - `influxdb_writer.py`: Writes stress test results to InfluxDB.
  - `stress_tester.py`: Main script for conducting the stress test.
- **`tests/`**: Contains test scripts.
  - `main.py`: Tests for validating the functionality of the tool.
- **`config.yaml`**: Configuration file for setting up the API and InfluxDB parameters.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`requirements.txt`**: Lists the Python dependencies for the project.

## Running Tests

To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

We welcome contributions to this project! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
