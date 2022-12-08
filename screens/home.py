from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from design.home_python import Ui_MainWindow as HomeWindow
from screens.main_mamdani import MainScreen


class HomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home_ui = HomeWindow()
        self.home_ui.setupUi(self)
        self.setWindowTitle("Home")
        style = """
        QPushButton{
        background-color: white;
        border-style: outset;
        border-width: 2px;
        border-radius: 15px;
        border-color: white;
        padding:10px;
        margin: 10px;
        }
        """
        self.setStyleSheet(style)

        self.home_ui.modul1.clicked.connect(self.modul1)

    def modul1(self):
        self.mamdani = MainScreen()
        self.mamdani.show()
