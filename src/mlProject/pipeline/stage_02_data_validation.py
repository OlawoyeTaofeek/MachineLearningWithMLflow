from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_validation import DataValidation
import logging
from mlProject.utils.logging_utils import setup_logging


class DataValidationTrainingPipeline:
    def __init__(self):
        pass    
    
    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate_data()
        except Exception as e:
            raise e
        

# if __name__ == '__main__':
#     try:
#         logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
#         obj = DataValidationTrainingPipeline()
#         obj.main()
#         logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logging.exception(e)
#         raise e