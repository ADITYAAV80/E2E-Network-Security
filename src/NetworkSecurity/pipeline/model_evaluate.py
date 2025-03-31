from src.NetworkSecurity.config.configuration import ConfigurationManager
from src.NetworkSecurity.components.model_evaluate import ModelEvaluate
from src.NetworkSecurity.logging.logger import logger

STAGE_NAME = "Model Evaluation Stage"
class ModelEvaluatePipeline:

    def __init__(self):
        pass

    def initiate_model_evaluate(self):
        try:
            cm = ConfigurationManager()
            model_train_evaluate = cm.get_model_evaluation_config()
            mt = ModelEvaluate(model_train_evaluate)
            mt.evaluate()
        except Exception as e:
            raise e


if __name__=="__main__":

    try:
        logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
        mep = ModelEvaluatePipeline()
        mep.initiate_model_evaluate()
        logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        logger.exception(e)
        raise e