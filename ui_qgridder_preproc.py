# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_preproc.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QGridderPreProc(object):
    def setupUi(self, QGridderPreProc):
        QGridderPreProc.setObjectName("QGridderPreProc")
        QGridderPreProc.resize(400, 110)
        self.gridLayout = QtWidgets.QGridLayout(QGridderPreProc)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.labelGridLayer = QtWidgets.QLabel(QGridderPreProc)
        self.labelGridLayer.setObjectName("labelGridLayer")
        self.horizontalLayout_11.addWidget(self.labelGridLayer)
        self.listGridLayer = QtWidgets.QComboBox(QGridderPreProc)
        self.listGridLayer.setEnabled(True)
        self.listGridLayer.setObjectName("listGridLayer")
        self.horizontalLayout_11.addWidget(self.listGridLayer)
        self.gridLayout.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.buttonProceedNumbering = QtWidgets.QPushButton(QGridderPreProc)
        self.buttonProceedNumbering.setObjectName("buttonProceedNumbering")
        self.horizontalLayout_13.addWidget(self.buttonProceedNumbering)
        self.gridLayout.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(48, 164, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)

        self.retranslateUi(QGridderPreProc)
        QtCore.QMetaObject.connectSlotsByName(QGridderPreProc)

    def retranslateUi(self, QGridderPreProc):
        _translate = QtCore.QCoreApplication.translate
        QGridderPreProc.setWindowTitle(_translate("QGridderPreProc", "Qgridder Pre-processing"))
        self.labelGridLayer.setText(_translate("QGridderPreProc", "Grid layer :"))
        self.buttonProceedNumbering.setText(_translate("QGridderPreProc", "Proceed to numbering"))

