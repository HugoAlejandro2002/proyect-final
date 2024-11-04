import albumentations as A
import cv2

class ImageResizer:
    def __init__(self, max_size: int = 640, border_value=(0, 0, 0)):
        self.transform = A.Compose([
            A.LongestMaxSize(max_size=max_size),
            A.PadIfNeeded(min_height=max_size, min_width=max_size, border_mode=cv2.BORDER_CONSTANT, value=border_value)
        ])

    def resize(self, image):
        return self.transform(image=image)['image']