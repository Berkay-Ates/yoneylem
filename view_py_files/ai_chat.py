# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/berkay/yoneylem/view_ui_files/ai_chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1364, 866)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit_user_message = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_user_message.sizePolicy().hasHeightForWidth())
        self.textEdit_user_message.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_user_message.setFont(font)
        self.textEdit_user_message.setObjectName("textEdit_user_message")
        self.horizontalLayout.addWidget(self.textEdit_user_message)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_4.addWidget(self.comboBox, 3, 0, 1, 1)
        self.pushButton_stop_ai = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_stop_ai.setFont(font)
        self.pushButton_stop_ai.setObjectName("pushButton_stop_ai")
        self.gridLayout_4.addWidget(self.pushButton_stop_ai, 1, 0, 1, 1)
        self.pushButton_send_ai = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_send_ai.setFont(font)
        self.pushButton_send_ai.setObjectName("pushButton_send_ai")
        self.gridLayout_4.addWidget(self.pushButton_send_ai, 0, 0, 1, 1)
        self.pushButton_clear_chat = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_clear_chat.setFont(font)
        self.pushButton_clear_chat.setObjectName("pushButton_clear_chat")
        self.gridLayout_4.addWidget(self.pushButton_clear_chat, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listView_loaded_files = QtWidgets.QListView(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listView_loaded_files.setFont(font)
        self.listView_loaded_files.setObjectName("listView_loaded_files")
        self.verticalLayout_3.addWidget(self.listView_loaded_files)
        self.label_ai_speed = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_ai_speed.setFont(font)
        self.label_ai_speed.setObjectName("label_ai_speed")
        self.verticalLayout_3.addWidget(self.label_ai_speed)
        self.horizontalSlider_ai_speed = QtWidgets.QSlider(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.horizontalSlider_ai_speed.setFont(font)
        self.horizontalSlider_ai_speed.setMinimum(1)
        self.horizontalSlider_ai_speed.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_ai_speed.setObjectName("horizontalSlider_ai_speed")
        self.verticalLayout_3.addWidget(self.horizontalSlider_ai_speed)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_upload_file = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_upload_file.setFont(font)
        self.pushButton_upload_file.setObjectName("pushButton_upload_file")
        self.verticalLayout_2.addWidget(self.pushButton_upload_file)
        self.pushButton_import_ai_suggestion = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_import_ai_suggestion.setFont(font)
        self.pushButton_import_ai_suggestion.setObjectName("pushButton_import_ai_suggestion")
        self.verticalLayout_2.addWidget(self.pushButton_import_ai_suggestion)
        self.pushButton_delete_selected_file = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_delete_selected_file.setFont(font)
        self.pushButton_delete_selected_file.setObjectName("pushButton_delete_selected_file")
        self.verticalLayout_2.addWidget(self.pushButton_delete_selected_file)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 2, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1051, 616))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_ai_chat = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ai_chat.sizePolicy().hasHeightForWidth())
        self.label_ai_chat.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_ai_chat.setFont(font)
        self.label_ai_chat.setText("")
        self.label_ai_chat.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_ai_chat.setWordWrap(True)
        self.label_ai_chat.setObjectName("label_ai_chat")
        self.gridLayout_3.addWidget(self.label_ai_chat, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit_user_message.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_user_message.setPlaceholderText(_translate("MainWindow", "Type..."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Options"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Llama 3.1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Llama 3.2"))
        self.pushButton_stop_ai.setText(_translate("MainWindow", "STOP"))
        self.pushButton_send_ai.setText(_translate("MainWindow", "SEND"))
        self.pushButton_clear_chat.setText(_translate("MainWindow", "Clear Chat"))
        self.groupBox.setTitle(_translate("MainWindow", "Files"))
        self.label_ai_speed.setText(_translate("MainWindow", "Output Speed: "))
        self.pushButton_upload_file.setText(_translate("MainWindow", "Upload file "))
        self.pushButton_import_ai_suggestion.setText(_translate("MainWindow", "Import Suggestion"))
        self.pushButton_delete_selected_file.setText(_translate("MainWindow", "Delete Selecte File"))
