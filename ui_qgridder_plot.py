# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_plot.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QGridderPlot(object):
    def setupUi(self, QGridderPlot):
        QGridderPlot.setObjectName("QGridderPlot")
        QGridderPlot.resize(494, 526)
        self.verticalLayout = QtWidgets.QVBoxLayout(QGridderPlot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = Mplwidget(QGridderPlot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(470, 460))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(QGridderPlot)
        QtCore.QMetaObject.connectSlotsByName(QGridderPlot)

    def retranslateUi(self, QGridderPlot):
        _translate = QtCore.QCoreApplication.translate
        QGridderPlot.setWindowTitle(_translate("QGridderPlot", "Qgridder Plot"))

from mplwidget import Mplwidget
