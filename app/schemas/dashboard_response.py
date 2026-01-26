from pydantic import BaseModel
from app.schemas.eval_metric import EvalMetric
from typing import List

class DashboardResponse(BaseModel):
    """
    DashboardResponse is a Pydantic model that represents the response structure 
    for dashboard metrics in the system.
    Attributes:
        metrics (List[EvalMetric]): A list of evaluation metrics to be displayed on the dashboard.
    """

    metrics: List[EvalMetric]
    threshold: dict
    status:str