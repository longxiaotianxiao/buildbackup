# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BuildDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(1027, 675)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OpenFileBtn = QtWidgets.QPushButton(self.frame)
        self.OpenFileBtn.setObjectName("OpenFileBtn")
        self.horizontalLayout.addWidget(self.OpenFileBtn)
        self.FilePathLabel = QtWidgets.QLabel(self.frame)
        self.FilePathLabel.setObjectName("FilePathLabel")
        self.horizontalLayout.addWidget(self.FilePathLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.WarehouseComBox = QtWidgets.QComboBox(self.frame)
        self.WarehouseComBox.setMinimumSize(QtCore.QSize(100, 0))
        self.WarehouseComBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.WarehouseComBox.setObjectName("WarehouseComBox")
        self.horizontalLayout.addWidget(self.WarehouseComBox)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FileTreeWidget = QtWidgets.QTreeWidget(self.frame_2)
        self.FileTreeWidget.setAlternatingRowColors(True)
        self.FileTreeWidget.setObjectName("FileTreeWidget")
        self.FileTreeWidget.headerItem().setText(0, "1")
        self.FileTreeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.FileTreeWidget)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(dialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.BackupLabel = QtWidgets.QLabel(self.frame_3)
        self.BackupLabel.setObjectName("BackupLabel")
        self.verticalLayout_2.addWidget(self.BackupLabel)
        self.StatusTextEdit = QtWidgets.QTextEdit(self.frame_3)
        self.StatusTextEdit.setObjectName("StatusTextEdit")
        self.verticalLayout_2.addWidget(self.StatusTextEdit)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(dialog)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.BuildBtn = QtWidgets.QPushButton(self.frame_4)
        self.BuildBtn.setObjectName("BuildBtn")
        self.horizontalLayout_2.addWidget(self.BuildBtn)
        self.verticalLayout_3.addWidget(self.frame_4)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "数据库备份恢复工具"))
        self.OpenFileBtn.setText(_translate("dialog", "打开合集根目录路径"))
        self.FilePathLabel.setText(_translate("dialog", "已选择合集路径:c://"))
        self.label_2.setText(_translate("dialog", "选择分支："))
        self.BackupLabel.setText(_translate("dialog", "最近版本的backup:"))
        self.BuildBtn.setText(_translate("dialog", "生成"))

