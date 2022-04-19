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
        self.fingers = [self.THUMB, self.INDEX, self.MIDDLE, self.RING, self.PINKY]

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

    def is_finger_active(self, hand, finger):
        finger_position = self.get_point_position(hand, finger)
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

        if position_f2[0] >= position_f1[0] + self.NEAR_TOLLERANCE*2 or position_f2[0] <= position_f1[0] - self.NEAR_TOLLERANCE*2:
            return False

        if position_f2[1] >= position_f1[1] + self.NEAR_TOLLERANCE or position_f2[1] <= position_f1[1] - self.NEAR_TOLLERANCE:
            return False

        return True

    def hand_close(self, hand):
        for finger in self.fingers:
            print(self.is_finger_active(hand, finger))

            if self.is_finger_active(hand, finger):
                return False


        print("\n\n\n\n")

        return True

    def draw_finger_area(self, img, hand, finger):
        position_f1 = self.get_point_position(hand, finger)

        cv2.rectangle(img, (position_f1[0] - self.NEAR_TOLLERANCE*2, position_f1[1] - self.NEAR_TOLLERANCE), (position_f1[0] + self.NEAR_TOLLERANCE*2, position_f1[1] + self.NEAR_TOLLERANCE), (255,111,111), cv2.FILLED)

import time


# import cv2

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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

    def showImage1(self, img):
        imgplot = plt.imshow(img)
        plt.show()


import copy
class Board:
    def __init__(self):
        self.canvas = None
        self.mode = "draw"

        self.actual_me = None
        self.old_me = None
        self.new_thing = False

        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0

    def init_board(self, image):
        if self.canvas is None:
            self.canvas = np.zeros_like(img)
            self.actual_me = copy.deepcopy(self.canvas)
            self.old_me = copy.deepcopy(self.canvas)

    def finger_on_board(self, pos_x, pos_y):
        if self.canvas is None:
            return False

        self.new_thing = True

        self.x2 = pos_x
        self.y2 = pos_y

        if self.x1 == 0 and self.y1 == 0:
            self.x1, self.y1 = self.x2, self.y2
            return True

        if self.mode == "draw" :
            cv2.line(self.canvas, (self.x1, self.y1), (self.x2, self.y2), (255, 255, 0), 5)
        else:
            cv2.circle(self.canvas, (self.x1, self.y1), 20, (0, 0, 0), -1)

        self.x1, self.y1 = self.x2, self.y2
        return True

    def finger_off_board(self):
        self.x1, self.y1 = 0, 0

        if self.canvas is None:
            return

        if self.new_thing:
            self.old_me = copy.deepcopy(self.actual_me)
            self.actual_me = copy.deepcopy(self.canvas)
            io.showImage1(self.old_me)

    def undo(self):
        if not self.new_thing:
            return

        io.showImage1(self.old_me)
        self.canvas = copy.copy(self.old_me)
        self.new_thing = False
        self.actual_me = copy.copy(self.canvas)
        self.old_me = copy.copy(self.canvas)

    def change_mode(self):
        if(self.mode == "draw"):
            self.mode = "delete"
        else:
            self.mode = "draw"


# -----------------------------------------

def try_set(a, b):
    if a != b:
        return b

    return a

# -----------------------------------------

import numpy as np

io = ImageIO()
d = HandDetect()

bb = Board()
img = io.captureImage()
bb.init_board(img)

operation_old = ""

while True:
    img = io.captureImage()
    d.detect_hands(img)

    operation = ""

    if d.get_point(0, HandDetect.INDEX):
        d.draw_finger_area(img, 0, d.MIDDLE)

        if not d.finger_near(0, d.INDEX, d.MIDDLE):
            p = d.get_point_position(0, HandDetect.INDEX)

            bb.finger_on_board(p[0], p[1])

            cv2.circle(img, (p[0], p[1]), 15, (0, 255, 0), cv2.FILLED)
        else:
            operation = try_set(operation_old, "off")

        if d.finger_near(0, d.MIDDLE, d.THUMB):
            operation = try_set(operation_old, "undo")

        if operation != operation_old:
            if operation == "off":
                bb.finger_off_board()
            elif operation == "undo":
                bb.undo()

        operation_old = operation


        if d.hand_close(0):
            bb.change_mode()

    img = d.draw_tracked_hand(img)
    img = cv2.add(bb.canvas, img)

    io.showFlippedImage(img)

    cv2.waitKey(1)
