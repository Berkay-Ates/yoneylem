from PyQt5.QtWidgets import *
from view_py_files.add_classroom import Ui_MainWindow as MainPage
from PyQt5.QtCore import pyqtSignal


class AddClassroomController(QMainWindow):
    
    data_signal = pyqtSignal(str) 

    def __init__(self) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.init_ui_elements()

    
    def init_ui_elements(self):
        self.main_page_view.pushButton_save_classroom.clicked.connect(self.on_save_classroom)


    def on_save_classroom(self):
        lesson_name = self.main_page_view.lineEdit_classroom_name.text()

        if not lesson_name:
            QMessageBox.warning(self, "Warning!", "Please enter a Classroom name.")
            return
        
        self.data_signal.emit(lesson_name)
        

    