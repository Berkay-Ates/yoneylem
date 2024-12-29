from PyQt5.QtWidgets import *
from view_py_files.add_lesson import Ui_MainWindow as MainPage
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class AddLessonController(QMainWindow):

    data_signal = pyqtSignal(dict)

    def __init__(self,data) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.init_ui_elements(data)

        self.model = QStandardItemModel(self.main_page_view.listView_lesson_instructors)
        self.main_page_view.listView_lesson_instructors.setModel(self.model)

    def init_ui_elements(self,data):
        self.main_page_view.pushButton_save_lesson.clicked.connect(self.on_save_lesson)
        self.main_page_view.pushButton_assign_instructor.clicked.connect(self.on_assign_instructor)
        self.main_page_view.pushButton_remove_selected_instructor.clicked.connect(self.on_remove_selected_instructor)
        if data is not None:
            for instructor in data["instructors"]:
                self.main_page_view.comboBox_instructors.addItem(instructor["instructor_name"])

    def on_assign_instructor(self):
        selected_instructor = self.main_page_view.comboBox_instructors.currentText()
        if selected_instructor:
            items = self.model.findItems(selected_instructor)
            if not items:
                item = QStandardItem(selected_instructor)
                self.model.appendRow(item)

    def on_remove_selected_instructor(self):
        selected_indexes = self.main_page_view.listView_lesson_instructors.selectedIndexes()
        if selected_indexes:
            self.model.removeRow(selected_indexes[0].row()) 

    def on_save_lesson(self):
        lesson_name = self.main_page_view.lineEdit_lesson_name.text()
        instructors = self.get_all_elements()
        grade = self.main_page_view.comboBox_grades.currentText()
        lesson_hour = self.main_page_view.lineEdit_lesson_hour.text()

        lesson_type = {
            "Face To Face": self.main_page_view.radioButton_face_to_face.isChecked(),
            "Online": self.main_page_view.radioButton_online.isChecked(),
            "Hybrid": self.main_page_view.radioButton_hybrid.isChecked(),
        }

        
        self.data_signal.emit(
                {
                    "lesson_name":lesson_name,
                    "instructors":instructors,
                    "grade":grade,
                    "lesson_type":lesson_type,
                    "lesson_hour":lesson_hour
                }
            )
        
        QMessageBox.information(None, "Success!", "Lesson has been added successfully!")


    def get_all_elements(self):
        model = self.main_page_view.listView_lesson_instructors.model()

        elements = []
        for row in range(model.rowCount()):
            item = model.item(row) 
            elements.append(item.text())  
        
        return elements