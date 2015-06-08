# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_check3D.ui'
#
# Created: Sat May 16 21:28:59 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_QGridderCheck3D(object):
    def setupUi(self, QGridderCheck3D):
        QGridderCheck3D.setObjectName(_fromUtf8("QGridderCheck3D"))
        QGridderCheck3D.resize(474, 396)
        self.gridLayout = QtGui.QGridLayout(QGridderCheck3D)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_25 = QtGui.QLabel(QGridderCheck3D)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout.addWidget(self.label_25, 0, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.listLayers3D = QtGui.QListWidget(QGridderCheck3D)
        self.listLayers3D.setObjectName(_fromUtf8("listLayers3D"))
        self.horizontalLayout_10.addWidget(self.listLayers3D)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.buttonLayer3DUp = QtGui.QPushButton(QGridderCheck3D)
        self.buttonLayer3DUp.setObjectName(_fromUtf8("buttonLayer3DUp"))
        self.verticalLayout_8.addWidget(self.buttonLayer3DUp)
        self.buttonLayer3DDown = QtGui.QPushButton(QGridderCheck3D)
        self.buttonLayer3DDown.setObjectName(_fromUtf8("buttonLayer3DDown"))
        self.verticalLayout_8.addWidget(self.buttonLayer3DDown)
        self.buttonLayer3DRemove = QtGui.QPushButton(QGridderCheck3D)
        self.buttonLayer3DRemove.setObjectName(_fromUtf8("buttonLayer3DRemove"))
        self.verticalLayout_8.addWidget(self.buttonLayer3DRemove)
        self.horizontalLayout_10.addLayout(self.verticalLayout_8)
        self.gridLayout.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(QGridderCheck3D)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label_23 = QtGui.QLabel(self.frame)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.verticalLayout_10.addWidget(self.label_23)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_21 = QtGui.QLabel(self.frame)
        self.label_21.setMaximumSize(QtCore.QSize(175, 16777215))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.horizontalLayout_14.addWidget(self.label_21)
        self.listReferenceGrid = QtGui.QComboBox(self.frame)
        self.listReferenceGrid.setObjectName(_fromUtf8("listReferenceGrid"))
        self.horizontalLayout_14.addWidget(self.listReferenceGrid)
        self.buttonAddNewLayer3D = QtGui.QPushButton(self.frame)
        self.buttonAddNewLayer3D.setMaximumSize(QtCore.QSize(140, 16777215))
        self.buttonAddNewLayer3D.setObjectName(_fromUtf8("buttonAddNewLayer3D"))
        self.horizontalLayout_14.addWidget(self.buttonAddNewLayer3D)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.label_24 = QtGui.QLabel(self.frame)
        self.label_24.setMaximumSize(QtCore.QSize(175, 16777215))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_16.addWidget(self.label_24)
        self.listExistingLayer = QtGui.QComboBox(self.frame)
        self.listExistingLayer.setObjectName(_fromUtf8("listExistingLayer"))
        self.horizontalLayout_16.addWidget(self.listExistingLayer)
        self.buttonAddExistingLayer3D = QtGui.QPushButton(self.frame)
        self.buttonAddExistingLayer3D.setMaximumSize(QtCore.QSize(140, 16777215))
        self.buttonAddExistingLayer3D.setObjectName(_fromUtf8("buttonAddExistingLayer3D"))
        self.horizontalLayout_16.addWidget(self.buttonAddExistingLayer3D)
        self.verticalLayout_10.addLayout(self.horizontalLayout_16)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBarCheck3D_2 = QtGui.QProgressBar(QGridderCheck3D)
        self.progressBarCheck3D_2.setProperty("value", 0)
        self.progressBarCheck3D_2.setObjectName(_fromUtf8("progressBarCheck3D_2"))
        self.horizontalLayout.addWidget(self.progressBarCheck3D_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCheck3D = QtGui.QPushButton(QGridderCheck3D)
        self.buttonCheck3D.setObjectName(_fromUtf8("buttonCheck3D"))
        self.horizontalLayout.addWidget(self.buttonCheck3D)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)

        self.retranslateUi(QGridderCheck3D)
        QtCore.QMetaObject.connectSlotsByName(QGridderCheck3D)

    def retranslateUi(self, QGridderCheck3D):
        QGridderCheck3D.setWindowTitle(_translate("QGridderCheck3D", "Qgridder 3D grid", None))
        self.label_25.setText(_translate("QGridderCheck3D", "List of layers (from top to bottom) : ", None))
        self.buttonLayer3DUp.setText(_translate("QGridderCheck3D", "Up", None))
        self.buttonLayer3DDown.setText(_translate("QGridderCheck3D", "Down", None))
        self.buttonLayer3DRemove.setText(_translate("QGridderCheck3D", "Remove", None))
        self.label_23.setText(_translate("QGridderCheck3D", "Add layer to list : ", None))
        self.label_21.setText(_translate("QGridderCheck3D", "New from reference grid :", None))
        self.buttonAddNewLayer3D.setText(_translate("QGridderCheck3D", "Add new layer...", None))
        self.label_24.setText(_translate("QGridderCheck3D", "Import existing layer : ", None))
        self.buttonAddExistingLayer3D.setText(_translate("QGridderCheck3D", "Add existing layer", None))
        self.buttonCheck3D.setText(_translate("QGridderCheck3D", "Check and correct 3D topology", None))

