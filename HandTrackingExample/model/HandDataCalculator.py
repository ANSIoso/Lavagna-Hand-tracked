import cv2
import mediapipe as mp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class HandDetect:
    # classe utilizzata per avere informazioni sulle "mani" attualmente inquadrate dalla telecamera

    # identificatori per le varie dita della mano
    THUMB = 4
    INDEX = 8
    MIDDLE = 12
    RING = 16
    PINKY = 20

    # area di tolleranza utilizzata per capire se un dito è vicino ad un'altro
    NEAR_TOLLERANCE = 30

    def __init__(self):
        self.result = None
        self.w_img = None
        self.h_img = None

        self.hand_inactivity_zone = [0, 1, 2, 3, 6, 10, 14, 18]
        self.fingers = [self.THUMB, self.INDEX, self.MIDDLE, self.RING, self.PINKY]

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()

        self.handInclination = 0

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

    def finger_near(self, hand, finger_one, finger_two, x_toll=1, y_toll=1):
        position_f1 = self.get_point_position(hand, finger_one)
        position_f2 = self.get_point_position(hand, finger_two)

        if not (position_f1 and position_f2):
            return False

        if position_f2[0] >= position_f1[0] + self.NEAR_TOLLERANCE * x_toll or position_f2[0] <= position_f1[
            0] - self.NEAR_TOLLERANCE * x_toll:
            return False

        if position_f2[1] >= position_f1[1] + self.NEAR_TOLLERANCE * y_toll or position_f2[1] <= position_f1[
            1] - self.NEAR_TOLLERANCE * y_toll:
            return False

        return True

    def hand_close(self, hand):
        for finger in self.fingers:

            if self.is_finger_active(hand, finger):
                return False

        return True

    def draw_finger_area(self, img, hand, finger):
        position_f1 = self.get_point_position(hand, finger)

        cv2.rectangle(img, (position_f1[0] - self.NEAR_TOLLERANCE * 2, position_f1[1] - self.NEAR_TOLLERANCE),
                      (position_f1[0] + self.NEAR_TOLLERANCE * 2, position_f1[1] + self.NEAR_TOLLERANCE),
                      (255, 111, 111), cv2.FILLED)

    def detect_hand_inclination(self):
        p1 = self.get_point_position(0, 3)
        p2 = self.get_point_position(0, 17)

        self.handInclination = p1[1] - p2[1]
