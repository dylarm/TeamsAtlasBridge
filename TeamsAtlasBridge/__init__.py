import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStyleFactory
import TeamsAtlasBridge.gui.main_window as mw
from TeamsAtlasBridge.constants import INPUT_TEAMS_FILE, INPUT_STUDENT_FILE


class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__setup_drop()
        self.__setup_buttons()
        self.__debug_print()

    def __debug_print(self):
        print(self.frame_grade_csv.pos())
        print(self.frame_grade_csv.size())
        print(self.frame_student_xlsx.pos())
        print(self.frame_student_xlsx.size())
        print(self.frame_student_xlsx.geometry())

    def __setup_drop(self):
        # TODO: Find a way of having a specific dropEvent for the buttons/frames?
        pass

    def __setup_buttons(self):
        self.button_input_students.clicked.connect(
            lambda: self._choose_dir(INPUT_STUDENT_FILE)
        )
        self.button_input_teams.clicked.connect(
            lambda: self._choose_dir(INPUT_TEAMS_FILE)
        )

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
