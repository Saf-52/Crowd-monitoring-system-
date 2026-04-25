import cv2
import os
import time

class ImageLoader:
    def __init__(self, folder_path):
        self.images = [
            os.path.join(folder_path, img)
            for img in os.listdir(folder_path)
            if img.endswith((".jpg", ".png"))
        ]
        self.index = 0

    def get_next_frame(self):
        if self.index >= len(self.images):
            self.index = 0  # loop dataset

        img_path = self.images[self.index]
        frame = cv2.imread(img_path)
        self.index += 1

        time.sleep(0.5)  # simulate real-time
        return frame
