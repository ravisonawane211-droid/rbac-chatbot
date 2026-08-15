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

    def send_for_evaluation(self, evaluation_request: EvaluationRequest) -> requests.Response:
        """Post the given request to the evaluation service, retrying on failure.

        Raises RequestException if all attempts fail.
        """
        self.logger.info(
            "sending evaluation request %s -> %s",
            evaluation_request,
            self.evaluation_service_url,
        )
        max_retry = 3
        for attempt in range(1, max_retry + 1):
            try:
                resp = requests.post(
                    self.evaluation_service_url,
                    json=evaluation_request.model_dump(),
                    timeout=120,
                )
                resp.raise_for_status()
            except requests.RequestException as exc:
                self.logger.warning(
                    "attempt %d/%d failed: %s",
                    attempt,
                    max_retry,
                    exc,
                )
                if attempt == max_retry:
                    # re‑raise or return None/False depending on your design
                    raise
            else:
                self.logger.info("evaluation service accepted request (%s)", resp.status_code)
                return resp

            # back‑off before retrying
            sleep_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
            time.sleep(sleep_time)
