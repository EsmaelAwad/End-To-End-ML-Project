import os
import sys


from networksecurity.exceptions.exception import NetworkSecurityException 
from networksecurity.logging.logger import setup_logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models_with_random_search

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow
from urllib.parse import urlparse
import dagshub

logger = setup_logging('ModelTrainer Logging Started')

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            logger.error(f"Error in ModelTrainer __init__ {str(e)}")
            raise NetworkSecurityException(f"Error in ModelTrainer __init__ {str(e)}",sys.exc_info(),1,logger=logger)
    
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                'LogisticRegression': LogisticRegression(),
                'AdaBoostClassifier': AdaBoostClassifier(),
                'GradientBoostingClassifier': GradientBoostingClassifier(),
                'RandomForestClassifier': RandomForestClassifier(),
                'DecisionTreeClassifier': DecisionTreeClassifier(),
                'KNeighborsClassifier': KNeighborsClassifier()
            }
            params = {
                    'LogisticRegression': {
                        'penalty': ['l1', 'l2'],
                        'C': [0.01, 0.1, 1, 10, 100],
                        'solver': ['liblinear', 'saga'],  # These support l1/l2
                        'max_iter': [100, 200, 500]
                    },
                    'AdaBoostClassifier': {
                        'n_estimators': [50, 100, 200],
                        'learning_rate': [0.01, 0.1, 1],
                    },
                    'GradientBoostingClassifier': {
                        'n_estimators': [100, 200, 300],
                        'learning_rate': [0.01, 0.1, 0.2],
                        'max_depth': [3, 5, 7],
                        'subsample': [0.8, 1.0]
                    },
                    'RandomForestClassifier': {
                        'n_estimators': [100, 200, 500],
                        'max_depth': [None, 10, 20, 30],
                        'min_samples_split': [2, 5, 10],
                        'min_samples_leaf': [1, 2, 4],
                        'bootstrap': [True, False]
                    },
                    'DecisionTreeClassifier': {
                        'criterion': ['gini', 'entropy'],
                        'max_depth': [None, 10, 20, 30],
                        'min_samples_split': [2, 5, 10]
                    },
                    'KNeighborsClassifier': {
                        'n_neighbors': [3, 5, 7, 9],
                        'weights': ['uniform', 'distance'],
                        'metric': ['euclidean', 'manhattan', 'minkowski']
                    }
                }
            models_report = evaluate_models_with_random_search(X_train=x_train, y_train=y_train,
                                                               X_test=x_test, y_test=y_test,
                                                               models=models,param_distributions=params,
                                                               scoring='accuracy')
            # models_report contains each model's best parameters and best score, We'll extract the best out of all of them based on the score.
            best_model_name = max(models_report, key=lambda x: models_report[x]['test_accuracy'])
            best_model = models[best_model_name]
            best_model_params = models_report[best_model_name]['best_params']
            best_model.set_params(**best_model_params)
            print(f"Best Model: {best_model_name}")
            y_pred_train = best_model.predict(x_train)
            y_pred_test = best_model.predict(x_test)
            train_score = get_classification_score(y_pred_train, y_train)
            test_score = get_classification_score(y_pred_test, y_test)
            print(f"Train Score: {train_score}")
            print(f"Test Score: {test_score}")
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model = NetworkModel(preprocessor=preprocessor, model=best_model)
            model_path = self.model_trainer_config.trained_model_file_path
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            save_object(model_path, model)
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=model_path,
                                                          train_metric_artifact=train_score,
                                                          test_metric_artifact=test_score
                                                          )
            logger.info(f"ModelTrainer train_model completed successfully")
            return model_trainer_artifact

        except Exception as e:
            logger.error(f"Error in ModelTrainer train_model {str(e)}")
            raise NetworkSecurityException(f"Error in ModelTrainer train_model {str(e)}",sys.exc_info(),3,logger=logger)
        
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = train_arr[:,:-1], train_arr[:,-1], test_arr[:,:-1], test_arr[:,-1]

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            logger.info(f"ModelTrainer initiate_model_trainer completed successfully")
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"Error in initiate_model_trainer {str(e)}")
            raise NetworkSecurityException(f"Error in initiate_model_trainer {str(e)}",sys.exc_info(),2,logger=logger)