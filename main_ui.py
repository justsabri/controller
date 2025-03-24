import sys
import time
from AlgProcesser import AlgorithmProcesser
from DataAcquisition import DataAcquisition
import Logger
from SystemMonitor import SysMonitor
from PlcAdapter import PlcAdapter
from m_ui import MWidget
from Ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal

class IPCWindow(QMainWindow, Ui_MainWindow):
    update_progress_signal = pyqtSignal(int, int)
    update_test_progress_signal = pyqtSignal(int)

    def __init__(self, parent = None):
        super(IPCWindow, self).__init__(parent)
        self.setupUi(self)

        self.m1.m_name.setText(self.m1.m_name.text() + '1')
        self.m2.m_name.setText(self.m2.m_name.text() + '2')

        # 连接 stateChanged 信号到槽函数
        self.update_progress_signal.connect(self.update_progress)
        self.update_test_progress_signal.connect(self.update_test_progress)
       
        self.record_flag.stateChanged.connect(self.on_record_flag_changed)

        self.right_board_bar.valueChanged.connect(lambda value: self.right_pct.setText(f"{value}%"))
        self.left_board_bar.valueChanged.connect(lambda value: self.left_pct.setText(f"{value}%"))

        self.up.clicked.disconnect()
        self.up.clicked.connect(self.on_up_clicked)
        self.down.clicked.disconnect()
        self.down.clicked.connect(self.on_down_clicked)
        self.left.clicked.disconnect()
        self.left.clicked.connect(self.on_left_clicked)
        self.right.clicked.disconnect()
        self.right.clicked.connect(self.on_right_clicked)

         # 计时器
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.on_long_press)  # 绑定长按回调
        self.long_press_btn = None

        # 连接鼠标按下 & 释放事件
        self.up.pressed.connect(lambda: self.start_long_press(self.up))  # 按下启动定时器
        self.up.released.connect(self.stop_long_press)  # 释放停止定时器
        self.down.pressed.connect(lambda: self.start_long_press(self.down))  # 按下启动定时器
        self.down.released.connect(self.stop_long_press)  # 释放停止定时器
        self.left.pressed.connect(lambda: self.start_long_press(self.left))  # 按下启动定时器
        self.left.released.connect(self.stop_long_press)  # 释放停止定时器
        self.right.pressed.connect(lambda: self.start_long_press(self.right))  # 按下启动定时器
        self.right.released.connect(self.stop_long_press)  # 释放停止定时器

        # self.autoRoll.clicked.disconnect()
        self.autoRoll.setCheckable(True)
        self.autoRoll.clicked.connect(self.auto_roll)
        # self.autoTrim.clicked.disconnect()
        self.autoTrim.setCheckable(True)
        self.autoTrim.clicked.connect(self.auto_trim)

        # tab2
        # self.start_test_btn.clicked.disconnect()
        self.start_test_btn.clicked.connect(self.start_test)
        # self.stop_test_btn.clicked.disconnect()
        self.stop_test_btn.clicked.connect(self.stop_test)

        # init server resources
        self.adapter = None
        self.data_acq = None
        self.alg_process = None
        self.sys_monitor = None
        self.logger = Logger.GetLogger(__name__)

        self.auto_mode = 0

        # connect
        self.actionconnect.triggered.connect(self.connect_and_monitor)

    def __del__(self):
        self.disconnect()

    def closeEvent(self, event):
        print("窗口关闭事件")
        self.disconnect()  # 标记对象删除
        event.accept()  # 允许窗口关闭

    def on_record_flag_changed(self, state):
        if state == 2:  # 2 表示选中 (Qt.Checked)
            self.alg_process.start_record()
        else:  # 0 表示未选中 (Qt.Unchecked)
            file_name = self.alg_process.stop_record()
            self.file_label.setText(file_name)

    def on_up_clicked(self):
        self.decrease_progress('both')

    def on_down_clicked(self):
        self.increase_progress('both')

    def on_left_clicked(self):
        self.increase_progress('right')

    def on_right_clicked(self):
        self.increase_progress('left')

    def start_long_press(self, button):
        """按钮按下时，启动计时器"""
        self.long_press_btn = button
        if not self.long_press_btn.isChecked():  # 只在按钮没有处于按下状态时启动
            self.long_press_btn.setChecked(True)
            self.timer.start()

    def stop_long_press(self):
        """按钮释放时，停止计时器"""
        self.long_press_btn.setChecked(False)
        self.timer.stop()

    def on_long_press(self):
        """长按时触发的事件"""
        self.long_press_btn.clicked.emit()

    def increase_progress(self, mode):
        processBar = []
        if mode == 'left':
            processBar.append(self.left_board_bar)
        elif mode == 'right':
            processBar.append(self.right_board_bar)
        elif mode == 'both':
            processBar.append(self.left_board_bar)
            processBar.append(self.right_board_bar)
        else:
            print('unknown mode: ', mode)
            return
        
        for bar in processBar:
            value = bar.value() + 1
            if value > 100:
                continue
            bar.setValue(value)
        if mode == 'both':
            self.alg_process.setLocationByPercent(mode, processBar[0].value(), processBar[1].value())
        else:
            self.alg_process.setLocationByPercent(mode, processBar[0].value())

    def decrease_progress(self, mode):
        processBar = []
        if mode == 'left':
            processBar.append(self.left_board_bar)
        elif mode == 'right':
            processBar.append(self.right_board_bar)
        elif mode == 'both':
            processBar.append(self.left_board_bar)
            processBar.append(self.right_board_bar)

        for bar in processBar:
            value = bar.value() - 1
            if value < 0:
                continue
            bar.setValue(value)
        if mode == 'both':
            self.alg_process.setLocationByPercent(mode, processBar[0].value(), processBar[1].value())
        else:
            self.alg_process.setLocationByPercent(mode, processBar[0].value())
        # self.alg_process.setLocationByPercent(mode, processBar[0].value())
    
    def start_test(self):
        speed = self.speed_edit.text()
        rpm = self.rpm_edit.text()
        file = speed + '_' + rpm
        self.data_acq.startTest(file)
        

    def stop_test(self):
        self.data_acq.stopTest()

    def get_progress(self, left, right):
        self.update_progress_signal.emit(left, right)

    def get_test_progress(self, value):
        self.update_test_progress_signal.emit(value)
    
    def update_progress(self, left, right):
        self.left_board_bar.setValue(left)
        self.right_board_bar.setValue(right)
    
    def update_test_progress(self, value):
        self.test_progress.setValue(value)
        if value == 100:
            self.stop_test_btn.clicked.emit()


    def auto_trim(self):
        """按钮点击时执行的逻辑"""
        if self.autoTrim.isChecked():
            self.auto_mode = 1
            self.alg_process.setAlgMode(1)
            self.alg_process.start_process()
        else:
            self.alg_process.stop_process()
            self.auto_mode = 0
        

    def auto_roll(self):
        """按钮点击时执行的逻辑"""
        if self.autoRoll.isChecked():
            self.auto_mode = 2
            self.alg_process.setAlgMode(2)
            self.alg_process.start_process()
        else:
            self.alg_process.stop_process()
            self.auto_mode = 0

    def connect_and_monitor(self):
        # self.statusBar.showMessage("连接中")
        # init server resources
        self.adapter = PlcAdapter()
        if not self.adapter.is_connected():
            QMessageBox.critical(self, "失败", "连接PLC失败!")
            return
        self.data_acq = self.adapter.get_data_acq()
        self.data_acq.setCallback(self.get_test_progress)
        self.alg_process = self.adapter.get_alg_process()
        self.alg_process.setCallback(self.get_progress)
        self.sys_monitor = self.adapter.get_sys_monitor()

        # init progress bar
        datas = self.sys_monitor.getInitValue()
        if 0<= datas[0] <= 100 and 0<= datas[0] <= 100:
            self.left_board_bar.setValue(int(datas[0]))
            self.right_board_bar.setValue(int(datas[1]))
        else:
            print('error init value: ', datas[0], datas[1])
            QMessageBox.critical(self, "错误", f"电机零位异常，当前读取到截流板位置为：\n左侧{datas[0]/2.0}mm 右侧{datas[1]/2.0}mm")
            return

        # start monitor
        while True:
            res = self.sys_monitor.start_monitor()
            if res:
                break
            time.sleep(1000)
        # self.statusBar.showMessage("已连接")
        # 创建 QTimer，每 1 秒触发一次
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_monitor_data)  # 绑定函数
        self.monitor_timer.start(1000)  # 每 1000ms (1s) 触发一次

    def disconnect(self):
        print('ui disconnect')
        if self.sys_monitor:
            self.sys_monitor.stop_monitor()
        if self.alg_process:
            self.alg_process.stop_process()
        if self.data_acq:
            self.data_acq.stopTest()
        if self.adapter:
            self.adapter.disconnect()

    def update_monitor_data(self):
        datas = self.sys_monitor.getMonitorData()
        self.m1.current.setText(str(datas[0]))
        self.m1.voltage.setText(str(datas[1]))
        self.m1.power.setText(str(datas[2]))
        self.m1.temperature.setText(str(datas[3]))
        self.m2.current.setText(str(datas[4]))
        self.m2.voltage.setText(str(datas[5]))
        self.m2.power.setText(str(datas[6]))
        self.m2.temperature.setText(str(datas[7]))
        self.trim_display.setText(str(datas[8]))
        self.roll_display.setText(str(datas[9]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = IPCWindow()
    myWin.show()
    sys.exit(app.exec_())
