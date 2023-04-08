from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QFrame, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPdfWriter, QPageLayout, QRegion, QPageSize
from PyQt5.QtCore import QSize, QMarginsF, QSizeF, QPoint, QRectF
import os
from functools import partial
from constants import *
from workarea import WorkArea
from editor import Editor

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()


        self.initUI()

    def initUI(self):

        self.setGeometry(0,0, WIDTH, HEIGHT)
        self.setMinimumSize(WIDTH, HEIGHT)
        self.setWindowTitle("Inkwell - New")


        #application icon
        icon = QIcon()
        pixmap = QPixmap("resources/draw_ink.png")
        icon.addPixmap(pixmap)
        #app.setWindowIcon(app_icon)

        # Set window icon
        self.setWindowIcon(icon)

       
        self.createMenu()

        self.editor = Editor(self)
        self.preview = WorkArea(self)

        self.editor.setTextChangedListener(self.onTextChanged)

        if DEBUG: 
            self.setStyleSheet("background-color: purple")



##        self.createEditorLayout()

    def createMenu(self): 
        # Create a menu bar
        self.menubar = self.menuBar()

        fileMenu = self.menubar.addMenu('File')
        
        newAction = QAction('New', self)
        fileMenu.addAction(newAction)
        
        openAction = QAction('Open', self)
        openAction.triggered.connect(self.open)
        fileMenu.addAction(openAction)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        
        printAction = QAction('Print', self)
        printAction.triggered.connect(partial(self.print, "test.pdf"))
        fileMenu.addAction(printAction)

        exitAction = QAction('Exit', self)
        fileMenu.addAction(exitAction)

    def onTextChanged(self):
        self.preview.setContent(self.editor.getLines())  

    def resizeEvent(self, event):
        editorWidth =  500
        previewWidth = self.get_width() - editorWidth

        windowContentHeight = self.get_height() - self.menubar.size().height()

        self.preview.resize(previewWidth, windowContentHeight)
        self.preview.move(0, self.menubar.size().height())
    
        self.editor.resize(editorWidth, windowContentHeight)
        self.editor.move(previewWidth, self.menubar.size().height())

    def open(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "Text Files (*.txt)")
        print("Selected file path:", file_path)

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.editor.clear()
                for line in file:
                    self.addLine(line)

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Text Files (*.txt)")
        print("Selected file path:", file_path)

        self.exportCurrentDocument(file_path)

#        if file_path and os.path.exists(file_path):
#            # display a warning dialog to confirm overwriting the file
#            response = QMessageBox.warning(None, "Overwrite File", "A file already exists at the selected location. Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#            
#            if response == QMessageBox.Yes:
#                self.exportCurrentDocument(file_path)
#            else:
#                # display another save file dialog for the user to choose a new file name/location
#                self.save()
#                return
#        else:
#            if file_path:
#
#                #file doesnt exist so save file. 
#                self.exportCurrentDocument(file_path)

    def exportCurrentDocument(self, path):
            with open(path, 'w') as file:
                for line in self.editor.getLines():
                    file.write(line + "\n")
        
    def print(self, outputName):
       
        print("Printing file to: " + outputName + ".pdf", "pages: ", len(self.preview.pages))
        i = 1
        myFrame = QFrame()

        pdfWriter = QPdfWriter(outputName)

        pageSize = QPageSize(QPageSize.Letter)

        pageLayout = QPageLayout(pageSize, QPageLayout.Portrait, QMarginsF(0, 0, 0, 0))
      
        pdfWriter.setPageLayout(pageLayout)
      
        painter = QPainter(pdfWriter)
        painter.translate(0,0)
        painter.scale(7.59, 7.58) #TODO 

        painter.begin(pdfWriter)

        for page in self.preview.pages:
            print("printing page: ", i)


            pageWidth = pageSize.size(QPageSize.Unit.Point).width() - pageLayout.margins().left() - pageLayout.margins().right()
            pageHeight = pageSize.size(QPageSize.Unit.Point).height() - pageLayout.margins().top() - pageLayout.margins().bottom()
         
            frameRect = QRectF(0, 0, page.size().width(), page.size().height())
            

            scaleX = pageWidth / frameRect.width()
            scaleY = pageHeight / frameRect.height()
            scaleFactor = min(scaleX, scaleY)

            # Scale the frame rectangle while preserving aspect ratio
            scaledRect = frameRect.adjusted(0, 0, frameRect.width() * scaleFactor, frameRect.height())


            print(scaledRect.width() / frameRect.width(), scaledRect.height() / frameRect.height())




            page.render(painter, QPoint(), QRegion(), QFrame.DrawChildren)
            

            #TODO determine if theres anotehr page first.
            pdfWriter.newPage()
            
            i += 1

        painter.end()


    
     #   painter.end()

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

    def addLine(self, line):
        self.editor.addLine(line)