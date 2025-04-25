from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True  # Assume valid unless proven wrong
            
            ## Read CSV
            data = pd.read_csv(self.config.ingestion_file)

            ## Extract all columns and schema
            all_cols = list(data.columns)
            all_schema = set(self.config.all_schema.keys())  # Convert to set for fast lookup

            ## Check for missing or extra columns
            missing_cols = all_schema - set(all_cols)
            extra_cols = set(all_cols) - all_schema

            if missing_cols or extra_cols:
                validation_status = False

            ## Write final status
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}\n")
                if missing_cols:
                    f.write(f"Missing Columns: {missing_cols}\n")
                if extra_cols:
                    f.write(f"Extra Columns: {extra_cols}\n")

            return validation_status

        except Exception as e:
            raise e
