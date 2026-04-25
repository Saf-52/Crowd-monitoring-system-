import cv2
import numpy as np

def estimate_crowd_count(image_path: str) -> int:
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError("Image not found")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection → density hint
    edges = cv2.Canny(gray, 50, 150)

    density = np.sum(edges > 0)

    # Heuristic scaling (simple & fast)
    estimated_count = int(density / 600)

    return max(estimated_count, 1)
