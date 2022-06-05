import time
from threading import Thread

from model.Board_m import Board
from model.HandDataCalculator import HandDetect
from model.ImageIO import ImageIO
from view.boardWindow import Ui_Board


class BoardController(Thread):

    def __init__(self, boardW: Ui_Board, image_io: ImageIO, handDetector: HandDetect, boardM: Board):
        super().__init__()

        self.boardW = boardW
        self.image_io = image_io
        self.handDetector = handDetector
        self.boardM = boardM

        '''______________'''
        self.operation_actual = ""
        self.operation_old = ""
        '''______________'''

    def run(self):
        while True:
            self.boardW.update_board()

            '''_______________________'''

            self.operation_actual = ""

            self.handDetector.detect_hands(self.image_io.lastImage)

            if not self.handDetector.get_point(0, HandDetect.INDEX):
                time.sleep(0.02)
                continue

            if not self.handDetector.finger_near(0, self.handDetector.INDEX, self.handDetector.MIDDLE, 2):
                p = self.handDetector.get_point_position(0, HandDetect.INDEX)

                self.boardM.finger_on_board(p[0], p[1])
            else:
                self.try_set("off")

            if self.handDetector.finger_near(0, self.handDetector.THUMB, self.handDetector.PINKY):
                self.try_set("undo")

            if self.handDetector.hand_close(0):
                self.try_set("mode")

            self.applay_operation()

            '''_______________________'''

            time.sleep(0.02)

    def try_set(self, new_operation):
        self.operation_actual = self.operation_old

        if self.operation_old != new_operation:
            self.operation_actual = new_operation

    def applay_operation(self):
        if self.operation_actual != self.operation_old:
            if self.operation_actual == "off":
                self.boardM.finger_off_board()
            elif self.operation_actual == "undo":
                self.boardM.undo()
            elif self.operation_actual == "mode":
                self.boardM.change_mode()

        self.operation_old = self.operation_actual