from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Ui_login import Ui_Form
import sys

class LoginWidget(QWidget, Ui_Form):
    def __init__(self, parent = None):
        super(LoginWidget, self).__init__(parent)
        self.setupUi(self)

        self.load_and_show_image('resources/login.jpg')

        self.login_btn.clicked.connect(self.login_action)
    
    def load_and_show_image(self, path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.label.setText("图片加载失败")
            return

        scaled_pixmap = pixmap.scaled(
            self.label.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)
        self.label.setScaledContents(True)

    def login_action(self):
        QMessageBox.critical(self, '错误', '用户名或密码错误！')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = LoginWidget()
    myWin.show()
    sys.exit(app.exec_())