from PyQt5 import QtWidgets, QtGui
from pathlib import Path
from TeamsAtlasBridge.helpers import valid_extension


class QFrameDragDrop(QtWidgets.QFrame):
    def __init__(self, parent) -> None:
        super(QFrameDragDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.file_path: Path = Path()
        # There's only one button that we need to find
        self.button = self.findChild(QtWidgets.QPushButton)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            tmp_file = Path(event.mimeData().urls()[0].toLocalFile())
            if valid_extension(tmp_file):
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        self.file_path = Path(event.mimeData().urls()[0].toLocalFile())
