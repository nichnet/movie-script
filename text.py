from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QDrag, QPixmap
from constants import *
import re


font = QFont('Courier', 12)


class Text(QLabel):

    def getBottom(self):
        return self.y + self.size().height()
         
    def __init__(self, parent, line, element, lastBottom = 0):
        super(Text, self).__init__(parent)

        self.parent = parent
        self.line = line
        self.element = element
        
        self.initUI(lastBottom)

    def initUI(self, lastBottom):
        self.setWordWrap(True)
        self.setFont(font)

        page_rule = page_rules.get(self.element.get("type"), {})

        self.uppercase = page_rule.get("uppercase", False)
        self.bold = page_rule.get("bold", False)
        self.italic = page_rule.get("italic", False)
        self.underline = page_rule.get("underline", False)

        self.updateStyleSheet()


        page_content_margin = page_rules.get(ElementType.PAGE).get("margin")#["page"]['margin']
        text_type_margin = page_rule.get("margin", {"left": 0, "right": 0, "top": 0, "bottom": 0})
        content_width = page_formats.get("letter").get("width") - page_content_margin.get("left", 0) - page_content_margin.get("right", 0)
        
        x = convert_inches_to_pixels(text_type_margin.get("left", 0) )
       # self.y = (self.line * LINE_HEIGHT) + convert_inches_to_pixels(text_type_margin.get("top", 0) )
       
        # to get this Y position, get the last bottom + the  margin top size
        self.y = lastBottom + convert_inches_to_pixels(text_type_margin.get("top", 0) )
        width = convert_inches_to_pixels(content_width - text_type_margin.get("left", 0) - text_type_margin.get("right", 0) )
        self.setFixedWidth(width)
        

        #set the initial size
        self.setGeometry(x, self.y, width, LINE_HEIGHT)

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


    def updateStyleSheet(self):
        
        _type = self.element.get("type")
        
        bgColor = "transparent"
        if get_debug_mode():
            if _type == ElementType.ACTION:
                bgColor = "green"
            elif _type == ElementType.SCENE:
                bgColor = "pink"
            elif _type == ElementType.TITLE:
                bgColor = "red"
            elif _type == ElementType.DIALOGUE:
                bgColor = "blue"
            elif _type == ElementType.TRANSITION:
                bgColor = "orange"

        #TODO built-in Courier font doesnt seem to support BOLD on some computers. Trying with another font that does
        # support it makes bold font but currently not working. Code here itself does work! Just need to add a local courier ttf which supports bold.

        weight = 'normal'

        if self.bold == True: 
            weight = 'bold'

        decoration = 'none'

        if self.underline:
            decoration = 'underline'

        self.setStyleSheet(f"text-decoration: {decoration}; font-weight: {weight}; background-color: {bgColor}")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: red;")

    def leaveEvent(self, event):
        self.updateStyleSheet()

    def mousePressEvent (self, event):
        print("clicked!")

    def setValue(self, value):
        _type = self.element.get("type")
        v = value

        if self.uppercase == True: 
            v = v.upper() 

        header = ""
        trailer = ""

        if _type == ElementType.TRANSITION:
            trailer = ":" 
        elif _type == ElementType.DIALOGUE:
            #character name
            speaker = self.element.get("speaker", "")
            
            voof = ""
 #           if self.element.get("voiceover", False) == True:
 #               voof += " (V.O.)"
 #           if self.element.get("offscreen", False) == True:
 #               voof += " (O.S.)"

            header = speaker + voof + self.line_break()
            header = header.upper()

        elif _type == ElementType.SCENE:
            intext = ""
            if self.element.get("int", False) == True:
                intext += "INT - "
            if self.element.get("ext", False) == True:
                intext += "EXT - "

#            if self.element.get("show_int_ext", False) == True:
            header = f'{self.element.get("scene_number", 1)} {intext}'


        #Allow bold, underline, break, and italic but no other HTML tags
        html_tags_to_keep = ['u', 'b', 'br', 'i']
        regex = re.compile(r'<(?!\/?(%s)\s*>)\/?.*?>' % '|'.join(html_tags_to_keep), re.IGNORECASE)
        v = regex.sub('', v)

        self.setText(header + v + trailer)

        #update the size of the label
        #since it has a fixed width, only the height may increase (or decrease)
        # and the value wrapped.
        self.adjustSize()

    def line_break(self):
        return "\r\n"

    def get_line_count(self):
        return int(self.size().height() / LINE_HEIGHT) + 1 # + 1 because each element will have a "new line" below it. 

    def get_height(self):
        self.size().height()