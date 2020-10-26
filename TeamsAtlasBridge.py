import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox

import gui.main_window as mw
from constants import INPUT_TEAMS_FILE, INPUT_STUDENT_FILE, VERSION
from process import generate_output

# Copyright © 2020, Dylan Armitage. Some rights reserved.
# This work is licensed under the GNU General Public License, version 3.

DEFAULT_LOG_FILE: Path = Path(f"./teams-atlas_bridge {datetime.now()}.log").absolute()


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__setup_buttons()
        self.setWindowTitle(f"{self.windowTitle()} ({VERSION})")
        logger.info("Main window setup")

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
        logging.debug("Finished setting up buttons.")

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
            generate_output(
                assignment_file=self.frame_grade_csv.file_path,
                student_list=self.frame_student_xlsx.file_path,
                output=Path(self.text_output_dir.text()).joinpath(
                    f"{self.frame_grade_csv.assignment_file_name}.xlsx"
                ),
            )
            msg = (
                f"Finished creating {self.frame_grade_csv.assignment_file_name}.xlsx"
                f" at {self.frame_grade_csv.file_path.absolute().parent}"
            )
            logger.info(msg)
            QMessageBox.information(self, "All done", msg)
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


def setup_logging(
    output_file: Path = DEFAULT_LOG_FILE,
    to_file: bool = False,
    default_level=logging.DEBUG,
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
    # TODO: Don't force-quite when error occurs. Try to log and write to file.


setup_logging(to_file=False)
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.debug("Running main function")
    main()
