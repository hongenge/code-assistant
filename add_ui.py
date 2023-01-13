# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\add_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddForm(object):
    def setupUi(self, AddForm):
        AddForm.setObjectName("AddForm")
        AddForm.resize(598, 288)
        self.pushButton = QtWidgets.QPushButton(AddForm)
        self.pushButton.setGeometry(QtCore.QRect(480, 10, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(AddForm)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 10, 401, 272))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit_keyword = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_keyword.setObjectName("lineEdit_keyword")
        self.verticalLayout_2.addWidget(self.lineEdit_keyword)
        self.lineEdit_title = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.verticalLayout_2.addWidget(self.lineEdit_title)
        self.lineEdit_example = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_example.setObjectName("lineEdit_example")
        self.verticalLayout_2.addWidget(self.lineEdit_example)
        self.textEdit_Note = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit_Note.setObjectName("textEdit_Note")
        self.verticalLayout_2.addWidget(self.textEdit_Note)
        self.layoutWidget1 = QtWidgets.QWidget(AddForm)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 62, 101))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(AddForm)
        QtCore.QMetaObject.connectSlotsByName(AddForm)

    def retranslateUi(self, AddForm):
        _translate = QtCore.QCoreApplication.translate
        AddForm.setWindowTitle(_translate("AddForm", "添加"))
        self.pushButton.setText(_translate("AddForm", "添加"))
        self.label.setText(_translate("AddForm", "快捷短语："))
        self.label_2.setText(_translate("AddForm", "标题："))
        self.label_4.setText(_translate("AddForm", "例子："))
        self.label_3.setText(_translate("AddForm", "代码："))

