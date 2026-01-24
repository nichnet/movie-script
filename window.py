from PyQt5.QtWidgets import (
    QMainWindow, QMenuBar, QAction, QActionGroup, QMenu,
    QFrame, QStatusBar, QLabel
)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtCore import Qt
import os

from config import WIDTH, HEIGHT, app_state
from workarea import WorkArea
from editor import Editor
from pdf_exporter import export_to_pdf
from help_dialog import HelpDialog, show_about
from file_handler import FileHandler


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setMinimumSize(WIDTH, HEIGHT)
        self.setWindowTitle("Inkwell - New")

        # Application icon
        icon = QIcon()
        pixmap = QPixmap("resources/draw_ink.png")
        icon.addPixmap(pixmap)
        self.setWindowIcon(icon)

        self.createMenu()

        self.editor = Editor(self)
        self.preview = WorkArea(self)

        # Initialize file handler
        self.file_handler = FileHandler(self.editor, self.updateWindowTitle)

        self.editor.setTextChangedListener(self.onTextChanged)

        self.createStatusBar()

        if app_state.debug:
            self.setStyleSheet("background-color: purple")

    def createMenu(self):
        self.menubar = self.menuBar()

        # File menu
        fileMenu = self.menubar.addMenu('File')

        newAction = QAction('New', self)
        newAction.setShortcut(QKeySequence.New)
        newAction.triggered.connect(self.new)
        fileMenu.addAction(newAction)

        openAction = QAction('Open', self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.open)
        fileMenu.addAction(openAction)

        saveAction = QAction('Save', self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction('Save As...', self)
        saveAsAction.triggered.connect(self.saveAs)
        fileMenu.addAction(saveAsAction)

        fileMenu.addSeparator()

        exportPdfAction = QAction('Export to PDF', self)
        exportPdfAction.setShortcut('Ctrl+E')
        exportPdfAction.triggered.connect(self.exportToPdf)
        fileMenu.addAction(exportPdfAction)

        exitAction = QAction('Exit', self)
        fileMenu.addAction(exitAction)

        # Document menu
        documentMenu = self.menubar.addMenu('Document')

        # Page Size submenu
        pageSizeMenu = QMenu('Page Size', self)
        documentMenu.addMenu(pageSizeMenu)

        pageSizeGroup = QActionGroup(self)

        self.letterAction = QAction('Letter', self, checkable=True)
        self.letterAction.setChecked(True)
        self.letterAction.triggered.connect(lambda: self.setPageSize('letter'))
        pageSizeGroup.addAction(self.letterAction)
        pageSizeMenu.addAction(self.letterAction)

        self.a4Action = QAction('A4', self, checkable=True)
        self.a4Action.triggered.connect(lambda: self.setPageSize('a4'))
        pageSizeGroup.addAction(self.a4Action)
        pageSizeMenu.addAction(self.a4Action)

        # Watermark toggle
        self.watermarkAction = QAction('Show Watermark', self, checkable=True)
        self.watermarkAction.setChecked(True)
        self.watermarkAction.triggered.connect(self.toggleWatermark)
        documentMenu.addAction(self.watermarkAction)

        # View menu
        viewMenu = self.menubar.addMenu('View')

        modeMenu = QMenu('Mode', self)
        viewMenu.addMenu(modeMenu)

        modeGroup = QActionGroup(self)

        self.lightModeAction = QAction('Light', self, checkable=True)
        self.lightModeAction.setChecked(True)
        self.lightModeAction.triggered.connect(lambda: self.setTheme(False))
        modeGroup.addAction(self.lightModeAction)
        modeMenu.addAction(self.lightModeAction)

        self.darkModeAction = QAction('Dark', self, checkable=True)
        self.darkModeAction.triggered.connect(lambda: self.setTheme(True))
        modeGroup.addAction(self.darkModeAction)
        modeMenu.addAction(self.darkModeAction)

        # Help menu
        helpMenu = self.menubar.addMenu('Help')

        helpAction = QAction('Help', self)
        helpAction.triggered.connect(self.showHelp)
        helpMenu.addAction(helpAction)

        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.showAbout)
        helpMenu.addAction(aboutAction)

    def createStatusBar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.pageCountLabel = QLabel("Pages: 0")
        self.wordCountLabel = QLabel("Words: 0")
        self.sceneCountLabel = QLabel("Scenes: 0")

        self.statusbar.addWidget(self.pageCountLabel)
        self.statusbar.addWidget(self.wordCountLabel)
        self.statusbar.addWidget(self.sceneCountLabel)

    def updateStatusBar(self):
        lines = self.editor.getLines()

        # Word count
        words = sum(len(line.split()) for line in lines)

        # Scene count (lines starting with #, but not ##)
        scenes = sum(
            1 for line in lines
            if line.strip().startswith('#') and not line.strip().startswith('##')
        )

        # Page count
        pages = len(self.preview.pages) if hasattr(self.preview, 'pages') else 0

        self.pageCountLabel.setText(f"Pages: {pages}")
        self.wordCountLabel.setText(f"Words: {words}")
        self.sceneCountLabel.setText(f"Scenes: {scenes}")

    def onTextChanged(self):
        self.file_handler.mark_changed()
        self.preview.setContent(self.editor.getLines())
        self.updateStatusBar()

    def setTheme(self, dark):
        app_state.dark_mode = dark
        self.applyTheme()

    def setPageSize(self, size):
        app_state.page_size = size
        self.preview.setContent(self.editor.getLines())

    def toggleWatermark(self, checked):
        app_state.show_watermark = checked
        self.preview.setContent(self.editor.getLines())

    def applyTheme(self):
        if app_state.dark_mode:
            self.setStyleSheet("background-color: #2b2b2b;")
            self.menubar.setStyleSheet("background-color: #3c3c3c; color: white;")
            self.statusbar.setStyleSheet("background-color: #3c3c3c; color: white;")
        else:
            self.setStyleSheet("")
            self.menubar.setStyleSheet("")
            self.statusbar.setStyleSheet("")

        self.editor.applyTheme()
        self.preview.applyTheme()

    def resizeEvent(self, event):
        editorWidth = 500
        previewWidth = self.get_width() - editorWidth

        windowContentHeight = (
            self.get_height()
            - self.menubar.size().height()
            - self.statusbar.size().height()
        )

        self.preview.resize(previewWidth, windowContentHeight)
        self.preview.move(0, self.menubar.size().height())

        self.editor.resize(editorWidth, windowContentHeight)
        self.editor.move(previewWidth, self.menubar.size().height())

    # File operations - delegated to FileHandler
    def new(self):
        self.file_handler.new(self)

    def open(self):
        self.file_handler.open(self, self.addLine)

    def save(self):
        self.file_handler.save(self)

    def saveAs(self):
        self.file_handler.save_as(self)

    def updateWindowTitle(self):
        self.setWindowTitle(self.file_handler.get_window_title())

    def exportToPdf(self):
        export_to_pdf(self, self.preview.pages)

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

    def addLine(self, line):
        self.editor.addLine(line)

    def showHelp(self):
        HelpDialog.show_help(self)

    def showAbout(self):
        show_about(self)

    def closeEvent(self, event):
        """Handle window close - prompt to save unsaved changes."""
        if self.file_handler._check_unsaved_changes(self, "closing"):
            event.accept()
        else:
            event.ignore()
