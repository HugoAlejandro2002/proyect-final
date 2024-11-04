from functools import cache
from ultralytics import YOLO
import numpy as np

from src.core.settings import get_settings

SETTINGS = get_settings()

class YOLOBodyClassifier:
    def __init__(self):
        self.model = YOLO(SETTINGS.yolo_body_classifier_path)
        self.classes = ["fat", "fit", "slim"]

    def classify(self, image: np.ndarray):
        results = self.model(image)
        if results and results[0].probs:
            top5_indices = results[0].probs.top5
            top5_confidences = results[0].probs.top5conf
            class_probabilities = {
                self.classes[i]: float(top5_confidences[idx]) for idx, i in enumerate(top5_indices)
            }
            return class_probabilities
        else:
            raise ValueError("No se pudo obtener resultados de clasificación.")
    
@cache
def get_yolo_body_classifier() -> YOLOBodyClassifier:
    return YOLOBodyClassifier()