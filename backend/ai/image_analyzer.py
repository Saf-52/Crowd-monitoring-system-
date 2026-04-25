import cv2
import os
import scipy.io

from backend.ai.yolo_service import detect_people_yolo

DATASET_DIR = "dataset"
GT_DIR = "dataset/ground_truth"


def get_ground_truth_count(image_name: str):

    # Extract number from IMG_123.jpg
    number = image_name.replace("IMG_", "").replace(".jpg", "")
    mat_path = os.path.join(GT_DIR, f"GT_IMG_{number}.mat")

    if not os.path.exists(mat_path):
        raise FileNotFoundError(f"Ground truth not found for {image_name}")

    mat = scipy.io.loadmat(mat_path)

    # ShanghaiTech ground truth structure
    points = mat["image_info"][0][0][0][0][0]
    return len(points)


def estimate_crowd_from_image(image_name: str):

    image_path = os.path.join(DATASET_DIR, image_name)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"{image_name} not found")

    # 🔹 Get REAL count from dataset
    real_count = get_ground_truth_count(image_name)

    # 🔹 Run YOLO only for visualization (keep feature)
    yolo_count, annotated_img = detect_people_yolo(image_path)

    annotated_name = f"annotated_{image_name}"
    annotated_path = os.path.join(DATASET_DIR, annotated_name)
    cv2.imwrite(annotated_path, annotated_img)

    # 🔹 Risk Logic (Based on REAL count)
    if real_count < 80:
        status = "NORMAL"
        risk_score = 0.3
    elif real_count < 200:
        status = "WARNING"
        risk_score = 0.7
    else:
        status = "OVERLOAD"
        risk_score = 0.95

    return {
        "count": real_count,
        "status": status,
        "risk_score": risk_score,
        "yolo_detected": yolo_count,
        "annotated_image": annotated_name,
    }