from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class MenuOption(QWidget):

    def __init__(self, parent=None, option_name=None):
        QWidget.__init__(self, parent=parent)
        self.lay = QHBoxLayout(self)

        self.name = self.add_option_name(option_name)
        # codice da cambiare provvisorio per immagine
        # self.name = self.add_option_name("ooo")

    def add_option_name(self, content):
        # method used to add a name to a menu option
        label = QLabel(content, self)

        self.lay.addWidget(label)

        return label

    def add_option_picture(self, img):
        # method used to add an icon/reference_picture to a menu option
        label = QLabel(self)

        self.label.setPixmap(QPixmap(img))

        self.lay.addWidget(label)

        return label
