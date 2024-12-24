# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
#
#
# def log_gabor_filter(shape, wavelength, sigma_on_f):
#     """
#     Generate a Log-Gabor filter in the frequency domain.
#
#     Parameters:
#     - shape: Tuple of (rows, cols) for the filter size.
#     - wavelength: Central wavelength of the filter.
#     - sigma_on_f: Bandwidth parameter (relative standard deviation in frequency domain).
#
#     Returns:
#     - Log-Gabor filter in frequency domain.
#     """
#     rows, cols = shape
#     x = np.linspace(-0.5, 0.5, cols)
#     y = np.linspace(-0.5, 0.5, rows)
#     X, Y = np.meshgrid(x, y)
#
#     # Radius and log frequency calculation
#     radius = np.sqrt(X ** 2 + Y ** 2)
#     radius[rows // 2, cols // 2] = 1  # Avoid division by zero at the center
#     log_radius = np.log(radius / wavelength)
#
#     # Create Log-Gabor filter
#     log_gabor = np.exp(-(log_radius ** 2) / (2 * np.log(sigma_on_f) ** 2))
#     log_gabor[radius > 0.5] = 0  # Remove high frequencies
#     return log_gabor
#
#
# def apply_log_gabor(image, log_gabor_filter):
#     """
#     Apply the Log-Gabor filter to an image using the frequency domain.
#
#     Parameters:
#     - image: Input grayscale image.
#     - log_gabor_filter: Log-Gabor filter in the frequency domain.
#
#     Returns:
#     - Filtered image in spatial domain.
#     """
#     # FFT of the image
#     fft_image = np.fft.fftshift(np.fft.fft2(image))
#     filtered_fft = fft_image * log_gabor_filter
#
#     # Inverse FFT to get the result
#     filtered_image = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))
#     return filtered_image
#
#
# # Load grayscale image
# image_path = "../dataset/001/S6001S00.jpg"  # Replace with your image path
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# if image is None:
#     print("Error: Unable to load image.")
#     exit()
#
# # Parameters for Log-Gabor filter
# wavelength = 10  # Central wavelength
# sigma_on_f = 0.56  # Bandwidth parameter
#
# # Create Log-Gabor filter
# log_gabor = log_gabor_filter(image.shape, wavelength, sigma_on_f)
#
# # Apply Log-Gabor filter
# filtered_image = apply_log_gabor(image, log_gabor)
#
# # Display results
# plt.figure(figsize=(12, 4))
#
# # Original Image
# plt.subplot(1, 3, 1)
# plt.title("Original Image")
# plt.imshow(image, cmap="gray")
# plt.axis("off")
#
# # Log-Gabor Filter
# plt.subplot(1, 3, 2)
# plt.title("Log-Gabor Filter")
# plt.imshow(log_gabor, cmap="gray")
# plt.axis("off")
#
# # Filtered Image
# plt.subplot(1, 3, 3)
# plt.title("Filtered Image")
# plt.imshow(filtered_image, cmap="gray")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt


def log_gabor_filter(shape, wavelength, sigma_on_f):
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols)
    y = np.linspace(-0.5, 0.5, rows)
    X, Y = np.meshgrid(x, y)
    radius = np.sqrt(X ** 2 + Y ** 2)
    radius[rows // 2, cols // 2] = 1
    log_radius = np.log(radius / wavelength)
    log_gabor = np.exp(-(log_radius ** 2) / (2 * np.log(sigma_on_f) ** 2))
    log_gabor[radius > 0.5] = 0
    return log_gabor


def apply_log_gabor(image, log_gabor_filter):
    fft_image = np.fft.fftshift(np.fft.fft2(image))
    filtered_fft = fft_image * log_gabor_filter
    filtered_image = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))
    return filtered_image


def process_and_save_log_gabor(base_folder, output_folder, wavelength=10, sigma_on_f=0.56):
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

            log_gabor = log_gabor_filter(image.shape, wavelength, sigma_on_f)
            filtered_image = apply_log_gabor(image, log_gabor)

            output_image_name = os.path.splitext(image_name)[0]+".jpg"
            output_image_path = os.path.join(output_subfolder, output_image_name)
            cv2.imwrite(output_image_path, (filtered_image * 255).astype(np.uint8))

            print(f"Processed and saved: {output_image_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_dir, "../processed_image")
    output_folder = os.path.join(script_dir, "../feature_image/gabor_filter")
    process_and_save_log_gabor(base_folder, output_folder, wavelength=10, sigma_on_f=0.56)
