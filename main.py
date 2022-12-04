import sys
import traceback
from PyQt5.QtWidgets import *
from main_mamdani import MainScreen


# sugeno trapezoidal func için graf eklemeyi ekle

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


# fuzzy_ctrl()

sys.excepthook = excepthook
app = QApplication([])
window = MainScreen()
window.show()
ret = app.exec_()
sys.exit(ret)
