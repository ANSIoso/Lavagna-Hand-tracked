import mediapipe as mp
import cv2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class HandDetect:
    THUMB = 4
    INDEX = 8
    MIDDLE = 12
    RING = 16
    PINKY = 20

    NEAR_TOLLERANCE = 40

    def __init__(self):
        self.result = None
        self.w_img = None
        self.h_img = None

        self.hand_inactivity_zone = [0, 1, 2, 3, 6, 10, 14, 18]

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()

        self.mpDraw = mp.solutions.drawing_utils

    def detect_hands(self, img):
        self.h_img, self.w_img, c = img.shape

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

    def draw_tracked_hand(self, img):
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def get_point(self, hand, point):
        if not self.result.multi_hand_landmarks:
            return False

        n_hands = len(self.result.multi_hand_landmarks)
        if n_hands <= hand:
            return False

        return self.result.multi_hand_landmarks[n_hands - hand - 1].landmark[point]

    def get_point_position(self, hand, point):
        point = self.get_point(hand, point)

        if not point:
            return False

        return int(point.x * self.w_img), int(point.y * self.h_img)

    def is_finger_active(self, finger):
        finger_position = self.get_point_position(0, finger)
        if not finger_position:
            return False

        points = []
        for point in self.hand_inactivity_zone:
            points.append(self.get_point_position(0, point))

        p = Point(finger_position)
        polygon = Polygon(points)

        return not polygon.contains(p)

    def finger_near(self, hand, finger_one, finger_two):
        position_f1 = self.get_point_position(hand, finger_one)
        position_f2 = self.get_point_position(hand, finger_two)

        if not(position_f1 and position_f2):
            return False

        if position_f2[0] >= position_f1[0] + self.NEAR_TOLLERANCE or position_f2[0] <= position_f1[0] - self.NEAR_TOLLERANCE:
            return False

        if position_f2[1] >= position_f1[1] + self.NEAR_TOLLERANCE or position_f2[1] <= position_f1[1] - self.NEAR_TOLLERANCE:
            return False

        return True

    def draw_finger_area(self, img, hand, finger):
        position_f1 = self.get_point_position(hand, finger);

        cv2.rectangle(img, (position_f1[0] - self.NEAR_TOLLERANCE, position_f1[1] - self.NEAR_TOLLERANCE), (position_f1[0] + self.NEAR_TOLLERANCE, position_f1[1] + self.NEAR_TOLLERANCE), (255,111,111), cv2.FILLED)

import time


# import cv2


class ImageIO:
    def __init__(self):
        self.cTime = time.time();
        self.pTime = time.time();
        self.cap = cv2.VideoCapture(0)

    def captureImage(self):
        succes, img = self.cap.read()

        if succes:
            return img
        return False

    def addProcessingInfo(self, img):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (255, 0, 255), 3)

    def showFlippedImage(self, img):
        img = cv2.flip(img, 1)
        self.showImage(img)

    def showImage(self, img):
        self.addProcessingInfo(img)
        cv2.imshow("image", img)


import copy
class Board:
    def __init__(self):
        self.canvas = None
        self.history = []
        self.mode = "drow"

        self.old_tings = True
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0

    def init_board(self, image):
        if self.canvas is None:
            self.canvas = np.zeros_like(img)

    def finger_on_board(self, pos_x, pos_y):
        if self.canvas is None:
            return False

        if self.old_tings:
            self.history.append(copy.deepcopy(self.canvas))
            self.old_tings = False

        self.x2 = pos_x
        self.y2 = pos_y

        if self.x1 == 0 and self.y1 == 0:
            self.x1, self.y1 = self.x2, self.y2
            return True

        cv2.line(self.canvas, (self.x1, self.y1), (self.x2, self.y2), (255, 255, 0), 5)
        self.x1, self.y1 = self.x2, self.y2
        return True

    def finger_off_board(self):
        print(len(self.history))

        self.x1, self.y1 = 0, 0
        self.old_tings = True



    def undo(self):
        print(len(self.history))

        if len(self.history) <= 1:
            return

        self.history.pop()
        print(len(self.history))
        self.canvas = self.history[-1]






import numpy as np

io = ImageIO()
d = HandDetect()

bb = Board()
img = io.captureImage()
bb.init_board(img)

while True:
    img = io.captureImage()
    d.detect_hands(img)

    if d.is_finger_active(HandDetect.INDEX) and not d.finger_near(0, d.INDEX, d.MIDDLE):
        p = d.get_point_position(0, HandDetect.INDEX)

        bb.finger_on_board(p[0], p[1])

        cv2.circle(img, (p[0], p[1]), 15, (0, 255, 0), cv2.FILLED)
    else:
        print("pico")
        bb.finger_off_board()

    d.draw_finger_area(img, 0, d.MIDDLE)

    if d.finger_near(0, d.MIDDLE, d.THUMB):
        bb.undo()

    # img = d.draw_tracked_hand(img)
    img = cv2.add(bb.canvas, img)

    d.draw_tracked_hand(img)
    io.showFlippedImage(img)

    cv2.waitKey(1)
