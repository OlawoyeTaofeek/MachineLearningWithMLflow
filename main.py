import os
import logging
import sys

from src.mlProject.utils.logging_utils import setup_logging

try:
    log_file_path =setup_logging('practice.log')
    logging.info(f"Logging is set up. Logs will be saved to {log_file_path}")
except Exception as e:
    print(f"Failed to set up logging: {e}")
    sys.exit(1)
    
    
import mlProject
print(mlProject.__version__)

