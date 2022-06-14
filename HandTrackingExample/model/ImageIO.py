import time
from threading import Thread

import cv2

class ImageIO(Thread):
    # class used to have a video stream from the cam, it takes a picture at each instance of time
    # and keeps it so other class can use it

    def __init__(self):
        super().__init__()

        # fields used to calculate the fps of the stream
        self.cTime = time.time();
        self.pTime = time.time();
        # open a channel with the cam for take the pictures
        self.cap = cv2.VideoCapture(0)

        # field to keep the last image
        self.lastImage = None
        # field to chose if add information to the picture
        self.processingInfo = False
        self.flipped = False

    def run(self):
        # at each instance of time:
        #   - take a new picture
        #   - if it not succede close the method
        #   - if is required add other information

        while True:
            succes, img = self.cap.read()

            if not succes:
                continue

            if self.flipped:
                img = self.flip_image(img)

            if self.processingInfo:
                img = self.add_ProcessingInfo(img)

            self.lastImage = img

            time.sleep(0.02)
            cv2.waitKey(0)

    def add_ProcessingInfo(self, img):
        # this method adds the information about average fps of the picture capturing
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

