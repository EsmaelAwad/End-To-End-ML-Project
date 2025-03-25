from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os 
import sys
from pymongo import MongoClient
from typing import List 
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import pandas as pd 
import numpy as np 
# Initialize the logger
logger = setup_logging()

# Loading the .env file to access creds and critical information.
load_dotenv()
# Form the connection URI
uri = os.getenv('MONGODB_URI')

class DataIngenstion:
    def __init__(self, mongodb_uri=uri ,data_ingestion_config=DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongodb_uri = mongodb_uri
            self.mongo_client = MongoClient(self.mongodb_uri)
            self.database_name = self.data_ingestion_config.database_name
            self.collection_name = self.data_ingestion_config.collection_name
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info(), 1000,logger=logger)
    
    def export_connection_as_df(self):
        try:
            collection = self.mongo_client[self.database_name][self.collection_name]
            df = pd.DataFrame(list(collection.find()))
            logger.info(f"Successfully fetched {df.shape[0]} rows and {df.shape[1]} columns from MongoDB.")
            
            if df.empty:
                logger.warning("Fetched DataFrame is empty! Skipping ingestion.")
                raise NetworkSecurityException("Fetched empty data from MongoDB", sys.exc_info(), 1005,logger=logger)
            
            if '_id' in df.columns:
                df = df.drop(columns='_id', axis=1)
            df.replace({'Na': np.nan, 'na': np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info(), 1002,logger=logger)

    
    def export_data_into_feature_store(self, dataframe:pd.DataFrame = None):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logger.info('Successfully exported the data as a csv file in the feature store.')
            return dataframe 
        except Exception as e:
            NetworkSecurityException(e, sys.exc_info(), 1003,logger=logger)
    def split_data_as_train_test(self, dataframe:pd.DataFrame = None):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size = self.data_ingestion_config.train_test_split_ratio
            )
            logger.info('Performed train test split on the data')
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logger.info('Exported the train and testing files')
        except Exception as e :
            NetworkSecurityException(e, sys.exc_info(), 1004,logger=logger)
            
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_connection_as_df()

            # Export to feature store
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)

            # Now correctly pass dataframe
            self.split_data_as_train_test(dataframe)

            # Create the artifact with paths
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info(), 1001,logger=logger)
