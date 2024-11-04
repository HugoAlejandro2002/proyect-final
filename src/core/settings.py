from functools import cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Routine Generator API"
    version: str = "1.0.0"
    debug: bool = True
    openai_api_key: str
    yolo_body_classifier_path: str = "model_artifacts/best.pt"
    rf_classifier_path: str = "model_artifacts/body_type_classifier.pkl"
    yolo_pose_path: str = "model_artifacts/yolo11n-pose.pt"
    yolo_human_path: str = "model_artifacts/yolov8n.pt"


    model_config = SettingsConfigDict(env_file=".env")

@cache
def get_settings() -> Settings:
    return Settings()