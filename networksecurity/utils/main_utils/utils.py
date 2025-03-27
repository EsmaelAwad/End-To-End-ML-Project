from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import yaml 
import sys , os 
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