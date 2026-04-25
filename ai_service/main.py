from detector import PersonDetector
from image_loader import ImageLoader
from counter import CrowdCounter
from smoothing import Smoother
from alert_logic import AlertLogic
from api_client import send_update

detector = PersonDetector()
loader = ImageLoader("../dataset")
counter = CrowdCounter()
smoother = Smoother()
alert_logic = AlertLogic(threshold=5)

CAMERA_ID = "CAM_01"

while True:
    frame = loader.get_next_frame()
    boxes = detector.detect(frame)
    count = counter.count(boxes)
    smooth_count = smoother.smooth(count)
    status = alert_logic.check(smooth_count)

    print(f"Count: {smooth_count:.2f} | Status: {status}")
    send_update(CAMERA_ID, int(smooth_count), status)
