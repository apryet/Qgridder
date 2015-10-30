# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_preproc.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_QGridderPreProc(object):
    def setupUi(self, QGridderPreProc):
        QGridderPreProc.setObjectName(_fromUtf8("QGridderPreProc"))
        QGridderPreProc.resize(400, 110)
        self.gridLayout = QtGui.QGridLayout(QGridderPreProc)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.labelGridLayer = QtGui.QLabel(QGridderPreProc)
        self.labelGridLayer.setObjectName(_fromUtf8("labelGridLayer"))
        self.horizontalLayout_11.addWidget(self.labelGridLayer)
        self.listGridLayer = QtGui.QComboBox(QGridderPreProc)
        self.listGridLayer.setEnabled(True)
        self.listGridLayer.setObjectName(_fromUtf8("listGridLayer"))
        self.horizontalLayout_11.addWidget(self.listGridLayer)
        self.gridLayout.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.buttonProceedNumbering = QtGui.QPushButton(QGridderPreProc)
        self.buttonProceedNumbering.setObjectName(_fromUtf8("buttonProceedNumbering"))
        self.horizontalLayout_13.addWidget(self.buttonProceedNumbering)
        self.gridLayout.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(48, 164, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)

        self.retranslateUi(QGridderPreProc)
        QtCore.QMetaObject.connectSlotsByName(QGridderPreProc)

    def retranslateUi(self, QGridderPreProc):
        QGridderPreProc.setWindowTitle(_translate("QGridderPreProc", "Qgridder Pre-processing", None))
        self.labelGridLayer.setText(_translate("QGridderPreProc", "Grid layer :", None))
        self.buttonProceedNumbering.setText(_translate("QGridderPreProc", "Proceed to numbering", None))

