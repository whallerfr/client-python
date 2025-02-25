from requests import post, get, RequestException
from json import JSONDecodeError, loads
from whaller_client.exceptions import MethodError, ApiError, HttpError, InvalidResponseError

class ApiClient:
    def __init__(self, base_url: str):
        """
        Client to interact with the Whaller API.
        """
        self.api_base_url = base_url.rstrip('/') + '/api/'

    def call_json(self, endpoint: str, method: str, data: dict = {}, headers: dict = {}) -> dict:
        """
        Sends a request to the API and returns the response in JSON format.

        :param endpoint: Relative URL of the endpoint
        :param method: HTTP method ('GET' or 'POST')
        :param data: Data sent in the request
        :param headers: HTTP headers
        :return: API response as a dictionary
        :raises MethodError: If the HTTP method is invalid
        :raises HttpError: If the request fails
        :raises InvalidResponseError: If the JSON response is malformed
        :raises ApiError: If the API returns an error code
        """
        req_headers = {'Content-Type': 'application/json'}
        req_headers.update(headers)
        api_url = f'{self.api_base_url}{endpoint}'

        try:
            if method == 'POST':
                response = post(api_url, json=data, headers=req_headers)
            elif method == 'GET':
                response = get(api_url, params=data, headers=req_headers)
            else:
                raise MethodError(f"Invalid HTTP method: {method}")

            # Check if the HTTP status is an error (4xx, 5xx)
            response.raise_for_status()

            try:
                response_data = loads(response.content)
            except JSONDecodeError as e:
                raise InvalidResponseError(f"Invalid JSON response from {api_url}") from e

            # Check if the response contains an API error
            if 'error' in response_data:
                error_message = response_data['error'].get('message', 'Unknown error')
                raise ApiError(f"API Error: {error_message}")

            return response_data.get('result', {})

        except RequestException as e:
            raise HttpError(f"HTTP error on {api_url}: {str(e)}") from e
