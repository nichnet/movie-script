from PyQt5.QtWidgets import QFrame

from config import LINE_HEIGHT, app_state
from elements import ElementType
from page_rules import PAGE_FORMATS, PAGE_RULES

class PageBody(QFrame):
    def __init__(self, parent):
        super(PageBody, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        page_format = PAGE_FORMATS.get("letter")
        page_margin_rule = PAGE_RULES.get(ElementType.PAGE).get("margin")

        PAGE_WIDTH = app_state.convert_inches_to_pixels(page_format.get("width"))
        PAGE_HEIGHT = app_state.convert_inches_to_pixels(page_format.get("height"))
        HEADER_HEIGHT = app_state.convert_inches_to_pixels(page_margin_rule.get("top", 0))

        MARGIN_LEFT = app_state.convert_inches_to_pixels(page_margin_rule.get("left", 0))
        MARGIN_RIGHT = app_state.convert_inches_to_pixels(page_margin_rule.get("right", 0))

        width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

        self.setGeometry(MARGIN_LEFT, HEADER_HEIGHT, width, PAGE_HEIGHT + HEADER_HEIGHT - (HEADER_HEIGHT * 2))

        backgroundColor = 'transparent'

        if app_state.debug:
            backgroundColor = 'cyan'

        self.setStyleSheet(f'background-color: {backgroundColor}')

    def adjustSize(self, lines):
        self.size().height = lines * LINE_HEIGHT      

