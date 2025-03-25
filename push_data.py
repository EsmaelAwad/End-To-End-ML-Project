from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import certifi
import pandas as pd
import pymongo 
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging
import sys 
import json
# Initializing the logger
logger = setup_logging(__name__)
logger.info("Logging started...")

# Load the environment variables
load_dotenv('.env')
mongodb_cluster_name = os.getenv("MONGODB_CLUSTER_NAME")
mongodb_cluster_password = os.getenv("MONGODB_CLUSTER_PASSWORD")
mongodb_cluster_username = os.getenv('MONGODB_CLUSTER_USERNAME')
# Form the connection URI
uri = f"mongodb+srv://{mongodb_cluster_username}:{mongodb_cluster_password}@cluster0.85htv.mongodb.net/?retryWrites=true&w=majority&appName={mongodb_cluster_name}"

# Create a new client and connect to the server
client = MongoClient(uri)

# Initialize a certificate to ensure a secure connection
ca = certifi.where()

class NetworkDataExtractor:
    """
    A class to extract, convert, and insert network-related data (e.g., phishing data) 
    from a CSV file into a MongoDB database.

    Attributes:
        data (pd.DataFrame): The loaded dataset.
        mongo_client (MongoClient): MongoDB client for inserting data.
    """

    def __init__(self, data: pd.DataFrame = None, mongo_client: pymongo.MongoClient = None):
        """
        Initializes the NetworkDataExtractor instance.

        Args:
            data (pd.DataFrame, optional): A pandas DataFrame to use directly instead of loading from CSV.
            mongo_client (pymongo.MongoClient, optional): A MongoDB client to override the default global client.

        Raises:
            NetworkSecurityException: If the CSV file is not found or the mongo client is not provided.
        """
        if not data:
            try:
                self.data = pd.read_csv('Network_Data/phishingData.csv')
            except FileNotFoundError:
                raise NetworkSecurityException("File not found", sys.exc_info(), 404)
        else:
            self.data = data

        if mongo_client:
            self.mongo_client = mongo_client
        else:
            raise NetworkSecurityException("MongoDB client not provided", sys.exc_info(), 8955)

    def convert_to_json(self) -> list:
        """
        Converts the internal DataFrame to a list of JSON documents (dictionaries).

        Returns:
            list: A list of dictionaries representing rows of the DataFrame.

        Raises:
            NetworkSecurityException: If conversion fails.
        """
        try:
            return list(json.loads(self.data.reset_index(drop=True).T.to_json()).values())
        except Exception:
            raise NetworkSecurityException("Failed to convert data to JSON", sys.exc_info(), 500)

    def insert_data_to_mongo_db(self, records: list, database: str, collection: str) -> dict:
        """
        Inserts JSON records into a MongoDB collection.

        Args:
            records (list): A list of dictionaries representing documents to insert.
            database (str): Target MongoDB database name.
            collection (str): Target MongoDB collection name.

        Returns:
            dict: Metadata about the insertion operation (e.g., status, number of records).

        Raises:
            NetworkSecurityException: If insertion fails.
        """
        try:
            db = self.mongo_client[database]
            col = db[collection]
            col.insert_many(records)
            return {
                'msg': 'Data inserted successfully',
                'status': 200,
                'database': database,
                'collection': collection,
                'n_records': len(records)
            }
        except pymongo.errors.PyMongoError:
            raise NetworkSecurityException("Failed to insert data into MongoDB", sys.exc_info(), 777)


if __name__ == "__main__":
    """
    Entry point for running the module as a script.
    It extracts data from CSV, converts it to JSON, and inserts it into MongoDB.
    Logs are recorded upon successful insertion.
    """
    try:
        # Create an instance of the extractor
        extractor = NetworkDataExtractor(mongo_client=client)

        # Convert CSV data to JSON list of records
        json_data = extractor.convert_to_json()

        # Insert data into MongoDB
        result = extractor.insert_data_to_mongo_db(json_data, 'NetworkSecurity', 'phishingData')

        # Logging output
        print(result)
        logger.info("Data inserted successfully")
        logger.info(result)
        logger.info("Logging ended...")

    except NetworkSecurityException as e:
        logger.error(f"Custom Exception: {str(e)}")
        print(f"Error: {e}")

    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        print(f"Unexpected error: {e}")