from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
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
        self.setWindowTitle("Inkwell - New")


        #application icon
        icon = QIcon()
        pixmap = QPixmap("resources/draw_ink.png")
        icon.addPixmap(pixmap)
        #app.setWindowIcon(app_icon)

        # Set window icon
        self.setWindowIcon(icon)

       


        self.editor = Editor(self)
        self.preview = WorkArea(self)

        self.editor.setTextChangedListener(self.onTextChanged)

##        self.createEditorLayout()

    def onTextChanged(self):
        self.preview.setContent(self.editor.getLines())  

#    def createEditorLayout(self):
 #       self.editor = Editor(self)
#        self.editor.move(0, self.get_width() / 2)


#    def setWorkareaContent(self, content):
#        self.preview.setContent(content)

    def resizeEvent(self, event):
        editorWidth =  500
        previewWidth = self.get_width() - editorWidth


        self.preview.resize(previewWidth, self.get_height())
        self.preview.move(0, 0)
    
        self.editor.resize(editorWidth, self.get_height())
        self.editor.move(previewWidth, 0)

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

    def addLine(self, line):
        self.editor.addLine(line)