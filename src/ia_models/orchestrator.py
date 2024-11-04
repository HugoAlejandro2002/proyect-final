from functools import cache

from src.ia_models.contour_feature_extractor import get_contour_feature_extractor
from src.ia_models.person_detector import get_person_detector
from src.ia_models.yolo_body_classifier import get_yolo_body_classifier
from src.utils.image_resizer import ImageResizer

class Orchestrator:
    def __init__(self ):
        self.detector = get_person_detector()
        self.classifier = get_yolo_body_classifier()
        self.feature_extractor = get_contour_feature_extractor()
        self.resizer = ImageResizer()

    def process_image(self, image_path: str):
        try:
            cropped_image = self.detector.detect_and_crop(image_path)
            if cropped_image is None:
                raise ValueError("No se detectó ninguna persona en la imagen.")

            resized_image = self.resizer.resize(cropped_image)

            class_probabilities_yolo = self.classifier.classify(resized_image)

            class_probabilities_rf = self.feature_extractor.classify(resized_image)

            combined_probabilities = {
                cls: class_probabilities_yolo.get(cls, 0) + class_probabilities_rf.get(cls, 0)
                for cls in set(class_probabilities_yolo) | set(class_probabilities_rf)
            }

            predicted_class = max(combined_probabilities, key=combined_probabilities.get)

            result = {
                "combined_probabilities": combined_probabilities,
                "predicted_class": predicted_class
            }

            return result

        except ValueError as e:
            print(f"Error durante el procesamiento: {e}")
            return None
        
@cache
def get_orquestator() -> Orchestrator:
    return Orchestrator()