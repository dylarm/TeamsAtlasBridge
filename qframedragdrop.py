from PyQt5 import QtWidgets, QtGui
from pathlib import Path


class QFrameDragDrop(QtWidgets.QFrame):
    def __init__(self, parent) -> None:
        super(QFrameDragDrop, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_file():
                print(path)
                print(f"Position: {event.pos()}")
                print(f"Source: {event.source()}")
