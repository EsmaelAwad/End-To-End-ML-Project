from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import yaml 
import sys , os 
import numpy as np
import pickle

logger = setup_logging('UTILS Logging Started')

def read_yaml_file(file_path:str = None):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error in read_yaml_file {str(e)}")
        raise NetworkSecurityException(f"Error in read_yaml_file {str(e)}",sys.exc_info(),1,logger=logger)

def write_yaml_file(file_path: str, content: object, replace: bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        logger.error(f"Error in write_yaml_file {str(e)}")
        raise NetworkSecurityException(f"Error in write_yaml_file {str(e)}",sys.exc_info(),2,logger=logger)
    
def save_numpy_array(file_path: str, nd_array:np.array = None):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path, 'wb') as f:
            np.save(f, nd_array)
    except Exception as e:
        logger.error(f"Error in save_numpy_array {str(e)}")
        raise NetworkSecurityException(f"Error in save_numpy_array {str(e)}",sys.exc_info(),3,logger=logger)
    
def save_object(file_path: str, obj: object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)
    except Exception as e:
        logger.error(f"Error in save_object {str(e)}")
        raise NetworkSecurityException(f"Error in save_object {str(e)}",sys.exc_info(),4,logger=logger)
    