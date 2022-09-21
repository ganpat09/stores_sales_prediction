from saleStorePredictor.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from saleStorePredictor.utils import read_yaml, create_directories
from saleStorePredictor.entity import DataIngestionConfig
from saleStorePredictor.entity import DataValidationConfig

from pathlib import Path
import os

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            ingested_train_dir=config.ingested_train_dir,
            ingested_test_dir=config.ingested_test_dir 
        )

        return data_ingestion_config


    def get_data_validation_config(self) -> DataValidationConfig:
    
        config = self.config.data_ingestion
        

        training_dataset = os.path.join(config.ingested_train_dir,config.train_file_name)
        testing_dataset = os.path.join(config.ingested_test_dir,config.test_file_name)
        dataValidationConfig = DataValidationConfig(
            training_dataset=training_dataset,
            test_dataset=testing_dataset,
            schema_path=SCHEMA_FILE_PATH
            )
        
        return  dataValidationConfig  


     


        

        