from PyQt5.QtWidgets import QMessageBox


class ErrorMessage:
    def __init__(self, title, content):
        self.msg = QMessageBox()
        self.msg.setText(content)
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setWindowTitle(title)

    def show(self):
        self.msg.exec_()
