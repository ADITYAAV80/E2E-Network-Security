import sys
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.pipeline.data_ingestion import DataIngestionTrainingPipeline
from src.NetworkSecurity.pipeline.data_validation import DataValidationTrainingPipeline
from src.NetworkSecurity.pipeline.data_transformation import DataTransformationTrainingPipeline
from src.NetworkSecurity.pipeline.model_train import ModelTrainingPipeline
from src.NetworkSecurity.pipeline.model_evaluate import ModelEvaluatePipeline
from src.NetworkSecurity.cloud.s3_syncer import S3Sync
from src.NetworkSecurity.constants import *
from src.NetworkSecurity.utils.common import read_yaml

class TrainingPipeline:
    def __init__(self):
        self.s3_sync = S3Sync()
        self.data_ingestion_artifact = None
        self.data_validation_artifact = None
        self.data_transformation_artifact = None
        self.model_trainer_artifact = None

    def start_data_ingestion(self):
        """Starts the data ingestion process"""
        
        STAGE_NAME="Data Ingestion Stage"
        try:
            logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
            ditp = DataIngestionTrainingPipeline()
            ditp.initiate_data_ingestion()
            logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            NetworkSecurityException(e,sys)

    def start_data_validation(self):
        """Starts the data validation process"""
        
        STAGE_NAME="Data Validation Stage"
        try:
            logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
            ditp = DataValidationTrainingPipeline()
            ditp.initiate_data_validation()
            logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            NetworkSecurityException(e,sys)

    def start_data_transformation(self):
        """Starts the data transformation process"""
        STAGE_NAME = "Data Transformation Stage"
        try:
            logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
            dt = DataTransformationTrainingPipeline()
            dt.initiate_data_transformation()
            logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        except Exception as e:
            logger.exception(e)
            NetworkSecurityException(e,sys)


    def start_model_training(self):
        """Starts the model training process"""

        STAGE_NAME = "Model Training Stage"
        try:
            logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
            mtp = ModelTrainingPipeline()
            mlflow_run_id = mtp.initiate_model_train()
            logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
            return mlflow_run_id

        except Exception as e:
            logger.exception(e)
            NetworkSecurityException(e,sys)

    def start_model_evaluation(self,mlflow_run_id):
        """Starts the model evaluation process"""
        STAGE_NAME = "Model Evaluation Stage"
        try:
            logger.info(f">>>>>Stage {STAGE_NAME} started <<<<<<")
            mep = ModelEvaluatePipeline()
            mep.initiate_model_evaluate(mlflow_run_id)
            logger.info(f">>>>Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

    def sync_artifact_dir_to_s3(self):
        """Uploads artifacts to S3"""
        
        config = read_yaml(CONFIG_FILE_PATH)
        artifact_folder = str(config.artifacts_root)

        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{artifact_folder}"
            self.s3_sync.sync_folder_to_s3(folder=artifact_folder, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logger.exception(e)
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        """Runs the entire pipeline in sequence"""
        try:
            logger.info("Starting Training Pipeline")

            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            mlflow_run_id = self.start_model_training()
            self.start_model_evaluation(mlflow_run_id)
            # Sync artifacts and model to S3
            self.sync_artifact_dir_to_s3()
            logger.info(" Training Pipeline Completed Successfully")
            return True
        
        except Exception as e:
            logger.exception(e)
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
