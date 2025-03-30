import os
import pandas as pd
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.exception.exception import NetworkSecurityException
import sys

class DataIngestion:
    ## gets config from ConfigManager
    def __init__(self, config):
        self.config = config

    ## extracts data from MongoDB and saves it as CSV
    def download_file(self):
        try:
            load_dotenv()
            MONGO_DB_URL = os.getenv("MONGO_DB_URL")

            # Connect to MongoDB Atlas
            client = MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())

            # Choose Database & Collection
            db = client[self.config.database_name]
            collection = db[self.config.collection_name]

            logger.info(f"Fetching data from MongoDB collection: {self.config.collection_name}")

            # Retrieve data from MongoDB
            data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field

            if not data:
                raise ValueError("No data found in the collection!")

            # Convert to Pandas DataFrame
            df = pd.DataFrame(data)

            # Save as CSV
            os.makedirs(self.config.ingestion_dir, exist_ok=True)
            csv_path = os.path.join(self.config.ingestion_dir, self.config.file_name)
            df.to_csv(csv_path, index=False)

            logger.info(f"Data successfully downloaded and saved to {csv_path}")

            return csv_path  # Return path for further processing

        except Exception as e:
            logger.error(f"Error during data download: {e}")
            NetworkSecurityException(e,sys)