from saleStorePredictor.config import ConfigurationManager
from saleStorePredictor.components import ModelEvaluationAndPusher, data_ingestion
from saleStorePredictor import logger


STAGE_NAME = "Model evaluation stage"

def main():
    config = ConfigurationManager()
    model_evaluation_config = config.get_model_evaluation_config()
    data_ingestion_artifact = config.get_data_ingestion_artifact()
    model_trainer_artifact = config.get_model_trainer_artifact()
    model_pusher_config = config.get_pusher_config()

    model_traner = ModelEvaluationAndPusher(
        model_evaluation_config=model_evaluation_config,
        data_ingestion_artifact=data_ingestion_artifact,
        model_trainer_artifact=model_trainer_artifact,
        model_pusher_config=model_pusher_config
    )
    model_traner.initiate_model_evaluation()



if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e