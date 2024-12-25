from PyQt5.QtWidgets import *
from dotenv import load_dotenv
from view_py_files.ai_chat import Ui_MainWindow as MainPage
from llama.versions.lama32 import Llama32
from PyQt5.QtCore import QTimer

class AIChatPageController(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.main_page_view = MainPage()
        self.main_page_view.setupUi(self)
        load_dotenv()
        self.main_page_view.pushButton_send_ai.clicked.connect(self.on_ai_chat_button_clicked)
        self.llama = Llama32()

    def on_ai_chat_button_clicked(self):
        user_message = self.main_page_view.textEdit_user_message.toPlainText().strip()
        if not user_message:
            QMessageBox.warning(self, "Warning!", "Please enter a message.")
            return
        
        messages = [{"role": "user", "content": user_message}]
        self.response = self.llama.generate(messages)  
        
        self.main_page_view.textEdit_user_message.clear()
        
        self.typing_index = 0 
        
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_next_character)
        self.typing_timer.start(50)  

    def type_next_character(self):
        CHUNK_SIZE = 15  
        if self.typing_index < len(self.response):
            current_text = self.main_page_view.label_ai_chat.text()
            self.main_page_view.label_ai_chat.setText(
                current_text + self.response[self.typing_index:self.typing_index + CHUNK_SIZE]
            )
            self.typing_index += CHUNK_SIZE
        else:
            self.typing_timer.stop() 