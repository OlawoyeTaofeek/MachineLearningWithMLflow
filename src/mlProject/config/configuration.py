from mlProject.constant import *
from mlProject.utils.common import load_yaml, create_directories
## Update my components
from mlProject.entity.config_entity import (DataIngestionConfig, 
                                            DataValidationConfig)


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, 
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH):
        self.config = load_yaml(config_filepath)
        self.params = load_yaml(params_filepath)
        self.schema = load_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_url= config.source_URL,
            local_data_dir = config.local_data_file,
            unzip_dir = config.unzip_dir
        )
        
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )
        return data_validation_config
    
    
        