import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from controller.Menu_C import MenuController

from model.Board_m import Board
from model.ImageIO import ImageIO
from view.menu1 import MenuUi
from PIL import Image

import numpy as np

class Ui_Board(object):
    canvas_border = 30

    def __init__(self, image_io: ImageIO, board_data: Board):
        super().__init__()

        self.image_io = image_io
        self.board_data = board_data

        self.menu_ui = None

        self.pointer_dimension = 16

    def setupUi(self, Board, menu_c: MenuController):
        Board.setObjectName("Board")
        Board.resize(838, 619)

        self.central_widget = QtWidgets.QWidget(Board)
        self.central_widget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.boardCanvas = QtWidgets.QLabel(self.central_widget)
        self.boardCanvas.setText("")
        self.boardCanvas.setPixmap(QtGui.QPixmap("\images.png"))
        self.boardCanvas.setScaledContents(False)
        self.boardCanvas.setObjectName("screen")
        self.gridLayout.addWidget(self.boardCanvas, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)

        Board.setCentralWidget(self.central_widget)

        self.add_menu(menu_c)

        self.retranslateUi(Board)

        self.central_widget.setStyleSheet("""
                #screen {
                    border: 3px solid #4e5766;
                    border-radius: 5px;
                    background-color: rgb(255, 255, 255);
                }
                """)

        QtCore.QMetaObject.connectSlotsByName(Board)

    def retranslateUi(self, Board):
        _translate = QtCore.QCoreApplication.translate
        Board.setWindowTitle(_translate("Board", "MainWindow"))

    def update_board(self):
        # at each time step:
        # - take image from the picture capture class
        # - take the canvas
        # - combine it
        # - show it in the canvas

        cv_img = self.image_io.lastImage
        board_lines = self.board_data.canvas
        cv_img = cv2.add(board_lines, cv_img)

        cv_img = self.show_pointer(cv_img)

        if cv_img is None:
            return

        qt_img = self.convert_cv_qt(cv_img, self.central_widget.width(), self.central_widget.height())

        self.boardCanvas.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, area_w, area_h):
        # method used to convert an image taken from open cv to a
        # format that can be shown in a qtcanvas

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

        qt_img_w = area_w - self.canvas_border
        qt_img_h = area_h - self.canvas_border
        p = convert_to_Qt_format.scaled(qt_img_w, qt_img_h, Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)

    def connect_timer(self, timer):
        timer.start()
        timer.update_signal.connect(self.update_board)

    def add_menu(self, menu_c: MenuController):
        # method used to add the menu gui to the window

        self.menu_ui = MenuUi(self.central_widget, menu_c.menu_m)
        # the gui should be also connected to the controller to interact with it
        # and also to update it
        self.menu_ui.connect_timer(menu_c)

        self.menu_ui.setGeometry(100, 100, 200, 300)

        # at the beginning the menu is not visible it is shown only if requested by hand sign
        self.menu_ui.setVisible(False)

    def add_pointer_in_screen(self, screen_img, x, y):
        if self.board_data.mode == "draw":
            overlay = Image.open("../HandTrackingExample/resurces/pencil-solid.png")
        if self.board_data.mode == "delete":
            overlay = Image.open("../HandTrackingExample/resurces/eraser-solid.png")


        overlay = overlay.resize((self.pointer_dimension, self.pointer_dimension))
        overlay = overlay.convert("RGBA")

        background = Image.fromarray(screen_img)
        background.paste(overlay, (x, y-10), overlay)

        return np.asarray(background)

    def show_pointer(self, screen_canvas):
        if self.board_data.pointer_position is None:
            return screen_canvas

        x = self.board_data.pointer_position[0]
        y = self.board_data.pointer_position[1]

        return self.add_pointer_in_screen(screen_canvas, x, y)