from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import os

from backend.core.dependencies import role_required
from backend.ai.image_analyzer import estimate_crowd_from_image

router = APIRouter(prefix="/ai", tags=["AI Crowd Analysis"])


# ==============================
# Request Schema
# ==============================
class AnalyzeRequest(BaseModel):
    camera_id: str
    image_name: str


# ==============================
# Response Schema
# ==============================
class AnalyzeResponse(BaseModel):
    camera_id: str
    count: int
    status: str
    risk_score: float
    yolo_detected: int
    annotated_image: str


# ==============================
# Hybrid AI Endpoint (Single Image)
# ==============================
@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_image(
    data: AnalyzeRequest,
    user=Depends(role_required(["admin", "security"]))
):
    try:
        result = estimate_crowd_from_image(data.image_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "camera_id": data.camera_id,
        "count": result["count"],
        "status": result["status"],
        "risk_score": result["risk_score"],
        "yolo_detected": result["yolo_detected"],
        "annotated_image": result["annotated_image"],
    }


# ==============================
# Batch Camera Analysis (25 Cameras)
# ==============================
@router.get("/batch_analyze")
def batch_analyze():

    results = []

    # Take first 25 images from dataset folder
    images = sorted([
        f for f in os.listdir("dataset")
        if f.startswith("IMG_") and f.endswith(".jpg")
    ])[:25]

    for idx, image_name in enumerate(images):
        try:
            data = estimate_crowd_from_image(image_name)

            results.append({
                "camera_id": f"CAM_{idx+1}",
                "image": image_name,
                "count": data["count"],
                "status": data["status"],
                "risk_score": data["risk_score"]
            })

        except FileNotFoundError:
            # Skip missing files safely
            continue

    return results