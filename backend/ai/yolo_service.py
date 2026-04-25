from ultralytics import YOLO
import cv2
import os

# 🔥 Use slightly stronger model than nano (still CPU safe)
model = YOLO("yolov8s.pt")
model.fuse()


def detect_people_yolo(image_path: str):
    """
    Detect people using YOLOv8.
    Returns:
    - person_count (int)
    - annotated_image (OpenCV image)
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)

    # ============================
    # ✅ Resize Before Detection
    # ============================
    h, w = image.shape[:2]

    if w > 1280:
        scale = 1280 / w
        image = cv2.resize(image, (1280, int(h * scale)))

    # ============================
    # Run YOLO (Person Class Only)
    # ============================
    results = model.predict(
        image,
        imgsz=960,
        conf=0.35,
        classes=[0],  # COCO class 0 = person
        verbose=False
    )

    person_count = 0
    annotated_image = image.copy()

    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                person_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(
                    annotated_image,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

    return person_count, annotated_image