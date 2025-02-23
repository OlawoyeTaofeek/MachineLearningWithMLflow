import os
import logging
import sys

from src.mlProject.utils.logging_utils import setup_logging
setup_logging("stage1_ingestion.log")  # 🌟 Creates logs/stage1_ingestion.log in main project folder

from mlProject.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data ingestion stage"

if __name__ == '__main__':
    try:
        logging.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.main()
        logging.info(f">>>>> stage {STAGE_NAME} completed <<<<<<\n\nX============X")
    except Exception as e:
        logging.error(f"Error in stage {STAGE_NAME}: {e}")
        raise e
