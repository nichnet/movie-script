from PyQt5.QtWidgets import QMainWindow
from constants import *

from workarea import WorkArea
from editor import Editor

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setMinimumSize(WIDTH, HEIGHT)
        self.setWindowTitle = "Script - New"


        self.createEditorLayout()

    def createEditorLayout(self):
        self.editor = Editor(self)
        self.editor.move(0, self.get_width() - 175)


    def setWorkareaContent(self, content):
        self.workarea = WorkArea(self)
        self.workarea.setContent(content)

    def resizeEvent(self, event):
        print(f"window resized {self.size().width()}")
        self.workarea.resize(self.get_width() - 175, self.get_height() - 200)
        self.editor.resize(self.get_width() - 175, 200)
        self.editor.move(0, self.get_height() - 200)

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

