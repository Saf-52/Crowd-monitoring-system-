import requests

BACKEND_URL = "http://127.0.0.1:8000/crowd/update"

def send_update(camera_id, count, status):
    payload = {
        "camera_id": camera_id,
        "count": count,
        "status": status
    }
    try:
        requests.post(BACKEND_URL, json=payload)
    except:
        print("Backend not reachable")
