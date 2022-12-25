# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/pythonProjects/tubitak-fuzzy/design/fis.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QMainWindow{\n"
"background-color:white;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mamdaniButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.mamdaniButton.setFont(font)
        self.mamdaniButton.setStyleSheet("QPushButton{\n"
"border: 1px solid transparent;\n"
"border-radius: 15px;\n"
"background-color:#1990EA;\n"
"padding: 15px;\n"
"margin :10px;\n"
"color:#fff;\n"
"}\n"
"QPushButton::hover{\n"
"background-color:white;\n"
"border: 1px solid #1990EA;\n"
"color:#000;\n"
"}\n"
"")
        self.mamdaniButton.setObjectName("mamdaniButton")
        self.horizontalLayout.addWidget(self.mamdaniButton)
        self.sugenoButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sugenoButton.setFont(font)
        self.sugenoButton.setStyleSheet("QPushButton{\n"
"border: 1px solid transparent;\n"
"border-radius: 15px;\n"
"background-color:#1990EA;\n"
"padding: 15px;\n"
"margin :10px;\n"
"color:#fff;\n"
"}\n"
"QPushButton::hover{\n"
"background-color:white;\n"
"border: 1px solid #1990EA;\n"
"color:#000\n"
"}\n"
"")
        self.sugenoButton.setObjectName("sugenoButton")
        self.horizontalLayout.addWidget(self.sugenoButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Bulanık Çıkarım Sistemi"))
        self.mamdaniButton.setText(_translate("MainWindow", "Mamdani Tipi Bulanık Çıkarım Sistemi"))
        self.sugenoButton.setText(_translate("MainWindow", "Sugeno Tipi Bulanık Çıkarım Sistemi"))

