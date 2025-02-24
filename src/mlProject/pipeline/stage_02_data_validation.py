from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_validation import DataValidation
import logging
from mlProject.utils.logging_utils import setup_logging


class DataValidationTrainingPipeline:
    """
    A pipeline class responsible for orchestrating the data validation process.

    This class ties together the configuration management and the actual validation logic.
    It ensures that the data is validated against the expected schema before being passed 
    to subsequent stages in the pipeline.
    """

    def __init__(self):
        """
        Initializes the DataValidationTrainingPipeline instance.

        Currently, there are no attributes set during initialization as all operations 
        are handled in the `main` method.
        """
        pass    

    def main(self):
        """
        Executes the data validation pipeline.

        Steps:
            1. Initializes the ConfigurationManager to load configurations.
            2. Retrieves the data validation configuration.
            3. Instantiates the DataValidation component with the configuration.
            4. Calls the `validate_data` method to perform validation.
        
        Raises:
            Exception: If any error occurs during the validation process, it is raised for handling upstream.
        """
        try:
            # Load configurations
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()

            # Perform data validation
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