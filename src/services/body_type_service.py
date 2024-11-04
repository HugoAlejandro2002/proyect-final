import os
import cv2
import numpy as np
import tempfile
from pathlib import Path

from src.ia_models.orchestrator import Orchestrator

class BodyTypeService:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def process_image_and_classify(self, image_bytes: bytes) -> dict:

        image_np = np.frombuffer(image_bytes, np.uint8)
        image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if image_cv is None:
            raise ValueError("Invalid image file.")

        temp_image_path = self.temp_dir / f"temp_image_{next(tempfile._get_candidate_names())}.jpg"
        cv2.imwrite(str(temp_image_path), image_cv)

        result  = self.orchestrator.process_image(str(temp_image_path))

        os.remove(temp_image_path)


        return result 
