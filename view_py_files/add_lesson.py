# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/berkay/yoneylem/view_ui_files/add_lesson.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 941)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_lesson_type = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_lesson_type.setTitle("")
        self.groupBox_lesson_type.setObjectName("groupBox_lesson_type")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_lesson_type)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_face_to_face = QtWidgets.QRadioButton(self.groupBox_lesson_type)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_face_to_face.setFont(font)
        self.radioButton_face_to_face.setObjectName("radioButton_face_to_face")
        self.gridLayout_2.addWidget(self.radioButton_face_to_face, 0, 0, 1, 1)
        self.radioButton_online = QtWidgets.QRadioButton(self.groupBox_lesson_type)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_online.setFont(font)
        self.radioButton_online.setObjectName("radioButton_online")
        self.gridLayout_2.addWidget(self.radioButton_online, 1, 0, 1, 1)
        self.radioButton_hybrid = QtWidgets.QRadioButton(self.groupBox_lesson_type)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_hybrid.setFont(font)
        self.radioButton_hybrid.setObjectName("radioButton_hybrid")
        self.gridLayout_2.addWidget(self.radioButton_hybrid, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_lesson_type, 2, 0, 1, 1)
        self.pushButton_save_lesson = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_save_lesson.setFont(font)
        self.pushButton_save_lesson.setObjectName("pushButton_save_lesson")
        self.gridLayout.addWidget(self.pushButton_save_lesson, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.lineEdit_lesson_name = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_lesson_name.setFont(font)
        self.lineEdit_lesson_name.setObjectName("lineEdit_lesson_name")
        self.verticalLayout.addWidget(self.lineEdit_lesson_name)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_lesson_hour = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_lesson_hour.setFont(font)
        self.lineEdit_lesson_hour.setObjectName("lineEdit_lesson_hour")
        self.verticalLayout.addWidget(self.lineEdit_lesson_hour)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listView_lesson_instructors = QtWidgets.QListView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_lesson_instructors.sizePolicy().hasHeightForWidth())
        self.listView_lesson_instructors.setSizePolicy(sizePolicy)
        self.listView_lesson_instructors.setMinimumSize(QtCore.QSize(0, 140))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listView_lesson_instructors.setFont(font)
        self.listView_lesson_instructors.setObjectName("listView_lesson_instructors")
        self.gridLayout_3.addWidget(self.listView_lesson_instructors, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_remove_selected_instructor = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_remove_selected_instructor.setFont(font)
        self.pushButton_remove_selected_instructor.setObjectName("pushButton_remove_selected_instructor")
        self.gridLayout_3.addWidget(self.pushButton_remove_selected_instructor, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.comboBox_instructors = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_instructors.setFont(font)
        self.comboBox_instructors.setObjectName("comboBox_instructors")
        self.verticalLayout.addWidget(self.comboBox_instructors)
        self.pushButton_assign_instructor = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_assign_instructor.setFont(font)
        self.pushButton_assign_instructor.setObjectName("pushButton_assign_instructor")
        self.verticalLayout.addWidget(self.pushButton_assign_instructor)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.comboBox_grades = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_grades.setFont(font)
        self.comboBox_grades.setObjectName("comboBox_grades")
        self.comboBox_grades.addItem("")
        self.comboBox_grades.addItem("")
        self.comboBox_grades.addItem("")
        self.comboBox_grades.addItem("")
        self.verticalLayout.addWidget(self.comboBox_grades)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.comboBox_lesson_group = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_lesson_group.setFont(font)
        self.comboBox_lesson_group.setObjectName("comboBox_lesson_group")
        self.comboBox_lesson_group.addItem("")
        self.comboBox_lesson_group.addItem("")
        self.comboBox_lesson_group.addItem("")
        self.comboBox_lesson_group.addItem("")
        self.verticalLayout.addWidget(self.comboBox_lesson_group)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.comboBox_obligation = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_obligation.setFont(font)
        self.comboBox_obligation.setObjectName("comboBox_obligation")
        self.comboBox_obligation.addItem("")
        self.comboBox_obligation.addItem("")
        self.verticalLayout.addWidget(self.comboBox_obligation)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.pushButton_update_lesson = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_update_lesson.setFont(font)
        self.pushButton_update_lesson.setObjectName("pushButton_update_lesson")
        self.gridLayout.addWidget(self.pushButton_update_lesson, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton_face_to_face.setText(_translate("MainWindow", "Face To Face"))
        self.radioButton_online.setText(_translate("MainWindow", "Online"))
        self.radioButton_hybrid.setText(_translate("MainWindow", "Hybrid"))
        self.pushButton_save_lesson.setText(_translate("MainWindow", "Add to Lesson List"))
        self.label_5.setText(_translate("MainWindow", "Lesson type"))
        self.label_6.setText(_translate("MainWindow", "Lesson Name"))
        self.lineEdit_lesson_name.setPlaceholderText(_translate("MainWindow", "Lesson Name"))
        self.label_2.setText(_translate("MainWindow", "Lesson Hours"))
        self.lineEdit_lesson_hour.setPlaceholderText(_translate("MainWindow", "Lesson Hour"))
        self.label.setText(_translate("MainWindow", "Instructors"))
        self.pushButton_remove_selected_instructor.setText(_translate("MainWindow", "Remove Selected Instructor"))
        self.label_3.setText(_translate("MainWindow", "Add Instructors"))
        self.comboBox_instructors.setPlaceholderText(_translate("MainWindow", "Select Instructor"))
        self.pushButton_assign_instructor.setText(_translate("MainWindow", "Add Selected Instructors"))
        self.label_4.setText(_translate("MainWindow", "Grade"))
        self.comboBox_grades.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox_grades.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox_grades.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox_grades.setItemText(3, _translate("MainWindow", "4"))
        self.label_7.setText(_translate("MainWindow", "Lesson Group"))
        self.comboBox_lesson_group.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox_lesson_group.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox_lesson_group.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox_lesson_group.setItemText(3, _translate("MainWindow", "4"))
        self.label_8.setText(_translate("MainWindow", "Obligation"))
        self.comboBox_obligation.setItemText(0, _translate("MainWindow", "mandatory"))
        self.comboBox_obligation.setItemText(1, _translate("MainWindow", "elective"))
        self.pushButton_update_lesson.setText(_translate("MainWindow", "Update Lesson"))
