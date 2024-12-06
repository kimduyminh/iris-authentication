import cv2
import numpy as np

def funHistogramEqualization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray)
    equalized_image_normalized = equalized_image
    return equalized_image_normalized
def CLAHE(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray)
    return clahe_image

def gamma_correction(image, gamma=1.2):
    # Normalize the image to [0, 1]
    image_normalized = image / 255.0
    # Apply gamma correction
    image_corrected = np.power(image_normalized, gamma)
    return np.uint8(image_corrected * 255)

def contrast_stretching(image):
    # Normalize the image
    min_val = np.min(image)
    max_val = np.max(image)
    # Apply contrast stretching
    stretched_image = ((image - min_val) / (max_val - min_val)) * 255
    return np.uint8(stretched_image)
