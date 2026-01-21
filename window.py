from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QActionGroup, QMenu, QFrame, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QStatusBar
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPdfWriter, QPageLayout, QRegion, QPageSize, QKeySequence
from PyQt5.QtCore import QSize, QMarginsF, QSizeF, QPoint, QRectF, Qt
import os
from constants import *
from constants import set_dark_mode, get_dark_mode
from workarea import WorkArea
from editor import Editor

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()


        self.initUI()

    def initUI(self):
        self.currentFilePath = None
        self.hasUnsavedChanges = False

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

        self.createStatusBar()

        if get_debug_mode():
            self.setStyleSheet("background-color: purple")



##        self.createEditorLayout()

    def createMenu(self): 
        # Create a menu bar
        self.menubar = self.menuBar()

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

        # View menu
        viewMenu = self.menubar.addMenu('View')

        # Mode submenu
        modeMenu = QMenu('Mode', self)
        viewMenu.addMenu(modeMenu)

        # Create action group for exclusive selection
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

        self.wordCountLabel = QLabel("Words: 0")
        self.sceneCountLabel = QLabel("Scenes: 0")
        self.pageCountLabel = QLabel("Pages: 0")

        self.statusbar.addWidget(self.pageCountLabel)
        self.statusbar.addWidget(self.wordCountLabel)
        self.statusbar.addWidget(self.sceneCountLabel)

    def updateStatusBar(self):
        lines = self.editor.getLines()

        # Word count
        words = 0
        for line in lines:
            words += len(line.split())

        # Scene count (lines starting with #, but not ##)
        scenes = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('##'):
                scenes += 1

        # Page count
        pages = len(self.preview.pages) if hasattr(self.preview, 'pages') else 0

        self.wordCountLabel.setText(f"Words: {words}")
        self.sceneCountLabel.setText(f"Scenes: {scenes}")
        self.pageCountLabel.setText(f"Pages: {pages}")

    def onTextChanged(self):
        self.hasUnsavedChanges = True
        self.preview.setContent(self.editor.getLines())
        self.updateStatusBar()

    def setTheme(self, dark):
        set_dark_mode(dark)
        self.applyTheme()

    def applyTheme(self):
        dark = get_dark_mode()
        if dark:
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

        windowContentHeight = self.get_height() - self.menubar.size().height() - self.statusbar.size().height()

        self.preview.resize(previewWidth, windowContentHeight)
        self.preview.move(0, self.menubar.size().height())
    
        self.editor.resize(editorWidth, windowContentHeight)
        self.editor.move(previewWidth, self.menubar.size().height())

    def new(self):
        if self.hasUnsavedChanges:
            response = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new document?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if response == QMessageBox.Save:
                self.save()
            elif response == QMessageBox.Cancel:
                return

        self.editor.clear()
        self.currentFilePath = None
        self.hasUnsavedChanges = False
        self.updateWindowTitle()

    def open(self):
        if self.hasUnsavedChanges:
            response = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before opening another document?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if response == QMessageBox.Save:
                self.save()
            elif response == QMessageBox.Cancel:
                return

        file_path, _ = QFileDialog.getOpenFileName(None, "Open Project", "", "Inkwell Files (*.ink)")

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.editor.clear()
                for line in file:
                    self.addLine(line)
            self.currentFilePath = file_path
            self.hasUnsavedChanges = False
            self.updateWindowTitle()

    def save(self):
        # If we have a current file, save directly to it
        if self.currentFilePath:
            self.exportCurrentDocument(self.currentFilePath)
        else:
            # No current file, prompt for save location
            self.saveAs()

    def saveAs(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Project", "", "Inkwell Files (*.ink)")

        if file_path:
            if not file_path.endswith('.ink'):
                file_path += '.ink'
            self.currentFilePath = file_path
            self.exportCurrentDocument(file_path)
            self.updateWindowTitle()

    def updateWindowTitle(self):
        if self.currentFilePath:
            filename = os.path.basename(self.currentFilePath)
            self.setWindowTitle(f"Inkwell - {filename}")
        else:
            self.setWindowTitle("Inkwell - New")

    def exportCurrentDocument(self, path):
        with open(path, 'w') as file:
            for line in self.editor.getLines():
                file.write(line + "\n")
        self.hasUnsavedChanges = False
        
    def exportToPdf(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Export to PDF", "", "PDF Files (*.pdf)")

        if not file_path:
            return

        if not file_path.endswith('.pdf'):
            file_path += '.pdf'

        if len(self.preview.pages) == 0:
            QMessageBox.warning(self, "Export Error", "No pages to export.")
            return

        pdfWriter = QPdfWriter(file_path)
        pageSize = QPageSize(QPageSize.Letter)
        pageLayout = QPageLayout(pageSize, QPageLayout.Portrait, QMarginsF(0, 0, 0, 0))
        pdfWriter.setPageLayout(pageLayout)

        # Higher resolution for sharper output
        pdfWriter.setResolution(300)

        pdfWidth = pdfWriter.width()
        pdfHeight = pdfWriter.height()

        painter = QPainter(pdfWriter)

        for i, page in enumerate(self.preview.pages):
            # Grab page and scale up for better quality
            pixmap = page.grab()

            scaleFactor = 3
            highResPixmap = pixmap.scaled(
                pixmap.width() * scaleFactor,
                pixmap.height() * scaleFactor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            # Calculate scale to fit PDF page
            scaleX = pdfWidth / highResPixmap.width()
            scaleY = pdfHeight / highResPixmap.height()
            scale = min(scaleX, scaleY)

            scaledWidth = int(highResPixmap.width() * scale)
            scaledHeight = int(highResPixmap.height() * scale)

            # Center on page
            x = (pdfWidth - scaledWidth) // 2
            y = (pdfHeight - scaledHeight) // 2

            targetRect = QRectF(x, y, scaledWidth, scaledHeight)
            sourceRect = QRectF(0, 0, highResPixmap.width(), highResPixmap.height())

            painter.drawPixmap(targetRect, highResPixmap, sourceRect)

            # Add new page if not the last one
            if i < len(self.preview.pages) - 1:
                pdfWriter.newPage()

        painter.end()

        QMessageBox.information(self, "Export Complete", f"PDF exported to:\n{file_path}")

    def get_width(self):
        return int(self.size().width())

    def get_height(self):
        return int(self.size().height())

    def addLine(self, line):
        self.editor.addLine(line)

    def showHelp(self):
        # If help dialog already exists and is visible, bring it to front
        if hasattr(self, 'helpDialog') and self.helpDialog is not None and self.helpDialog.isVisible():
            self.helpDialog.raise_()
            self.helpDialog.activateWindow()
            return

        self.helpDialog = QDialog(self)
        self.helpDialog.setWindowTitle("Formatting Help")
        self.helpDialog.setMinimumSize(500, 400)
        self.helpDialog.setWindowFlags(self.helpDialog.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self.helpDialog)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)

        helpText = """
<h2>Document Formatting Rules</h2>

<h3>Line Prefixes</h3>
<table>
<tr><td><b>*</b></td><td>Title (centered, bold, underlined, uppercase)</td></tr>
<tr><td><b>#</b></td><td>Scene heading (bold, uppercase)</td></tr>
<tr><td><b>#I</b></td><td>Interior scene (adds "INT - " prefix)</td></tr>
<tr><td><b>#E</b></td><td>Exterior scene (adds "EXT - " prefix)</td></tr>
<tr><td><b>##</b></td><td>Transition (right-aligned, uppercase, adds colon)</td></tr>
<tr><td><b>@</b></td><td>Dialogue with speaker</td></tr>
</table>

<h3>Dialogue Format</h3>
<p>Use <b>@Speaker "dialogue text"</b></p>
<p>Example: <code>@John "Hello, how are you?"</code></p>

<h3>Inline Formatting</h3>
<table>
<tr><td><b>&lt;b&gt;text&lt;/b&gt;</b></td><td>Bold text</td></tr>
<tr><td><b>&lt;i&gt;text&lt;/i&gt;</b></td><td>Italic text</td></tr>
<tr><td><b>&lt;u&gt;text&lt;/u&gt;</b></td><td>Underlined text</td></tr>
<tr><td><b>&lt;br&gt;</b></td><td>Line break</td></tr>
</table>

<h3>Plain Text</h3>
<p>Any line without a prefix is treated as <b>Action/Description</b>.</p>

<h3>Examples</h3>
<pre>
*My Movie Title

#I Coffee Shop - Day
John enters the coffee shop.

@John "I'll have a coffee, please."

##CUT TO

#E Street - Night
The city lights flicker in the &lt;b&gt;rain&lt;/b&gt;.
</pre>
"""

        helpLabel = QLabel(helpText)
        helpLabel.setWordWrap(True)
        helpLabel.setTextFormat(1)  # RichText
        contentLayout.addWidget(helpLabel)

        scrollArea.setWidget(contentWidget)
        layout.addWidget(scrollArea)

        self.helpDialog.show()

    def showAbout(self):
        QMessageBox.about(self, "About Inkwell",
            "Inkwell - Screenplay Editor\n\n"
            "A simple screenplay writing application.\n\n"
            "Write your screenplay using simple formatting rules\n"
            "and export to PDF.")