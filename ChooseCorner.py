import cv2
import os

path = 'C:/Users/Asus/Desktop/CV-Final-Project/train/images/'
destination = "C:/Users/Asus/Desktop/CV-Final-Project/train-corners/"
images = os.listdir(path)
# Create a list to store the image file names and clicked locations
dataset = []


def onclick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the image file name and clicked location to the dataset
        dataset.append((path + img, (x, y)))
        print(f"Clicked location: x={x}, y={y}")


for img in images:
    # Load the image
    image = cv2.imread(path + img)
    # Create a window and display the image
    cv2.namedWindow("Image")
    cv2.imshow("Image", cv2.resize(image, (1024, 686)))
    # Set the mouse callback function to handle clicks
    cv2.setMouseCallback("Image", onclick)

    while True:
        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF

        # If the 'q' key is pressed, break from the loop
        if key == ord("q"):
            with open(f"{destination + img[:-4]}.txt", "w+") as file:
                for data in dataset:
                    file.write(f"{data[1][0]},{data[1][1]}\n")
            dataset = []
            break
    # Save the dataset to a file

# Close all windows
cv2.destroyAllWindows()
