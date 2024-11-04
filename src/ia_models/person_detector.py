from functools import cache
import cv2
from ultralytics import YOLO

from src.core.settings import get_settings

SETTINGS = get_settings()

class PersonDetector:
    def __init__(self):
        self.model = YOLO(SETTINGS.yolo_human_path)

    def detect_and_crop(self, image_path: str):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Error al cargar la imagen en {image_path}.")

        results = self.model(image)
        max_area = 0
        best_crop = None

        for detection in results[0].boxes.data:
            class_detected = int(detection[5])
            if class_detected == 0:  # Clase 'person'
                x1, y1, x2, y2 = map(int, detection[:4])
                area = (x2 - x1) * (y2 - y1)

                if area > max_area:
                    max_area = area
                    best_crop = image[y1:y2, x1:x2]

        return best_crop
    
@cache
def get_person_detector() -> PersonDetector:
    return PersonDetector()