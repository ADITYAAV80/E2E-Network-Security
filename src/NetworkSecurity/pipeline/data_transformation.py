from src.NetworkSecurity.config.configuration import ConfigurationManager
from src.NetworkSecurity.components.data_transformation import DataTransformation
from src.NetworkSecurity.logging.logger import logger
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"
class DataTransformationTrainingPipeline:

    def __init__(self):
        pass
    def initiate_data_transformation(self):

        try:
            with open(Path("artifacts/data_validation/status.txt"),"r") as f:
                doc = f.read()
                status = doc.split(" ")[-1].strip().lower() == "true"
                if status:
                    cm = ConfigurationManager()
                    data_transformation_config = cm.get_data_transformation_config()
                    dt = DataTransformation(data_transformation_config)
                    dt.train_test_splitting()

        except Exception as e:
            raise e


if __name__=="__main__":

    try:
        logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
        dt = DataTransformationTrainingPipeline()
        dt.initiate_data_transformation()
        logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        logger.exception(e)
        raise e