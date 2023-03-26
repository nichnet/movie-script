from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from page import Page

import fparse;

from constants import *


class WorkArea(QScrollArea): 

    def __init__(self, parent):
        super(WorkArea, self).__init__(parent)
        self.parent = parent

        #accept drag/drops
        self.setAcceptDrops(True)

#        self.current_page = 0
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


    def clearEditor(self):
        self.pages = []

        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



    def setContent(self, content):

        current_lines = 0
        self.current_page = None

        self.lastElement = None
        page_count = 0

        self.clearEditor()


        for line in content:
            element = fparse.parse_line(line)

            if element == None:
                continue

            if self.current_page == None or current_lines > MAX_LINES_PER_PAGE:
                page_count += 1
                current_lines = 0
                self.current_page = Page(self.parent, page_count)

                #add header content (just page number)
                lastElement = self.current_page.add_header_element(0, {"type": ElementType.PAGE_NUMBER, "value": str(page_count)})

                #render the page to the view
                self.pages.append(self.current_page)
                self.vbox.addWidget(self.current_page)

            #add elements to the current page
            _type = element.get("type") 

            if _type == ElementType.ACTION or _type == ElementType.SCENE or _type == ElementType.DIALOGUE:
                pass
                current_lines += 1


            lastBottom = 0
            if lastElement != None:
                lastBottom = lastElement.getBottom()

            lastElement = self.current_page.add_body_element(current_lines, element, lastBottom)
            
            current_lines += lastElement.get_line_count()

        self.setWidget(self.container)

    def prev_page(self):
        pass
        #self.current_page = max(0, self.current_page - 1)
        #self.ensureWidgetVisible(self.pages[self.current_page])

    def next_page(self):
        pass
        #self.current_page = min(len(self.pages) - 1, self.current_page + 1)
        #self.ensureWidgetVisible(self.pages[self.current_page])


    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()

        for n in range(self.vbox.count()):
            # Get the widget at each index in turn.
            w = self.vbox.itemAt(n).widget()
            if pos.x() < w.x() + w.size().width() // 2:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.vbox.insertWidget(n-1, widget)
                break

        e.accept()