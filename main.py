import sys

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStyleFactory
import gui.main_window as mw


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
