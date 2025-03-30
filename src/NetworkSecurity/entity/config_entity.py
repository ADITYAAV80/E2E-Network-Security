from pydantic import BaseModel
from pathlib import Path

class DataIngestionConfig(BaseModel):
    ## config
    ingestion_dir: Path
    collection_name: str
    database_name: str
    file_name: str