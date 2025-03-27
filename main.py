from networksecurity.components.data_ingestion import DataIngenstion
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logger import setup_logging
from networksecurity.exceptions.exception import NetworkSecurityException
import sys 
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
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
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngenstion(mongodb_uri=uri,data_ingestion_config=data_ingestion_config)
        logger.info('Initiating the data ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logger.info('Data Ingestion Completed')
        data_validation_config = DataValidationConfig(training_pipeline_config)        
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info('Data Validation Completed')
        print(data_validation_artifact)
    except Exception as e:
        NetworkSecurityException(e, sys.exc_info(),1, logger=logger)

