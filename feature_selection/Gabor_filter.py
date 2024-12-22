# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# def create_gabor_filter(ksize=31, sigma=4.0, theta=0, lambd=10.0, gamma=0.5, psi=0):
#     """
#     Create and return a Gabor filter kernel.
#     Parameters:
#     - ksize: Size of the filter kernel (must be odd).
#     - sigma: Standard deviation of the Gaussian envelope.
#     - theta: Orientation of the filter in radians.
#     - lambd: Wavelength of the sinusoidal factor.
#     - gamma: Spatial aspect ratio.
#     - psi: Phase offset.
#     """
#     kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
#     return kernel
#
# def apply_gabor_filter(image, kernel):
#     """
#     Apply a Gabor filter to an input image.
#     """
#     filtered_image = cv2.filter2D(image, cv2.CV_8UC3, kernel)
#     return filtered_image
#
# def display_results(original, filtered, kernel):
#     """
#     Display the original image, the Gabor kernel, and the filtered result.
#     """
#     plt.figure(figsize=(12, 4))
#
#     # Display original image
#     plt.subplot(1, 3, 1)
#     plt.title("Original Image")
#     plt.imshow(original, cmap="gray")
#     plt.axis("off")
#
#     # Display Gabor kernel
#     plt.subplot(1, 3, 2)
#     plt.title("Gabor Kernel")
#     plt.imshow(kernel, cmap="gray")
#     plt.axis("off")
#
#     # Display filtered image
#     plt.subplot(1, 3, 3)
#     plt.title("Filtered Image")
#     plt.imshow(filtered, cmap="gray")
#     plt.axis("off")
#
#     plt.tight_layout()
#     plt.show()
#
# # Load and preprocess the image
# image_path = "../dataset/001/S6001S00.jpg"  # Replace with your image path
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# if image is None:
#     print("Error: Unable to load image.")
#     exit()
#
# # Create Gabor filter kernel
# gabor_kernel = create_gabor_filter(ksize=31, sigma=5, theta=np.pi / 4, lambd=10, gamma=0.5, psi=0)
#
# # Apply Gabor filter to the image
# filtered_image = apply_gabor_filter(image, gabor_kernel)
#
# # Display the results
# display_results(image, filtered_image, gabor_kernel)





import cv2
import numpy as np
import os

def create_gabor_filter(ksize=31, sigma=4.0, theta=0, lambd=10.0, gamma=0.5, psi=0):
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
    return kernel

def apply_gabor_filter(image, kernel):
    filtered_image = cv2.filter2D(image, cv2.CV_8UC3, kernel)
    return filtered_image

def process_and_save_images(base_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    gabor_kernel = create_gabor_filter(ksize=31, sigma=5, theta=np.pi / 4, lambd=10, gamma=0.5, psi=0)

    for folder_index in range(0, 1000):
        folder_name = f"{base_folder}/{folder_index:03d}"
        if not os.path.exists(folder_name):
            continue

        output_subfolder = f"{output_folder}/{folder_index:03d}"
        os.makedirs(output_subfolder, exist_ok=True)

        for image_name in os.listdir(folder_name):
            image_path = os.path.join(folder_name, image_name)
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue

            filtered_image = apply_gabor_filter(image, gabor_kernel)
            output_image_path = os.path.join(output_subfolder, image_name)
            cv2.imwrite(output_image_path, filtered_image)
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_dir, "../processed_image")
    output_folder = os.path.join(script_dir, "../feature_image/gabor_filter")
    process_and_save_images(base_folder, output_folder)

