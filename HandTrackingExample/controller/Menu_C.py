import time

from PyQt5 import QtCore

from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.MenuOptions import MenuOptions
from model.Menu_m import MenuM


class MenuController(QtCore.QThread):
    update_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()

    def __init__(self, menu: MenuM, board: Board, hand_detector: HandDetect, parent=None):
        super(MenuController, self).__init__(parent)

        self.menu_m = menu
        self.board = board
        self.hand_detector = hand_detector

        self.tolerance = 40

        self.selection_time = 3
        self.selection_timer = 0

        self.is_running = False
        self.close_signal.connect(self.stop)

    def run(self):
        while True:
            '''menu_pos = self.hand_detector.get_point_position(1, 2)
            self.menu_m.menu_pos_x = menu_pos[0]
            self.menu_m.menu_pos_y = menu_pos[1]'''

            self.hand_detector.detect_hand_inclination()
            hand_inclination = self.hand_detector.handInclination
            self.navigate_menu_option(hand_inclination)

            self.select_menu_option()
            self.menu_m.selection_time = self.selection_timer

            self.update_signal.emit()
            time.sleep(0.5)

    def start(self):
        if self.is_running:
            return

        self.is_running = True
        self.menu_m.open_menu()
        super().start()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        self.menu_m.close_menu()
        self.terminate()

    def navigate_menu_option(self, val):
        if -self.tolerance < val and val < self.tolerance:
            return

        if val < -self.tolerance:
            self.menu_m.previous_choice()

        if val > self.tolerance:
            self.menu_m.next_choice()

    def select_menu_option(self):
        if not self.hand_detector.hand_close(1):
            self.reset_timer()
            return

        self.selection_timer += 1

        if self.selection_timer < self.selection_time:
            return

        self.reset_timer()
        self.apply_selection()

    def reset_timer(self):
        if self.selection_timer == 0:
            return

        self.selection_timer = 0

    def apply_selection(self):
        if self.menu_m.actual_section != self.menu_m.INITIAL:
            self.apply_board_modification()
            return

        if self.menu_m.get_choice() == MenuOptions.exit:
            self.close_signal.emit()

        if self.menu_m.get_choice() == MenuOptions.change_colors:
            self.menu_m.load_option(self.menu_m.COLORS)

        if self.menu_m.get_choice() == MenuOptions.pencil_thickness:
            self.menu_m.load_option(self.menu_m.THICKNESS)

        if self.menu_m.get_choice() == MenuOptions.switch_mode:
            self.board.change_mode()
            self.close_signal.emit()

    def apply_board_modification(self):
        if self.menu_m.actual_section == self.menu_m.COLORS:
            self.board.color = self.menu_m.get_choice()[1]

        if self.menu_m.actual_section == self.menu_m.THICKNESS:
            self.board.dimension = self.menu_m.get_choice()[1]

        self.close_signal.emit()

