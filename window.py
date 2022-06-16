from PyQt5.QtWidgets import QMainWindow
from constants import *

from workarea import WorkArea


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle = "Script - New"

    def setWorkareaContent(self, content):
        self.workarea = WorkArea(self)
        self.workarea.setContent(content)

    def resizeEvent(self, event):
        print(f"window resized {self.size().width()}")
        self.workarea.resize(self.get_width(), self.get_height())

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

