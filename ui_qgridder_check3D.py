# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgridder_check3D.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QGridderCheck3D(object):
    def setupUi(self, QGridderCheck3D):
        QGridderCheck3D.setObjectName("QGridderCheck3D")
        QGridderCheck3D.resize(474, 396)
        self.gridLayout = QtWidgets.QGridLayout(QGridderCheck3D)
        self.gridLayout.setObjectName("gridLayout")
        self.label_25 = QtWidgets.QLabel(QGridderCheck3D)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 0, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.listLayers3D = QtWidgets.QListWidget(QGridderCheck3D)
        self.listLayers3D.setObjectName("listLayers3D")
        self.horizontalLayout_10.addWidget(self.listLayers3D)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.buttonLayer3DUp = QtWidgets.QPushButton(QGridderCheck3D)
        self.buttonLayer3DUp.setObjectName("buttonLayer3DUp")
        self.verticalLayout_8.addWidget(self.buttonLayer3DUp)
        self.buttonLayer3DDown = QtWidgets.QPushButton(QGridderCheck3D)
        self.buttonLayer3DDown.setObjectName("buttonLayer3DDown")
        self.verticalLayout_8.addWidget(self.buttonLayer3DDown)
        self.buttonLayer3DRemove = QtWidgets.QPushButton(QGridderCheck3D)
        self.buttonLayer3DRemove.setObjectName("buttonLayer3DRemove")
        self.verticalLayout_8.addWidget(self.buttonLayer3DRemove)
        self.horizontalLayout_10.addLayout(self.verticalLayout_8)
        self.gridLayout.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(QGridderCheck3D)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_10.addWidget(self.label_23)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setMaximumSize(QtCore.QSize(175, 16777215))
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_14.addWidget(self.label_21)
        self.listReferenceGrid = QtWidgets.QComboBox(self.frame)
        self.listReferenceGrid.setObjectName("listReferenceGrid")
        self.horizontalLayout_14.addWidget(self.listReferenceGrid)
        self.buttonAddNewLayer3D = QtWidgets.QPushButton(self.frame)
        self.buttonAddNewLayer3D.setMaximumSize(QtCore.QSize(140, 16777215))
        self.buttonAddNewLayer3D.setObjectName("buttonAddNewLayer3D")
        self.horizontalLayout_14.addWidget(self.buttonAddNewLayer3D)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_24 = QtWidgets.QLabel(self.frame)
        self.label_24.setMaximumSize(QtCore.QSize(175, 16777215))
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_16.addWidget(self.label_24)
        self.listExistingLayer = QtWidgets.QComboBox(self.frame)
        self.listExistingLayer.setObjectName("listExistingLayer")
        self.horizontalLayout_16.addWidget(self.listExistingLayer)
        self.buttonAddExistingLayer3D = QtWidgets.QPushButton(self.frame)
        self.buttonAddExistingLayer3D.setMaximumSize(QtCore.QSize(140, 16777215))
        self.buttonAddExistingLayer3D.setObjectName("buttonAddExistingLayer3D")
        self.horizontalLayout_16.addWidget(self.buttonAddExistingLayer3D)
        self.verticalLayout_10.addLayout(self.horizontalLayout_16)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBarCheck3D_2 = QtWidgets.QProgressBar(QGridderCheck3D)
        self.progressBarCheck3D_2.setProperty("value", 0)
        self.progressBarCheck3D_2.setObjectName("progressBarCheck3D_2")
        self.horizontalLayout.addWidget(self.progressBarCheck3D_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCheck3D = QtWidgets.QPushButton(QGridderCheck3D)
        self.buttonCheck3D.setObjectName("buttonCheck3D")
        self.horizontalLayout.addWidget(self.buttonCheck3D)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)

        self.retranslateUi(QGridderCheck3D)
        QtCore.QMetaObject.connectSlotsByName(QGridderCheck3D)

    def retranslateUi(self, QGridderCheck3D):
        _translate = QtCore.QCoreApplication.translate
        QGridderCheck3D.setWindowTitle(_translate("QGridderCheck3D", "Qgridder 3D grid"))
        self.label_25.setText(_translate("QGridderCheck3D", "List of layers (from top to bottom) : "))
        self.buttonLayer3DUp.setText(_translate("QGridderCheck3D", "Up"))
        self.buttonLayer3DDown.setText(_translate("QGridderCheck3D", "Down"))
        self.buttonLayer3DRemove.setText(_translate("QGridderCheck3D", "Remove"))
        self.label_23.setText(_translate("QGridderCheck3D", "Add layer to list : "))
        self.label_21.setText(_translate("QGridderCheck3D", "New from reference grid :"))
        self.buttonAddNewLayer3D.setText(_translate("QGridderCheck3D", "Add new layer..."))
        self.label_24.setText(_translate("QGridderCheck3D", "Import existing layer : "))
        self.buttonAddExistingLayer3D.setText(_translate("QGridderCheck3D", "Add existing layer"))
        self.buttonCheck3D.setText(_translate("QGridderCheck3D", "Check and correct 3D topology"))

