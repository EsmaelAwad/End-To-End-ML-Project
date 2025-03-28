from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import sys 

logger = setup_logging('ModelTrainer Logging Started')

def get_classification_score(y_pred, y_true):
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        accuracy = accuracy_score(y_true, y_pred)
        return ClassificationMetricArtifact(f1, precision, recall, accuracy)
    except Exception as e:
        logger.error(f"Error in get_classification_score {str(e)}")
        raise NetworkSecurityException(f"Error in get_classification_score {str(e)}",sys.exc_info(),1,logger=logger)