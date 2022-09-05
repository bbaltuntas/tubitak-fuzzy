# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/pythonProjects/fuzzyProject/design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inputButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputButton.sizePolicy().hasHeightForWidth())
        self.inputButton.setSizePolicy(sizePolicy)
        self.inputButton.setStyleSheet("")
        self.inputButton.setObjectName("inputButton")
        self.verticalLayout.addWidget(self.inputButton)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_7.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_7.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.verticalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.inputList = QtWidgets.QListWidget(self.centralwidget)
        self.inputList.setObjectName("inputList")
        self.verticalLayout_6.addWidget(self.inputList)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.outputList = QtWidgets.QListView(self.centralwidget)
        self.outputList.setObjectName("outputList")
        self.verticalLayout_5.addWidget(self.outputList)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setObjectName("listView_2")
        self.verticalLayout_4.addWidget(self.listView_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Input_Variable = QtWidgets.QAction(MainWindow)
        self.actionAdd_Input_Variable.setObjectName("actionAdd_Input_Variable")
        self.actionAdd_Output_Variable = QtWidgets.QAction(MainWindow)
        self.actionAdd_Output_Variable.setObjectName("actionAdd_Output_Variable")
        self.actionAdd_Mamdani_Rules = QtWidgets.QAction(MainWindow)
        self.actionAdd_Mamdani_Rules.setObjectName("actionAdd_Mamdani_Rules")
        self.menuEdit.addAction(self.actionAdd_Input_Variable)
        self.menuEdit.addAction(self.actionAdd_Output_Variable)
        self.menuEdit.addAction(self.actionAdd_Mamdani_Rules)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.inputButton.setText(_translate("MainWindow", "Input Variables"))
        self.pushButton_3.setText(_translate("MainWindow", "Output Variables"))
        self.pushButton_2.setText(_translate("MainWindow", "Mamdani Rules"))
        self.label.setText(_translate("MainWindow", "Input Variables"))
        self.label_2.setText(_translate("MainWindow", "Output Variables"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionAdd_Input_Variable.setText(_translate("MainWindow", "Add Input Variable"))
        self.actionAdd_Output_Variable.setText(_translate("MainWindow", "Add Output Variable"))
        self.actionAdd_Mamdani_Rules.setText(_translate("MainWindow", "Add Mamdani Rules"))
