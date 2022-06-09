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

app = QtWidgets.QApplication(sys.argv)
BoardW = QtWidgets.QMainWindow()

imgio = ImageIO()
imgio.daemon = True
imgio.want_flipped(True)
imgio.want_processing_info(True)
imgio.start()

board = Board()

while imgio.lastImage is None:
    print("ciao")
board.init_board(imgio.lastImage)

detector = HandDetect(imgio)
det_c = HandDetector_c(detector)
det_c.daemon = True
det_c.start()

ui = Ui_Board(imgio, board)
bc = BoardController(ui, detector, board)
bc.daemon = True
bc.start()

ui.setupUi(BoardW)

BoardW.show()
sys.exit(app.exec_())