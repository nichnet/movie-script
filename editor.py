import re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QFont

from constants import *


font = QFont('Courier', 12)

class Editor(QWidget): 

    def __init__(self, parent):
        super(Editor, self).__init__(parent)

        self.lines = []

        self.initUI()

    def resize(self,width, height):
        #TODO RESIZE NOT WORKING FOR TEXTEDIT. WONT FILL WINDOW HEIGHT
        self.setFixedSize(width, height)
        self.textedit.setFixedSize(width, height)
        self.textedit.setGeometry(0,0, width, height)


    def initUI(self):
        self.container = QWidget(self)
        self.setStyleSheet("background-color: #C8C8C8")

        self.page_format = page_formats.get("letter")

        self.textedit = QTextEdit(self.container)
        self.textedit.setAlignment(QtCore.Qt.AlignTop)


        self.textedit.setFont(font)

        bgColor = '#C8C8C8'

        if DEBUG: 
            bgColor = 'green'

        self.textedit.setStyleSheet(f"background-color: {bgColor}; padding-left:10; padding-top:10; padding-bottom:10; padding-right:10;")

    def clear(self):
        self.textedit.setPlainText('')

    def setTextChangedListener(self, callback):
        self.textedit.textChanged.connect(callback)
        
    def setValue(self, value):
        self.textedit.setPlainText(value)


    def addLine(self, line):
#        self.lines.append(line)
        self.textedit.setPlainText(self.textedit.toPlainText() + line + "\n")

    def getLines(self):
        trimmed = re.sub(r'\n+', '\n', self.textedit.toPlainText())
        return trimmed.split('\n')
