# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '12.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 800)
        MainWindow.setMinimumSize(QtCore.QSize(480, 800))
        MainWindow.setMaximumSize(QtCore.QSize(480, 800))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Downloads/Pi.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color:rgb(66, 66, 66);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.preview = QtWidgets.QGraphicsView(self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(30, 150, 421, 321))
        self.preview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.preview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.preview.setObjectName("preview")
        self.on = QtWidgets.QToolButton(self.centralwidget)
        self.on.setGeometry(QtCore.QRect(140, 580, 191, 61))
        self.on.setStyleSheet("\n"
"background-color:rgb(8, 170, 5);\n"
"color:rgb(255,255,255);\n"
"font: 8pt \"IMPACT\";\n"
"font-size:22px;")
        self.on.setCheckable(True)
        self.on.setChecked(False)
        self.on.setObjectName("on")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 680, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-70, 20, 621, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.user = QtWidgets.QLabel(self.centralwidget)
        self.user.setGeometry(QtCore.QRect(110, 520, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.user.setFont(font)
        self.user.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size:22px;")
        self.user.setAlignment(QtCore.Qt.AlignCenter)
        self.user.setWordWrap(True)
        self.user.setObjectName("user")
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(110, 700, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.status.setFont(font)
        self.status.setStyleSheet("color: rgb(255, 255, 255);")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setWordWrap(True)
        self.status.setObjectName("status")
        self.preview.raise_()
        self.on.raise_()
        self.label.raise_()
        self.user.raise_()
        self.status.raise_()
        self.label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.on.setText(_translate("MainWindow", "Démarrer "))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">ACCES</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Système de Contrôle d\'Accès</span></p><p align=\"center\"><span style=\" color:#ffffff;\">par Biométrie</span></p></body></html>"))
        self.user.setText(_translate("MainWindow", " "))
        self.status.setText(_translate("MainWindow", "Non Autorisé"))

