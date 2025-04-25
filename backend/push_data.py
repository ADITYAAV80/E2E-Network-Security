import os
import sys
import json
import certifi
from dotenv import load_dotenv
import pandas as pd
import pymongo
from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logger

"""
certifi.where()
Ensures a secure TLS/SSL connection.
Fixes SSL certificate verification errors when connecting to cloud MongoDB services.
"""

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class NetWorkDataExtract():

    def __init__(self):
        pass

    def cv_to_json_converter(self,file_path):

        try:
            df = pd.read_csv(file_path)
            df.drop(columns=["id"],inplace=True)
            ## converts to json
            json_str = json.loads(df.T.to_json()) #{0:row1,1:row2,...}
            records = list(json_str.values()) # [{row1},{row2}...]

            logger.info("Converted file to JSON")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        return records
    
    def insert_data_mongodb(self,records,database,collection):

        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())

            database_obj = self.mongo_client[self.database] 
            collection_obj = database_obj[self.collection] 
            collection_obj.insert_many(self.records)

            logger.info("Records inserted in database")
            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":

    FILEPATH="NetworkSecurityData/PriorETL/data.csv"
    DATABASE="PhishingData"
    Collection="NetworkData"
    nde = NetWorkDataExtract()
    records = nde.cv_to_json_converter(file_path=FILEPATH)
    no_of_records = nde.insert_data_mongodb(
            records=records,
            database=DATABASE,
            collection=Collection)