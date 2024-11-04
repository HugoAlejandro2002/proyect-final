from functools import cache
import joblib
import pandas as pd
import numpy as np
import cv2
from ultralytics import YOLO

from src.utils.image_filter import ImageFilter
from src.core.settings import get_settings

SETTINGS = get_settings()

class ContourFeatureExtractor:
    def __init__(self):
        self.yolo_model = YOLO(SETTINGS.yolo_pose_path)
        self.rf_model = joblib.load(SETTINGS.rf_classifier_path)
        self.image_filter = ImageFilter()
        self.feature_columns = self.rf_model.feature_names_in_
        self.classes = ["fat", "fit", "slim"]

    def calculate_distance_to_contour(self, point, contour):
        point = point.cpu().numpy() if hasattr(point, 'cpu') else np.array(point)
        contour_points = contour.reshape(-1, 2)
        dists = np.sqrt((contour_points[:, 0] - point[0]) ** 2 + (contour_points[:, 1] - point[1]) ** 2)
        return dists.min()

    def extract_features(self, image):
        filtered_image = self.image_filter.apply_filters(image)

        contours, _ = cv2.findContours(filtered_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("No se encontró ningún contorno.")

        largest_contour = max(contours, key=cv2.contourArea)
        body_area = float(cv2.contourArea(largest_contour))
        x, y, w, h = cv2.boundingRect(largest_contour)
        bounding_box_area = float(w * h)
        aspect_ratio = float(w / h)
        contour_box_ratio = body_area / bounding_box_area

        results = self.yolo_model(image)
        keypoints = results[0].keypoints.xy[0]
        keypoints = keypoints.cpu().numpy() if hasattr(keypoints, 'cpu') else np.array(keypoints)

        distances = {
            'left_shoulder_dist': self.calculate_distance_to_contour(keypoints[5], largest_contour),
            'right_shoulder_dist': self.calculate_distance_to_contour(keypoints[6], largest_contour),
            'left_hip_dist': self.calculate_distance_to_contour(keypoints[11], largest_contour),
            'right_hip_dist': self.calculate_distance_to_contour(keypoints[12], largest_contour),
            'left_knee_dist': self.calculate_distance_to_contour(keypoints[13], largest_contour),
            'right_knee_dist': self.calculate_distance_to_contour(keypoints[14], largest_contour)
        }

        shoulder_symmetry = abs(distances['left_shoulder_dist'] - distances['right_shoulder_dist'])
        hip_symmetry = abs(distances['left_hip_dist'] - distances['right_hip_dist'])
        knee_symmetry = abs(distances['left_knee_dist'] - distances['right_knee_dist'])

        features = {
            'body_area': body_area,
            'bounding_box_area': bounding_box_area,
            'aspect_ratio': aspect_ratio,
            'contour_box_ratio': contour_box_ratio,
            'shoulder_width': float(abs(keypoints[6][0] - keypoints[5][0])),
            'waist_width': float(abs(keypoints[12][0] - keypoints[11][0])),
            'leg_length': float((abs(keypoints[13][1] - keypoints[11][1]) + abs(keypoints[14][1] - keypoints[12][1])) / 2),
            'shoulder_symmetry': shoulder_symmetry,
            'hip_symmetry': hip_symmetry,
            'knee_symmetry': knee_symmetry,
            **distances
        }

        # Crear el DataFrame y reordenar las columnas para que coincidan con el entrenamiento
        features_df = pd.DataFrame([features])
        features_df = features_df.reindex(columns=self.feature_columns)

        return features_df

    def classify(self, image):
        features_df = self.extract_features(image)
        prediction_proba = self.rf_model.predict_proba(features_df)[0]
        class_probabilities = {self.classes[i]: prob for i, prob in enumerate(prediction_proba)}
        return class_probabilities

    
@cache
def get_contour_feature_extractor() -> ContourFeatureExtractor:
    return ContourFeatureExtractor()