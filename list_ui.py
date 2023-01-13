# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListForm(object):
    def setupUi(self, ListForm):
        ListForm.setObjectName("ListForm")
        ListForm.resize(713, 463)
        self.tableView = QtWidgets.QTableView(ListForm)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 621, 461))
        self.tableView.setObjectName("tableView")
        self.verticalLayoutWidget = QtWidgets.QWidget(ListForm)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(620, 10, 91, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_add = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.verticalLayout.addWidget(self.pushButton_add)
        self.pushButton_edit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.verticalLayout.addWidget(self.pushButton_edit)
        self.pushButton_del = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_del.setObjectName("pushButton_del")
        self.verticalLayout.addWidget(self.pushButton_del)

        self.retranslateUi(ListForm)
        QtCore.QMetaObject.connectSlotsByName(ListForm)

    def retranslateUi(self, ListForm):
        _translate = QtCore.QCoreApplication.translate
        ListForm.setWindowTitle(_translate("ListForm", "Form"))
        self.pushButton_add.setText(_translate("ListForm", "添加"))
        self.pushButton_edit.setText(_translate("ListForm", "编辑"))
        self.pushButton_del.setText(_translate("ListForm", "删除"))

