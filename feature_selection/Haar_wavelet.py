# import cv2
# import pywt
# import matplotlib.pyplot as plt
#
# def haar_wavelet_transform(image):
#     """
#     Apply Haar wavelet transform to an image.
#     """
#     # Perform single-level Haar wavelet decomposition
#     coeffs = pywt.dwt2(image, 'haar')
#     cA, (cH, cV, cD) = coeffs  # Approximation, Horizontal, Vertical, and Diagonal coefficients
#
#     return cA, cH, cV, cD
#
# # Load image in grayscale
# image_path = "../dataset/001/S6001S00.jpg"  # Replace with your image path
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# if image is None:
#     print("Error: Unable to load image.")
#     exit()
#
# # Apply Haar Wavelet Transform
# cA, cH, cV, cD = haar_wavelet_transform(image)
#
# # Display results
# plt.figure(figsize=(10, 8))
#
# plt.subplot(2, 2, 1)
# plt.title("Approximation Coefficients")
# plt.imshow(cA, cmap="gray")
#
# plt.subplot(2, 2, 2)
# plt.title("Horizontal Coefficients")
# plt.imshow(cH, cmap="gray")
#
# plt.subplot(2, 2, 3)
# plt.title("Vertical Coefficients")
# plt.imshow(cV, cmap="gray")
#
# plt.subplot(2, 2, 4)
# plt.title("Diagonal Coefficients")
# plt.imshow(cD, cmap="gray")
#
# plt.tight_layout()
# plt.show()

import cv2
import pywt
import os
import matplotlib.pyplot as plt

def haar_wavelet_transform(image):
    coeffs = pywt.dwt2(image, 'haar')
    cA, (cH, cV, cD) = coeffs
    return cA, cH, cV, cD

def process_and_save_images(base_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_index in range(1000):
        folder_name = f"{base_folder}/{folder_index:03d}"
        if not os.path.exists(folder_name):
            continue

        for image_name in os.listdir(folder_name):
            image_path = os.path.join(folder_name, image_name)
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue

            cA, cH, cV, cD = haar_wavelet_transform(image)
            image_base_name = os.path.splitext(image_name)[0]
            output_subfolder = os.path.join(output_folder, f"{folder_index:03d}", image_base_name)
            os.makedirs(output_subfolder, exist_ok=True)

            plt.imsave(f"{output_subfolder}cA.jpg", cA, cmap='gray')
            plt.imsave(f"{output_subfolder}cH.jpg", cH, cmap='gray')
            plt.imsave(f"{output_subfolder}cV.jpg", cV, cmap='gray')
            plt.imsave(f"{output_subfolder}cD.jpg", cD, cmap='gray')

            print(f"Processed and saved: {output_subfolder}")
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_dir, "../processed_image")
    output_folder = os.path.join(script_dir, "../feature_image/gabor_filter")
    process_and_save_images(base_folder, output_folder)


