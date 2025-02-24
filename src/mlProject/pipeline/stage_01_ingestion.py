from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_ingestion import DataIngestion
from mlProject.utils.logging_utils import setup_logging
import logging


class DataIngestionTrainingPipeline:
    """
    A pipeline class responsible for orchestrating the data ingestion process.

    This pipeline manages the complete data ingestion flow by:
    1. Downloading the dataset from the specified source URL.
    2. Extracting the downloaded dataset if it's in a compressed format.
    
    It uses configuration details provided by the ConfigurationManager and handles 
    any errors that occur during the ingestion process.
    """

    def __init__(self):
        """
        Initializes the DataIngestionTrainingPipeline instance.

        Currently, no attributes are initialized, as all operations are managed within the `main` method.
        """
        pass 
    
    def main(self):
        """
        Executes the data ingestion pipeline.

        Steps:
            1. Loads the data ingestion configuration using ConfigurationManager.
            2. Instantiates the DataIngestion component with the given configuration.
            3. Downloads the data file if it does not already exist locally.
            4. Extracts the downloaded file to the specified directory.

        Raises:
            Exception: Propagates any exception that occurs during data ingestion.
        """
        try:
            # Load configurations
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()

            # Perform data ingestion steps
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()

        except Exception as e:
            raise e
