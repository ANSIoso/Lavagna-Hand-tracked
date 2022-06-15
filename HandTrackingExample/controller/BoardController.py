import time

from PyQt5 import QtCore

from controller.Menu_C import MenuController
from model.Board_m import Board
from model.HandDetector_m import HandDetect


class BoardController(QtCore.QThread):
    # class used to interact with the board to:
    # - open menu
    # - report the position of the finger and draw
    # - apply the gesture detected to actual operation on the board
    # - update the interface of it

    update_signal = QtCore.pyqtSignal()

    def __init__(self, handDetector: HandDetect, boardM: Board, menu_c: MenuController, parent=None):
        super(BoardController, self).__init__(parent)

        self.board_ui = None
        self.handDetector = handDetector
        self.boardM = boardM

        # fields used to record last operation so the same can't be performed many times in sequence
        self.operation_actual = ""
        self.operation_old = ""

        # information about the condition of this tread
        self.is_running = False

        self.menu_ready_to_open = False

        self.menu_c = menu_c

    def run(self):
        # method used to describe the operation that the controller has to perform at each timestep

        self.is_running = True

        while True:
            # at the beginning there isn't an operation to perform
            self.operation_actual = ""

            if self.handDetector.exist_hand(0):
                # (checked that there is the first hand on the screen):
                # - if the INDEX and the MIDDLE ^0 aren't near, record the position of the INDEX
                #   as a point in the actual line
                # - in the opposite the actual line is over
                if self.handDetector.finger_near(0, self.handDetector.INDEX, self.handDetector.MIDDLE, 2):
                    self.try_set_operation("off")
                else:
                    p = self.handDetector.get_point_position(0, HandDetect.INDEX)
                    self.boardM.finger_on_board(p[0], p[1])

            if self.handDetector.exist_hand(1):
                if self.handDetector.hand_open(1):
                    self.menu_ready_to_open = True

                # (checked that there is the second hand on the screen):
                # - if the hand ^1 is closed and the menù is ready to open, open the menù
                if self.handDetector.hand_close(1) and self.menu_ready_to_open:
                    self.open_menu()
                    self.menu_ready_to_open = False

                # - if the THUMB and the PINKY ^1 are near, undo the last line
                if self.handDetector.finger_near(1, self.handDetector.THUMB, self.handDetector.PINKY):
                    self.try_set_operation("undo")

            # at the end of a time step apply the last operation that has been recorded
            self.applay_operation()

            # comunicate to update the gui
            self.update_signal.emit()
            time.sleep(0.02)

    def try_set_operation(self, new_operation):
        # method used to record the new operation to apply only if is different from the last one
        self.operation_actual = self.operation_old

        if self.operation_old != new_operation:
            self.operation_actual = new_operation

    def applay_operation(self):
        # method that apply the last operation recorded
        # and record it as the previous one
        if self.operation_actual != self.operation_old:
            if self.operation_actual == "off":
                self.boardM.finger_off_board()
            elif self.operation_actual == "undo":
                self.boardM.undo()

        self.operation_old = self.operation_actual

    def open_menu(self):
        # method that open the menù if it isn't already opened
        if self.menu_c.is_running:
            return

        self.menu_c.menu_m.open_menu()
        self.menu_c.start()
