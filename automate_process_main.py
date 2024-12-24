import preprocessing.localization as lc
import preprocessing.normalization as nm
import InterceptionV3_training as model
import feature_selection.Gabor_filter as gab
import feature_selection.Haar_wavelet as hw
import feature_selection.laplacian as lp
import feature_selection.LogGabor_filter as lb
import cv2
import os
import time
import timeit


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
def iterate_dataset_normalize(dataset_path,option):
    if option == 0:
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
def multiple_feat_selection(option):
    if (option == 0):
        print("Choose feature selection method:")
        print("1.Gabor filter")
        print("2.LogGabor")
        print("3.Laplacian")
        print("4.Haar wavelet")
        option = int(input("Enter your choice: "))
    if option == 1:
        print("Processing Gabor Filter")
        gab.main()
    if option == 4:
        print("Processing Haar Wavelet")
        hw.main()
    if option == 3:
        print("Processing Laplacian")
        lp.main()
    if option == 2:
        print("Processing Log Gabor")
        lb.main()

def case_5_with_combinations():
    number_of_trained_models = 0
    result = open("result.txt", "a")
    dataset_path = "dataset"
    processed_path = "processed_image"

    # Loop through all normalization methods (Case 2)
    normalization_options = [2,3]
    feature_selection_options = [1, 2, 3]

    for normalization_option in normalization_options:
        print("Starting localization...")
        iterate_dataset_localization(dataset_path)
        start1 = time.time()
        print(f"Starting normalization with option {normalization_option}...")
        iterate_dataset_normalize(processed_path, normalization_option)
        end1 = time.time()
        # After normalization, loop through all feature selection methods (Case 3)
        for feature_selection_option in feature_selection_options:
            start2 = time.time()
            print(f"Starting feature selection with option {feature_selection_option}...")
            multiple_feat_selection(feature_selection_option)
            end2 = time.time()
            time.sleep(60)
            print("Number of trained models: ", number_of_trained_models)
            result_train = model.main()
            print("Writing to result.txt...")
            train_accuracy = result_train[0]
            val_accuracy = result_train[1]
            time_trained = result_train[2]
            result.writelines("Trained with "+str(normalization_option)+" and "+str(feature_selection_option)+" :\n")
            result.writelines("Train accuracy: "+str(train_accuracy/100)+"\n")
            result.writelines("Validation accuracy: "+str(val_accuracy/100)+"\n")
            result.writelines("Normalizing time: "+str(end1-start1)+" s\n")
            result.writelines("Feature selection time: "+str(end2-start2)+" s\n")
            result.writelines("Training time: "+time_trained+" s\n")
            result.writelines("........................................\n")
            print("Done writing result")
            number_of_trained_models += 1


print("Main Menu")
print("1. Multiple localization")
print("2. Multiple Normalization")
print("3. Multiple Feature Selection")
print("4. Train")
print("5. Looping through all methods and testing")
option = int(input("Enter your choice: "))
if option == 1:
    dataset_path = "dataset"
    iterate_dataset_localization(dataset_path)
if option == 2:
    processed_path = "processed_image"
    iterate_dataset_normalize(processed_path,0)
if option == 3:
    multiple_feat_selection(0)
if option == 4:
    model.main()
if option == 5:
    case_5_with_combinations()




