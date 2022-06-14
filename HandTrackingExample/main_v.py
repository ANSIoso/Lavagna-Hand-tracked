import sys

from pyqt5_plugins.examplebutton import QtWidgets

from controller.BoardController import BoardController
from controller.HandDetector_c import HandDetector_c
from controller.Menu_C import MenuController
from model.Board_m import Board
from model.HandDetector_m import HandDetect
from model.ImageIO import ImageIO
from model.Menu_m import MenuM
from view.boardWindow import Ui_Board

# creating main window
app = QtWidgets.QApplication(sys.argv)
BoardW = QtWidgets.QMainWindow()

# creating object that takes care of take video stream
imgio = ImageIO()
imgio.daemon = True
imgio.want_flipped(True)
imgio.start()

# wait until the stream produce an actual image
while imgio.lastImage is None:
    print("loading")

# create the object that takes care of detect hand informations
hand_detector = HandDetect(imgio)
det_c = HandDetector_c(hand_detector)
det_c.daemon = True
det_c.start()

# create the board "logic"
board_m = Board()

# create menu logic and controller
menu_m = MenuM()
menu_c = MenuController(menu_m, board_m, hand_detector)

# create board ui and controller and connect them
board_m.init_board(imgio.lastImage)
board_c = BoardController(hand_detector, board_m, menu_c)
board_c.daemon = True
ui = Ui_Board(imgio, board_m)
ui.connect_timer(board_c)

ui.setupUi(BoardW, menu_c)
BoardW.show()

sys.exit(app.exec_())
