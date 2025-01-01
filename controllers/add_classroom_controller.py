from PyQt5.QtWidgets import *
from view_py_files.add_classroom import Ui_MainWindow as MainPage
from PyQt5.QtCore import pyqtSignal


class AddClassroomController(QMainWindow):

    data_signal = pyqtSignal(str)
    data_signal_update = pyqtSignal(str, int)

    def __init__(self, data="Error", index=None) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.index = index
        self.init_ui_elements(data)

    def init_ui_elements(self, data):
        self.main_page_view.pushButton_save_classroom.clicked.connect(self.on_save_classroom)
        self.main_page_view.pushButton_update_classroom.clicked.connect(self.on_update_classroom)
        self.main_page_view.lineEdit_classroom_name.setText(data)

    def on_save_classroom(self):
        lesson_name = self.main_page_view.lineEdit_classroom_name.text()

        if not lesson_name:
            QMessageBox.warning(self, "Warning!", "Please enter a Classroom name.")
            return

        self.data_signal.emit(lesson_name)
        QMessageBox.information(None, "Success!", "Classroom has been saved successfully!")

    def on_update_classroom(self):
        lesson_name = self.main_page_view.lineEdit_classroom_name.text()

        if not lesson_name:
            QMessageBox.warning(self, "Warning!", "Please enter a Classroom name.")
            return

        self.data_signal_update.emit(lesson_name, self.index)
        QMessageBox.information(None, "Success!", "Classroom has been updated successfully!")
