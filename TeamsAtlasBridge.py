import logging
import logging.config
import sys
import signal
import traceback
from io import StringIO
from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox

import gui.main_window as mw
import check_updates
from constants import INPUT_TEAMS_FILE, INPUT_STUDENT_FILE, VERSION
from process import generate_output

# Copyright © 2020, Dylan Armitage. Some rights reserved.
# This work is licensed under the GNU General Public License, version 3.

DEFAULT_LOG_FILE: Path = Path(f"./teams-atlas_bridge {datetime.now()}.log").absolute()


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        logger.info(f"Starting Teams-ATLAS Bridge, {VERSION}")
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__setup_buttons()
        self.setWindowTitle(f"{self.windowTitle()} ({VERSION})")
        version_label = QtWidgets.QLabel()
        version_label.setText(f"Version: {VERSION} {self.check_updates(at_start=True)}")
        version_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        version_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.statusbar.addPermanentWidget(version_label)
        self.error_dialog = QtWidgets.QErrorMessage()  # For use later, if needed
        self.__setup_signal_capture()
        logger.info("Main window set up")

    def __setup_buttons(self) -> None:
        logging.debug("Setting up buttons...")
        self.button_input_students.clicked.connect(
            lambda: self._choose_file(INPUT_STUDENT_FILE)
        )
        self.button_input_teams.clicked.connect(
            lambda: self._choose_file(INPUT_TEAMS_FILE)
        )
        self.button_process.clicked.connect(self._process_files)
        self.button_output_dir.clicked.connect(self.choose_output_dir)
        self.button_default_output_dir.clicked.connect(
            lambda: self.choose_output_dir(str(self.frame_grade_csv.file_path.parent))
        )
        logging.debug("Finished setting up buttons.")

    def __setup_signal_capture(self) -> None:
        logger.debug("Setting up signal capture")
        signal.signal(signal.SIGABRT, self.__signal_handler)

    def __signal_handler(self, signal_num: signal.Signals, frame) -> None:
        frame_print = StringIO()
        traceback.print_stack(frame, file=frame_print)
        file_name = Path(f"./TAB Error {datetime.now()}.log").absolute()
        with open(file_name, "a") as f:
            f.write(frame_print.getvalue())
        logger.error(
            f"Received signal {signal_num}, {signal.strsignal(signal_num)}\n"
            f"Frame: {frame}\n"
            f"Traceback:\n"
            f"{frame_print.getvalue()}"
        )
        self.error_dialog.showMessage(
            f"Error: received signal {signal_num}, {signal.strsignal(signal_num)}. \n"
            f"Please send '{file_name.name}' to maintainer "
            f"(located at {file_name.parent})"
        )

    def check_updates(self, at_start: bool = False) -> str:
        logger.info("Checking for new version...")
        ret: str = ""
        version, link = check_updates.get_latest_ver()
        update_available = check_updates.update_available(latest_ver=version)
        if update_available:
            ret = f"(Update: {version})"
            logger.info(f"New version available: {version}")
            response = QMessageBox.question(
                self,
                "Update Available",
                f"A new update is available!\n"
                f"Current version: {VERSION}\n"
                f"New version: {version}\n"
                f"Go to download page?",
            )
            logger.debug(f"Response: {response}")
            if response == QMessageBox.Yes:
                logger.info(f"Opening {link}")
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))
            else:
                logger.info("Not going to update page.")
        elif not at_start and not update_available:
            logger.info(f"Already at latest version {VERSION}")
            QMessageBox.information(
                self,
                "Check for Updates",
                f"No update available.\nAlready running most recent version {VERSION}",
            )
        return ret

    def __actual_process(self, output_file: Path) -> None:
        generate_output(
            assignment_file=self.frame_grade_csv.file_path,
            student_list=self.frame_student_xlsx.file_path,
            output=output_file,
        )
        msg = (
            f"Finished creating {self.frame_grade_csv.assignment_file_name}.xlsx"
            f" at {self.text_output_dir.text()}"
        )
        logger.info(msg)
        QMessageBox.information(self, "All done", msg)

    def _process_files(self) -> None:
        logging.info("Processing files")
        if (
            self.frame_grade_csv.file_path.is_file()
            and self.frame_student_xlsx.file_path.is_file()
        ):
            logging.info("Both files are selected")
            logging.debug(
                f"self.frame_grade_csv.file_path: {self.frame_grade_csv.file_path}\n"
                f"self.frame_grade_csv.assignment_file_name: {self.frame_grade_csv.assignment_file_name}\n"
                f"self.frame_student_xlsx.file_path: {self.frame_student_xlsx.file_path}\n"
                f"Output: {Path(self.text_output_dir.text()).joinpath(self.frame_grade_csv.assignment_file_name)}.xlsx"
            )
            # Both files loaded, good
            output_file = Path(self.text_output_dir.text()).joinpath(
                f"{self.frame_grade_csv.assignment_file_name}.xlsx"
            )
            if output_file.exists():
                logger.info("Output File already exists!")
                overwrite_prompt = QMessageBox()
                overwrite_prompt.setWindowTitle("Output File Exists")
                overwrite_prompt.setText(
                    f"The file '{output_file.name}' already exists."
                    f"Would you like to overwrite, or save to a different file?"
                )
                overwrite_prompt.addButton(
                    QtWidgets.QPushButton("Overwrite"), QMessageBox.YesRole
                )
                overwrite_prompt.addButton(
                    QtWidgets.QPushButton("Rename"), QMessageBox.RejectRole
                )
                overwrite_prompt.addButton(
                    QtWidgets.QPushButton("Cancel"), QMessageBox.NoRole
                )
                response = overwrite_prompt.exec_()
                logger.debug(f"Response: {response}")
                if response == QMessageBox.RejectRole:
                    logger.info("Response: Rename file")
                    # TODO: Create renaming dialog
                else:
                    pass  # Rewriting is automatic
                if (
                    response == QMessageBox.RejectRole
                    or response == QMessageBox.YesRole
                ):
                    self.__actual_process()
            else:
                self.__actual_process()
        else:
            # Pop up an error
            msg = (
                f"One of both of the files have not been loaded.\n"
                f"Currently loaded files:\n\n"
                f"Teams CSV -- {self.frame_grade_csv.file_path.name}\n\n"
                f"Student Logins -- {self.frame_student_xlsx.file_path.name}"
            )
            logger.info(msg)
            QMessageBox.warning(self, "File(s) not loaded", msg)

    def choose_output_dir(self, chosen: str = "") -> None:
        logging.info("Setting output directory")
        if chosen and Path(chosen).is_dir():
            logging.debug(f"Output directory already 'chosen': {chosen}")
            self.text_output_dir.setText(chosen)
            logging.debug(f"Output directory set: {Path(chosen)}")
        else:
            logging.debug("Output directory not chosen, running dir selection...")
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            options |= QtWidgets.QFileDialog.ShowDirsOnly
            output_dir = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Choose output folder",
                directory=str(Path().home()),
                options=options,
            )
            logging.debug(f"Directory chosen: {output_dir}")
            self.text_output_dir.setText(output_dir)

    def _choose_file(self, file_type: int = 0) -> None:
        logging.debug("Running _choose_file()")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_filter: str = "All files (*.*)"
        initial_filter = file_filter
        if file_type == INPUT_STUDENT_FILE:
            initial_filter = "Excel Workbook (*.xlsx)"
            file_filter += f";;{initial_filter}"
            file_type_text = "Student Login"
        elif file_type == INPUT_TEAMS_FILE:
            initial_filter = "CSV File (*.csv)"
            file_filter += f";;{initial_filter}"
            file_type_text = "Teams Grade CSV"
        else:
            file_type_text = ""
        caption = f"Choose {file_type_text} file"
        logging.debug(
            f"Caption: {caption}\n"
            f"file_filter: {file_filter}\n"
            f"initial_filter: {initial_filter}"
        )
        file_path = Path(
            QtWidgets.QFileDialog.getOpenFileName(
                self,
                caption,
                str(Path().home()),
                filter=file_filter,
                initialFilter=initial_filter,
                options=options,
            )[0]
        )
        logging.info(f"File path: {file_path}")
        if file_type == INPUT_STUDENT_FILE:
            self.frame_student_xlsx.file_path = file_path
            self.frame_student_xlsx.process_drop()
            logging.debug("Student Login file set")
        elif file_type == INPUT_TEAMS_FILE:
            self.frame_grade_csv.file_path = file_path
            self.frame_grade_csv.process_drop()
            logging.debug("Teams grade CSV file set")

    def about_app(self) -> None:
        msg = (
            f"<b>Bridging the disconnect between <i>MS Teams</i> and <i>ATLAS</i></b><br><br>"
            f"Made in response to the 2020 COVID-19 pandemic and online school<br><br>"
            f"Version {VERSION}<br><br>"
            f"Copyright © 2020, Dylan Armitage<br>"
            f"Licensed under the GNU General Public License, version 3<br>"
            f"Source code hosted on <a href='https://github.com/dylarm/TeamsAtlasBridge'>GitHub</a>"
        )  # Wow it's been forever since I've dealt with HTML tags
        QMessageBox.about(self, "About TAB", msg)

    def about_qt(self) -> None:
        QMessageBox.aboutQt(self, "About Qt")


def setup_logging(
    output_file: Path = DEFAULT_LOG_FILE,
    to_file: bool = False,
    default_level=logging.INFO,
    str_format: str = "%(asctime)s: [%(name)s/%(levelname)s] %(message)s",
) -> None:
    """Setup logging configuration"""
    if to_file:
        logging.basicConfig(
            filename=str(output_file), level=default_level, format=str_format
        )
    else:
        logging.basicConfig(level=default_level, format=str_format)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    logger.debug("App style set")
    form = MainWindow()
    form.show()
    logger.debug("Executing app...")
    app.exec_()


setup_logging(to_file=False)
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.debug("Running main function")
    main()
