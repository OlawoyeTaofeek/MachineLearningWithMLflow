import os
import logging
import sys

from mlProject.utils.logging_utils import setup_logging
from mlProject.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data ingestion stage"
setup_logging("stage1_ingestion.log")

if __name__ == '__main__':
    try:
        logging.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.main()
        logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<<\n\nX============X")
    except Exception as e:
        logging.error(f"Error in stage {STAGE_NAME}: {e}")
        raise e


