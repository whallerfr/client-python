"""
Unit tests for the Me class.
"""
import unittest
from unittest.mock import MagicMock, patch
from whaller_client.endpoints.me import Me


class TestMe(unittest.TestCase):
    """Tests for the Me class."""

    def setUp(self):
        """Initial setup for each test."""
        self.mock_client = MagicMock()
        self.me = Me(self.mock_client)

    def test_init(self):
        """Test Me class initialization."""
        self.assertEqual(self.me.client, self.mock_client)

    def test_get(self):
        """Test the get method."""
        # Mock configuration
        self.mock_client.call_get.return_value = {"id": 123, "name": "Test User"}
        
        # Call the method to test
        result = self.me.get()
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me", {}, True)
        self.assertEqual(result, {"id": 123, "name": "Test User"})

    def test_get_notifications(self):
        """Test the get_notifications method."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "message": "Test notification"}]
        
        # Call the method to test
        result = self.me.get_notifications("test_login")
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("persons/test_login/notifications", {}, True)
        self.assertEqual(result, [{"id": 1, "message": "Test notification"}])

    def test_list_spheres(self):
        """Test the list_spheres method without parameters."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "name": "Test Sphere"}]
        
        # Call the method to test
        result = self.me.list_spheres()
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/spheres", {}, True)
        self.assertEqual(result, [{"id": 1, "name": "Test Sphere"}])

    def test_list_spheres_with_params(self):
        """Test the list_spheres method with parameters."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "name": "Test Sphere"}]
        
        # Call the method to test
        params = {"limit": 10, "offset": 0}
        result = self.me.list_spheres(params)
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/spheres", params, True)
        self.assertEqual(result, [{"id": 1, "name": "Test Sphere"}])

    def test_list_networks(self):
        """Test the list_networks method without parameters."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "name": "Test Network"}]
        
        # Call the method to test
        result = self.me.list_networks()
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/networks", {}, True)
        self.assertEqual(result, [{"id": 1, "name": "Test Network"}])

    def test_list_networks_with_params(self):
        """Test the list_networks method with parameters."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "name": "Test Network"}]
        
        # Call the method to test
        params = {"limit": 10, "offset": 0}
        result = self.me.list_networks(params)
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/networks", params, True)
        self.assertEqual(result, [{"id": 1, "name": "Test Network"}])

    def test_list_phones_without_status(self):
        """Test the list_phones method without status."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "number": "+33123456789"}]
        
        # Call the method to test
        result = self.me.list_phones()
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/phones", {}, True)
        self.assertEqual(result, [{"id": 1, "number": "+33123456789"}])

    def test_list_phones_with_status(self):
        """Test the list_phones method with status."""
        # Mock configuration
        self.mock_client.call_get.return_value = [{"id": 1, "number": "+33123456789", "status": "verified"}]
        
        # Call the method to test
        result = self.me.list_phones("verified")
        
        # Verifications
        self.mock_client.call_get.assert_called_once_with("me/phones", {"status": "verified"}, True)
        self.assertEqual(result, [{"id": 1, "number": "+33123456789", "status": "verified"}])


if __name__ == '__main__':
    unittest.main() 