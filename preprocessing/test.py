import cv2
import preprocessing.localization_for_authentication as lc

# Load the image
image_path = r"D:\Project\Iris\iris-authentication\ai\download.jpg"
image = cv2.imread(image_path)

# Perform localization
localized_image = lc.localization(image)
cv2.imshow("Localized Image", localized_image)
# Check if localization was successful
if localized_image is not None:
    # Display the localized iris
    cv2.imshow("Localized Iris", localized_image)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()  # Close the display window
else:
    print("Iris localization failed or no iris detected.")
