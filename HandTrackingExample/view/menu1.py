from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.uic.properties import QtCore

from model import Menu_m
from view.menu_option1 import MenuOption


class MenuUi(QWidget):
    def __init__(self, parent = None, menu: Menu_m = None):
        QWidget.__init__(self, parent=parent)

        self.menu_m = menu

        self.lay = QVBoxLayout(self)

        self.setStyleSheet("""
                            #menu_list {
                                background-color: #4e5766;
                                border-radius: 5px;
                            }
        
                            #menu_list QLabel {
                                background-color: #434b58;
                                border-radius: 5px;
                                
                                qproperty-alignment: AlignCenter;
                                color: #f1f8f9;
                            }
                            
                            #chosen_option0 QLabel {
                                background-color: #ff7372;
                                border-radius: 5px;
                                
                                qproperty-alignment: AlignCenter;
                                color: #f1f8f9;
                            }
                            
                            #chosen_option1 QLabel {
                                background-color: #ff7372;
                                border-radius: 10px;
                                
                                qproperty-alignment: AlignCenter;
                                color: #f1f8f9;
                            }
                            
                            #chosen_option2 QLabel {
                                background-color: #ff7372;
                                border-radius: 15px;
                                
                                qproperty-alignment: AlignCenter;
                                color: #f1f8f9;
                            }
                            
                            #
                            """)

        self.option_list = QWidget(self)
        self.option_list.setObjectName("menu_list")
        self.option_list_lay = QVBoxLayout(self.option_list)

        self.lay.addWidget(self.option_list)

    def update(self):
        self.should_visualize_menu()

        self.clear_all_options()

        self.load_options()

        self.last_menu_section = self.menu_m.actual_section

    def load_options(self):
        option_count = 0

        for option in self.menu_m.actual_menu_option:
            self.add_option(option[0], option_count)
            option_count += 1

    def add_option(self, content, option_number):
        m_option = MenuOption(self.option_list, content)

        if option_number == self.menu_m.actual_choice:
            m_option.setObjectName("chosen_option" + str(self.menu_m.selection_time))

        self.option_list_lay.addWidget(m_option)

    def should_visualize_menu(self):
        self.setVisible(self.menu_m.open)

        #if not self.menu_m.open:
        #    return

        #self.move(self.menu_m.menu_pos_x, self.menu_m.menu_pos_y)

    def clear_all_options(self):
        for i in reversed(range(self.option_list_lay.count())):
            self.option_list_lay.itemAt(i).widget().deleteLater()

    def connect_timer(self, timer):
        timer.update_signal.connect(self.update)