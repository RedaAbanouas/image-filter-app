import base64

import cv2
import numpy as np


FILTERS = {"gaussian": "Gaussian", "median": "Median", "bilateral": "Bilateral"}


def _png_data(image):
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode a processed image.")
    return "data:image/png;base64," + base64.b64encode(encoded).decode("ascii")


def process_image(image_bytes, filter_name, kernel_size, low_threshold, high_threshold):
    """Run grayscale → denoise → Sobel gradient → Canny and return displayable stages."""
    array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The uploaded file is not a readable image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if filter_name == "gaussian":
        filtered = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    elif filter_name == "median":
        filtered = cv2.medianBlur(gray, kernel_size)
    elif filter_name == "bilateral":
        filtered = cv2.bilateralFilter(gray, kernel_size, 75, 75)
    else:
        raise ValueError("Choose Gaussian, Median, or Bilateral filtering.")

    grad_x = cv2.Sobel(filtered, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(filtered, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(grad_x, grad_y)
    gradient = cv2.convertScaleAbs(magnitude)
    edges = cv2.Canny(filtered, low_threshold, high_threshold)
    return {
        "original": _png_data(image),
        "grayscale": _png_data(gray),
        "filtered": _png_data(filtered),
        "gradient": _png_data(gradient),
        "edges": _png_data(edges),
    }
