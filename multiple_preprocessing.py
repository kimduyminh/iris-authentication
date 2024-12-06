import preprocessing.localization as lc
import preprocessing.normalization as nm
import cv2
import os


def iterate_dataset_localization(dataset_path):
    num_of_pics = 0
    num_of_err = 0
    error_ids=[]
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg"):  # Adjust for your image format
                num_of_pics+=1
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
                    print(f"Error processing image: {image_path}, ID: {id_number}, Error: {e}")
                    num_of_err+=1
                    error_ids.append(image_path)
    print("Error files: ")
    for error_id in error_ids:
        print(error_id)
    print("Number of images: "+str(num_of_pics))
    print("Number of errors: "+str(num_of_err))
def iterate_dataset_normalize(dataset_path):
    print("Choose normalization method:")
    print("1.HisEqual")
    print("2.CLAHE")
    print("3.Gamma Correction")
    print("4.Contrast stretching")
    option = int(input("Enter your choice: "))
    error_ids = []
    if option == 1:
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".jpg"):  # Adjust for your image format
                    try:
                        image_path = os.path.join(root, file)
                        id_number = os.path.basename(root)  # Extract the ID number from the folder name
                        image = cv2.imread(image_path)
                        resized_image = nm.funHistogramEqualization(image)
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
                        print(f"Error processing image: {image_path}, ID: {id_number}, Error: {e}")
                        error_ids.append(image_path)
    if option == 2:
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".jpg"):  # Adjust for your image format
                    try:
                        image_path = os.path.join(root, file)
                        id_number = os.path.basename(root)  # Extract the ID number from the folder name
                        image = cv2.imread(image_path)
                        resized_image = nm.gamma_correction(image)
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
                        print(f"Error processing image: {image_path}, ID: {id_number}, Error: {e}")
                        error_ids.append(image_path)
    if option == 3:
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".jpg"):  # Adjust for your image format
                    try:
                        image_path = os.path.join(root, file)
                        id_number = os.path.basename(root)  # Extract the ID number from the folder name
                        image = cv2.imread(image_path)
                        resized_image = nm.CLAHE(image)
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
                        print(f"Error processing image: {image_path}, ID: {id_number}, Error: {e}")
                        error_ids.append(image_path)
    if option == 4:
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".jpg"):  # Adjust for your image format
                    try:
                        image_path = os.path.join(root, file)
                        id_number = os.path.basename(root)  # Extract the ID number from the folder name
                        image = cv2.imread(image_path)
                        resized_image = nm.contrast_stretching(image)
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
                        print(f"Error processing image: {image_path}, ID: {id_number}, Error: {e}")
                        error_ids.append(image_path)
    print("Error files: ")
    for error_id in error_ids:
        print(error_id)
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

