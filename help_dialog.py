from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QMessageBox
from PyQt5.QtCore import Qt


HELP_TEXT = """
<h2>Document Formatting Rules</h2>

<h3>Title Page</h3>
<table>
<tr><td><b>**T</b></td><td>Title page title</td></tr>
<tr><td><b>**A</b></td><td>Author line</td></tr>
<tr><td><b>**C</b></td><td>Comment</td></tr>
<tr><td><b>**D</b></td><td>Date/draft info</td></tr>
</table>

<h3>Scene Headings</h3>
<p><b>Location types:</b></p>
<table>
<tr><td><b>#I</b></td><td>INT.</td></tr>
<tr><td><b>#E</b></td><td>EXT.</td></tr>
<tr><td><b>#IE</b></td><td>INT./EXT.</td></tr>
<tr><td><b>#EI</b></td><td>EXT./INT.</td></tr>
</table>

<p><b>Time of day</b> (add after /):</p>
<table>
<tr><td><b>/D</b></td><td>DAY</td></tr>
<tr><td><b>/N</b></td><td>NIGHT</td></tr>
<tr><td><b>/DN</b></td><td>DAY/NIGHT</td></tr>
<tr><td><b>/ND</b></td><td>NIGHT/DAY</td></tr>
<tr><td><b>/DAWN</b></td><td>DAWN (or any custom word)</td></tr>
<tr><td><b>/"text"</b></td><td>Multi-word time (in quotes, uppercase)</td></tr>
</table>

<p><b>Examples:</b></p>
<pre>
#I/D Coffee Shop        &rarr;  INT. COFFEE SHOP - DAY
#E/N Street             &rarr;  EXT. STREET - NIGHT
#IE/D Car               &rarr;  INT./EXT. CAR - DAY
#I/DAWN Bedroom         &rarr;  INT. BEDROOM - DAWN
#E/"Soon after" Park    &rarr;  EXT. PARK - SOON AFTER
#I/"The next day" House &rarr;  INT. HOUSE - THE NEXT DAY
#I Coffee Shop          &rarr;  INT. COFFEE SHOP
</pre>

<h3>Other Elements</h3>
<table>
<tr><td><b>*</b></td><td>In-script title (centered, bold, underlined)</td></tr>
<tr><td><b>##</b></td><td>Transition (right-aligned, adds colon)</td></tr>
<tr><td><b>@</b></td><td>Dialogue with speaker</td></tr>
<tr><td><b>~</b></td><td>Watermark (diagonal text across page)</td></tr>
</table>

<h3>Watermark</h3>
<p>Add a diagonal watermark by starting a line with <b>~</b></p>
<p>Example: <code>~DRAFT</code> or <code>~CONFIDENTIAL</code></p>
<p>The watermark appears on all pages until a new one is defined.</p>
<p>Use empty <b>~</b> to remove watermark from subsequent pages.</p>
<p>Toggle visibility in <b>Document &gt; Show Watermark</b>.</p>

<h3>Dialogue Format</h3>
<p>Use <b>@Speaker "dialogue text"</b></p>
<p>Example: <code>@John "Hello, how are you?"</code></p>

<h3>Inline Formatting (HTML)</h3>
<table>
<tr><td><b>&lt;b&gt;text&lt;/b&gt;</b></td><td>Bold text</td></tr>
<tr><td><b>&lt;i&gt;text&lt;/i&gt;</b></td><td>Italic text</td></tr>
<tr><td><b>&lt;u&gt;text&lt;/u&gt;</b></td><td>Underlined text</td></tr>
<tr><td><b>&lt;br&gt;</b></td><td>Line break</td></tr>
</table>

<h3>Plain Text</h3>
<p>Any line without a prefix is treated as <b>Action/Description</b>.</p>

<h3>Full Example</h3>
<pre>
~DRAFT
**T My Movie Title
**A Written by
**A John Smith
**C Based on a true story

#I/D Coffee Shop
John enters the coffee shop.

@John "I'll have a coffee, please."

##CUT TO

#E/N Street
The city lights flicker in the &lt;b&gt;rain&lt;/b&gt;.

#IE/D Car - Moving
Sarah drives while talking on the phone.
</pre>
"""

ABOUT_TEXT = """Inkwell - Screenplay Editor

A simple screenplay writing application.

Write your screenplay using simple formatting rules
and export to PDF."""


class HelpDialog(QDialog):
    _instance = None

    @classmethod
    def show_help(cls, parent):
        """Show the help dialog. Reuses existing instance if open."""
        if cls._instance is not None and cls._instance.isVisible():
            cls._instance.raise_()
            cls._instance.activateWindow()
            return cls._instance

        cls._instance = cls(parent)
        cls._instance.show()
        return cls._instance

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Formatting Help")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)

        helpLabel = QLabel(HELP_TEXT)
        helpLabel.setWordWrap(True)
        helpLabel.setTextFormat(Qt.RichText)
        contentLayout.addWidget(helpLabel)

        scrollArea.setWidget(contentWidget)
        layout.addWidget(scrollArea)


def show_about(parent):
    """Show the about dialog."""
    QMessageBox.about(parent, "About Inkwell", ABOUT_TEXT)
