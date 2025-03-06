"""
Unit tests for the Invitation class.
"""
import unittest
from unittest.mock import MagicMock
from whaller_client.endpoints.invitation import Invitation


class TestInvitation(unittest.TestCase):
    """Tests for the Invitation class."""

    def setUp(self):
        """Initial setup for each test."""
        self.mock_client = MagicMock()
        self.invitation = Invitation(self.mock_client)

    def test_init(self):
        """Test Invitation class initialization."""
        self.assertEqual(self.invitation.client, self.mock_client)

    def test_remove_one(self):
        """Test the remove_one method."""
        # Mock configuration
        self.mock_client.call_auth_post.return_value = {}
        
        # Call the method to test
        invitation_id = 123
        self.invitation.remove_one(invitation_id)
        
        # Verifications
        self.mock_client.call_auth_post.assert_called_once_with(
            'invitation', 
            data={"id": invitation_id}
        )


if __name__ == '__main__':
    unittest.main() 