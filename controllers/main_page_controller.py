import json
from PyQt5.QtWidgets import *
from controllers.ai_chat_page_controller import AIChatPageController
from view_py_files.main_page import Ui_MainWindow as MainPage
from controllers.add_lesson_controller import AddLessonController
from controllers.add_instructor_controller import AddInstructorController
from controllers.add_classroom_controller import AddClassroomController
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from utils.draw_file import generate_schedule_pdf, format_solver_solution
from utils.solve_schedule import solve_schedule


class MainPageController(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        self.init_ui_elements()
        self.config_data = {"instructors": [], "lessons": [], "classrooms": []}

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

        self.main_page_view.pushButton_find_solution.clicked.connect(self.on_find_solution_clicked)

    def on_find_solution_clicked(self):
        from pprint import pprint

        file_name = self.main_page_view.lineEdit_outupt_file_name.text().split(".")[0] + ".pdf"

        if file_name == ".pdf":
            QMessageBox.warning(self, "Warning!", "Please enter a valid file name!")
            return

        pprint(self.config_data)
        solution = solve_schedule(self.config_data)
        if solution is None:
            QMessageBox.warning(self, "Warning!", "No solution found!")
            return

        formatted_solution = format_solver_solution(solution)
        generate_schedule_pdf(formatted_solution, file_name)
        QMessageBox.information(self, "Success!", "Schedule has been generated successfully!")

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
        self.inspect_classroom = AddClassroomController(
            self.config_data["classrooms"][selected_indexes], selected_indexes
        )
        self.inspect_classroom.main_page_view.pushButton_save_classroom.setEnabled(False)
        self.inspect_classroom.data_signal_update.connect(self.on_classroom_data_updated)
        self.inspect_classroom.show()

    def on_inspect_lesson_clicked(self):
        selected_indexes = self.main_page_view.listView_lessons.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Warning!", "Please select a lesson to inspect")
            return

        selected_indexes = selected_indexes[0].row()

        self.inspect_lesson = AddLessonController(self.config_data)

        self.inspect_lesson.main_page_view.lineEdit_lesson_name.setText(
            self.config_data["lessons"][selected_indexes]["name"]
        )
        self.inspect_lesson.main_page_view.lineEdit_lesson_hour.setText(
            str(self.config_data["lessons"][selected_indexes]["duration"])
        )

        for instructor in self.config_data["lessons"][selected_indexes]["instructors"]:
            item = QStandardItem(instructor)
            self.inspect_lesson.model.appendRow(item)

        lesson_type = self.config_data["lessons"][selected_indexes]["type"]

        if lesson_type == "FaceToFace":
            self.inspect_lesson.main_page_view.radioButton_face_to_face.setChecked(True)
        elif lesson_type == "Online":
            self.inspect_lesson.main_page_view.radioButton_online.setChecked(True)
        elif lesson_type == "Hybrid":
            self.inspect_lesson.main_page_view.radioButton_hybrid.setChecked(True)

        self.inspect_lesson.main_page_view.comboBox_grades.setCurrentText(
            str(self.config_data["lessons"][selected_indexes]["grade"])
        )
        self.inspect_lesson.main_page_view.comboBox_lesson_group.setCurrentText(
            str(self.config_data["lessons"][selected_indexes]["group"])
        )
        self.inspect_lesson.main_page_view.comboBox_obligation.setCurrentText(
            self.config_data["lessons"][selected_indexes]["obligation"]
        )
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
        self.inspect_instructor = AddInstructorController(self.config_data, selected_indexes)

        self.inspect_instructor.main_page_view.lineEdit_instructor_name.setText(
            self.config_data["instructors"][selected_indexes]["name"]
        )
        for lesson in self.config_data["instructors"][selected_indexes]["lessons"]:
            item = QStandardItem(lesson)
            self.inspect_instructor.model.appendRow(item)

        for day in self.config_data["instructors"][selected_indexes]["preferred_days"]:
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

        self.inspect_instructor.data_signal_update.connect(self.on_instructor_data_updated)
        self.inspect_instructor.main_page_view.pushButton_save_instructor.setEnabled(False)
        self.inspect_instructor.show()

    def on_add_instructor_clicked(self):
        self.add_instructor_page = AddInstructorController(self.config_data)
        self.add_instructor_page.show()
        self.add_instructor_page.data_signal.connect(self.on_instructor_data_received)
        self.add_instructor_page.main_page_view.pushButton_update_instructor.setEnabled(False)

    def on_add_lesson_clicked(self):
        self.add_lesson_page = AddLessonController(self.config_data)
        self.add_lesson_page.show()
        self.add_lesson_page.data_signal.connect(self.on_lesson_data_received)

    def on_add_classroom_clicked(self):
        self.add_classroom_page = AddClassroomController()
        self.add_classroom_page.show()
        self.add_classroom_page.data_signal.connect(self.on_classroom_data_received)
        self.add_classroom_page.main_page_view.pushButton_update_classroom.setEnabled(False)

    def on_chat_page_clicked(self):
        self.ai_chat_page = AIChatPageController()
        self.ai_chat_page.show()

    def on_classroom_data_received(self, data):
        self.config_data["classrooms"].append(data)
        self.update_list_views()

    def on_lesson_data_received(self, data):
        self.config_data["lessons"].append(data)
        self.update_list_views()

    def on_classroom_data_updated(self, data, index):
        self.config_data["classrooms"][index] = data
        self.update_list_views()


    def on_instructor_data_updated(self, data, index):
        self.config_data["instructors"][index] = data
        self.update_list_views()

    def on_instructor_data_received(self, data):
        self.config_data["instructors"].append(data)
        self.update_list_views()

    def save_configuration(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json);;All Files (*)", options=options
        )

        if file_name:
            with open(file_name, "w") as json_file:
                json.dump(self.config_data, json_file, indent=4)

            QMessageBox.information(None, "Success!", "Configuration has been saved successfully!")

        self.main_page_view.label_output_file.setText("Exported File:" + file_name)

    def load_configuration(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)", options=options
        )

        if file_name:
            with open(file_name, "r") as json_file:
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
            item = QStandardItem(lesson["name"])
            self.lesson_model.appendRow(item)

        for instructor in self.config_data["instructors"]:
            item = QStandardItem(instructor["name"])
            self.instructor_model.appendRow(item)

        for classroom in self.config_data["classrooms"]:
            item = QStandardItem(classroom)
            self.classroom_model.appendRow(item)
