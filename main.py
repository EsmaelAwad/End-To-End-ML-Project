from networksecurity.components.data_ingestion import DataIngenstion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.logging.logger import setup_logging
from networksecurity.exceptions.exception import NetworkSecurityException
import sys 
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
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
        logger.info('Data Transformation Starte')
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                 data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logger.info('Data Transformation Completed')
    except Exception as e:
        logger.error('Error In Training Pipeline')
        raise NetworkSecurityException(e, sys.exc_info(),1, logger=logger)

