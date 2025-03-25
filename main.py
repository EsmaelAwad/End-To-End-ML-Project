from networksecurity.components.data_ingestion import DataIngenstion
from networksecurity.logging.logger import setup_logging
from networksecurity.exceptions.exception import NetworkSecurityException
import sys 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from dotenv import load_dotenv
import os 
# Loading the .env file to access creds and critical information.
load_dotenv()
# Form the connection URI
uri = os.getenv('MONGODB_URI')
if __name__ == '__main__':
    try:
        logger = setup_logging()
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion = DataIngenstion(mongodb_uri=uri,data_ingestion_config=data_ingestion_config)
        logger.info('Initiating the data ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        NetworkSecurityException(e, sys.exc_info(),1, logger=logger)

