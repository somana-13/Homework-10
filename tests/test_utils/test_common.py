import pytest
import os
from unittest.mock import patch, mock_open
from app.utils.common import setup_logging
import logging.config

@patch('logging.config.fileConfig')
@patch('os.path.normpath')
@patch('os.path.join')
def test_setup_logging(mock_join, mock_normpath, mock_fileconfig):
    # Setup mocks
    mock_join.return_value = '/mock/path/to/logging.conf'
    mock_normpath.return_value = '/normalized/path/to/logging.conf'
    
    # Call the function
    setup_logging()
    
    # Assert fileConfig was called with the expected path
    mock_fileconfig.assert_called_once_with('/normalized/path/to/logging.conf', disable_existing_loggers=False)
    
    # Assert join was called correctly to build the path
    assert mock_join.call_count == 1
    # The join should include dirname, .., .., and 'logging.conf'
    args = mock_join.call_args[0]
    assert len(args) >= 4
    assert args[-1] == 'logging.conf'
    
    # Assert normpath was called with the result of join
    mock_normpath.assert_called_once_with('/mock/path/to/logging.conf')
