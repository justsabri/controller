# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\深海\截流板\controller\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 799)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 30, 741, 511))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.main_tab = QtWidgets.QWidget()
        self.main_tab.setObjectName("main_tab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.main_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 451, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.autoTrim = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.autoTrim.setObjectName("autoTrim")
        self.gridLayout.addWidget(self.autoTrim, 4, 0, 1, 1)
        self.autoRoll = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.autoRoll.setObjectName("autoRoll")
        self.gridLayout.addWidget(self.autoRoll, 4, 2, 1, 1)
        self.up = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.up.setCheckable(False)
        self.up.setAutoRepeat(False)
        self.up.setObjectName("up")
        self.gridLayout.addWidget(self.up, 6, 1, 1, 1)
        self.right = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.right.setCheckable(False)
        self.right.setObjectName("right")
        self.gridLayout.addWidget(self.right, 7, 2, 1, 1)
        self.left_board_bar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_board_bar.sizePolicy().hasHeightForWidth())
        self.left_board_bar.setSizePolicy(sizePolicy)
        self.left_board_bar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.left_board_bar.setProperty("value", 0)
        self.left_board_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.left_board_bar.setTextVisible(True)
        self.left_board_bar.setOrientation(QtCore.Qt.Vertical)
        self.left_board_bar.setInvertedAppearance(True)
        self.left_board_bar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.left_board_bar.setObjectName("left_board_bar")
        self.gridLayout.addWidget(self.left_board_bar, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.left_pct = QtWidgets.QLabel(self.gridLayoutWidget)
        self.left_pct.setAlignment(QtCore.Qt.AlignCenter)
        self.left_pct.setObjectName("left_pct")
        self.gridLayout.addWidget(self.left_pct, 2, 0, 1, 1)
        self.right_pct = QtWidgets.QLabel(self.gridLayoutWidget)
        self.right_pct.setAlignment(QtCore.Qt.AlignCenter)
        self.right_pct.setObjectName("right_pct")
        self.gridLayout.addWidget(self.right_pct, 2, 2, 1, 1)
        self.down = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.down.setCheckable(False)
        self.down.setObjectName("down")
        self.gridLayout.addWidget(self.down, 8, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.record_flag = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.record_flag.setObjectName("record_flag")
        self.gridLayout.addWidget(self.record_flag, 0, 0, 1, 1)
        self.file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.file_label.setObjectName("file_label")
        self.gridLayout.addWidget(self.file_label, 0, 1, 1, 2)
        self.left = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.left.setCheckable(False)
        self.left.setObjectName("left")
        self.gridLayout.addWidget(self.left, 7, 0, 1, 1)
        self.right_board_bar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setKerning(True)
        self.right_board_bar.setFont(font)
        self.right_board_bar.setProperty("value", 0)
        self.right_board_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.right_board_bar.setTextVisible(True)
        self.right_board_bar.setOrientation(QtCore.Qt.Vertical)
        self.right_board_bar.setInvertedAppearance(True)
        self.right_board_bar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.right_board_bar.setObjectName("right_board_bar")
        self.gridLayout.addWidget(self.right_board_bar, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.trim_display = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trim_display.setFont(font)
        self.trim_display.setAlignment(QtCore.Qt.AlignCenter)
        self.trim_display.setObjectName("trim_display")
        self.gridLayout.addWidget(self.trim_display, 3, 0, 1, 1)
        self.roll_display = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.roll_display.setFont(font)
        self.roll_display.setAlignment(QtCore.Qt.AlignCenter)
        self.roll_display.setObjectName("roll_display")
        self.gridLayout.addWidget(self.roll_display, 3, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 3)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 1)
        self.gridLayout.setRowStretch(7, 1)
        self.gridLayout.setRowStretch(8, 1)
        self.tabWidget.addTab(self.main_tab, "")
        self.test_tab = QtWidgets.QWidget()
        self.test_tab.setObjectName("test_tab")
        self.label = QtWidgets.QLabel(self.test_tab)
        self.label.setGeometry(QtCore.QRect(30, 50, 121, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.test_tab)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 121, 21))
        self.label_2.setObjectName("label_2")
        self.speed_edit = QtWidgets.QLineEdit(self.test_tab)
        self.speed_edit.setGeometry(QtCore.QRect(120, 50, 113, 20))
        self.speed_edit.setObjectName("speed_edit")
        self.rpm_edit = QtWidgets.QLineEdit(self.test_tab)
        self.rpm_edit.setGeometry(QtCore.QRect(120, 80, 113, 20))
        self.rpm_edit.setObjectName("rpm_edit")
        self.start_test_btn = QtWidgets.QPushButton(self.test_tab)
        self.start_test_btn.setGeometry(QtCore.QRect(30, 170, 91, 31))
        self.start_test_btn.setObjectName("start_test_btn")
        self.test_progress = QtWidgets.QProgressBar(self.test_tab)
        self.test_progress.setGeometry(QtCore.QRect(30, 130, 231, 23))
        self.test_progress.setProperty("value", 0)
        self.test_progress.setObjectName("test_progress")
        self.stop_test_btn = QtWidgets.QPushButton(self.test_tab)
        self.stop_test_btn.setGeometry(QtCore.QRect(140, 170, 91, 31))
        self.stop_test_btn.setObjectName("stop_test_btn")
        self.tabWidget.addTab(self.test_tab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.m1 = MWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m1.sizePolicy().hasHeightForWidth())
        self.m1.setSizePolicy(sizePolicy)
        self.m1.setMinimumSize(QtCore.QSize(100, 200))
        self.m1.setBaseSize(QtCore.QSize(100, 200))
        self.m1.setObjectName("m1")
        self.gridLayout_3.addWidget(self.m1, 0, 0, 1, 1)
        self.m2 = MWidget(self.horizontalLayoutWidget)
        self.m2.setMinimumSize(QtCore.QSize(100, 200))
        self.m2.setObjectName("m2")
        self.gridLayout_3.addWidget(self.m2, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        self.frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.VLine)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 793, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.actionconnect = QtWidgets.QAction(MainWindow)
        self.actionconnect.setObjectName("actionconnect")
        self.menu.addAction(self.actionconnect)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.autoTrim.setText(_translate("MainWindow", "自动纵倾"))
        self.autoRoll.setText(_translate("MainWindow", "自动横倾"))
        self.up.setText(_translate("MainWindow", "上"))
        self.right.setText(_translate("MainWindow", "右"))
        self.left_pct.setText(_translate("MainWindow", "0%"))
        self.right_pct.setText(_translate("MainWindow", "0%"))
        self.down.setText(_translate("MainWindow", "下"))
        self.record_flag.setText(_translate("MainWindow", "测试数据记录"))
        self.file_label.setText(_translate("MainWindow", "file_path"))
        self.left.setText(_translate("MainWindow", "左"))
        self.trim_display.setText(_translate("MainWindow", "trim_display"))
        self.roll_display.setText(_translate("MainWindow", "roll_display"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), _translate("MainWindow", "主界面"))
        self.label.setText(_translate("MainWindow", "航速（kn）"))
        self.label_2.setText(_translate("MainWindow", "转速（r/min）"))
        self.start_test_btn.setText(_translate("MainWindow", "开始记录"))
        self.stop_test_btn.setText(_translate("MainWindow", "结束记录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.test_tab), _translate("MainWindow", "航速最优测试"))
        self.menu.setTitle(_translate("MainWindow", "设备"))
        self.actionconnect.setText(_translate("MainWindow", "connect"))
from m_ui import MWidget
