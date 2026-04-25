from ultralytics import YOLO

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")  # lightweight & fast

    def detect(self, image):
        results = self.model(image, verbose=False)
        boxes = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls == 0:  # class 0 = person
                    boxes.append(box.xyxy[0].tolist())

        return boxes
