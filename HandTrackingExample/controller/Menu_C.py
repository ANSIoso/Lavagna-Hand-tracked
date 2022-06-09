import time
from threading import Thread

from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.MenuOptions import MenuOptions
from model.Menu_m import MenuM
from view.menu1 import MenuUi


class MenuController(Thread):

    def __init__(self, menu: MenuM, menu_ui: MenuUi, board: Board, hand_detector: HandDetect):
        Thread.__init__(self)
        self.menu = menu
        self.menu_ui = menu_ui
        self.board = board
        self.hand_detector = hand_detector

        self.tolerance = 40

        self.selection_time = 3
        self.selection_timer = 0

    def run(self):
        while True:
            self.hand_detector.detect_hand_inclination()
            hand_inclination = self.hand_detector.handInclination
            self.navigate_menu_option(hand_inclination)

            print(self.menu.actual_menu_option[self.menu.actual_choice][0])
            print("incl =" + str(hand_inclination))

            self.select_menu_option()
            self.menu_ui.update()

            time.sleep(1)

    def navigate_menu_option(self, val):

        if -self.tolerance < val and val < self.tolerance:
            return

        if val < -self.tolerance:
            self.menu.previous_choice()

        if val > self.tolerance:
            self.menu.next_choice()

    def select_menu_option(self):
        if not self.hand_detector.hand_close(0):
            self.reset_timer()
            return

        print(self.selection_timer)
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
        if self.menu.actual_section != self.menu.INITIAL:
            self.apply_board_modification()
            return

        print("choice: " + self.menu.get_choice()[0])

        print("poss: " + MenuOptions.change_colors[0])
        if self.menu.get_choice() == MenuOptions.change_colors:
            self.menu.load_option(self.menu.COLORS)

        if self.menu.get_choice() == MenuOptions.pencil_thickness:
            self.menu.load_option(self.menu.THICKNESS)

        if self.menu.get_choice() == MenuOptions.switch_mode:
            self.board.change_mode()

    def apply_board_modification(self):
        if self.menu.actual_section == self.menu.COLORS:
            self.board.color = self.menu.get_choice()[1]

        if self.menu.actual_section == self.menu.THICKNESS:
            self.board.dimension = self.menu.get_choice()[1]

        self.menu.load_option(self.menu.INITIAL)