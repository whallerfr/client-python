"""
Unit tests for the Client class.
"""
import unittest
from unittest.mock import MagicMock, patch
from whaller_client.client import Client


class TestClient(unittest.TestCase):
    """Tests for the Client class."""

    def setUp(self):
        """Initial setup for each test."""
        self.base_url = "https://api.whaller.com"
        self.client_id = "test_client_id"
        self.client_token = "test_client_token"
        self.client = Client(self.base_url, self.client_id, self.client_token)

    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.api.api_base_url, "https://api.whaller.com/api/")
        self.assertEqual(self.client.authenticator.client_id, self.client_id)
        self.assertEqual(self.client.authenticator.client_token, self.client_token)
        self.assertIsNotNone(self.client.logger)

    def test_set_credentials(self):
        """Test the set_credentials method."""
        login = "test_login"
        password = "test_password"
        self.client.set_credentials(login, password)
        self.assertEqual(self.client.authenticator.login, login)
        self.assertEqual(self.client.authenticator.password, password)

    @patch('whaller_client.auth.Authenticator.authenticate')
    def test_authenticate(self, mock_authenticate):
        """Test the authenticate method."""
        self.client.authenticate()
        mock_authenticate.assert_called_once_with(self.client.api)

    @patch('whaller_client.auth.Authenticator.get_bearer_token')
    def test_get_api_token(self, mock_get_bearer_token):
        """Test the get_api_token method."""
        mock_get_bearer_token.return_value = {"Authorization": "Bearer test_token"}
        token = self.client.get_api_token()
        mock_get_bearer_token.assert_called_once_with(self.client.api)
        self.assertEqual(token, {"Authorization": "Bearer test_token"})

    @patch('whaller_client.auth.Authenticator.refresh_token')
    def test_refresh_token(self, mock_refresh_token):
        """Test the refresh_token method delegates to authenticator with api client."""
        self.client.refresh_token()
        mock_refresh_token.assert_called_once_with(self.client.api)

    @patch('whaller_client.auth.Authenticator.get_bearer_token')
    @patch('whaller_client.api.ApiClient.call_json')
    def test_call_post_with_auth(self, mock_call_json, mock_get_bearer_token):
        """Test the call_post method with authentication."""
        mock_get_bearer_token.return_value = {"Authorization": "Bearer test_token"}
        mock_call_json.return_value = {"success": True}
        
        result = self.client.call_post("test/endpoint", {"data": "value"}, True)
        
        mock_get_bearer_token.assert_called_once_with(self.client.api)
        mock_call_json.assert_called_once_with(
            "test/endpoint", 
            "POST", 
            {"data": "value"}, 
            {"Authorization": "Bearer test_token"}
        )
        self.assertEqual(result, {"success": True})

    @patch('whaller_client.api.ApiClient.call_json')
    def test_call_post_without_auth(self, mock_call_json):
        """Test the call_post method without authentication."""
        mock_call_json.return_value = {"success": True}
        
        result = self.client.call_post("test/endpoint", {"data": "value"}, False)
        
        mock_call_json.assert_called_once_with(
            "test/endpoint", 
            "POST", 
            {"data": "value"}, 
            {}
        )
        self.assertEqual(result, {"success": True})

    @patch('whaller_client.auth.Authenticator.get_bearer_token')
    @patch('whaller_client.api.ApiClient.call_json')
    def test_call_get_with_auth(self, mock_call_json, mock_get_bearer_token):
        """Test the call_get method with authentication."""
        mock_get_bearer_token.return_value = {"Authorization": "Bearer test_token"}
        mock_call_json.return_value = {"success": True}
        
        result = self.client.call_get("test/endpoint", {"data": "value"}, True)
        
        mock_get_bearer_token.assert_called_once_with(self.client.api)
        mock_call_json.assert_called_once_with(
            "test/endpoint", 
            "GET", 
            {"data": "value"}, 
            {"Authorization": "Bearer test_token"}
        )
        self.assertEqual(result, {"success": True})

    @patch('whaller_client.api.ApiClient.call_json')
    def test_call_get_without_auth(self, mock_call_json):
        """Test the call_get method without authentication."""
        mock_call_json.return_value = {"success": True}
        
        result = self.client.call_get("test/endpoint", {"data": "value"}, False)
        
        mock_call_json.assert_called_once_with(
            "test/endpoint", 
            "GET", 
            {"data": "value"}, 
            {}
        )
        self.assertEqual(result, {"success": True})


if __name__ == '__main__':
    unittest.main() 