from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from page import Page

import fparse;

from config import MAX_LINES_PER_PAGE, app_state
from elements import ElementType

# Title page element types
TITLE_PAGE_TYPES = {
    ElementType.TITLE_PAGE_TITLE,
    ElementType.TITLE_PAGE_AUTHOR,
    ElementType.TITLE_PAGE_COMMENT,
    ElementType.TITLE_PAGE_DATE,
}


class WorkArea(QScrollArea): 

    def __init__(self, parent):
        super(WorkArea, self).__init__(parent)
        self.parent = parent

        self.pages = []

        self.initUI()

    def resize(self,width, height):
        self.setFixedSize(width, height)


    def initUI(self):
#        self.resize(self.WORKAREA_WIDTH, self.WORKAREA_HEIGHT)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self.container = QWidget()

        self.vbox = QVBoxLayout(self.container)  
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter)

        if app_state.debug:
            self.container.setStyleSheet(f"background-color: pink;")      


    def clearEditor(self):
        self.pages = []

        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



    def setContent(self, content):
        # Save scroll position before rebuilding
        scroll_pos = self.verticalScrollBar().value()

        current_lines = 0
        self.current_page = None

        self.lastElement = None
        page_count = 0
        scene_count = 0
        is_on_title_page = False
        title_page_ended = False
        self.clearEditor()


        for line in content:
            element = fparse.parse_line(line)

            if element == None:
                continue

            _type = element.get("type")
            is_title_page_element = _type in TITLE_PAGE_TYPES

            # Check if we're transitioning from title page to regular content
            if is_on_title_page and not is_title_page_element:
                title_page_ended = True
                is_on_title_page = False

            # Force new page if title page just ended
            need_new_page = (
                self.current_page == None or
                current_lines > MAX_LINES_PER_PAGE or
                title_page_ended
            )

            if need_new_page:
                title_page_ended = False  # Reset flag

                # Determine if this is a title page
                if is_title_page_element and page_count == 0:
                    is_on_title_page = True
                    # Title page doesn't increment page count
                    display_page_num = None
                else:
                    page_count += 1
                    display_page_num = page_count

                current_lines = 0
                self.lastElement = None
                self.current_page = Page(self.parent, display_page_num if display_page_num else 0)

                # Add page number header only for non-title pages
                if display_page_num is not None:
                    self.current_page.add_header_element(0, {"type": ElementType.PAGE_NUMBER, "value": str(display_page_num)})

                # Render the page to the view
                self.pages.append(self.current_page)
                self.vbox.addWidget(self.current_page)

            # Add elements to the current page
            if _type == ElementType.SCENE:
                scene_count = scene_count + 1
                element['scene_number'] = scene_count

            if _type == ElementType.ACTION or _type == ElementType.SCENE or _type == ElementType.DIALOGUE:
                current_lines += 1

            lastBottom = 0
            if self.lastElement != None:
                lastBottom = self.lastElement.getBottom()

            self.lastElement = self.current_page.add_body_element(current_lines, element, lastBottom)

            current_lines += self.lastElement.get_line_count() + 1

        self.setWidget(self.container)

        # Restore scroll position after rebuild
        self.verticalScrollBar().setValue(scroll_pos)

    def applyTheme(self):
        dark = app_state.dark_mode
        if dark:
            self.container.setStyleSheet("background-color: #2b2b2b;")
            self.setStyleSheet("background-color: #2b2b2b;")
        else:
            self.container.setStyleSheet("")
            self.setStyleSheet("")

        # Re-render content to apply theme to pages and text
        if hasattr(self, 'parent') and hasattr(self.parent, 'editor'):
            self.setContent(self.parent.editor.getLines())