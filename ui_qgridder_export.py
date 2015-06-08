# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_export.ui'
#
# Created: Fri May 15 23:22:24 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QGridderExport(object):
    def setupUi(self, QGridderExport):
        QGridderExport.setObjectName(_fromUtf8("QGridderExport"))
        QGridderExport.resize(355, 195)
        self.gridLayout = QtGui.QGridLayout(QGridderExport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_12 = QtGui.QLabel(QGridderExport)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.verticalLayout.addWidget(self.label_12)
        self.listGridLayer = QtGui.QComboBox(QGridderExport)
        self.listGridLayer.setObjectName(_fromUtf8("listGridLayer"))
        self.verticalLayout.addWidget(self.listGridLayer)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(QGridderExport)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.textOutTextFileName = QtGui.QLineEdit(QGridderExport)
        self.textOutTextFileName.setObjectName(_fromUtf8("textOutTextFileName"))
        self.horizontalLayout_17.addWidget(self.textOutTextFileName)
        self.buttonBrowseOutputFile = QtGui.QPushButton(QGridderExport)
        self.buttonBrowseOutputFile.setObjectName(_fromUtf8("buttonBrowseOutputFile"))
        self.horizontalLayout_17.addWidget(self.buttonBrowseOutputFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_17)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.buttonExportTextFile = QtGui.QPushButton(QGridderExport)
        self.buttonExportTextFile.setObjectName(_fromUtf8("buttonExportTextFile"))
        self.horizontalLayout_5.addWidget(self.buttonExportTextFile)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 60, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)

        self.retranslateUi(QGridderExport)
        QtCore.QMetaObject.connectSlotsByName(QGridderExport)

    def retranslateUi(self, QGridderExport):
        QGridderExport.setWindowTitle(_translate("QGridderExport", "Qgridder Export", None))
        self.label_12.setText(_translate("QGridderExport", "Grid layer :", None))
        self.label.setText(_translate("QGridderExport", "Output file :", None))
        self.buttonBrowseOutputFile.setText(_translate("QGridderExport", "Browse ...", None))
        self.buttonExportTextFile.setText(_translate("QGridderExport", "Export", None))

