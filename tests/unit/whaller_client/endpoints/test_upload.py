"""
Unit tests for the Upload class.
"""
import unittest
from unittest.mock import MagicMock, patch
import uuid
import math
from whaller_client.endpoints.upload import Upload


class TestUpload(unittest.TestCase):
    """Tests for the Upload class."""

    def setUp(self):
        """Initial setup for each test."""
        self.mock_client = MagicMock()
        self.upload = Upload(self.mock_client)

    def test_init(self):
        """Test Upload class initialization."""
        self.assertEqual(self.upload.client, self.mock_client)
        self.assertEqual(self.upload.chunksize, 10 * 1024 * 1024)  # 10 MB

    def test_upload(self):
        """Test the _upload method."""
        # Mock configuration
        self.mock_client.send_post_content.return_value = {"id": 123}
        
        # Call the method to test
        endpoint = "test/endpoint"
        params = {"param1": "value1"}
        files = {"file1": "file_content"}
        
        result = self.upload._upload(endpoint, params, files)
        
        # Verifications
        self.mock_client.send_post_content.assert_called_once_with(endpoint, params, files)
        self.assertEqual(result, {"id": 123})

    @patch('uuid.uuid4')
    def test_upload_with_chunking(self, mock_uuid4):
        """Test the _upload_with_chunking method."""
        # Mock configuration
        mock_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')
        mock_uuid4.return_value = mock_uuid
        
        self.mock_client.send_post_content.return_value = {"id": 123}
        
        # Call the method to test
        endpoint = "test/endpoint"
        filename = "test.txt"
        content = b"a" * (self.upload.chunksize + 1000)  # Slightly larger than chunk size
        mimes = "text/plain"
        sphere_external_id = "test_sphere_id"
        
        result = self.upload._upload_with_chunking(endpoint, filename, content, mimes, sphere_external_id)
        
        # Verifications
        dztotalfilesize = len(content)
        dztotalchunkcount = math.ceil(dztotalfilesize / self.upload.chunksize)
        
        # Verify that send_post_content was called the correct number of times
        self.assertEqual(self.mock_client.send_post_content.call_count, dztotalchunkcount)
        
        # Verify the parameters of the first call
        first_call_args = self.mock_client.send_post_content.call_args_list[0][0]
        self.assertEqual(first_call_args[0], endpoint)
        
        first_call_params = first_call_args[1]
        self.assertEqual(first_call_params['dzuuid'], str(mock_uuid))
        self.assertEqual(first_call_params['dztotalfilesize'], dztotalfilesize)
        self.assertEqual(first_call_params['dztotalchunkcount'], dztotalchunkcount)
        self.assertEqual(first_call_params['dzchunkindex'], 0)
        self.assertEqual(first_call_params['dzchunkbyteoffset'], 0)
        self.assertEqual(first_call_params['sphere_id'], sphere_external_id)
        
        # Verify the result
        self.assertEqual(result, {"id": 123})

    @patch.object(Upload, '_upload')
    def test_boxresource_small_file(self, mock_upload):
        """Test the boxresource method with a small file."""
        # Mock configuration
        mock_upload.return_value = {"id": 123}
        
        # Call the method to test
        filename = "test.txt"
        content = b"Small file content"
        mimes = "text/plain"
        sphere_external_id = "test_sphere_id"
        
        result = self.upload.boxresource(filename, content, mimes, sphere_external_id)
        
        # Verifications
        mock_upload.assert_called_once_with(
            'upload/box_resource',
            {'sphere_id': sphere_external_id},
            {'userfile': (filename, content, mimes)}
        )
        self.assertEqual(result, {"id": 123})

    @patch.object(Upload, '_upload_with_chunking')
    def test_boxresource_large_file(self, mock_upload_with_chunking):
        """Test the boxresource method with a large file."""
        # Mock configuration
        mock_upload_with_chunking.return_value = {"id": 123}
        
        # Call the method to test
        filename = "test.txt"
        content = b"a" * (self.upload.chunksize + 1000)  # Slightly larger than chunk size
        mimes = "text/plain"
        sphere_external_id = "test_sphere_id"
        
        result = self.upload.boxresource(filename, content, mimes, sphere_external_id)
        
        # Verifications
        mock_upload_with_chunking.assert_called_once_with(
            'upload/box_resource',
            filename,
            content,
            mimes,
            sphere_external_id
        )
        self.assertEqual(result, {"id": 123})


if __name__ == '__main__':
    unittest.main() 