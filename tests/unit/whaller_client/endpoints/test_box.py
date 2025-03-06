"""
Unit tests for the Box class.
"""
import unittest
from unittest.mock import MagicMock, patch
import os
from whaller_client.endpoints.box import Box


class TestBox(unittest.TestCase):
    """Tests for the Box class."""

    def setUp(self):
        """Initial setup for each test."""
        self.mock_client = MagicMock()
        self.sphere_external_id = "test_sphere_id"
        self.box = Box(self.mock_client, self.sphere_external_id)

    def test_init(self):
        """Test Box class initialization."""
        self.assertEqual(self.box.client, self.mock_client)
        self.assertEqual(self.box.sphere_external_id, self.sphere_external_id)
        self.assertIsNotNone(self.box.upload_client)

    def test_create_folder_without_parent(self):
        """Test the create_folder method without parent."""
        # Mock configuration
        folder_id = 123
        self.mock_client.call_auth_post.return_value = {"id": folder_id}
        
        # Call the method to test
        result = self.box.create_folder("Test Folder")
        
        # Verifications
        self.mock_client.call_auth_post.assert_called_once_with(
            f'spheres/{self.sphere_external_id}/boxresources',
            {'name': 'Test Folder', 'type': 1}
        )
        self.assertEqual(result, folder_id)

    def test_create_folder_with_parent(self):
        """Test the create_folder method with parent."""
        # Mock configuration
        folder_id = 123
        parent_id = 456
        self.mock_client.call_auth_post.return_value = {"id": folder_id}
        
        # Call the method to test
        result = self.box.create_folder("Test Folder", parent_id)
        
        # Verifications
        self.mock_client.call_auth_post.assert_called_once_with(
            f'spheres/{self.sphere_external_id}/boxresources',
            {'name': 'Test Folder', 'type': 1, 'parent_id': parent_id}
        )
        self.assertEqual(result, folder_id)

    def test_create_folder_error(self):
        """Test the create_folder method with an error."""
        # Mock configuration
        self.mock_client.call_auth_post.return_value = {}  # No ID in the response
        
        # Call the method to test
        result = self.box.create_folder("Test Folder")
        
        # Verifications
        self.assertEqual(result, -1)  # Should return -1 if ID is not in the response

    @patch('whaller_client.endpoints.upload.Upload.boxresource')
    def test_create_file_without_parent(self, mock_boxresource):
        """Test the create_file method without parent."""
        # Mock configuration
        file_id = 123
        mock_boxresource.return_value = {"id": file_id}
        
        file_response = {"id": 456, "name": "Test", "ext": "txt"}
        self.mock_client.call_auth_post.return_value = file_response
        
        # Call the method to test
        file_name = "Test.txt"
        file_content = b"Test content"
        file_mime = "text/plain"
        
        result = self.box.create_file(file_name, file_content, file_mime)
        
        # Verifications
        mock_boxresource.assert_called_once_with(
            file_name, file_content, file_mime, self.sphere_external_id
        )
        
        self.mock_client.call_auth_post.assert_called_once_with(
            f'spheres/{self.sphere_external_id}/boxresources',
            {
                'name': 'Test',
                'ext': 'txt',
                'cloudfile_id': file_id,
                'type': 2
            }
        )
        
        self.assertEqual(result, file_response)

    @patch('whaller_client.endpoints.upload.Upload.boxresource')
    def test_create_file_with_parent(self, mock_boxresource):
        """Test the create_file method with parent."""
        # Mock configuration
        file_id = 123
        parent_id = 789
        mock_boxresource.return_value = {"id": file_id}
        
        file_response = {"id": 456, "name": "Test", "ext": "txt", "parent_id": parent_id}
        self.mock_client.call_auth_post.return_value = file_response
        
        # Call the method to test
        file_name = "Test.txt"
        file_content = b"Test content"
        file_mime = "text/plain"
        
        result = self.box.create_file(file_name, file_content, file_mime, parent_id)
        
        # Verifications
        mock_boxresource.assert_called_once_with(
            file_name, file_content, file_mime, self.sphere_external_id
        )
        
        self.mock_client.call_auth_post.assert_called_once_with(
            f'spheres/{self.sphere_external_id}/boxresources',
            {
                'name': 'Test',
                'ext': 'txt',
                'cloudfile_id': file_id,
                'type': 2,
                'parent_id': parent_id
            }
        )
        
        self.assertEqual(result, file_response)


if __name__ == '__main__':
    unittest.main() 