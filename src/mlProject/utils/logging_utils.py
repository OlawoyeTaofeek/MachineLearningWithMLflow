import os
import logging
import sys

def setup_logging(log_filename: str) -> str:
    """
    Setup logging for the application.

    Args:
        log_filename (str): The name of the log file to create (e.g., "data_ingestion.log").

    Returns:
        str: The full path of the log file created.
    """
    # Get the current working directory (main project folder)
    project_root = os.getcwd()  # Gets the folder where you run the main script
    log_dir = os.path.join(project_root, "logs")  
    os.makedirs(log_dir, exist_ok=True)

    # Full log file path
    log_file_path = os.path.join(log_dir, log_filename)

    # Remove existing handlers to prevent duplicate logs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout),  # Also print to console for debugging
        ]
    )
    return log_file_path
