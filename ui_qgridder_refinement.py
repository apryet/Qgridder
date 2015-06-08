# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_refinement.ui'
#
# Created: Fri May 15 23:22:25 2015
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

class Ui_QGridderRefinement(object):
    def setupUi(self, QGridderRefinement):
        QGridderRefinement.setObjectName(_fromUtf8("QGridderRefinement"))
        QGridderRefinement.resize(548, 233)
        self.verticalLayout_7 = QtGui.QVBoxLayout(QGridderRefinement)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.labelGridLayer = QtGui.QLabel(QGridderRefinement)
        self.labelGridLayer.setObjectName(_fromUtf8("labelGridLayer"))
        self.horizontalLayout_11.addWidget(self.labelGridLayer)
        self.listGridLayer = QtGui.QComboBox(QGridderRefinement)
        self.listGridLayer.setEnabled(True)
        self.listGridLayer.setObjectName(_fromUtf8("listGridLayer"))
        self.horizontalLayout_11.addWidget(self.listGridLayer)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.label_9 = QtGui.QLabel(QGridderRefinement)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_7.addWidget(self.label_9)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_11 = QtGui.QLabel(QGridderRefinement)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout.addWidget(self.label_11)
        self.sboxDivideHoriz = QtGui.QSpinBox(QGridderRefinement)
        self.sboxDivideHoriz.setMinimum(1)
        self.sboxDivideHoriz.setMaximum(100)
        self.sboxDivideHoriz.setObjectName(_fromUtf8("sboxDivideHoriz"))
        self.horizontalLayout.addWidget(self.sboxDivideHoriz)
        self.label_10 = QtGui.QLabel(QGridderRefinement)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout.addWidget(self.label_10)
        self.sboxDivideVert = QtGui.QSpinBox(QGridderRefinement)
        self.sboxDivideVert.setMinimum(1)
        self.sboxDivideVert.setMaximum(100)
        self.sboxDivideVert.setObjectName(_fromUtf8("sboxDivideVert"))
        self.horizontalLayout.addWidget(self.sboxDivideVert)
        self.checkDivideRatio = QtGui.QCheckBox(QGridderRefinement)
        self.checkDivideRatio.setObjectName(_fromUtf8("checkDivideRatio"))
        self.horizontalLayout.addWidget(self.checkDivideRatio)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.checkTopo = QtGui.QCheckBox(QGridderRefinement)
        self.checkTopo.setObjectName(_fromUtf8("checkTopo"))
        self.horizontalLayout_8.addWidget(self.checkTopo)
        spacerItem = QtGui.QSpacerItem(128, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.progressBarRegularRefine = QtGui.QProgressBar(QGridderRefinement)
        self.progressBarRegularRefine.setProperty("value", 0)
        self.progressBarRegularRefine.setObjectName(_fromUtf8("progressBarRegularRefine"))
        self.horizontalLayout_2.addWidget(self.progressBarRegularRefine)
        self.labelIterations = QtGui.QLabel(QGridderRefinement)
        self.labelIterations.setObjectName(_fromUtf8("labelIterations"))
        self.horizontalLayout_2.addWidget(self.labelIterations)
        self.labelIter = QtGui.QLabel(QGridderRefinement)
        self.labelIter.setObjectName(_fromUtf8("labelIter"))
        self.horizontalLayout_2.addWidget(self.labelIter)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonRefine = QtGui.QPushButton(QGridderRefinement)
        self.buttonRefine.setObjectName(_fromUtf8("buttonRefine"))
        self.horizontalLayout_2.addWidget(self.buttonRefine)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)

        self.retranslateUi(QGridderRefinement)
        QtCore.QMetaObject.connectSlotsByName(QGridderRefinement)

    def retranslateUi(self, QGridderRefinement):
        QGridderRefinement.setWindowTitle(_translate("QGridderRefinement", "Qgridder Refinement", None))
        self.labelGridLayer.setText(_translate("QGridderRefinement", "Grid layer :", None))
        self.label_9.setText(_translate("QGridderRefinement", "Divide by :", None))
        self.label_11.setText(_translate("QGridderRefinement", "horizontally :", None))
        self.label_10.setText(_translate("QGridderRefinement", "vertically :", None))
        self.checkDivideRatio.setText(_translate("QGridderRefinement", "Lock 1:1 ratio", None))
        self.checkTopo.setText(_translate("QGridderRefinement", "Check topology  for selected model type", None))
        self.labelIterations.setText(_translate("QGridderRefinement", "Iterations : ", None))
        self.labelIter.setText(_translate("QGridderRefinement", "0", None))
        self.buttonRefine.setText(_translate("QGridderRefinement", "Refine selection ", None))

