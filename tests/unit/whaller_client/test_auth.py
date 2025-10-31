"""
Unit tests for the Authenticator class.
"""
import unittest
from unittest.mock import MagicMock, patch
from base64 import b64encode
from whaller_client.auth import Authenticator


class TestAuthenticator(unittest.TestCase):
    """Tests for the Authenticator class."""

    def setUp(self):
        """Initial setup for each test."""
        self.client_id = "test_client_id"
        self.client_token = "test_client_token"
        self.authenticator = Authenticator(self.client_id, self.client_token)

    def test_init(self):
        """Test authenticator initialization."""
        self.assertEqual(self.authenticator.client_id, self.client_id)
        self.assertEqual(self.authenticator.client_token, self.client_token)
        self.assertIsNone(self.authenticator.token)
        self.assertIsNone(self.authenticator.login)
        self.assertIsNone(self.authenticator.password)

    def test_set_credentials(self):
        """Test the set_credentials method."""
        login = "test_login"
        password = "test_password"
        self.authenticator.set_credentials(login, password)
        self.assertEqual(self.authenticator.login, login)
        self.assertEqual(self.authenticator.password, password)

    @patch('whaller_client.api.ApiClient.call_json')
    def test_authenticate(self, mock_call_json):
        """Test the authenticate method."""
        # Mock configuration
        mock_api_client = MagicMock()
        mock_call_json.return_value = {"auth_token": "test_auth_token"}
        mock_api_client.call_json = mock_call_json
        
        # Set credentials
        login = "test_login"
        password = "test_password"
        self.authenticator.set_credentials(login, password)
        
        # Call the method to test
        self.authenticator.authenticate(mock_api_client)
        
        # Verifications
        expected_token = (self.client_id + ':::' + self.client_token).encode("utf-8")
        expected_header = {"X-Application": b64encode(expected_token)}
        expected_data = {'signin-login': login, 'signin-password': password}
        
        mock_call_json.assert_called_once_with(
            'person/login', 
            'POST', 
            expected_data, 
            expected_header
        )
        self.assertEqual(self.authenticator.token, "test_auth_token")

    def test_get_bearer_token_with_existing_token(self):
        """Test the get_bearer_token method with an existing token."""
        # Set token
        self.authenticator.token = "existing_token"
        
        # Call the method to test
        mock_api_client = MagicMock()
        result = self.authenticator.get_bearer_token(mock_api_client)
        
        # Verifications
        self.assertEqual(result, {"Authorization": "Bearer existing_token"})
        # Verify that authenticate was not called
        mock_api_client.call_json.assert_not_called()

    def test_get_bearer_token_without_token(self):
        """Test the get_bearer_token method without an existing token."""
        # Mock configuration
        self.authenticator.token = None
        mock_api_client = MagicMock()
        
        # Directly patch the authenticate method of the instance
        original_authenticate = self.authenticator.authenticate
        self.authenticator.authenticate = MagicMock()
        
        # Simulate the effect of authenticate
        def side_effect(api_client):
            self.authenticator.token = "new_token"
        self.authenticator.authenticate.side_effect = side_effect
        
        # Call the method to test
        result = self.authenticator.get_bearer_token(mock_api_client)
        
        # Verifications
        self.authenticator.authenticate.assert_called_once_with(mock_api_client)
        self.assertEqual(result, {"Authorization": "Bearer new_token"})
        
        # Restore the original method
        self.authenticator.authenticate = original_authenticate


    @patch('whaller_client.auth.Authenticator.get_bearer_token')
    @patch('whaller_client.api.ApiClient.call_json')
    def test_refresh_token_with_existing_token(self, mock_call_json, mock_get_bearer_token):
        """Test refresh_token when a token already exists."""
        # Arrange
        self.authenticator.set_credentials('login_user', 'secret')
        self.authenticator.token = 'existing_token'
        mock_get_bearer_token.return_value = {"Authorization": "Bearer existing_token"}
        mock_call_json.return_value = {"auth_token": "refreshed_token"}

        mock_api_client = MagicMock()
        mock_api_client.call_json = mock_call_json

        # Act
        self.authenticator.refresh_token(mock_api_client)

        # Assert
        expected_data = {"auth_token": "existing_token", "login": "login_user", "renew": True}
        mock_call_json.assert_called_once_with(
            'person/status_auth_by_token',
            'POST',
            expected_data,
            {"Authorization": "Bearer existing_token"}
        )
        self.assertEqual(self.authenticator.token, 'refreshed_token')

    @patch('whaller_client.auth.Authenticator.get_bearer_token')
    @patch('whaller_client.api.ApiClient.call_json')
    def test_refresh_token_without_existing_token_triggers_authenticate(self, mock_call_json, mock_get_bearer_token):
        """Test refresh_token triggers authenticate when token is missing."""
        # Arrange
        self.authenticator.set_credentials('login_user', 'secret')
        self.authenticator.token = None

        # Patch instance authenticate to set an initial token
        original_authenticate = self.authenticator.authenticate
        def authenticate_side_effect(api_client):
            self.authenticator.token = 'initial_token'
        self.authenticator.authenticate = MagicMock(side_effect=authenticate_side_effect)

        mock_get_bearer_token.return_value = {"Authorization": "Bearer initial_token"}
        mock_call_json.return_value = {"auth_token": "refreshed_token"}

        mock_api_client = MagicMock()
        mock_api_client.call_json = mock_call_json

        # Act
        self.authenticator.refresh_token(mock_api_client)

        # Assert
        self.authenticator.authenticate.assert_called_once_with(mock_api_client)
        expected_data = {"auth_token": "initial_token", "login": "login_user", "renew": True}
        mock_call_json.assert_called_once_with(
            'person/status_auth_by_token',
            'POST',
            expected_data,
            {"Authorization": "Bearer initial_token"}
        )
        self.assertEqual(self.authenticator.token, 'refreshed_token')

        # Restore original method
        self.authenticator.authenticate = original_authenticate

if __name__ == '__main__':
    unittest.main() 