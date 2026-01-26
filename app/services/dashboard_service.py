from app.schemas.eval_metric import EvalMetric
import requests
from app.config.config import get_settings
from app.utils.logger import get_logger
from app.schemas.app_config import AppConfig
from app.services.db_service import DatabaseService
from functools import lru_cache

logger = get_logger(__name__)
settings = get_settings()

@lru_cache
def get_app_config() -> AppConfig:
        """Return application configuration"""
        logger.info("Fetching app configuration from app_config table")
        
        db_service = DatabaseService(db_path="./resources/data/db/rbac_chatbot.db")

        query = "SELECT enable_eval,eval_type FROM app_config;"
        app_config = None
        try:
            with db_service.get_db() as conn:
                row = conn.execute(query).fetchone()
                enable_eval = row["enable_eval"]
                eval_type = row["eval_type"]
                app_config = AppConfig(enable_eval=enable_eval,
                                    eval_type=eval_type)
        except Exception as e:
            logger.error(f"error while retricing app config from app_config table : {e}")
            raise e
        return app_config


class DashboardService:

    def __init__(self,app_name:str):
        self.eval_api_url = settings.evaluation_service_url
        self.app_name = app_name
        logger.info(f"DashboardService initialized with eval_api_url: {self.eval_api_url}")

    
    def get_metrics(self) -> list[EvalMetric]:
        """Fetch dashboard metrics for the specified application.

        Returns:
            List of EvalMetric objects.
        """
        try:
            response = requests.get(f"{self.eval_api_url}/metrics/{self.app_name}")
            response.raise_for_status()
            threshold = response.json().get("threashold", {})
            metric_response = response.json().get("eval_metrics", [])
            metrics = []
            for metric in metric_response:
                logger.debug(f"Metric fetched: {metric}")
                status = "red" if metric.get("metric_value") < threshold.get(metric.get("metric_name"), 0) else "green"
                eval_metric = EvalMetric(
                    project_id=metric.get("project_id"),
                    environment=metric.get("environment"),
                    question=metric.get("question"),
                    answer=metric.get("answer"),
                    metric_name=metric.get("metric_name"),
                    metric_value=metric.get("metric_value"),
                    eval_status=status
                )
                metrics.append(eval_metric)
                
            logger.info(f"Fetched {len(metrics)} metrics for app: {self.app_name}")
            return metrics,threshold
        except requests.RequestException as e:
            logger.error(f"Error fetching metrics for app {self.app_name}: {e}")
            raise e