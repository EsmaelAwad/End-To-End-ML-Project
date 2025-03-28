from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os 
import sys

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging

logger = setup_logging('ModelTrainer Logging Started')

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            logger.error(f"Error in NetworkModel __init__ {str(e)}")
            raise NetworkSecurityException(f"Error in NetworkModel __init__ {str(e)}",sys.exc_info(),1,logger=logger)
    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            return self.model.predict(x_transformed)
        except Exception as e:
            logger.error(f"Error in predict {str(e)}")
            raise NetworkSecurityException(f"Error in predict {str(e)}",sys.exc_info(),2,logger=logger)