# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/pythonProjects/tubitak-fuzzy/design/language.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lang_list_widget = QtWidgets.QListWidget(Dialog)
        self.lang_list_widget.setObjectName("lang_list_widget")
        self.verticalLayout.addWidget(self.lang_list_widget)
        self.selected_lan_text = QtWidgets.QLabel(Dialog)
        self.selected_lan_text.setText("")
        self.selected_lan_text.setObjectName("selected_lan_text")
        self.verticalLayout.addWidget(self.selected_lan_text)
        self.set_lan_button = QtWidgets.QPushButton(Dialog)
        self.set_lan_button.setObjectName("set_lan_button")
        self.verticalLayout.addWidget(self.set_lan_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.set_lan_button.setText(_translate("Dialog", "Seç"))

