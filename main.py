from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.pipeline.data_ingestion import DataIngestionTrainingPipeline
import sys

STAGE_NAME="Data Ingestion Stage"

try:
    logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
    ditp = DataIngestionTrainingPipeline()
    ditp.initiate_data_ingestion()
    logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    NetworkSecurityException(e,sys)