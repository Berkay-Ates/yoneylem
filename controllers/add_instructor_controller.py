from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from view_py_files.add_instructor import Ui_MainWindow as MainPage
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal

class AddInstructorController(QMainWindow):

    data_signal = pyqtSignal(dict) 

    def __init__(self, data) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.init_ui_elements(data)
    
    def init_ui_elements(self, data):
        self.main_page_view.pushButton_save_instructor.clicked.connect(self.on_save_instructor)
        self.main_page_view.pushButton_assign_lesson.clicked.connect(self.on_assign_lesson)
        self.main_page_view.pushButton_remove_selected_lesson.clicked.connect(self.on_remove_selected_lesson)

        for lesson in data['lessons']:
            self.main_page_view.comboBox_lessons.addItem(lesson['lesson_name'])

        self.model = QStandardItemModel(self.main_page_view.listView_instructor_lessons)
        self.main_page_view.listView_instructor_lessons.setModel(self.model)

    def on_remove_selected_lesson(self):
        selected_indexes = self.main_page_view.listView_instructor_lessons.selectedIndexes()
        if selected_indexes:
            self.model.removeRow(selected_indexes[0].row())

    def on_assign_lesson(self):
        selected_lesson = self.main_page_view.comboBox_lessons.currentText()

        if selected_lesson:
            items = self.model.findItems(selected_lesson, QtCore.Qt.MatchExactly)
            if not items: 
                item = QStandardItem(selected_lesson)
                self.model.appendRow(item)

    def on_save_instructor(self):
        instructor_name = self.main_page_view.lineEdit_instructor_name.text()

        lessons = self.get_all_elements()

        days = {
            "Monday": self.main_page_view.checkBox_monday.isChecked(),
            "Tuesday": self.main_page_view.checkBox_tuesday.isChecked(),
            "Wednesday": self.main_page_view.checkBox_wednesday.isChecked(),
            "Thursday": self.main_page_view.checkBox_thursday.isChecked(),
            "Friday": self.main_page_view.checkBox_friday.isChecked(),
        }

        value = {
            "instructor_name": instructor_name,
            "lessons": lessons,
            "preferred_days": days
        }
        print(value)
        self.data_signal.emit(value)
        QMessageBox.information(None, "Success!", "Instructor has been added successfully!")



    def get_all_elements(self):
        model = self.main_page_view.listView_instructor_lessons.model()

        elements = []
        for row in range(model.rowCount()):
            item = model.item(row) 
            elements.append(item.text())  
        
        return elements
