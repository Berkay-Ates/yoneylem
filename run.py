from PyQt5.QtWidgets import QApplication
from controllers.main_page_controller import MainPageController

app = QApplication([])
window = MainPageController()
window.show()
app.exec_()
