import time
from threading import Thread

import cv2

class ImageIO(Thread):
    def __init__(self):
        super().__init__()

        self.cTime = time.time();
        self.pTime = time.time();
        self.cap = cv2.VideoCapture(0)

        self.lastImage = None
        self.processingInfo = False
        self.flipped = False

    def run(self):

        while True:
            succes, img = self.cap.read()

            if not succes:
                return

            if self.flipped:
                img = self.flip_image(img)

            if self.processingInfo:
                img = self.add_ProcessingInfo(img)

            self.lastImage = img

            time.sleep(0.02)
            cv2.waitKey(0)

    def add_ProcessingInfo(self, img):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime

        img = cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (255, 0, 255), 3)
        return img

    def flip_image(self, img):
        img = cv2.flip(img, 1)
        return img

    def want_processing_info(self, want):
        if want != True and want != False:
            return
        self.processingInfo = want

    def want_flipped(self, want):
        if want != True and want != False:
            return
        self.flipped = want

