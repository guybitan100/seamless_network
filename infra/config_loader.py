import yaml


class ConfigLoader:
    """Loads configuration from a YAML file."""

    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    @staticmethod
    def load_config(yaml_file):
        """
        Load configuration from a YAML file.

        Args:
            yaml_file (str): Path to the YAML file.

        Returns:
            dict: Configuration data.
        """
        with open(yaml_file, "r") as file:
            return yaml.safe_load(file)

    def get(self, key):
        """Get a configuration value by key."""
        return self.config.get(key)
