from src.NetworkSecurity.config.configuration import ConfigurationManager
from src.NetworkSecurity.components.data_ingestion import DataIngestion
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.exception.exception import NetworkSecurityException
import sys

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:

    def __init__(self):
        pass
    def initiate_data_ingestion(self):

        try:
            cm = ConfigurationManager()
            data_ingestion_config = cm.get_data_ingestion_config()
            di = DataIngestion(data_ingestion_config)
            di.download_file()
        except Exception as e:
            NetworkSecurityException(e,sys)

#### this will only run if you execute it directly like below
if __name__=="__main__":

    try:
        logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
        ditp = DataIngestionTrainingPipeline()
        ditp.initiate_data_ingestion()
        logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        NetworkSecurityException(e,sys)