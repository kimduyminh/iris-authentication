import os
import shutil
import cv2
import numpy as np
import time

def localization(frame):
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 2)

        circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=10,
            maxRadius=50
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            return circles[0][0]  # x, y, r
        return None
    except Exception as e:
        print(f"Error in localization: {e}")
        return None

def start_cam_login(username: str):
    folder_path = "../captured"
    os.makedirs(folder_path, exist_ok=True)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera.")
        return

    detected_circle = None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break

        clean_frame = frame.copy()
        result = localization(frame)

        if result is not None:
            x, y, r = result
            detected_circle = (x, y, r)

            # Draw the circle and center on the live footage
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Exiting camera...")
            break
        elif key == ord('s') and detected_circle is not None:
            x, y, r = detected_circle
            crop_size = int(r * 1.5)
            x1, y1 = max(x - crop_size, 0), max(y - crop_size, 0)
            x2, y2 = min(x + crop_size, clean_frame.shape[1]), min(y + crop_size, clean_frame.shape[0])
            cropped_image = clean_frame[y1:y2, x1:x2]

            # Save 4 images in the 'captured' folder
            for i in range(1, 5):
                image_path = os.path.join(folder_path, f"{i}.jpg")
                cv2.imwrite(image_path, cropped_image)
                print(f"Iris image {i} saved as '{image_path}'.")
                time.sleep(0.5)

            print("All 4 images have been saved successfully.")
            break
    cam.release()
    cv2.destroyAllWindows()


def start_cam_create(username: str):
    print("Starting camera...")

    # Ensure the folder exists
    folder_path = os.path.join("../database_images", username)
    os.makedirs(folder_path, exist_ok=True)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Cannot open camera.")

    detected_circle = None  # Store detected circle data
    image_names = []  # List to store saved image names

    while True:
        ret, frame = cam.read()
        if not ret:
            raise Exception("Failed to grab frame.")

        # Keep a clean version of the frame for saving
        clean_frame = frame.copy()

        # Detect the iris
        result = localization(frame)

        if result is not None:
            x, y, r = result
            detected_circle = (x, y, r)

            # Draw the circle and center on the live footage
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)  # Circle
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)  # Center

        # Display the live video feed with the circle
        cv2.imshow('Camera', frame)

        # Capture keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            # Press 'q' to exit the loop manually
            print("Exiting...")
            break

        elif key == ord('s') and detected_circle is not None:
            # Save 4 images when 's' is pressed and a circle is detected
            x, y, r = detected_circle
            crop_size = int(r * 1.5)
            x1, y1 = max(x - crop_size, 0), max(y - crop_size, 0)
            x2, y2 = min(x + crop_size, clean_frame.shape[1]), min(y + crop_size, clean_frame.shape[0])
            cropped_image = clean_frame[y1:y2, x1:x2]  # Use clean_frame for saving

            # Save 4 images in the folder with names username_01.jpg, username_02.jpg, username_03.jpg, username_04.jpg
            for i in range(1, 5):
                image_name = f"{username}_{i:02}.jpg"  # Format the image name
                image_path = os.path.join(folder_path, image_name)
                cv2.imwrite(image_path, cropped_image)
                image_names.append(image_name)  # Add the image name to the list
                print(f"Image {image_name} saved at {image_path}")
                time.sleep(0.25)

            print("All 4 images have been saved successfully.")
            break

    # Release the camera and close the window
    cam.release()
    cv2.destroyAllWindows()

    # Delete the folder if no images were saved
    if not image_names:
        print(f"Deleting folder {folder_path} because no images were saved.")
        shutil.rmtree(folder_path, ignore_errors=True)

    return image_names