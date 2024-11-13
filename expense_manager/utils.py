import argparse
import logging


def parse_arguments() -> argparse.Namespace:
    """
    This function parses command-line argument.
    Shows help and Usage of program
    Returns: arguments object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        dest="DEBUG",
        action="store_true",
        help="Run the program in debug mode.",
    )
    parser.add_argument(dest="DATA_PATH", type=str, help="Monthly Expense data path")
    parser.add_argument(
        dest="DATE_MMYYYY", type=str, help="Transaction month to process"
    )
    parser.add_argument(
        dest="SORT_COLUMN", type=str, help="Column used to sort the expense file"
    )

    return parser.parse_args()


def setup_logging(
    log_name: str, is_file_handler: bool, log_file: str, log_level: int
) -> logging.Logger:
    """
    This Function sets up logger object either stream or file or both.
    Args:
        log_name: Logger name
        is_file_handler: flag if logger file is required
        log_file: path of log file
        log_level: log level either logging.INFO or logging.DEBUG

    Returns:
        logger: logging.Logger object
    """
    log_format = "%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s"
    logger = logging.getLogger(log_name)
    # stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    # file handler
    if is_file_handler:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        logger.setLevel(log_level)

    return logger
