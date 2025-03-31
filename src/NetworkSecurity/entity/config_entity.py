from pydantic import BaseModel,HttpUrl
from pathlib import Path

class DataIngestionConfig(BaseModel):
    ## config
    ingestion_dir: Path
    collection_name: str
    database_name: str
    file_name: str

class DataValidationConfig(BaseModel):

    root_dir: Path
    ingestion_file: str
    STATUS_FILE: Path
    all_schema: dict

class DataTransformationConfig(BaseModel):

    ##config
    root_dir: Path
    data_path: Path
    ##params
    test_size: float
    random_state: int

class ModelTrainerConfig(BaseModel):
    ## from config
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
  
    mlflow_uri: HttpUrl
    mlflow_experiment: str
    standard_scaler_name: str
    
    ## from params
    models: list
    hyperparams: dict

    ## from schema 
    target_column: str

class ModelEvaluationConfig(BaseModel):
    ## from config
    root_dir: Path
    test_data_path: Path
    metric_file_name: str
    target_column: str
    mlflow_uri: str
    ss_file_path: str
    model_run: str