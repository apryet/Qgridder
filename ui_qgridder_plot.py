# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_plot.ui'
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

class Ui_QGridderPlot(object):
    def setupUi(self, QGridderPlot):
        QGridderPlot.setObjectName(_fromUtf8("QGridderPlot"))
        QGridderPlot.resize(494, 526)
        self.verticalLayout = QtGui.QVBoxLayout(QGridderPlot)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = Mplwidget(QGridderPlot)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(470, 460))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(QGridderPlot)
        QtCore.QMetaObject.connectSlotsByName(QGridderPlot)

    def retranslateUi(self, QGridderPlot):
        QGridderPlot.setWindowTitle(_translate("QGridderPlot", "Qgridder Plot", None))

from mplwidget import Mplwidget
