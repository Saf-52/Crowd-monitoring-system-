import os
import cv2
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
)
from ultralytics import YOLO

# ---------------------------
# Load YOLOv8
# ---------------------------
model = YOLO("yolov8n.pt")

# ---------------------------
# Dynamic Path Setup
# ---------------------------
current_file = os.path.abspath(__file__)
backend_folder = os.path.dirname(os.path.dirname(current_file))
project_root = os.path.dirname(backend_folder)

image_folder = os.path.join(project_root, "dataset")
gt_folder = os.path.join(project_root, "dataset", "ground_truth")

true_counts = []
pred_counts = []

# ---------------------------
# Collect Counts
# ---------------------------
for img_name in os.listdir(image_folder):

    if not img_name.endswith(".jpg"):
        continue

    img_path = os.path.join(image_folder, img_name)
    gt_path = os.path.join(gt_folder, "GT_" + img_name.replace(".jpg", ".mat"))

    if not os.path.exists(gt_path):
        continue

    # Ground Truth
    mat = scipy.io.loadmat(gt_path)
    gt_points = mat["image_info"][0][0][0][0][0]
    true_count = len(gt_points)

    # YOLO Prediction
    image = cv2.imread(img_path)
    results = model(image, verbose=False)
    detections = results[0].boxes.cls.cpu().numpy()
    predicted_count = np.sum(detections == 0)

    true_counts.append(true_count)
    pred_counts.append(predicted_count)

true_counts = np.array(true_counts)
pred_counts = np.array(pred_counts)

# ---------------------------
# Regression Metrics
# ---------------------------
mae = mean_absolute_error(true_counts, pred_counts)
mse = mean_squared_error(true_counts, pred_counts)

print("\nCrowd Counting Metrics:")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))

# ---------------------------
# Linear Calibration
# ---------------------------
scale_factor = np.mean(true_counts) / (np.mean(pred_counts) + 1e-6)
scaled_pred_counts = pred_counts * scale_factor

print("\nScale Factor:", round(scale_factor, 2))

# ---------------------------
# Binary Threshold (Median of GT)
# ---------------------------
threshold = np.median(true_counts)

print("Binary Threshold (GT Median):", round(threshold, 2))

def classify_binary(count):
    if count <= threshold:
        return "SAFE"
    else:
        return "DENSE"

true_labels = [classify_binary(c) for c in true_counts]
pred_labels = [classify_binary(c) for c in scaled_pred_counts]

# ---------------------------
# Confusion Matrix
# ---------------------------
labels = ["SAFE", "DENSE"]

cm = confusion_matrix(true_labels, pred_labels, labels=labels)

plt.figure(figsize=(5,4))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Greens",
    xticklabels=labels,
    yticklabels=labels,
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Binary Crowd Risk Confusion Matrix")
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), "confusion_matrix_binary.png")
plt.savefig(output_path)
plt.show()

accuracy = np.trace(cm) / np.sum(cm)

print("\nBinary Classification Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")
print(classification_report(true_labels, pred_labels))