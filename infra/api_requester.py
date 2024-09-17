import requests
import time


class APIRequester:
    """Handles making API requests to fetch domain reputation."""

    def __init__(self, api_url, auth_token):
        self.api_url = api_url
        self.headers = {"Authorization": f"Token {auth_token}"}

    def fetch_reputation(self, domain):
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
            response = requests.get(self.api_url.format(domain), headers=self.headers)
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
