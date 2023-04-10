from PyQt5.QtWidgets import QFrame
from constants import *

class PageBody(QFrame):
    def __init__(self, parent):
        super(PageBody, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        page_format = page_formats.get("letter")
        page_margin_rule = page_rules.get(ElementType.PAGE).get("margin")
 
        PAGE_WIDTH = convert_inches_to_pixels(page_format.get("width"))
        PAGE_HEIGHT = convert_inches_to_pixels(page_format.get("height"))
        HEADER_HEIGHT = convert_inches_to_pixels(page_margin_rule.get("top", 0))
       
        MARGIN_LEFT = convert_inches_to_pixels(page_margin_rule.get("left", 0))
        MARGIN_RIGHT = convert_inches_to_pixels(page_margin_rule.get("right", 0))

        width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

        self.setGeometry(MARGIN_LEFT, HEADER_HEIGHT, width, PAGE_HEIGHT + HEADER_HEIGHT - (HEADER_HEIGHT * 2))

        backgroundColor = 'transparent'

        if get_debug_mode(): 
            backgroundColor = 'cyan'

        self.setStyleSheet(f'background-color: {backgroundColor}')

    def adjustSize(self, lines):
        self.size().height = lines * LINE_HEIGHT      

