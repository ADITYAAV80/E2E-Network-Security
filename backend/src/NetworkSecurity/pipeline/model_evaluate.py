from src.NetworkSecurity.config.configuration import ConfigurationManager
from src.NetworkSecurity.components.model_evaluate import ModelEvaluate
from src.NetworkSecurity.logging.logger import logger

STAGE_NAME = "Model Evaluation Stage"
class ModelEvaluatePipeline:

    def __init__(self):
        pass

    def initiate_model_evaluate(self,mlflow_run_id):
        try:
            logger.info(f"Configuration manager loaded")
            cm = ConfigurationManager()
            model_train_evaluate = cm.get_model_evaluation_config()
            logger.info(f"Model Evaluate loaded")
            mt = ModelEvaluate(model_train_evaluate)
            logger.info(f"Evaluate called")
            mt.evaluate(mlflow_run_id)
        except Exception as e:
            logger.exception(e)
            raise e


if __name__=="__main__":

    try:
        logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
        mep = ModelEvaluatePipeline()
        mlflow_run_id = "8f25b84701844ea7848d7812a3700d9b"
        mep.initiate_model_evaluate(mlflow_run_id)
        logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        logger.exception(e)
        raise e