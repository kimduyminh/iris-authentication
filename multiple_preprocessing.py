import preprocessing.localization as lc
import preprocessing.normalization as nm
import cv2
import os


def iterate_dataset_localization(dataset_path):
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg"):  # Adjust for your image format
                try:
                    image_path = os.path.join(root, file)
                    id_number = os.path.basename(root)  # Extract the ID number from the folder name
                    image = cv2.imread(image_path)
                    resized_image=lc.localization(image)
                # Process the image and ID number as needed
                    print(f"Processing image: {image_path}, ID: {id_number}")
                # Extract ID and filename
                    id_dir, filename = os.path.split(image_path)
                    id_number = os.path.basename(id_dir)

                # Create the output directory if it doesn't exist
                    output_dir = os.path.join("processed_image", id_number)
                    os.makedirs(output_dir, exist_ok=True)

                # Construct the output filename
                    output_filename = os.path.join(output_dir, filename)
                    cv2.imwrite(output_filename, resized_image)
                except Exception as e:
                    print(e)
def iterate_dataset_normalize(dataset_path):
    print("Choose normalization method:")
    print("1.HisEqual")
    print("2.CLAHE")
    option = int(input("Enter your choice: "))
    if option == 1:
        opt = "funHistogramEqualization"
    if option == 2:
        opt = "CLAHE"
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg"):  # Adjust for your image format
                try:
                    image_path = os.path.join(root, file)
                    id_number = os.path.basename(root)  # Extract the ID number from the folder name
                    image = cv2.imread(image_path)
                    resized_image=nm.get(opt)(image)
                # Process the image and ID number as needed
                    print(f"Processing image: {image_path}, ID: {id_number}")
                # Extract ID and filename
                    id_dir, filename = os.path.split(image_path)
                    id_number = os.path.basename(id_dir)

                # Create the output directory if it doesn't exist
                    output_dir = os.path.join("processed_image", id_number)
                    os.makedirs(output_dir, exist_ok=True)

                # Construct the output filename
                    output_filename = os.path.join(output_dir, filename)
                    cv2.imwrite(output_filename, resized_image)
                except Exception as e:
                    print(e)
print("Multiple preprocessing")
print("1. Multiple localization")
print("2. Multiple Normalization")
option = int(input("Enter your choice: "))
if option == 1:
    dataset_path = "dataset"
    iterate_dataset_localization(dataset_path)
if option == 2:
    processed_path = "processed_image"
    iterate_dataset_normalize(processed_path)

