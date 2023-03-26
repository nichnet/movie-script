import sys
import ctypes
from functools import partial

from constants import *

from PyQt5.QtWidgets import *
from window import Window 

myappid = 'com.nichnet.inkwell.100' # arbitrary string


win = None

def init_dpi(app):
    screen = app.screens()[0]
    set_dpi(screen.physicalDotsPerInch())

def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  

    app = QApplication(sys.argv)

    
    init_dpi(app)

    global win
    win = Window()
 #   win.setWorkareaContent(lines)

    file_path = './example/script.txt'

    with open(file_path, 'r') as file:
        for line in file:
            win.addLine(line)
#            out.append(parse_line(line))
#
 #   return out

  #  lines = parser.from_file('./example/script.txt')


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