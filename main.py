from PyQt5.QtWidgets import QApplication
import sys
from gui.main_window import AppMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())
