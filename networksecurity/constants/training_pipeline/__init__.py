import os 
import sys 
import pandas as pd 

"""
Data Ingestion Related Constans
"""
DATA_INGESTION_COLLECTION_NAME = 'phishingData'
DATA_INGESTION_DATABASE_NAME = 'NetworkSecurity'
DATA_INGESTION_DIR_NAME = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR = 'feature_store'
DATA_INGESTION_INGESTED_DIR = 'ingested'
DATA_INGESTION_TEST_RATIO = 0.2

"""
Default Values For Training
"""
TARGET_COLUMN = 'Result'
PIPELINE_NAME = 'NetworkSecurity'
ARTIFACTS_DIR = 'Artifacts'
FILE_NAME = 'phishingData.csv'

TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'
