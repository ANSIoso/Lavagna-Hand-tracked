import time

from PyQt5 import QtCore

from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.MenuOptions import MenuOptions
from model.Menu_m import MenuM


class MenuController(QtCore.QThread):
    # class used to interact with the menu to:
    # - navigate through it
    # - update the interface of it

    update_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()

    def __init__(self, menu: MenuM, board: Board, hand_detector: HandDetect, parent=None):
        super(MenuController, self).__init__(parent)

        self.menu_m = menu
        self.board = board
        self.hand_detector = hand_detector

        # value in which a rotation is not considered for moving in the menù
        self.tolerance = 40

        # time step needed to select an option in the menù
        self.selection_time = 3
        self.selection_timer = 0

        # information about the condition of this tread
        self.is_running = False
        self.close_signal.connect(self.stop)

    def run(self):
        # method used to describe the operation that the controller has to perform at each timestep

        while True:
            '''menu_pos = self.hand_detector.get_point_position(1, 2)
            self.menu_m.menu_pos_x = menu_pos[0]
            self.menu_m.menu_pos_y = menu_pos[1]'''

            # detect the inclination of the "menu hand" if it is enough
            # navigate through the menù based on the "dirction"
            self.hand_detector.detect_hand_inclination()
            hand_inclination = self.hand_detector.handInclination
            self.navigate_menu_option(hand_inclination)

            # check if the user is trying to select an option
            self.select_menu_option()
            self.menu_m.selection_time = self.selection_timer

            # update the interface
            self.update_signal.emit()
            time.sleep(0.5)

    def start(self):
        if self.is_running:
            return

        self.is_running = True
        # reset the structure of menu as is it fresh opened
        self.menu_m.open_menu()
        super().start()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        self.menu_m.close_menu()
        self.terminate()

    def navigate_menu_option(self, val):
        # check if the inclination is enough
        if -self.tolerance < val and val < self.tolerance:
            return

        # based on the inclination move in the menù in the right direction
        if val < -self.tolerance:
            self.menu_m.previous_choice()

        if val > self.tolerance:
            self.menu_m.next_choice()

    def select_menu_option(self):
        # the user is trying to select an option if he has closed the second hand
        if not self.hand_detector.hand_close(1):
            # if the selection is nullified or not exist the timer is reset
            self.reset_timer()
            return

        self.selection_timer += 1

        if self.selection_timer < self.selection_time:
            return

        # when the selection lasts for long enough:
        # - the timer is reset and the operation applied
        self.reset_timer()
        self.apply_selection()

    def reset_timer(self):
        if self.selection_timer == 0:
            return

        self.selection_timer = 0

    def apply_selection(self):
        # based on what is the operation recorded in the menù

        if self.menu_m.actual_section != self.menu_m.INITIAL:
            # if is the actual section is not INITIAL you want to modify bord parameters
            self.apply_board_modification()
            return

        # instead, based on the choice of INITIAL menù you can:

        # - close menu
        if self.menu_m.get_choice() == MenuOptions.exit:
            self.close_signal.emit()

        # - load color section of the menù
        if self.menu_m.get_choice() == MenuOptions.change_colors:
            self.menu_m.load_option(self.menu_m.COLORS)

        # - load thickness section of the menù
        if self.menu_m.get_choice() == MenuOptions.pencil_thickness:
            self.menu_m.load_option(self.menu_m.THICKNESS)

        # - switch trough pen and eraser mode
        if self.menu_m.get_choice() == MenuOptions.switch_mode:
            self.board.change_mode()
            self.close_signal.emit()

    def apply_board_modification(self):
        # based on the menu choice and section you can

        # - change color of the brush
        if self.menu_m.actual_section == self.menu_m.COLORS:
            self.board.color = self.menu_m.get_choice()[1]

        # - change dimension of the brush
        if self.menu_m.actual_section == self.menu_m.THICKNESS:
            self.board.dimension = self.menu_m.get_choice()[1]

        # once the modification is applied close the menù
        self.close_signal.emit()

