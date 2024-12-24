import cv2
import numpy as np

def localization(frame):
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Enhance contrast
        gray = cv2.equalizeHist(gray)

        # Apply Gaussian blur
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 2)

        # Detect circles using HoughCircles
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
            # Convert to integers
            circles = np.uint16(np.around(circles))
            # Return the first detected circle
            return circles[0][0]  # x, y, r
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def start_cam():
    print("CAM STARTED")
# Open the default camera
    cam = cv2.VideoCapture(0)

    detected_circle = None  # Store detected circle data

    while True:
        ret, frame = cam.read()

        if not ret:
            print("Failed to grab frame.")
            break

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
            # Save the image when 's' is pressed and a circle is detected
            x, y, r = detected_circle
            crop_size = int(r * 1.5)
            x1, y1 = max(x - crop_size, 0), max(y - crop_size, 0)
            x2, y2 = min(x + crop_size, clean_frame.shape[1]), min(y + crop_size, clean_frame.shape[0])
            cropped_image = clean_frame[y1:y2, x1:x2]  # Use clean_frame for saving

            # Save the cropped image
            cv2.imwrite(r"captured/detected_iris.jpg", cropped_image)
            print("Iris detected and image saved as 'captured/detected_iris.jpg'.")

    # Release the camera and close the window
    cam.release()
    cv2.destroyAllWindows()
