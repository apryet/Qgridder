# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_export.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QGridderExport(object):
    def setupUi(self, QGridderExport):
        QGridderExport.setObjectName("QGridderExport")
        QGridderExport.resize(355, 195)
        self.gridLayout = QtWidgets.QGridLayout(QGridderExport)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_12 = QtWidgets.QLabel(QGridderExport)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.listGridLayer = QtWidgets.QComboBox(QGridderExport)
        self.listGridLayer.setObjectName("listGridLayer")
        self.verticalLayout.addWidget(self.listGridLayer)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(QGridderExport)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.textOutTextFileName = QtWidgets.QLineEdit(QGridderExport)
        self.textOutTextFileName.setObjectName("textOutTextFileName")
        self.horizontalLayout_17.addWidget(self.textOutTextFileName)
        self.buttonBrowseOutputFile = QtWidgets.QPushButton(QGridderExport)
        self.buttonBrowseOutputFile.setObjectName("buttonBrowseOutputFile")
        self.horizontalLayout_17.addWidget(self.buttonBrowseOutputFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_17)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.buttonExportTextFile = QtWidgets.QPushButton(QGridderExport)
        self.buttonExportTextFile.setObjectName("buttonExportTextFile")
        self.horizontalLayout_5.addWidget(self.buttonExportTextFile)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)

        self.retranslateUi(QGridderExport)
        QtCore.QMetaObject.connectSlotsByName(QGridderExport)

    def retranslateUi(self, QGridderExport):
        _translate = QtCore.QCoreApplication.translate
        QGridderExport.setWindowTitle(_translate("QGridderExport", "Qgridder Export"))
        self.label_12.setText(_translate("QGridderExport", "Grid layer :"))
        self.label.setText(_translate("QGridderExport", "Output file :"))
        self.buttonBrowseOutputFile.setText(_translate("QGridderExport", "Browse ..."))
        self.buttonExportTextFile.setText(_translate("QGridderExport", "Export"))

