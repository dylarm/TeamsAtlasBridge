from pathlib import Path

from PyQt5 import QtWidgets, QtGui

from constants import INPUT_TEAMS_FRAME, INPUT_STUDENT_FRAME
from helpers import valid_extension
from process import assignment_name, assignment_file_name, class_period


class QFrameDragDrop(QtWidgets.QFrame):
    def __init__(self, parent) -> None:
        super(QFrameDragDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.file_path: Path = Path()
        self.assignment_name: str = ""
        self.assignment_file_name: str = ""

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            try:
                tmp_file = Path(event.mimeData().urls()[0].toLocalFile())
                if valid_extension(tmp_file):
                    self.__process_event(tmp_file, event)
            except IndexError:
                pass
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        self.file_path = Path(event.mimeData().urls()[0].toLocalFile())
        if self.objectName() == INPUT_TEAMS_FRAME:
            self.assignment_name = assignment_name(self.file_path)
            self.assignment_file_name = assignment_file_name(
                assignment=self.assignment_name, period=class_period(self.file_path)
            )
            self.setWindowIconText(f"{self.assignment_file_name}.xlsx")
        self.findChild(QtWidgets.QPushButton).setText(self.file_path.name)

    def __process_event(self, file: Path, event: QtGui.QDropEvent) -> None:
        if "grades" in file.name and self.objectName() == INPUT_TEAMS_FRAME:
            event.accept()
        elif "Student Portal" in file.name and self.objectName() == INPUT_STUDENT_FRAME:
            event.accept()
        else:
            event.ignore()
