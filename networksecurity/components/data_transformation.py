import sys, os , numpy as np, pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline 
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import setup_logging
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import save_numpy_array, save_object
logger = setup_logging('DataTransformation Logging Started')
class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            logger.error(f"Error in DataTransformation __init__ {str(e)}")
            raise NetworkSecurityException(f"Error in DataTransformation __init__ {str(e)}",sys.exc_info(),1,logger=logger)
    
    def get_data_transformation_pipeline(self)->Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline(steps=[('imputer', imputer)])
            return processor 
        
        except Exception as e:
            logger.error(f"Error in get_data_transformation_pipeline {str(e)}")
            raise NetworkSecurityException(f"Error in get_data_transformation_pipeline {str(e)}",sys.exc_info(),2,logger=logger)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logger.info('Data Transformation Started')
        try:
            # Load cleaned training and testing datasets
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            # Clean target labels directly from full DataFrames
            train_df[TARGET_COLUMN] = train_df[TARGET_COLUMN].replace({-1: 0, 1: 1})
            test_df[TARGET_COLUMN] = test_df[TARGET_COLUMN].replace({-1: 0, 1: 1})

            # Now split after cleaning
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_test_df = test_df[TARGET_COLUMN]


            # Get preprocessing pipeline
            processor = self.get_data_transformation_pipeline()
            preprocessor_object = processor.fit(input_feature_train_df)

            # Transform the input features
            transformed_input_feature_train = preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test = preprocessor_object.transform(input_feature_test_df)

            # Concatenate transformed features with target column
            train_arr = np.concatenate((transformed_input_feature_train, target_train_df.values.reshape(-1, 1)), axis=1)
            test_arr = np.concatenate((transformed_input_feature_test, target_test_df.values.reshape(-1, 1)), axis=1)

            # Save the transformed arrays and preprocessor
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            logger.info('Data Transformation Completed')

            # Return the artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            logger.error(f"Error in DataTransformation Initiation {str(e)}")
            raise NetworkSecurityException(f"Error in DataTransformation Initiation {str(e)}", sys.exc_info(), 2, logger=logger)