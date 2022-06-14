import time

from PyQt5 import QtCore

from controller.Menu_C import MenuController
from model.Board_m import Board
from model.HandDetector_m import HandDetect


class BoardController(QtCore.QThread):
    update_signal = QtCore.pyqtSignal()

    def __init__(self, handDetector: HandDetect, boardM: Board, menu_c: MenuController, parent=None):
        super(BoardController, self).__init__(parent)

        self.board_ui = None
        self.handDetector = handDetector
        self.boardM = boardM

        '''______________'''
        self.operation_actual = ""
        self.operation_old = ""
        '''______________'''

        self.is_running = False
        self.menu_c = menu_c

    def run(self):
        self.is_running = True

        while True:
            '''_______________________'''

            self.operation_actual = ""

            if self.handDetector.exist_hand(0):
                if not self.handDetector.finger_near(0, self.handDetector.INDEX, self.handDetector.MIDDLE, 2):
                    p = self.handDetector.get_point_position(0, HandDetect.INDEX)

                    self.boardM.finger_on_board(p[0], p[1])
                else:
                    self.try_set("off")

            if self.handDetector.exist_hand(1):

                if self.handDetector.is_finger_active(1, self.handDetector.THUMB) and self.handDetector.finger_near(1, self.handDetector.THUMB, self.handDetector.MIDDLE):
                    self.open_menu()

                if self.handDetector.finger_near(1, self.handDetector.THUMB, self.handDetector.PINKY):
                    self.try_set("undo")

            # encode hand out of screen closes menu

            self.applay_operation()
            '''_______________________'''

            self.update_signal.emit()
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

        self.operation_old = self.operation_actual

    def open_menu(self):
        if self.menu_c.is_running:
            return

        self.menu_c.menu_m.open_menu()
        self.menu_c.start()
