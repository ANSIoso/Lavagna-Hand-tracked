import cv2
import mediapipe as mp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from model.ImageIO import ImageIO


class HandDetect:
    # class used to get information about the hands as:
    #  - inclination of them
    #  - position of the fingers

    # identifier of each finger
    THUMB = 4
    INDEX = 8
    MIDDLE = 12
    RING = 16
    PINKY = 20

    # amount of space in where the fingers are considered near
    NEAR_TOLLERANCE = 30

    def __init__(self, image_io: ImageIO):
        # object used for capturing images
        self.image_io = image_io

        # field with all the computed data on the hands
        self.result = None

        # field that contains the dimensions of the image that must be computed
        self.w_img = None
        self.h_img = None

        # points of the hand that indicates the deadzone of it
        # (if a finger enter this zone is considered "not active")
        self.hand_inactivity_zone = [0, 1, 2, 3, 6, 10, 14, 18]

        self.fingers = [self.THUMB, self.INDEX, self.MIDDLE, self.RING, self.PINKY]

        # utility class for open cv
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

        # field that indicates the number of hand that are detected
        self.n_hands = 0
        # field that indicates the inclination of the hand
        self.handInclination = 0


    def detect_hands(self):
        # method used for calculate all the information about the hands

        # 1- get the last image taken by imageIO
        # 2- retrive information about the image
        # 3- convert the image in RGB
        # 4- pass the converted RGBimage to cv2
        # 5- if cv2 found data calculate number of hands

        img = self.image_io.lastImage
        self.h_img, self.w_img, c = img.shape

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            self.n_hands = len(self.result.multi_hand_landmarks)

    def draw_tracked_hand(self, img):
        # method used to draw the hand landmarks on an image
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def exist_hand(self, hand):
        # found if a hand has been detected
        if not self.result or not self.result.multi_hand_landmarks:
            return False

        if self.n_hands <= hand:
            return False

        return True

    def get_point(self, hand, point):
        # method that return the data on a point of a hand
        if not self.result.multi_hand_landmarks:
            return False

        if not self.exist_hand(hand):
            return False

        return self.result.multi_hand_landmarks[hand - 1].landmark[point]

    def get_point_position(self, hand, point):
        # method that return the position of a point of a hand
        point = self.get_point(hand, point)

        if not point:
            return False

        return int(point.x * self.w_img), int(point.y * self.h_img)

    def is_finger_active(self, hand, finger):
        # found if a finger is out of the deadzone

        # found the position of a finger
        finger_position = self.get_point_position(hand, finger)
        if not finger_position:
            return False

        # create a polygon with all the points of the deadzone
        points = []
        for point in self.hand_inactivity_zone:
            points.append(self.get_point_position(hand, point))

        p = Point(finger_position)
        polygon = Polygon(points)

        # check if the point that i'm looking for is in the poligon
        return not polygon.contains(p)

    def finger_near(self, hand, finger_one, finger_two, x_toll=1, y_toll=1):
        # method that check if two fingers are near
        position_f1 = self.get_point_position(hand, finger_one)
        position_f2 = self.get_point_position(hand, finger_two)

        if not (position_f1 and position_f2):
            return False

        # if  !((finger1.x - tollerance) > finger2.x > (finger1.x + tollerance))
        # the two finger are not near on the x axis

        if position_f2[0] >= position_f1[0] + self.NEAR_TOLLERANCE * x_toll or position_f2[0] <= position_f1[
            0] - self.NEAR_TOLLERANCE * x_toll:
            return False

        # if  !((finger1.y - tollerance) > finger2.y > (finger1.y + tollerance))
        # the two finger are not near on the y axis

        if position_f2[1] >= position_f1[1] + self.NEAR_TOLLERANCE * y_toll or position_f2[1] <= position_f1[
            1] - self.NEAR_TOLLERANCE * y_toll:
            return False

        return True

    def hand_close(self, hand):
        # method that check if the hand is closed

        if not self.exist_hand(hand):
            return False

        # for each finger check if it is active, if it found an active one
        # the hand is not closed
        for finger in self.fingers:
            if self.is_finger_active(hand, finger):
                return False

        return True

    def draw_finger_area(self, img, hand, finger):
        # method that draw the "influence area" of a finger

        position_f1 = self.get_point_position(hand, finger)

        cv2.rectangle(img, (position_f1[0] - self.NEAR_TOLLERANCE * 2, position_f1[1] - self.NEAR_TOLLERANCE),
                      (position_f1[0] + self.NEAR_TOLLERANCE * 2, position_f1[1] + self.NEAR_TOLLERANCE),
                      (255, 111, 111), cv2.FILLED)

    def detect_hand_inclination(self):
        # method that calculate the inclination of the hand
        # taken two points in the hand (first point) - (second point) we can get 3 results:
        #                              - = 0 the hand is straight
        #                              - > 0 bent
        #                              - < 0 bent

        if not self.exist_hand(1):
            return

        p1 = self.get_point_position(1, 3)
        p2 = self.get_point_position(1, 17)

        self.handInclination = p1[1] - p2[1]
