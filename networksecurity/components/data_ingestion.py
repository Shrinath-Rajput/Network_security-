import os
import sys
import numpy as np
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Fetch data from MongoDB Atlas and return as DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            ca = certifi.where()

            mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=ca,
                serverSelectionTimeoutMS=30000
            )

            collection = mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            logging.info("MongoDB data loaded into DataFrame successfully")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """
        Save raw data into feature store
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

            dataframe.to_csv(feature_store_path, index=False, header=True)

            logging.info("Data exported to feature store")
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split dataset into train and test
        """
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            os.makedirs(
                os.path.dirname(self.data_ingestion_config.training_file_path),
                exist_ok=True
            )

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info("Train-test split completed successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """
        Complete data ingestion pipeline
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
