from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import yaml 
import sys , os 
import numpy as np
import pickle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score

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

def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        logger.error(f"Error in load_object {str(e)}")
        raise NetworkSecurityException(e, sys.exc_info(), 5, logger=logger)

def load_numpy_array_data(file_path:str)-> np.ndarray:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, 'rb') as f:
            return np.load(f)
    except Exception as e:
        logger.error(f"Error in load_numpy_array {str(e)}")
        raise NetworkSecurityException(f"Error in load_numpy_array {str(e)}",sys.exc_info(),6,logger=logger)
    
def evaluate_models_with_random_search(X_train, y_train, X_test, y_test, models: dict, param_distributions: dict, scoring='accuracy', cv=3, n_iter=10, random_state=42):
    try:
        report = {}

        for model_name in models.keys():
            print(f"Evaluating {model_name}...")
            model = models[model_name]
            params = param_distributions[model_name]

            # Randomized Search CV
            rs = RandomizedSearchCV(model, params, n_iter=n_iter, scoring=scoring, cv=cv, random_state=random_state, n_jobs=-1)
            rs.fit(X_train, y_train)

            # Set best params & retrain
            model.set_params(**rs.best_params_)
            model.fit(X_train, y_train)

            # Predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Metrics
            train_score = accuracy_score(y_train, y_train_pred)
            test_score = accuracy_score(y_test, y_test_pred)

            # Save result
            report[model_name] = {
                'best_params': rs.best_params_,
                'train_accuracy': train_score,
                'test_accuracy': test_score
            }
            print(f"{model_name} evaluated. Test accuracy: {test_score}, \nTrain accuracy: {train_score}, \nBest params: {rs.best_params_}")
        return report

    except Exception as e:
        raise NetworkSecurityException(f"Error in evaluate_models_with_random_search: {str(e)}", sys.exc_info(), 1, logger=logger)
