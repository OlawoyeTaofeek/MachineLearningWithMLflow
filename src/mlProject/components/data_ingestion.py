from mlProject.entity.config_entity import DataIngestionConfig
import os
import zipfile
from mlProject.utils.logging_utils import setup_logging
from mlProject.utils.common import get_size
import logging
import urllib.request as request
from pathlib import Path


class DataIngestion:
    """
    A class to handle the data ingestion process, which includes:
    1. Downloading a dataset from a specified URL.
    2. Extracting the downloaded zip file to a specified directory.

    Attributes:
        config (DataIngestionConfig): Configuration Class(object) containing necessary parameters 
                                      for data ingestion such as source URL, local paths, and unzip directory.
    """

    def __init__(self, config: DataIngestionConfig):
        """
        Initializes the DataIngestion object with the given configuration.

        Args:
            config (DataIngestionConfig): An object containing all necessary configurations 
                                          like source URL, local file path, and unzip directory path.
        """
        self.config = config

    def download_file(self):
        """
        Downloads the dataset from the specified URL if it doesn't already exist locally.

        - If the file exists, it logs the file size instead of downloading it again.
        - If the file doesn't exist, it downloads the file and logs relevant information (e.g., headers).

        Uses:
            - urllib.request for downloading files.
            - get_size utility for displaying file size if already downloaded.
            - Logging to track the download process.
        """
        if not os.path.exists(self.config.local_data_dir):
            filename, headers = request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_dir
            )
            logging.info(f"{filename} downloaded successfully! File details:\n{headers}")
        else:
            logging.info(f"File already exists. Size: {get_size(Path(self.config.local_data_dir))}")

    def extract_zip_file(self):
        """
        Extracts the contents of the downloaded zip file into the specified directory.

        - Creates the unzip directory if it doesn't exist.
        - Extracts all contents from the zip file to the unzip path.
        - Logs the extraction process for traceability.

        Raises:
            FileNotFoundError: If the zip file to extract doesn't exist.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        if not os.path.exists(self.config.local_data_dir):
            raise FileNotFoundError(f"Zip file not found at {self.config.local_data_dir}. Please download it first.")

        with zipfile.ZipFile(self.config.local_data_dir, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            logging.info(f"Data extracted successfully to {unzip_path}.")
