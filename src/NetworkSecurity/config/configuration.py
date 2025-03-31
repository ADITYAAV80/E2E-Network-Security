from src.NetworkSecurity.constants import *
from src.NetworkSecurity.utils.common import read_yaml,create_directories
from src.NetworkSecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    
    )

## reads from config/config.yaml
class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self)->DataIngestionConfig:

        config = self.config.data_ingestion

        # create artifacts/data_ingestion
        create_directories([config.ingestion_dir])

        ##return data_ingestion_config object which is validated
        data_ingestion_config = DataIngestionConfig(

            ingestion_dir = config.ingestion_dir,
            collection_name = config.collection_name,
            database_name = config.database_name,
            file_name = config.file_name
        )

        return data_ingestion_config
    
    def get_data_validation_config(self)->DataValidationConfig:

        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            ingestion_file = config.ingestion_file,
            STATUS_FILE = config.STATUS_FILE,
            all_schema = schema
        )

        return data_validation_config
    
    def get_data_transformation_config(self)->DataTransformationConfig:

        config = self.config.data_transformation
        params = self.params.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            data_path = config.data_path,
            test_size = params.test_size,
            random_state = params.random_state
        )

        return data_transformation_config
    
    def get_model_trainer_config(self)->ModelTrainerConfig:

        config = self.config.model_trainer
        params = self.params.model_trainer
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            mlflow_uri = config.mlflow_uri,
            mlflow_experiment = config.mlflow_experiment,
            standard_scaler_name = config.standard_scaler_name,

            models = list(params.model.keys()),
            hyperparams = params.model.to_dict(),
            
            target_column = schema.name           
        )

        return model_trainer_config