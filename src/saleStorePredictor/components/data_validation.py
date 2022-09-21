import pandas  as pd
from saleStorePredictor.utils import read_yaml
import os
from pathlib import Path
from saleStorePredictor.entity import DataValidationConfig
from saleStorePredictor.config import ConfigurationManager

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig):
        self.data_validation_config = data_validation_config
        self.train = pd.read_csv(self.data_validation_config.training_dataset)
        self.test = pd.read_csv(self.data_validation_config.test_dataset)

    def validate_schema(self):
       
        schema_path = self.data_validation_config.schema_path

        if  os.path.exists(schema_path):
                schema = read_yaml(Path(schema_path))                
                cols = schema.columns.keys()

                for c in self.train.columns:
                    if c not in cols:
                        return False

                for c in self.test.columns:
                    if c not in cols:
                        return False 

                return True               

    

    def remove_duplicates(self):
        self.train = self.train.drop_duplicates()
        self.test = self.test.drop_duplicates()
        self.train.to_csv(self.data_validation_config.training_dataset)
        self.test.to_csv(self.data_validation_config.test_dataset)
        print("succefully remove duplicated")