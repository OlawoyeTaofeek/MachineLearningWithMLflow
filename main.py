from mlProject.utils.logging_utils import setup_logging
from mlProject.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline
from mlProject.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from mlProject.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
import logging


# ----------- Data Ingestion Stage -----------
STAGE_NAME = "Data Ingestion Stage"
setup_logging("stage1_ingestion.log")  # GLOBAL logging for this stage

try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<<")
    pipeline = DataIngestionTrainingPipeline()
    pipeline.main()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<<\n\nX============X")
except Exception as e:
    logging.error(f"Error in {STAGE_NAME}: {e}")
    raise e


# ----------- Data Validation Stage -----------
STAGE_NAME = "Data Validation Stage"
setup_logging("stage2_data_validation.log")  # GLOBAL logging for this stage

try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.main()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logging.error(f"Error in {STAGE_NAME}: {e}")
    raise e


# ----------- Data Validation Stage -----------

STAGE_NAME = "Data Transformation Stage"
setup_logging("stage3_data_transformation.log")  # GLOBAL logging for this stage

try:
    logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataTransformationTrainingPipeline()
    obj.main()
    logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logging.exception(e)
    raise e
