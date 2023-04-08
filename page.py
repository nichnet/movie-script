from PyQt5.QtWidgets import QFrame

from pagebody import PageBody
from text import Text

from constants import *

class Page(QFrame):
    def __init__(self, parent, page_number):
        super(Page, self).__init__(parent)
        self.parent = parent
        self.page_number = page_number



        page_format = page_formats.get("letter")
        page_margin_rule = page_rules.get(ElementType.PAGE).get("margin")
        self.PAGE_WIDTH = convert_inches_to_pixels(page_format.get("width"))
        self.PAGE_HEIGHT = convert_inches_to_pixels(page_format.get("height"))
        self.HEADER_HEIGHT = convert_inches_to_pixels(page_margin_rule.get("top", 0))
        self.MARGIN_LEFT = convert_inches_to_pixels(page_margin_rule.get("left", 0))
        self.MARGIN_RIGHT = convert_inches_to_pixels(page_margin_rule.get("right", 0))

        self.initUI()


    def get_page_number(self):
        return self.page_number
    
    def initUI(self):
        headerColor = 'transparent'
        footerColor = 'transparent'
        bgColor = 'transparent'

        if DEBUG:
            headerColor = 'green'
            footerColor = 'pink'
            bgColor = 'yellow'


       # self.page = QFrame()
        self.setFixedSize(self.PAGE_WIDTH, self.PAGE_HEIGHT)
        self.setStyleSheet(f'background-color: transparent')
    
        self.bg = QFrame(self)
        self.bg.setGeometry(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT)

        self.bg.setStyleSheet(f'background-color: white; border: 1px solid black')
        

        width = self.PAGE_WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT

        #body
        self.body = PageBody(self)

        #header
        self.header = QFrame(self)
        self.header.setGeometry(self.MARGIN_LEFT, 0, width, self.HEADER_HEIGHT)

     

        self.header.setStyleSheet(f'background-color: {headerColor}')

        #footer
        self.footer = QFrame(self)
        self.footer.setGeometry(self.MARGIN_LEFT, self.PAGE_HEIGHT - self.HEADER_HEIGHT, width, self.HEADER_HEIGHT)
        self.footer.setStyleSheet(f'background-color: {footerColor}')

    
    def add_body_element(self, line, element, lastBottom):
        text = Text(self.body, line, element, lastBottom)
        return text

    def add_header_element(self, line, element):
        text = Text(self.header, line, element)
        return text
