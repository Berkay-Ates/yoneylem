import json
from PyQt5.QtWidgets import *
from controllers.ai_chat_page_controller import AIChatPageController
from view_py_files.main_page import Ui_MainWindow as MainPage
from controllers.add_lesson_controller import AddLessonController
from controllers.add_instructor_controller import AddInstructorController
from controllers.add_classroom_controller import AddClassroomController
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class MainPageController(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.init_ui_elements()
        self.config_data = {
            "instructors": [],
            "lessons": [],
            "classrooms": []
        }
    
    def init_ui_elements(self):
        self.main_page_view.menuMain_Page.triggered.connect(self.on_chat_page_clicked)
        self.main_page_view.pushButton_add_classroom.clicked.connect(self.on_add_classroom_clicked)
        self.main_page_view.pushButton_add_lesson.clicked.connect(self.on_add_lesson_clicked)
        self.main_page_view.pushButton_add_instructor.clicked.connect(self.on_add_instructor_clicked)

        self.main_page_view.pushButton_load_variables.clicked.connect(self.load_configuration)
        self.main_page_view.pushButton_export_variables.clicked.connect(self.save_configuration)

        self.main_page_view.pushButton_inspect_classroom.clicked.connect(self.on_inspect_classroom_clicked)
        self.main_page_view.pushButton_inspect_lesson.clicked.connect(self.on_inspect_lesson_clicked)   
        self.main_page_view.pushButton_inspect_instructors.clicked.connect(self.on_inspect_instructor_clicked)

        self.main_page_view.pushButton_delete_classroom.clicked.connect(self.on_delete_classroom_clicked)
        self.main_page_view.pushButton_delete_lesson.clicked.connect(self.on_delete_lesson_clicked)
        self.main_page_view.pushButton_delete_instructor.clicked.connect(self.on_delete_instructor_clicked)

        self.instructor_model = QStandardItemModel(self.main_page_view.listView_instructors)
        self.lesson_model = QStandardItemModel(self.main_page_view.listView_lessons)
        self.classroom_model = QStandardItemModel(self.main_page_view.listView_classrooms)

        self.main_page_view.listView_instructors.setModel(self.instructor_model)
        self.main_page_view.listView_lessons.setModel(self.lesson_model)
        self.main_page_view.listView_classrooms.setModel(self.classroom_model)

    def on_delete_instructor_clicked(self):
        selected_indexes = self.main_page_view.listView_instructors.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select an instructor to delete.")
            return
        selected_indexes = selected_indexes[0].row()
        self.config_data["instructors"].pop(selected_indexes)
        self.update_list_views()

    def on_delete_lesson_clicked(self):
        selected_indexes = self.main_page_view.listView_lessons.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select a lesson to delete.")
            return
        selected_indexes = selected_indexes[0].row()
        self.config_data["lessons"].pop(selected_indexes)
        self.update_list_views()

    def on_delete_classroom_clicked(self):
        selected_indexes = self.main_page_view.listView_classrooms.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select a classroom to delete.")
            return
        selected_indexes = selected_indexes[0].row()
        self.config_data["classrooms"].pop(selected_indexes)
        self.update_list_views()

    def on_inspect_classroom_clicked(self):
        selected_indexes = self.main_page_view.listView_classrooms.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select a classroom to inspect.")
            return
        selected_indexes = selected_indexes[0].row()
        self.inspect_classroom = AddClassroomController()
        self.inspect_classroom.main_page_view.lineEdit_classroom_name.setText(self.config_data["classrooms"][selected_indexes]) 
        self.inspect_classroom.show()


    def on_inspect_lesson_clicked(self):
        selected_indexes = self.main_page_view.listView_lessons.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select a lesson to inspect")
            return
        
        selected_indexes = selected_indexes[0].row()
        
        self.inspect_lesson = AddLessonController(self.config_data)

        self.inspect_lesson.main_page_view.lineEdit_lesson_name.setText(self.config_data["lessons"][selected_indexes]["lesson_name"])
        self.inspect_lesson.main_page_view.lineEdit_lesson_hour.setText(str(self.config_data["lessons"][selected_indexes]["lesson_hour"]))

        for instructor in self.config_data["lessons"][selected_indexes]["instructors"]:
            item = QStandardItem(instructor)
            self.inspect_lesson.model.appendRow(item)
        
        for lesson_type, value in self.config_data["lessons"][selected_indexes]["lesson_type"].items():
            if value:
                if lesson_type == "Face To Face":
                    self.inspect_lesson.main_page_view.radioButton_face_to_face.setChecked(True)
                elif lesson_type == "Online":
                    self.inspect_lesson.main_page_view.radioButton_online.setChecked(True)
                elif lesson_type == "Hybrid":
                    self.inspect_lesson.main_page_view.radioButton_hybrid.setChecked(True)

        self.inspect_lesson.main_page_view.comboBox_grades.setCurrentText(self.config_data["lessons"][selected_indexes]["grade"])
        self.inspect_lesson.main_page_view.pushButton_save_lesson.setEnabled(False)
        self.inspect_lesson.main_page_view.pushButton_assign_instructor.setEnabled(False)
        self.inspect_lesson.main_page_view.pushButton_remove_selected_instructor.setEnabled(False)
        self.inspect_lesson.show()


        
    def on_inspect_instructor_clicked(self):
        selected_indexes = self.main_page_view.listView_instructors.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select an instructor to inspect.")
            return 
        selected_indexes = selected_indexes[0].row()
        self.inspect_instructor = AddInstructorController(self.config_data)

        self.inspect_instructor.main_page_view.lineEdit_instructor_name.setText(self.config_data["instructors"][selected_indexes]["instructor_name"])   
        for lesson in self.config_data["instructors"][selected_indexes]["lessons"]:
            item = QStandardItem(lesson)
            self.inspect_instructor.model.appendRow(item)

        for day, value in self.config_data["instructors"][selected_indexes]["preferred_days"].items():
            if value:
                if day == "Monday":
                    self.inspect_instructor.main_page_view.checkBox_monday.setChecked(True)
                elif day == "Tuesday":
                    self.inspect_instructor.main_page_view.checkBox_tuesday.setChecked(True)
                elif day == "Wednesday":
                    self.inspect_instructor.main_page_view.checkBox_wednesday.setChecked(True)
                elif day == "Thursday":
                    self.inspect_instructor.main_page_view.checkBox_thursday.setChecked(True)
                elif day == "Friday":
                    self.inspect_instructor.main_page_view.checkBox_friday.setChecked(True) 
        self.inspect_instructor.main_page_view.pushButton_save_instructor.setEnabled(False)
        self.inspect_instructor.main_page_view.pushButton_assign_lesson.setEnabled(False)
        self.inspect_instructor.main_page_view.pushButton_remove_selected_lesson.setEnabled(False)
        self.inspect_instructor.show()


    def on_add_instructor_clicked(self):
        self.add_instructor_page = AddInstructorController(self.config_data)
        self.add_instructor_page.show()
        self.add_instructor_page.data_signal.connect(self.on_instructor_data_received)

    def on_add_lesson_clicked(self):
        self.add_lesson_page = AddLessonController(self.config_data)
        self.add_lesson_page.show()
        self.add_lesson_page.data_signal.connect(self.on_lesson_data_received)

    def on_add_classroom_clicked(self):
        self.add_classroom_page = AddClassroomController()
        self.add_classroom_page.show()
        self.add_classroom_page.data_signal.connect(self.on_classroom_data_received)

    def on_chat_page_clicked(self):
        self.ai_chat_page = AIChatPageController()
        self.ai_chat_page.show()

    def on_classroom_data_received(self, data):
        self.config_data["classrooms"].append(data)
        self.update_list_views()


    def on_lesson_data_received(self, data):
        self.config_data["lessons"].append(data)
        self.update_list_views()


    def on_instructor_data_received(self, data):
        self.config_data["instructors"].append(data)
        self.update_list_views()


    def save_configuration(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            with open(file_name, 'w') as json_file:
                json.dump(self.config_data, json_file, indent=4)

            QMessageBox.information(None, "Success!", "Configuration has been saved successfully!")

        self.main_page_view.label_output_file.setText("Exported File:" + file_name)
    

    def load_configuration(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r') as json_file:
                self.config_data = json.load(json_file)

            self.update_list_views()
            QMessageBox.information(None, "Success!", "Configuration has been loaded successfully!")
        self.main_page_view.label_input_file.setText("Loaded File: " + file_name)


    # Clear the list then add the elements from the config_data
    def update_list_views(self):
        self.instructor_model.clear()
        self.lesson_model.clear()
        self.classroom_model.clear()

        for lesson in self.config_data["lessons"]:
            item = QStandardItem(lesson["lesson_name"])
            self.lesson_model.appendRow(item)

        for instructor in self.config_data["instructors"]:
            item = QStandardItem(instructor["instructor_name"])
            self.instructor_model.appendRow(item)

        for classroom in self.config_data["classrooms"]:
            item = QStandardItem(classroom)
            self.classroom_model.appendRow(item)

    

        
