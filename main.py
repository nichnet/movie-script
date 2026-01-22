import sys
from PyQt5.QtWidgets import QApplication
from config import app_state
from window import Window 

#myappid = 'com.nichnet.inkwell.100' # arbitrary string

win = None

def init_dpi(app):
    screen = app.screens()[0]
    app_state.dpi = screen.physicalDotsPerInch()

if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == '--debug':
        print("debug mode")
        app_state.debug = True

        #TODO Only works for WIN.
#    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  

    app = QApplication(sys.argv)

    
    init_dpi(app)

#    global win
    win = Window()

    win.show()

    #clean exit
    sys.exit(app.exec_())