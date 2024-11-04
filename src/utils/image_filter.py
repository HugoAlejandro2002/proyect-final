import cv2

class ImageFilter:
    def __init__(self, blur_kernel=(11, 11), morph_kernel_size=(5, 5)):
        self.blur_kernel = blur_kernel
        self.morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_kernel_size)

    def apply_filters(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        threshold = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.morph_kernel, iterations=2)
        return closed