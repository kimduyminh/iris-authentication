import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('S6000S00cropped&resized.jpg', cv2.IMREAD_COLOR)


def funHistogramEqualization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray)
    equalized_image_normalized = equalized_image / 255.0


    plt.subplot(1, 3, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original Grayscale")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(equalized_image_normalized, cmap='gray')
    plt.title("Histogram Equalization")
    plt.axis('off')


def CLAHEandHistogram(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray)

    plt.subplot(1, 3, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original Grayscale")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(clahe_image, cmap='gray')
    plt.title("CLAHE Enhanced")
    plt.axis('off')


    equalized_image = cv2.equalizeHist(gray)
    equalized_image_normalized = equalized_image / 255.0

    plt.subplot(1, 3, 3)
    plt.imshow(equalized_image_normalized, cmap='gray')
    plt.title("Histogram Equalization")
    plt.axis('off')

    plt.show()


CLAHEandHistogram(image)
