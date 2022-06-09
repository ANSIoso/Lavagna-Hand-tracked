import time
from threading import Thread

from model.HandDetector_m import HandDetect


class HandDetector_c(Thread):
    def __init__(self, hand_detector: HandDetect):
        super().__init__()

        self.hand_detector = hand_detector

    def run(self):
        while True:
            self.hand_detector.detect_hands()
            time.sleep(0.02)
