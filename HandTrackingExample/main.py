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


class DrawingPoint:
    def __init__(self, dim=10, color=(155, 155, 155)):
        self.dim = dim
        self.color = color


class Drawing:
    def __init__(self):
        self.drawing_points = []
        self.last_affected_points = {}
        self.current_operation = "add"

    def add_affected_points(self, pos_x, pos_y, dp):
        self.last_affected_points[(pos_x, pos_y)] = dp

    def confirm_drawing_operation(self):
        if self.current_operation == "add" :
            self.add_new_points()
        else:
            self.delete_points()

    def add_new_points(self):
        self.drawing_points.append(self.last_affected_points)

    def delete_points(self, pos_x, pos_y):
        for line in self.drawing_points:
            del line[(pos_x, pos_y)]



io = ImageIO()
d = HandDetect()
drow = Drawing()
pollp = None

while True:
    img = io.captureImage()
    d.detect_hands(img)

    '''p = d.get_point_position(0, 0)

    if p:
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 1)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 2)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 5)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 9)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 13)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)

        p = d.get_point_position(0, 17)
        cv2.circle(img, (p[0], p[1]), 15, (255, 255, 255), cv2.FILLED)'''

    for line in drow.drawing_points:
        for pino in line:
            cv2.circle(img, (pino[0], pino[1]), 15, (0, 255, 0), cv2.FILLED)


    if d.is_finger_active(HandDetect.INDEX):
        p = d.get_point_position(0, HandDetect.INDEX)
        cv2.circle(img, (p[0], p[1]), 15, (0, 255, 0), cv2.FILLED)

        palla = DrawingPoint()
        drow.add_affected_points(p[0], p[1], palla)
    else:
        drow.add_new_points()

    # img = d.draw_tracked_hand(img)
    io.showFlippedImage(img)

    cv2.waitKey(1)
