from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from model import Menu_m
from view.menu_option1 import MenuOption


class MenuUi(QWidget):

    def __init__(self, parent = None, menu: Menu_m = None):
        QWidget.__init__(self, parent=parent)
        self.menu_m = menu

        self.lay = QVBoxLayout(self)

        self.label_title = QLabel("Menu", self)
        self.lay.addWidget(self.label_title)

        self.option_list = QWidget(self)
        self.option_list_lay = QVBoxLayout(self.option_list)

        self.lay.addWidget(self.option_list)

        self.last_menu_section = ""

    def add_option(self, content):
        m_option = MenuOption(self.option_list, content)
        self.option_list_lay.addWidget(m_option)

    def update(self):
        if self.menu_m.actual_section == self.last_menu_section:
            return

        print("test " + str(self.menu_m.actual_section))
        self.clear_all_options()

        for option in self.menu_m.actual_menu_option:
            self.add_option(option[0])

    def clear_all_options(self):
        for i in reversed(range(self.option_list_lay.count())):
            self.option_list_lay.itemAt(i).widget().deleteLater()