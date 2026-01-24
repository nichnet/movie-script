from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics
from PyQt5.QtCore import Qt

from pagebody import PageBody
from text import Text

from config import app_state
from elements import ElementType
from page_rules import PAGE_FORMATS, PAGE_RULES


class WatermarkLabel(QLabel):
    """A label that displays diagonal watermark text."""

    def __init__(self, parent, text=""):
        super().__init__(parent)
        self.watermark_text = text
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_watermark(self, text):
        self.watermark_text = text
        self.update()

    def paintEvent(self, event):
        if not self.watermark_text or not app_state.show_watermark:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate diagonal length of the page (this is max text width we can fit)
        import math
        diagonal = math.sqrt(self.width() ** 2 + self.height() ** 2)

        # Find font size that makes text span ~70% of the diagonal
        target_width = diagonal * 0.7
        font_size = 20  # Start with base size

        font = QFont('Arial', font_size, QFont.Bold)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.watermark_text)

        # Scale font size to fit target width
        if text_width > 0:
            font_size = int(font_size * (target_width / text_width))
            font_size = max(40, min(font_size, 200))  # Clamp between 40 and 200

        font = QFont('Arial', font_size, QFont.Bold)
        painter.setFont(font)

        # Set color - light gray with transparency
        color = QColor(150, 150, 150, 60)
        painter.setPen(color)

        # Calculate center and rotate
        center_x = self.width() // 2
        center_y = self.height() // 2

        painter.translate(center_x, center_y)
        painter.rotate(-45)

        # Draw text centered
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.watermark_text)
        text_height = fm.height()

        painter.drawText(-text_width // 2, text_height // 4, self.watermark_text)
        painter.end()


class Page(QFrame):
    def __init__(self, parent, page_number, watermark=None):
        super(Page, self).__init__(parent)
        self.parent = parent
        self.page_number = page_number
        self.watermark_text = watermark

        page_format = PAGE_FORMATS.get(app_state.page_size)
        page_margin_rule = PAGE_RULES.get(ElementType.PAGE).get("margin")
        self.PAGE_WIDTH = app_state.convert_inches_to_pixels(page_format.get("width"))
        self.PAGE_HEIGHT = app_state.convert_inches_to_pixels(page_format.get("height"))
        self.HEADER_HEIGHT = app_state.convert_inches_to_pixels(page_margin_rule.get("top", 0))
        self.MARGIN_LEFT = app_state.convert_inches_to_pixels(page_margin_rule.get("left", 0))
        self.MARGIN_RIGHT = app_state.convert_inches_to_pixels(page_margin_rule.get("right", 0))

        self.initUI()


    def get_page_number(self):
        return self.page_number
    
    def initUI(self):
        headerColor = 'transparent'
        footerColor = 'transparent'
        bgColor = 'transparent'

        if app_state.debug:
            headerColor = 'green'
            footerColor = 'pink'
            bgColor = 'yellow'


       # self.page = QFrame()
        self.setFixedSize(self.PAGE_WIDTH, self.PAGE_HEIGHT)
      # self.setStyleSheet(f'background-color: transparent; ')
    
        self.bg = QFrame(self)
        self.bg.setGeometry(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT)

        self.applyTheme()
        
        #add shadow effect to page
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)

        # Apply the drop shadow effect to the button
        self.setGraphicsEffect(shadow)

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

        # Watermark (on top of everything)
        self.watermark_label = WatermarkLabel(self, self.watermark_text or "")
        self.watermark_label.setGeometry(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT)
        self.watermark_label.raise_()  # Bring to front

    
    def add_body_element(self, line, element, lastBottom):
        text = Text(self.body, line, element, lastBottom)
        return text

    def add_header_element(self, line, element):
        text = Text(self.header, line, element)
        return text

    def applyTheme(self):
        dark = app_state.dark_mode
        if dark:
            self.bg.setStyleSheet('background-color: #1e1e1e; border: 1px solid #555;')
        else:
            self.bg.setStyleSheet('background-color: white; border: 1px solid black;')
