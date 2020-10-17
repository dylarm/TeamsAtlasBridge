import sys
from pathlib import Path

import PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QStyleFactory
import gui.main_window as mw


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__setup_drop()
        self.setAcceptDrops(True)

    def __setup_drop(self):
        pass

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if Path(path).is_file():
                print(path)
                print(f"Position: {event.pos()}")
                print(f"Source: {event.source()}")


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
