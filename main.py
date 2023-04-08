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
    #TODO Only works for WIN.
#    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  

    app = QApplication(sys.argv)

    
    init_dpi(app)

    global win
    win = Window()

    win.show()

    #clean exit
    sys.exit(app.exec_())


 
if __name__ == "__main__":
    main()