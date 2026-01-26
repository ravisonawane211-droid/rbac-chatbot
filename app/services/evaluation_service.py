import requests
from app.config.config import get_settings
from app.schemas.evaluation_request import EvaluationRequest
from app.utils.logger import get_logger
import time
import random


settings = get_settings()

class EvaluationService:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.evaluation_service_url = settings.evaluation_service_url
        self.logger.info(f"Initialised EvaluationService to connect : {self.evaluation_service_url}")

    def send_for_evaluation(self, evaluation_request: EvaluationRequest):
        self.logger.info(f"Submitted request to evaluation service with payload: {evaluation_request}")
        max_retry_count = 3
        for attempt in range(1,max_retry_count+1):
            try:
                requests.post(self.evaluation_service_url, json=evaluation_request.model_dump())
            except Exception as e:
                self.logger.error(f"error occurred while calling evaluation servie {self.evaluation_service_url} , error :{e}")

            if attempt < max_retry_count:
                sleep_time = (2 ** attempt) * 0.1
                sleep_time += random.uniform(0, 0.1)
                time.sleep(sleep_time)
        return
