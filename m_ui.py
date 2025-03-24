from PyQt5.QtWidgets import QWidget, QApplication
from Ui_m_data import Ui_Form
import sys

class MWidget(QWidget, Ui_Form):
    def __init__(self, parent = None):
        super(MWidget, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MWidget()
    myWin.show()
    sys.exit(app.exec_()) 