import numpy as np
import os
from tensorflow import keras
import cv2

# # Step 1: Collecting the dataset
# dataset = []
#
# # Define the path to the directory containing the text files
# directory = "C:/Users/Asus/Desktop/CV-Final-Project/train-corners"
#
# # Loop through each text file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".txt"):
#         # Read the text file
#         with open(os.path.join(directory, filename), "r") as file:
#             # Extract the corner coordinates from the text file
#             coordinates = []
#             for line in file:
#                 if line != '':
#                     c = line.strip().split(",")
#                     coordinates.append((int(c[0]), int(c[1])))
#             # Append the image file name and corner coordinates to the dataset
#             dataset.append((filename[:-4], coordinates))
#
# # Step 2: Preprocessing the dataset
# train_images = []
# train_labels = []
#
# directory = "C:/Users/Asus/Desktop/CV-Final-Project/train/images/"
# # Loop through each image and its corner coordinates in the dataset
# for image_name, coordinates in dataset:
#     # Load the image
#     image = cv2.imread(os.path.join(directory, image_name + ".jpg"))
#     # Resize the image if needed
#     image = cv2.resize(image, (1024, 686))
#     # Normalize pixel values
#     image = image / 255.0
#     # Append the preprocessed image and its corner coordinates to the training set
#     train_images.append(image)
#     train_labels.append(coordinates)
#
# # Convert the training set to NumPy arrays
# train_images = np.array(train_images)
# train_labels = np.array(train_labels)
#
# # Split the dataset into train and test sets (80% for training, 20% for testing)
# split_index = int(0.8 * len(train_images))
# test_images = train_images[:split_index]
# test_labels = train_labels[:split_index]
# train_images = train_images[split_index:]
# train_labels = train_labels[split_index:]
#
# # Step 3: Building the CNN model
# model = keras.Sequential([
#     keras.layers.Conv2D(16, (3, 3), activation='relu'),
#     keras.layers.MaxPooling2D((2, 2)),
#     keras.layers.Conv2D(32, (3, 3), activation='relu'),
#     keras.layers.MaxPooling2D((2, 2)),
#     keras.layers.Flatten(),
#     keras.layers.Dense(64, activation='relu'),
#     keras.layers.Dense(8)  # output layer with 8 units for corner coordinates
# ])
# train_labels = np.array([np.reshape(label, (8,)) for label in train_labels])
#
# # Step 4: Training the model
# model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
# model.fit(train_images, train_labels, epochs=150, batch_size=8)
# test_labels = np.array([np.reshape(label, (8,)) for label in test_labels])
# # Step 5: Evaluating the model
# test_loss, test_accuracy = model.evaluate(test_images, test_labels)
# print('Test Loss:', test_loss)
# print('Test Accuracy:', test_accuracy)
# model.save("Task2_Model")


model = keras.models.load_model("Task2_Model")
# Step 6: Using the trained model
new_images = []
directory = "C:/Users/Asus/Desktop/CV-Final-Project/test/images/1024"
# Loop through each image and its corner coordinates in the dataset
images = os.listdir(directory)
for image_name in images:
    # Load the image
    image = cv2.imread(os.path.join(directory, image_name))
    # Resize the image if needed
    # image = cv2.resize(image, (1024, 686))
    # Normalize pixel values
    image = image / 255.0
    # Append the preprocessed image and its corner coordinates to the training set
    new_images.append(image)
new_images = np.array(new_images)
result = model.predict(new_images)
counter = 0
dest = "C:/Users/Asus/Desktop/CV-Final-Project/test/corners/"
for image_name in images:
    # Load the image
    image = cv2.imread(os.path.join(directory, image_name))
    # Resize the image if needed
    image = cv2.resize(image, (1024, 686))
    # Normalize pixel values
    for i in range(0, 4):
        center = (int(result[counter][2 * i]), int(result[counter][2 * i + 1]))  # x, y
        file = open(os.path.join(dest, image_name[:-4] + ".txt"), "a+")
        file.write(str(center[0]) + "," + str(center[1]))
        file.write("\n")
        radius = 6
        color = (0, 0, 255)  # BGR format, red is (0, 0, 255)
        thickness = 10
        cv2.circle(image, center, radius, color, thickness)
    cv2.imshow("image", image)
    cv2.waitKey(0)

    counter += 1
cv2.destroyAllWindows()
