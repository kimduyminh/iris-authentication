# import cv2
# import matplotlib.pyplot as plt
#
# def laplacian_of_gaussian(image, ksize=5, sigma=1.0):
#     """
#     Apply the Laplacian of Gaussian filter to detect edges.
#     Parameters:
#     - ksize: Kernel size for Gaussian blur.
#     - sigma: Standard deviation of Gaussian blur.
#     """
#     # Gaussian Blur
#     blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
#     # Apply Laplacian
#     log_image = cv2.Laplacian(blurred, cv2.CV_64F)
#     return log_image
#
# # Load grayscale image
# image_path = "../dataset/001/S6001S00.jpg"  # Replace with your image path
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# if image is None:
#     print("Error: Unable to load image.")
#     exit()
#
# # Apply LoG Filter
# log_result = laplacian_of_gaussian(image, ksize=5, sigma=1.0)
#
# # Display results
# plt.figure(figsize=(8, 4))
#
# plt.subplot(1, 2, 1)
# plt.title("Original Image")
# plt.imshow(image, cmap="gray")
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.title("Laplacian of Gaussian")
# plt.imshow(log_result, cmap="gray")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

import cv2
import os
import matplotlib.pyplot as plt

def laplacian_of_gaussian(image, ksize=5, sigma=1.0):
    blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
    log_image = cv2.Laplacian(blurred, cv2.CV_64F)
    return log_image

def process_and_save_log_images(base_folder, output_folder, ksize=5, sigma=1.0):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_index in range(1000):
        folder_name = f"{base_folder}/{folder_index:03d}"
        if not os.path.exists(folder_name):
            continue

        output_subfolder = os.path.join(output_folder, f"{folder_index:03d}")
        os.makedirs(output_subfolder, exist_ok=True)

        for image_name in os.listdir(folder_name):
            image_path = os.path.join(folder_name, image_name)
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue

            log_result = laplacian_of_gaussian(image, ksize, sigma)

            output_image_name = os.path.splitext(image_name)[0]+".jpg"
            output_image_path = os.path.join(output_subfolder, output_image_name)
            cv2.imwrite(output_image_path, log_result)

            print(f"Processed and saved: {output_image_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_dir, "../processed_image")
    output_folder = os.path.join(script_dir, "../feature_image/gabor_filter")
    process_and_save_log_images(base_folder, output_folder, ksize=5, sigma=1.0)

