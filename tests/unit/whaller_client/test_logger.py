"""
Unit tests for the Logger class.
"""
import unittest
import os
import logging
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from whaller_client.logger import Logger


class TestLogger(unittest.TestCase):
    """Tests for the Logger class."""

    def setUp(self):
        """Initial setup for each test."""
        # Create a temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()
        self.logger_name = "test_logger"
        self.log_file_path = os.path.join(self.temp_dir, f"{self.logger_name}.log")

    def tearDown(self):
        """Cleanup after each test."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)

    @patch('logging.getLogger')
    @patch('logging.FileHandler')
    def test_init_with_custom_path(self, mock_file_handler, mock_get_logger):
        """Test logger initialization with a custom path."""
        # Mock configuration
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = False
        
        mock_handler = MagicMock()
        mock_file_handler.return_value = mock_handler
        
        # Call the method to test
        logger = Logger(self.logger_name, self.temp_dir + '/', logging.DEBUG)
        
        # Verifications
        mock_get_logger.assert_called_once_with(self.logger_name)
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
        mock_file_handler.assert_called_once_with(os.path.join(self.temp_dir, f"{self.logger_name}.log"))
        mock_handler.setLevel.assert_called_once()
        mock_handler.setFormatter.assert_called_once()
        mock_logger.addHandler.assert_called_once_with(mock_handler)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('logging.getLogger')
    def test_init_creates_directory(self, mock_get_logger, mock_exists, mock_makedirs):
        """Test that the logger creates the log directory if it doesn't exist."""
        # Mock configuration
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = True
        
        # Call the method to test
        Logger(self.logger_name, self.temp_dir + '/')
        
        # Verifications
        mock_exists.assert_called_once_with(self.temp_dir + '/')
        mock_makedirs.assert_called_once_with(self.temp_dir + '/', exist_ok=True)

    @patch('logging.getLogger')
    @patch('logging.FileHandler')
    @patch('os.path.exists', return_value=True)
    def test_init_creates_file_handler(self, mock_exists, mock_file_handler, mock_get_logger):
        """Test that the logger creates a FileHandler with the correct formatter."""
        # Mock configuration
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = False
        
        mock_handler = MagicMock()
        mock_file_handler.return_value = mock_handler
        
        # Call the method to test
        Logger(self.logger_name, self.temp_dir + '/')
        
        # Verifications
        mock_file_handler.assert_called_once_with(os.path.join(self.temp_dir, f"{self.logger_name}.log"))
        mock_handler.setLevel.assert_called_once()
        mock_handler.setFormatter.assert_called_once()
        mock_logger.addHandler.assert_called_once_with(mock_handler)

    def test_logging_methods(self):
        """Test the logging methods."""
        # Create a mock for the logger
        mock_logger = MagicMock()
        
        # Create a Logger instance with the mock
        logger = Logger(self.logger_name, self.temp_dir + '/')
        logger.current_logger = mock_logger
        
        # Test the logging methods
        test_message = "Test message"
        
        logger.debug(test_message)
        mock_logger.debug.assert_called_once_with(test_message)
        
        logger.info(test_message)
        mock_logger.info.assert_called_once_with(test_message)
        
        logger.warning(test_message)
        mock_logger.warning.assert_called_once_with(test_message)
        
        logger.error(test_message)
        mock_logger.error.assert_called_once_with(test_message)

    def test_logging_methods_with_none_logger(self):
        """Test the logging methods when the logger is None."""
        # Create a Logger instance with a None logger
        logger = Logger(self.logger_name, self.temp_dir + '/')
        logger.current_logger = None
        
        # Verify that the methods don't raise exceptions
        try:
            logger.debug("Test")
            logger.info("Test")
            logger.warning("Test")
            logger.error("Test")
        except Exception as e:
            self.fail(f"Logging methods raised an exception: {e}")


if __name__ == '__main__':
    unittest.main() 