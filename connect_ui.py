from Ui_connect import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal
import sys
import subprocess

class ConnectWidget(QWidget, Ui_Form):
    connect_signal = pyqtSignal(str, str)
    def __init__(self, parent = None):
        super(ConnectWidget, self).__init__(parent)
        self.setupUi(self)

        self.ping_btn.clicked.connect(self.test_connect)
        self.connect_btn.clicked.connect(self.connect_plc)

    def test_connect(self):
        self.host = self.ip_adresses.text()
        result = subprocess.run(["ping", "-n", "4", self.host], capture_output=True, text=True)
        output = result.stdout  # 获取标准输出内容
        QMessageBox.information(self, '通信结果：\n', output)
        return output  # 获取输出内容
    
    def connect_plc(self):
        self.close()
        self.connect_signal.emit(self.ip_adresses.text(), self.ip_port.text())
        # self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = ConnectWidget()
    myWin.show()
    sys.exit(app.exec_())