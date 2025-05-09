from src.NetworkSecurity.config.configuration import ConfigurationManager
from src.NetworkSecurity.components.data_validation import DataValidation
from src.NetworkSecurity.logging.logger import logger

STAGE_NAME = "Data Validation Stage"
class DataValidationTrainingPipeline:

    def __init__(self):
        pass
    def initiate_data_validation(self):

        try:
            logger.info(f"Configuration manager loaded")
            cm = ConfigurationManager()
            data_validation_config = cm.get_data_validation_config()
            logger.info(f"Data Validation module loaded")
            dv = DataValidation(data_validation_config)
            logger.info(f"Validating all columns......")
            dv.validate_all_columns()
        except Exception as e:
            logger.exception(e)
            raise e


if __name__=="__main__":

    try:
        logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
        ditp = DataValidationTrainingPipeline()
        ditp.initiate_data_validation()
        logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        logger.exception(e)
        raise e