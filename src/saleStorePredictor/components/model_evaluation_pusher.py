from saleStorePredictor import logging
from saleStorePredictor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
from saleStorePredictor.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from saleStorePredictor.constants import *
import numpy as np
import pandas as pd
import os
import sys
from saleStorePredictor.utils import save_json,load_json, read_yaml,load_bin,write_yaml
from saleStorePredictor.entity.model_factory import evaluate_regression_model
import shutil





class ModelEvaluationAndPusher:

    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig
                 ):
        try:
          #  logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_pusher_config = model_pusher_config
           
        except Exception as e:
            raise  e

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
               # logging.info(f"{'>>' * 30}Model evaluation file not found.<<<<<<<")
                write_yaml(model_evaluation_file_path)
                return model

         #   logging.info(f"{'>>' * 30}Model Evaluation logging started  {model_evaluation_file_path}.<<<<<<<< <<")    
            model_eval_file_content = read_yaml(Path(model_evaluation_file_path))

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model

            logging.info(f"{model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY]}")    

            model = load_bin(Path(model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY]))


            return model
        except Exception as e:
            raise  e


    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = Path(self.model_evaluation_config.model_evaluation_file_path)
            model_eval_content = read_yaml(eval_file_path).to_dict()
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous eval result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: str(model_evaluation_artifact.evaluated_model_path),
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_content}")
            logging.info(f"type eval result:{(model_eval_content)}")

            write_yaml(eval_file_path, model_eval_content)

        except Exception as e:
            raise e


    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = Path(self.model_trainer_artifact.trained_model_file_path)
            logging.info(f"Installing model evaluation artifacts {trained_model_file_path}")
            trained_model_object = load_bin(trained_model_file_path)

            train_file_path = Path(self.data_ingestion_artifact.train_file_path)
            test_file_path =   Path(self.data_ingestion_artifact.test_file_path)

            schema_file_path =  SCHEMA_FILE_PATH


            train_dataframe = pd.read_csv(train_file_path)
            test_dataframe = pd.read_csv(test_file_path)

           
                                                          
            schema_content = read_yaml(schema_file_path)
            target_column_name = schema_content.target_column

           # logging.info(f"{target_column_name}")

            # target_column
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")

            # dropping target column from the dataframe
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")

            model = self.get_best_model()

            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

                shutil.copy(model_evaluation_artifact.evaluated_model_path,self.model_pusher_config.model_pusher_file_path)
                return model_evaluation_artifact

            model_list = [model, trained_model_object]

            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                               X_train=train_dataframe,
                                                               y_train=train_target_arr,
                                                               X_test=test_dataframe,
                                                               y_test=test_target_arr,
                                                               base_accuracy=self.model_trainer_artifact.model_accuracy,
                                                               )
            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")




            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path
                                                   )
                logging.info(response)

                shutil.copy(response.evaluated_model_path,self.model_pusher_config.model_pusher_file_path)


                return response



            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False)

            shutil.copy(model_evaluation_artifact.evaluated_model_path,self.model_pusher_config.model_pusher_file_path)
                                                        
            return model_evaluation_artifact
        except Exception as e:
            raise e

    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")