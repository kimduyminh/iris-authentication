import cv2
import numpy as np
import os
import pywt
import matplotlib.pyplot as plt

#Gabor
def create_gabor_filter(ksize=31, sigma=4.0, theta=0, lambd=10.0, gamma=0.5, psi=0):
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
    return kernel

def apply_gabor_filter(image, kernel):
    filtered_image = cv2.filter2D(image, cv2.CV_8UC3, kernel)
    return filtered_image

def process_and_save_imagesGabor(base_folder, output_folder):
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


#Haar_wavelet
def haar_wavelet_transform(image):
    coeffs = pywt.dwt2(image, 'haar')
    cA, (cH, cV, cD) = coeffs
    return cA, cH, cV, cD

def process_and_save_imagesHaar(base_folder, output_folder):
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

            plt.imsave(f"{output_subfolder}/cA.jpg", cA, cmap='gray')
            plt.imsave(f"{output_subfolder}/cH.jpg", cH, cmap='gray')
            plt.imsave(f"{output_subfolder}/cV.jpg", cV, cmap='gray')
            plt.imsave(f"{output_subfolder}/cD.jpg", cD, cmap='gray')

            print(f"Processed and saved: {output_subfolder}")

#Laplacian

def laplacian_of_gaussian(image, ksize=5, sigma=1.0):
    blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
    log_image = cv2.Laplacian(blurred, cv2.CV_64F)
    return log_image

def process_and_save_log_imagesLapla(base_folder, output_folder, ksize=5, sigma=1.0):
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

            output_image_name = os.path.splitext(image_name)[0] + "_LoG.jpg"
            output_image_path = os.path.join(output_subfolder, output_image_name)
            cv2.imwrite(output_image_path, log_result)

            print(f"Processed and saved: {output_image_path}")

#Log_Gabor

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

            output_image_name = os.path.splitext(image_name)[0] + "_LogGabor.jpg"
            output_image_path = os.path.join(output_subfolder, output_image_name)
            cv2.imwrite(output_image_path, (filtered_image * 255).astype(np.uint8))

            print(f"Processed and saved: {output_image_path}")
