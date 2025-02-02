import os
import logging

def setup_logging(log_filename: str) -> str:
    """
    Setup logging for the application.

    Args:
        log_filename (str): The name of the log file to create (e.g., "data_ingestion.log").

    Returns:
        str: The full path of the log file created.
    """
    # Create a log directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    log_file_path = os.path.join(log_dir, log_filename)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(),  # Also print to console for debugging
        ]
    )
    return log_file_path
