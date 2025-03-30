from src.NetworkSecurity.constants import *
from src.NetworkSecurity.utils.common import read_yaml,create_directories
from src.NetworkSecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig
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