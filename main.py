import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


if __name__ == "__main__":
    try:
        logging.info("Starting Network Security Training Pipeline")

        training_pipeline_config = TrainingPipelineConfig()

        # Data Ingestion
        data_ingestion = DataIngestion(
            DataIngestionConfig(training_pipeline_config)
        )
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")

        # Data Validation
        data_validation = DataValidation(
            data_ingestion_artifact,
            DataValidationConfig(training_pipeline_config)
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")

        # Data Transformation
        data_transformation = DataTransformation(
            data_validation_artifact,
            DataTransformationConfig(training_pipeline_config)
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")

        # Model Trainer
        model_trainer = ModelTrainer(
            model_trainer_config=ModelTrainerConfig(training_pipeline_config),
            data_transformation_artifact=data_transformation_artifact
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
