from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QDrag, QPixmap
from constants import *

font = QFont('Courier', 12)


class Text(QLabel):
    def __init__(self, parent, line, element):
        super(Text, self).__init__(parent)

        self.parent = parent
        self.line = line
        self.element = element
        
        self.initUI()

    def initUI(self):
        self.setWordWrap(True)
        self.setFont(font)

        page_rule = page_rules.get(self.element.get("type"), {})

        self.uppercase = page_rule.get("uppercase", False)
        self.bold = page_rule.get("bold", False)
        self.italic = page_rule.get("bold", False)


        if self.bold: 
            self.weight = "bold" 
        else:
            self.weight =  "normal"

        self.updateStyleSheet("transparent")


        page_content_margin = page_rules.get("page").get("margin")#["page"]['margin']
        text_type_margin = page_rule.get("margin", {"left": 0, "right": 0, "top": 0, "bottom": 0})
        content_width = page_formats.get("letter").get("width") - page_content_margin.get("left", 0) - page_content_margin.get("right", 0)
        
        x = convert_inches_to_pixels(get_dpi(), text_type_margin.get("left", 0) )
        y = self.line * LINE_HEIGHT + convert_inches_to_pixels(get_dpi(), text_type_margin.get("top", 0) )
        width = convert_inches_to_pixels(get_dpi(), content_width - text_type_margin.get("left", 0) - text_type_margin.get("right", 0) )
        self.setFixedWidth(width)
        

        #set the initial size
        self.setGeometry(x, y, width, LINE_HEIGHT)

        #set alignment
        alignment = QtCore.Qt.AlignLeft
        alignment_type = page_rule.get("align", "left")

        if alignment_type == 'center':
            alignment = QtCore.Qt.AlignHCenter
        elif alignment_type == 'right':
            alignment = QtCore.Qt.AlignRight
        else:
            #left or not set, align left
            alignment = QtCore.Qt.AlignLeft

        self.setAlignment(alignment | QtCore.Qt.AlignTop)

        #finally set the value        
        self.setValue(self.element.get("value"))

    def updateStyleSheet(self, bcolor):
        self.setStyleSheet(f"font-weight: { self.weight }; background-color: {bcolor};")

    def enterEvent(self, event):
        self.updateStyleSheet("red")

    def leaveEvent(self, event):
        self.updateStyleSheet("transparent")

    def mousePressEvent (self, event):
        print("clicked!")


    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            drag = QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)
            drag.exec_(QtCore.Qt.MoveAction)


    def setValue(self, value):
        _type = self.element.get("type")
        v = value

        if self.uppercase == True: 
            v = v.upper() 

        header = ""
        trailer = ""

        if _type == "transition":
            trailer = ":" 
        elif _type == "dialogue":
            #character name
            character = self.element.get("character")
            
            voof = ""
            if self.element.get("voiceover", False) == True:
                voof += " (V.O.)"
            if self.element.get("offscreen", False) == True:
                voof += " (O.S.)"

            header = character + voof + self.line_break()
            header = header.upper()

        elif _type == "scene":
            intext = ""
            if self.element.get("int", False) == True:
                intext += "INT - "
            else:
                intext += "EXT - "

            if self.element.get("show_int_ext", False) == True:
                header = intext

        self.setText(header + v + trailer)

        #update the size of the label
        #since it has a fixed width, only the height may increase (or decrease)
        # and the value wrapped.
        self.adjustSize()

    def line_break(self):
        return "\r\n"

    def get_line_count(self):
        return int(self.size().height() / LINE_HEIGHT)