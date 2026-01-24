import sys
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from config import app_state
from window import Window

win = None

def init_dpi(app):
    screen = app.screens()[0]
    app_state.dpi = screen.physicalDotsPerInch()

if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == '--debug':
        print("debug mode")
        app_state.debug = True

    # Set AppUserModelID for Windows taskbar icon
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.nichnet.inkwell')

    app = QApplication(sys.argv)

    # Set application icon (for taskbar)
    app.setWindowIcon(QIcon("resources/draw_ink.png"))

    init_dpi(app)

#    global win
    win = Window()

    win.show()

    #clean exit
    sys.exit(app.exec_())