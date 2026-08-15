import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from app.auth.jwt_bearer import JWTBearer
from app.config.config import get_settings
from app.schemas.dashboard_response import DashboardResponse
from app.schemas.save_config_request import SaveConfigRequest
from app.schemas.save_config_response import SaveConfigResponse
from app.services.dashboard_service import DashboardService
from app.services.db_execute_service import DatabaseExecuteService
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
settings = get_settings()
auth_scheme = JWTBearer()


@router.get("/metrics/{app_name}", response_model=DashboardResponse)
def get_dashboard_metrics(app_name: str, user_info: dict = Depends(auth_scheme)) -> DashboardResponse:
    """Retrieve dashboard metrics for the specified application."""
    logger.info(f"Fetching dashboard metrics for app: {app_name} by {user_info['user_id']}")

    if not app_name:
        raise HTTPException(status_code=400, detail="Application name is required")

    dashboard_service = DashboardService(app_name=app_name)
    metrics, threshold = dashboard_service.get_metrics()

    dashboard_response = DashboardResponse(
        metrics=metrics,
        threshold=threshold,
        status="success",
    )
    logger.info(f"Dashboard {len(metrics)} metrics for app {app_name} retrieved successfully.")
    return dashboard_response


@router.post(
    path="/config",
    summary="Saves an app configuration",
    description="Saves an app configuration of the application",
)
def save_app_config(
    save_config_request: SaveConfigRequest,
    user_info: dict = Depends(auth_scheme),
) -> SaveConfigResponse:
    """Save application configuration details."""
    logger.info(
        f"Request received for saving app config with request: {save_config_request} by {user_info['user_id']}"
    )

    if not save_config_request.enable_eval or not save_config_request.eval_type:
        raise HTTPException(status_code=400, detail="Enable Evaluation and evaluation Type are required")

    database_execute_service = DatabaseExecuteService(db_config=settings.database_url)
    user_df = pd.DataFrame([
        {
            "enable_eval": save_config_request.enable_eval,
            "eval_type": save_config_request.eval_type,
        }
    ])
    database_execute_service.save_dataframe_to_table(df=user_df, table_name="app_config")

    logger.info("App config saved successfully")

    return SaveConfigResponse(
        message="App Config saved successfully",
        status="success",
    )