"""
Unit tests for custom exceptions.
"""
import unittest
from whaller_client.exceptions import (
    MethodError, ApiError, HttpError, InvalidResponseError, UploadError
)


class TestExceptions(unittest.TestCase):
    """Tests for custom exceptions."""

    def test_method_error(self):
        """Test the MethodError exception."""
        message = "Invalid HTTP method"
        error = MethodError(message)
        self.assertEqual(error.message, message)
        self.assertEqual(str(error), repr(message))

    def test_api_error(self):
        """Test the ApiError exception."""
        message = "API error message"
        error = ApiError(message)
        self.assertEqual(error.message, message)
        self.assertEqual(str(error), repr(message))

    def test_http_error(self):
        """Test the HttpError exception."""
        message = "HTTP error message"
        error = HttpError(message)
        self.assertEqual(error.message, message)
        self.assertEqual(str(error), repr(message))

    def test_invalid_response_error(self):
        """Test the InvalidResponseError exception."""
        message = "Invalid JSON response"
        error = InvalidResponseError(message)
        self.assertEqual(error.message, message)
        self.assertEqual(str(error), repr(message))

    def test_upload_error(self):
        """Test the UploadError exception."""
        message = "Upload error message"
        error = UploadError(message)
        self.assertEqual(error.message, message)
        self.assertEqual(str(error), repr(message))


if __name__ == '__main__':
    unittest.main() 