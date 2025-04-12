import cv_draw
"""
from picamera2 import Picamera2
class Camera(Picamera2):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(self.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.start()

    def capture(self, *args, **kwargs):
        frame = super().capture_array()
        return cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
"""
import cv2
class VideoCapture(cv2.VideoCapture):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open(*args)

    def capture(self, *args, **kwargs):
        return cv_draw.shrink(super().read()[1])

    def release(self, *args, **kwargs):
        return super().release()

