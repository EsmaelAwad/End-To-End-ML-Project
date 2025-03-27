from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from scipy.stats import ks_2samp 
import pandas as pd 
import os, sys 
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import yaml 
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils import write_yaml_file
logger = setup_logging('DataValidation Logging Started')

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 logger = logger):
        try: 
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.logger = logger 
        except Exception as e:
            self.logger.error(f"Error in DataValidation __init__ {str(e)}")
            raise NetworkSecurityException(f"Error in DataValidation __init__ {str(e)}",sys.exc_info(),1,logger=logger)
        
    def check_number_of_columns(self, dataframe: pd.DataFrame)-> bool:
        try:
            if dataframe.shape[1] == len(self._schema_config['columns']):
                logger.info(f"Number of columns in the dataframe is as expected")
                return True 
            else:
                logger.error(f"Expected number of columns is {len(self._schema_config['columns'])} but got {dataframe.shape[1]}")
                return False 
        except Exception as e:
            self.logger.error(f"Error in check_number_of_columns {str(e)}")
            raise NetworkSecurityException(f"Error in check_number_of_columns {str(e)}",sys.exc_info(),3,logger=logger)
    
    def check_numerical_columns(self, dataframe: pd.DataFrame)-> bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            for column in numerical_columns:
                if column not in dataframe.columns:
                    logger.error(f"Column {column} is not present in the dataframe")
                    return False 
            logger.info(f"All the numerical columns are present in the dataframe")
            return True 
        except Exception as e:
            self.logger.error(f"Error in check_numerical_columns {str(e)}")
            raise NetworkSecurityException(f"Error in check_numerical_columns {str(e)}",sys.exc_info(),4,logger=logger)

    def which_cols_are_missing(self, dataframe: pd.DataFrame)-> list:
        try:
            missing_cols = list(set(self._schema_config['columns']) - set(dataframe.columns))
            return missing_cols
        except Exception as e:
            self.logger.error(f"Error in which_cols_are_missing {str(e)}")
            raise NetworkSecurityException(f"Error in which_cols_are_missing {str(e)}",sys.exc_info(),5,logger=logger)
    
    def detect_data_drift(self, base_df, current_df, threshold = 0.05)-> bool:
        try:
            status = True
            drift_columns = []
            for column in base_df.columns:
                statistic, pvalue = ks_2samp(base_df[column], current_df[column])
                if pvalue < threshold:
                    drift_columns.append(column)
            if drift_columns:
                logger.warning(f"Data Drift detected in the following columns: {drift_columns}")
                status = False
                # Writing to the drift report
                drift_report = {
                    'drift_columns': drift_columns
                }
                write_yaml_file(self.data_validation_config.drift_report_file_path, drift_report, replace=True) 
            else:
                logger.info("No Data Drift detected")
            return status 
        except Exception as e:
            self.logger.error(f"Error in detect_data_drift {str(e)}")
            raise NetworkSecurityException(f"Error in detect_data_drift {str(e)}",sys.exc_info(),6,logger=logger)
        
    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # Reading the data from the specified file paths, Train and Test
            train_dataframe = pd.read_csv(train_file_path)
            test_dataframe = pd.read_csv(test_file_path)
            # Checking the number of columns
            status = self.check_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train Dataframe has {train_dataframe.shape[1]} columns, expected {len(self._schema_config['columns'])}"
                logger.error(error_message)
            status = self.check_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test Dataframe has {test_dataframe.shape[1]} columns, expected {len(self._schema_config['columns'])}"
                logger.error(error_message)
            # Checking if numerical columns are present
            status = self.check_numerical_columns(train_dataframe)
            if not status:
                error_message = f"Numerical columns are missing in Train Dataframe"
                logger.error(error_message)
            status = self.check_numerical_columns(test_dataframe)
            if not status:
                error_message = f"Numerical columns are missing in Test Dataframe"
                logger.error(error_message)
            if not status:
                logger.warning(f"Some columns are missing in the dataframes, They are:\n {self.which_cols_are_missing(train_dataframe)}")
            # Checking for drift in the data
            status = self.detect_data_drift(train_dataframe, test_dataframe)
            if not status:
                logger.warning("Data Drift detected in the dataframes")
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            # We can write a condition here to write the files only if the status is True, but for now we will be writing the files.
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            self.logger.error(f"Error in DataValidation __init__ {str(e)}")
            raise NetworkSecurityException(f"Error in DataValidation __init__ {str(e)}",sys.exc_info(),2,logger=logger)
        
