import cv2
import numpy as np

def localization(frame):
    try:
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Step 2: Enhance contrast
        gray = cv2.equalizeHist(gray)

        # Step 3: Apply Gaussian blur
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 2)

        # Step 4: Edge detection
        edges = cv2.Canny(gray_blurred, 50, 150)

        # Step 5: Detect circles using HoughCircles
        circles = cv2.HoughCircles(
            edges,
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

            for circle in circles[0, :]:
                x, y, r = circle
                # Return the first detected circle
                return x, y, r
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Open the default camera
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Detect the iris
    result = localization(frame)

    if result is not None:
        x, y, r = result
        # Draw the circle and center
        cv2.circle(frame, (x, y), r, (0, 255, 0), 2)  # Circle
        cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)  # Center

        # Save the detected iris region
        crop_size = int(r * 1.5)
        x1, y1 = max(x - crop_size, 0), max(y - crop_size, 0)
        x2, y2 = min(x + crop_size, frame.shape[1]), min(y + crop_size, frame.shape[0])
        cropped_image = frame[y1:y2, x1:x2]
        cv2.imwrite("detected_iris.jpg", cropped_image)

    # Display the live video feed
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close the window
cam.release()
cv2.destroyAllWindows()
