import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox
import TeamsAtlasBridge.gui.main_window as mw
from TeamsAtlasBridge.constants import INPUT_TEAMS_FILE, INPUT_STUDENT_FILE
from TeamsAtlasBridge.process import generate_output


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__setup_buttons()
        self.__debug_print()

    def __debug_print(self):
        print(self.frame_grade_csv.pos())
        print(self.frame_grade_csv.size())
        print(self.frame_student_xlsx.pos())
        print(self.frame_student_xlsx.size())
        print(self.frame_student_xlsx.geometry())

    def __setup_buttons(self):
        self.button_input_students.clicked.connect(
            lambda: self._choose_dir(INPUT_STUDENT_FILE)
        )
        self.button_input_teams.clicked.connect(
            lambda: self._choose_dir(INPUT_TEAMS_FILE)
        )
        self.button_process.clicked.connect(self._process_files)

    def _process_files(self):
        if (
            self.frame_grade_csv.file_path.is_file()
            and self.frame_student_xlsx.file_path.is_file()
        ):
            # Both files loaded, good
            generate_output(
                assignment_file=self.frame_grade_csv.file_path,
                student_list=self.frame_student_xlsx,
                output=self.frame_grade_csv.file_path.absolute().parent.joinpath(
                    f"{self.frame_grade_csv.assignment_file_name}.xlsx"
                ),
            )
        else:
            # Pop up an error
            msg = (
                f"One of both of the files have not been loaded.\n"
                f"Currently loaded files:\n\n"
                f"Teams CSV -- {self.frame_grade_csv.file_path.name}\n\n"
                f"Student Logins -- {self.frame_student_xlsx.file_path.name}"
            )
            QMessageBox.warning(self, "File(s) not loaded", msg)

    def _choose_dir(self, file_type: int = 0) -> None:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        caption = f"Choose {file_type} file"
        file_filter: str = "All files (*.*)"
        initial_filter = file_filter
        if file_type == INPUT_STUDENT_FILE:
            initial_filter = "Excel Workbook (*.xlsx)"
            file_filter += f";;{initial_filter}"
        elif file_type == INPUT_TEAMS_FILE:
            initial_filter = "CSV File (*.csv)"
            file_filter += f";;{initial_filter}"
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
        if type == INPUT_STUDENT_FILE:
            self.student_file = file_path
        elif type == INPUT_TEAMS_FILE:
            self.teams_file = file_path


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
