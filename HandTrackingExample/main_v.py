import sys

from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets

from controller.BoardController import BoardController
from controller.HandDetector_c import HandDetector_c
from controller.Menu_C import MenuController
from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.ImageIO import ImageIO
from model.Menu_m import MenuM
from view.boardWindow import Ui_Board


app = QtWidgets.QApplication(sys.argv)
BoardW = QtWidgets.QMainWindow()

imgio = ImageIO()
imgio.daemon = True
imgio.want_flipped(True)
imgio.start()

while imgio.lastImage is None:
    print("ciao")

hand_detector = HandDetect(imgio)
det_c = HandDetector_c(hand_detector)
det_c.daemon = True
det_c.start()

board_m = Board()

menu_m = MenuM()
menu_c = MenuController(menu_m, board_m, hand_detector)

board_m.init_board(imgio.lastImage)
board_c = BoardController(hand_detector, board_m, menu_c)
board_c.daemon = True
ui = Ui_Board(imgio, board_m)
ui.connect_timer(board_c)

ui.setupUi(BoardW, menu_c)
BoardW.show()

sys.exit(app.exec_())
