import logging
from pathlib import Path

from PyQt5 import QtWidgets, QtGui

from constants import INPUT_TEAMS_FRAME, INPUT_STUDENT_FRAME
from helpers import valid_extension
from process import assignment_name, assignment_file_name, class_period

logger = logging.getLogger(__name__)


class QFrameDragDrop(QtWidgets.QFrame):
    def __init__(self, parent) -> None:
        super(QFrameDragDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.file_path: Path = Path()
        self.assignment_name: str = ""
        self.assignment_file_name: str = ""
        logger.debug("QFrameDragDrop initialized")

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        logger.debug("File drag enter event")
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            logger.debug(
                f"Checking validity on {event.mimeData().urls()[0].toLocalFile()}"
            )
            try:
                tmp_file = Path(event.mimeData().urls()[0].toLocalFile())
                if valid_extension(tmp_file):
                    logger.debug("Valid file extension!")
                    self.__process_event(tmp_file, event)
            except IndexError:
                pass
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        self.file_path = Path(event.mimeData().urls()[0].toLocalFile())
        logger.info(f"File dropped: {self.file_path}")
        if self.objectName() == INPUT_TEAMS_FRAME:
            logger.info("Processing for grades...")
            self.assignment_name = assignment_name(self.file_path)
            self.assignment_file_name = assignment_file_name(
                assignment=self.assignment_name, period=class_period(self.file_path)
            )
            self.setWindowIconText(f"{self.assignment_file_name}.xlsx")
            logger.info("Finished processing")
            logger.debug(f"File(s) that may be exported: {self.windowIconText()}")
        self.findChild(QtWidgets.QPushButton).setText(self.file_path.name)
        logger.debug("'button' text changed")

    def __process_event(self, file: Path, event: QtGui.QDropEvent) -> None:
        logger.debug(f"Processing file drag event: {file.name}")
        if "grades" in file.name and self.objectName() == INPUT_TEAMS_FRAME:
            logger.debug("File met 'grades' criteria")
            event.accept()
        elif "Student Portal" in file.name and self.objectName() == INPUT_STUDENT_FRAME:
            logger.debug("File met 'student logins' criteria")
            event.accept()
        else:
            logger.debug("File did not meet any criteria -- rejecting")
            event.ignore()
