from ultralytics import YOLO
import os

# # Load a model
# model = YOLO('yolov8n.yaml')  # build a new model from YAML
# model.train(data="data.yaml", epochs=150)
path = 'C:/Users/Asus/Desktop/CV-Final-Project/test/images/1024/'
dest = "C:/Users/Asus/Desktop/CV-Final-Project/test/boxes/"
testImages = os.listdir(path)
model = YOLO('best2.pt')
for img in testImages:
    source = path + img
    results = model.predict(source, save=True, augment=True)
    for result in results:
        boxes = result.boxes
        if boxes:
            for box in boxes:
                cls = box.cls
                rect = box.xyxy
                file = open(os.path.join(dest, img[:-4] + ".txt"), "a")
                file.write(str(cls.tolist()))
                file.write("\n")
                file.write(str(rect.tolist()))
                file.write("\n")
        else:
            file = open(os.path.join(dest, img[:-4] + ".txt"), "a")
            file.write("\n")
            file.write("\n")
