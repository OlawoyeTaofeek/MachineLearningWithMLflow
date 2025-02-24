from mlProject.constant import *
from mlProject.utils.common import load_yaml, create_directories
from mlProject.entity.config_entity import (DataIngestionConfig, 
                                            DataValidationConfig)


class ConfigurationManager:
    """
    A class responsible for managing configurations across various pipeline stages.
    It loads configuration files (YAML) and returns stage-specific configuration 
    objects with all necessary parameters.

    Attributes:
        config (dict): Loaded configuration from the main config YAML file.
        params (dict): Loaded parameters from the params YAML file.
        schema (dict): Loaded schema definitions from the schema YAML file.
    """

    def __init__(self, config_filepath=CONFIG_FILE_PATH, 
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        """
        Initializes the ConfigurationManager by loading the configuration, parameters, 
        and schema files. Also ensures that the main artifacts directory exists.

        Args:
            config_filepath (str): Path to the main configuration YAML file.
            params_filepath (str): Path to the parameters YAML file.
            schema_filepath (str): Path to the schema YAML file.
        """
        self.config = load_yaml(config_filepath)
        self.params = load_yaml(params_filepath)
        self.schema = load_yaml(schema_filepath)

        # Create the main artifacts directory
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves the configuration required for the data ingestion stage.

        Process:
            - Extracts data ingestion-related configurations from the loaded YAML.
            - Creates the root directory for data ingestion artifacts.
            - Returns a DataIngestionConfig object with all relevant attributes.

        Returns:
            DataIngestionConfig: An object containing:
                - root_dir (str): Directory to store data ingestion artifacts.
                - source_url (str): URL from which the raw data will be downloaded.
                - local_data_dir (str): Local file path for the downloaded data.
                - unzip_dir (str): Directory where the data will be extracted.
        """
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_URL,
            local_data_dir=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Retrieves the configuration required for the data validation stage.

        Process:
            - Extracts data validation-related configurations from the loaded YAML.
            - Loads the expected schema for validation.
            - Creates the root directory for data validation artifacts.
            - Returns a DataValidationConfig object with all relevant attributes.

        Returns:
            DataValidationConfig: An object containing:
                - root_dir (str): Directory for storing validation artifacts.
                - STATUS_FILE (str): Path to the file where validation status will be recorded.
                - unzip_data_dir (str): Directory where the ingested data is located.
                - all_schema (dict): Expected columns and data types for validation.
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            unzip_data_dir=config.unzip_data_dir,
            all_schema=schema
        )
        return data_validation_config
