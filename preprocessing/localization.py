## For whole iris detection

import cv2
import numpy as np

def localization(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 2)
        #gray_blurred = cv2.bilateralFilter(gray_blurred, d=9, sigmaColor=75, sigmaSpace=75)
        circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=30,
            param1=60,
            param2=30,
            minRadius=40,
            maxRadius=100
        )
        if circles is not None:
            circles = np.uint16(np.around(circles))
            x = circles[0][0][0]
            y = circles[0][0][1]
            r = circles[0][0][2]
            zoom_out_factor = 1
            crop_size = int(r * zoom_out_factor * 2)
            x1, y1 = max(x - crop_size, 0), max(y - crop_size, 0)
            x2, y2 = min(x + crop_size, image.shape[1]), min(y + crop_size, image.shape[0])

            cropped_image = image[y1:y2, x1:x2]
            resized_image = cv2.resize(cropped_image, (224, 224))
            return resized_image
        else:
            print("No circles detected.")
            return None
    except Exception as e:
        print(e)
