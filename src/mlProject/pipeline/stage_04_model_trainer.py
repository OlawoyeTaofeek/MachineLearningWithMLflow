from mlProject.config.configuration import ConfigurationManager
from mlProject.components.model_trainer import ModelTrainer
import logging 
from mlProject.utils.logging_utils import setup_logging



STAGE_NAME = "Model Trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()




# if __name__ == '__main__':
#     try:
#         logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
#         obj = ModelTrainerTrainingPipeline()
#         obj.main()
#         logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logging.exception(e)
#         raise e
