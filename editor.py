from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtGui import QFont

from constants import *


font = QFont('Courier', 12)

class Editor(QWidget): 

    def __init__(self, parent):
        super(Editor, self).__init__(parent)

        self.initUI()

    def resize(self,width, height):
        print(f"resized: {width} {self.textedit.size().width()}")
        self.setFixedSize(width, height)
       # self.textedit.setFixedSize(width, height)


    def initUI(self):
        self.container = QWidget(self)
        self.setStyleSheet("background-color:cyan")

        page_format = page_formats.get("letter")




        self.textedit = QTextEdit(self.container)
        self.textedit.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)


        self.textedit.setGeometry(0,0, convert_inches_to_pixels(page_format.get("width")), convert_inches_to_pixels(page_format.get("height")))



        self.textedit.setFont(font)
        self.textedit.setStyleSheet("background-color: red;padding-left:10; padding-top:10; padding-bottom:10; padding-right:10;")


    def setValue(self, value):
        self.textedit.setPlainText(value)