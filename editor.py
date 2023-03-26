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
        self.setFixedSize(width, height)
        self.textedit.setGeometry(0,0, width, height)


    def initUI(self):
        self.container = QWidget(self)
        self.setStyleSheet("background-color:cyan")

        self.page_format = page_formats.get("letter")


        self.textedit = QTextEdit(self.container)
        self.textedit.setAlignment(QtCore.Qt.AlignTop)


        self.textedit.setFont(font)
        self.textedit.setStyleSheet("background-color: #C6C6C6; padding-left:10; padding-top:10; padding-bottom:10; padding-right:10;")

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
