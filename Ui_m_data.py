# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\深海\截流板\controller\m_data.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(113, 178)
        self.m_name = QtWidgets.QLabel(Form)
        self.m_name.setGeometry(QtCore.QRect(10, 10, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.m_name.setFont(font)
        self.m_name.setObjectName("m_name")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 61, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 61, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 61, 21))
        self.label_5.setObjectName("label_5")
        self.voltage = QtWidgets.QLabel(Form)
        self.voltage.setGeometry(QtCore.QRect(70, 90, 61, 21))
        self.voltage.setObjectName("voltage")
        self.current = QtWidgets.QLabel(Form)
        self.current.setGeometry(QtCore.QRect(70, 60, 61, 21))
        self.current.setObjectName("current")
        self.power = QtWidgets.QLabel(Form)
        self.power.setGeometry(QtCore.QRect(70, 120, 61, 21))
        self.power.setObjectName("power")
        self.temperature = QtWidgets.QLabel(Form)
        self.temperature.setGeometry(QtCore.QRect(70, 150, 61, 21))
        self.temperature.setObjectName("temperature")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.m_name.setText(_translate("Form", "电机"))
        self.label_2.setText(_translate("Form", "电流"))
        self.label_3.setText(_translate("Form", "电压"))
        self.label_4.setText(_translate("Form", "功率"))
        self.label_5.setText(_translate("Form", "温度"))
        self.voltage.setText(_translate("Form", "0"))
        self.current.setText(_translate("Form", "0"))
        self.power.setText(_translate("Form", "0"))
        self.temperature.setText(_translate("Form", "0"))
