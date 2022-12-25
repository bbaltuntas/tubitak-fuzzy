from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from design.fis_python import Ui_MainWindow as HomeWindow
from screens.main_mamdani import MainScreen as MamdaniScreen
from screens.main_sugeno import MainSugeno as SugenoScreen


class HomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home_ui = HomeWindow()
        self.home_ui.setupUi(self)
        self.setWindowTitle("Home")

        self.home_ui.mamdaniButton.clicked.connect(self.open_mamdani)
        self.home_ui.sugenoButton.clicked.connect(self.open_sugeno)

    def open_mamdani(self):
        self.mamdani = MamdaniScreen()
        self.mamdani.show()

    def open_sugeno(self):
        self.sugeno = SugenoScreen()

