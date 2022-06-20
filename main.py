
from PyQt5.QtWidgets import *
import sys
from functools import partial
from examplescript import content
from constants import *

from window import Window 


win = None

def init_dpi(app):
    screen = app.screens()[0]
    set_dpi(screen.physicalDotsPerInch())

def main():
    app = QApplication(sys.argv)
    
    init_dpi(app)

    global win
    win = Window()
    win.setWorkareaContent(content)

    #btn = QPushButton(win)
    #btn.setGeometry(1000, 500, 50, 20)
    #btn.clicked.connect(workarea.next_page)
    #btn2 = QPushButton(win)
    #btn2.setGeometry(940, 500, 50, 20)
    #btn2.clicked.connect(workarea.prev_page)

    win.show()

    #clean exit
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()