"""
Unit tests for the ApiClient class.
"""
import unittest
from unittest.mock import patch, MagicMock
from json import JSONDecodeError
from requests import RequestException
from whaller_client.api import ApiClient
from whaller_client.exceptions import MethodError, ApiError, HttpError, InvalidResponseError


class TestApiClient(unittest.TestCase):
    """Tests for the ApiClient class."""

    def setUp(self):
        """Initial setup for each test."""
        self.base_url = "https://api.whaller.com"
        self.api_client = ApiClient(self.base_url)

    def test_init(self):
        """Test ApiClient initialization."""
        self.assertEqual(self.api_client.api_base_url, "https://api.whaller.com/api/")
        
        # Test with a trailing slash
        api_client_with_slash = ApiClient("https://api.whaller.com/")
        self.assertEqual(api_client_with_slash.api_base_url, "https://api.whaller.com/api/")

    @patch('whaller_client.api.post')
    def test_call_json_post_success(self, mock_post):
        """Test the call_json method with POST and success."""
        # Mock configuration
        mock_response = MagicMock()
        mock_response.content = '{"result": {"success": true}}'
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call the method to test
        result = self.api_client.call_json(
            "test/endpoint", 
            "POST", 
            {"data": "value"}, 
            {"Custom-Header": "value"}
        )
        
        # Verifications
        mock_post.assert_called_once_with(
            "https://api.whaller.com/api/test/endpoint",
            json={"data": "value"},
            headers={"Content-Type": "application/json", "Custom-Header": "value"}
        )
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, {"success": True})

    @patch('whaller_client.api.get')
    def test_call_json_get_success(self, mock_get):
        """Test the call_json method with GET and success."""
        # Mock configuration
        mock_response = MagicMock()
        mock_response.content = '{"result": {"success": true}}'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call the method to test
        result = self.api_client.call_json(
            "test/endpoint", 
            "GET", 
            {"data": "value"}, 
            {"Custom-Header": "value"}
        )
        
        # Verifications
        mock_get.assert_called_once_with(
            "https://api.whaller.com/api/test/endpoint",
            params={"data": "value"},
            headers={"Content-Type": "application/json", "Custom-Header": "value"}
        )
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, {"success": True})

    def test_call_json_invalid_method(self):
        """Test the call_json method with an invalid HTTP method."""
        with self.assertRaises(MethodError):
            self.api_client.call_json("test/endpoint", "INVALID", {}, {})

    @patch('whaller_client.api.post')
    def test_call_json_http_error(self, mock_post):
        """Test the call_json method with an HTTP error."""
        # Mock configuration
        mock_post.side_effect = RequestException("HTTP Error")
        
        # Call the method to test and verification
        with self.assertRaises(HttpError):
            self.api_client.call_json("test/endpoint", "POST", {}, {})

    @patch('whaller_client.api.post')
    def test_call_json_invalid_json(self, mock_post):
        """Test the call_json method with an invalid JSON response."""
        # Mock configuration
        mock_response = MagicMock()
        mock_response.content = 'Invalid JSON'
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call the method to test and verification
        with self.assertRaises(InvalidResponseError):
            self.api_client.call_json("test/endpoint", "POST", {}, {})

    @patch('whaller_client.api.post')
    def test_call_json_api_error(self, mock_post):
        """Test the call_json method with an API error."""
        # Mock configuration
        mock_response = MagicMock()
        mock_response.content = '{"error": {"message": "API Error"}}'
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call the method to test and verification
        with self.assertRaises(ApiError):
            self.api_client.call_json("test/endpoint", "POST", {}, {})

    @patch('whaller_client.api.post')
    def test_call_json_empty_result(self, mock_post):
        """Test the call_json method with an empty result."""
        # Mock configuration
        mock_response = MagicMock()
        mock_response.content = '{}'
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call the method to test
        result = self.api_client.call_json("test/endpoint", "POST", {}, {})
        
        # Verifications
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main() 