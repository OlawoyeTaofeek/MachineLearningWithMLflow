from mlProject.entity.config_entity import DataIngestionConfig
import os
import zipfile
from mlProject.utils.logging_utils import setup_logging
from mlProject.utils.common import get_size
import logging
import urllib.request as request
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
    def download_file(self):
        if not os.path.exists(self.config.local_data_dir):
            filename, headers = request.urlretrieve(
                url = self.config.source_url,
                filename = self.config.local_data_dir
            )
            logging.info(f"{filename} download! with following info: \n{headers}")
        else:
            logging.info(f"File already exists of size: {get_size(Path(self.config.local_data_dir))}")
            
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_dir, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            