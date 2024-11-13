import pytest
import argparse
import logging
from unittest.mock import patch
from expense_manager.utils import parse_arguments, setup_logging


# Test cases for parse_arguments
def test_parse_arguments_required_args():
    """Test parsing command-line arguments with required arguments."""
    test_args = ["program_name", "data/path.csv", "01-2024", "date"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.DATA_PATH == "data/path.csv"
        assert args.DATE_MMYYYY == "01-2024"
        assert args.SORT_COLUMN == "date"
        assert args.DEBUG is False  # Default state


def test_parse_arguments_with_debug_flag():
    """Test parsing command-line arguments with the debug flag."""
    test_args = ["program_name", "data/path.csv", "01-2024", "date", "-d"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.DEBUG is True


def test_parse_arguments_missing_required_arg():
    """Test parsing command-line arguments with missing required arguments."""
    test_args = ["program_name", "data/path.csv", "01-2024"]
    with patch("sys.argv", test_args), pytest.raises(SystemExit) as excinfo:
        parse_arguments()
    assert excinfo.type == SystemExit
    assert excinfo.value.code != 0  # Indicates error in parsing


def test_parse_arguments_help_message(capsys):
    """Test if help message is displayed when using -h or --help flag."""
    test_args = ["program_name", "-h"]
    with patch("sys.argv", test_args), pytest.raises(SystemExit) as excinfo:
        parse_arguments()
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "Monthly Expense data path" in captured.out
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 0  # Indicates normal exit after showing help


# Test cases for setup_logging
def test_setup_logging_stream_only():
    """Test setting up logger with stream handler only."""
    logger = setup_logging("test_logger", False, "test.log", logging.INFO)
    assert logger.name == "test_logger"
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in logger.handlers
    )
    assert logger.level == logging.DEBUG


def test_setup_logging_with_file_handler(tmp_path):
    """Test setting up logger with both stream and file handlers."""
    log_file = tmp_path / "test.log"
    logger = setup_logging("test_logger", True, str(log_file), logging.INFO)

    # Check if file handler is added
    assert any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)
    assert logger.level == logging.INFO

    # Verify the log file path
    file_handler = next(
        (h for h in logger.handlers if isinstance(h, logging.FileHandler)), None
    )
    assert file_handler.baseFilename == str(log_file)


# Test cases for invalid log level or file path
def test_setup_logging_invalid_log_file(tmp_path):
    """Test handling of invalid log file path."""
    with pytest.raises(OSError):
        setup_logging("test_logger", True, "/invalid/path/test.log", logging.INFO)
