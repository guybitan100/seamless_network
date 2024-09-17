# stress_test.py
import argparse
import signal
import sys
from config_loader import ConfigLoader
from infra.stress_tester import StressTester


def signal_handler(signum, frame):
    """
    Handle signal interrupts (e.g., KeyboardInterrupt) to exit the script gracefully.

    Args:
        signum: Signal number.
        frame: Current stack frame.
    """
    print("KeyboardInterrupt detected. Ending stress test early.")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reputation Service Stress Test")
    parser.add_argument(
        "--config_file",
        type=str,
        default="config.yaml",
        help="Path to the YAML configuration file.",
    )
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

    # Initialize the configuration loader
    config_loader = ConfigLoader(args.config_file)

    # Initialize and run the stress test
    tester = StressTester(config_loader)
    tester.stress_test(args.concurrent_requests, args.num_domains, args.timeout)
