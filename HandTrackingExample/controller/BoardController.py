import time
from threading import Thread

from controller.Menu_C import MenuController
from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.Menu_m import MenuM
from view.boardWindow import Ui_Board
from view.menu1 import MenuUi


class BoardController(Thread):

    def __init__(self, boardW: Ui_Board, handDetector: HandDetect, boardM: Board):
        super().__init__()

        self.boardW = boardW
        self.handDetector = handDetector
        self.boardM = boardM

        '''______________'''
        self.operation_actual = ""
        self.operation_old = ""
        '''______________'''

    def run(self):
        self.open_menu()
        while True:
            self.boardW.update_board()

            '''_______________________'''

            self.operation_actual = ""

            if not self.handDetector.exist_hand(1):
                time.sleep(0.02)
                continue

            if not self.handDetector.finger_near(0, self.handDetector.INDEX, self.handDetector.MIDDLE, 2):
                p = self.handDetector.get_point_position(0, HandDetect.INDEX)

                self.boardM.finger_on_board(p[0], p[1])
            else:
                self.try_set("off")

            if self.handDetector.finger_near(0, self.handDetector.THUMB, self.handDetector.PINKY):
                self.try_set("undo")

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

        self.operation_old = self.operation_actual

    def open_menu(self):
        m = MenuM()
        menu_ui = MenuUi(self.boardW.bo, m)

        menuC = MenuController(m, menu_ui, self.boardM, self.handDetector)
        menuC.daemon = True
        menuC.start()

        self.boardW.show_menu(menu_ui)