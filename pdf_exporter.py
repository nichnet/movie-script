from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPdfWriter, QPageLayout, QPageSize, QFont, QFontMetrics
from PyQt5.QtCore import QMarginsF, QRectF, Qt

from config import app_state
from text import Text


def export_to_pdf(parent, pages):
    """Export pages to a PDF file with vector text rendering.

    Args:
        parent: Parent widget for dialogs
        pages: List of page widgets to export

    Returns:
        True if export successful, False otherwise
    """
    file_path, _ = QFileDialog.getSaveFileName(
        parent, "Export to PDF", "", "PDF Files (*.pdf)"
    )

    if not file_path:
        return False

    if not file_path.endswith('.pdf'):
        file_path += '.pdf'

    if len(pages) == 0:
        QMessageBox.warning(parent, "Export Error", "No pages to export.")
        return False

    pdf_writer = QPdfWriter(file_path)
    qt_page_size = QPageSize.Letter if app_state.page_size == 'letter' else QPageSize.A4
    page_size = QPageSize(qt_page_size)
    page_layout = QPageLayout(page_size, QPageLayout.Portrait, QMarginsF(0, 0, 0, 0))
    pdf_writer.setPageLayout(page_layout)
    pdf_writer.setResolution(300)

    pdf_width = pdf_writer.width()
    pdf_height = pdf_writer.height()

    painter = QPainter(pdf_writer)

    for i, page in enumerate(pages):
        # Get page dimensions for scaling
        page_width = page.width()
        page_height = page.height()

        # Calculate scale factors from widget coordinates to PDF coordinates
        scale_x = pdf_width / page_width
        scale_y = pdf_height / page_height

        # Draw white background (no border)
        painter.fillRect(QRectF(0, 0, pdf_width, pdf_height), Qt.white)

        # Collect all Text widgets from header, body, and footer
        text_widgets = []

        # Get text from header
        for child in page.header.findChildren(Text):
            text_widgets.append((child, page.header))

        # Get text from body
        for child in page.body.findChildren(Text):
            text_widgets.append((child, page.body))

        # Render each text widget
        for text_widget, container in text_widgets:
            render_text_widget(painter, text_widget, container, scale_x, scale_y)

        # Add new page if not the last one
        if i < len(pages) - 1:
            pdf_writer.newPage()

    painter.end()

    QMessageBox.information(parent, "Export Complete", f"PDF exported to:\n{file_path}")
    return True


def render_text_widget(painter, text_widget, container, scale_x, scale_y):
    """Render a Text widget directly to the PDF painter as vector text."""

    # Get the text content (plain text, stripping HTML)
    text = text_widget.text()
    if not text:
        return

    # Calculate absolute position (container position + widget position within container)
    # Use geometry() because Text class has a self.y attribute that shadows QWidget.y()
    geom = text_widget.geometry()
    abs_x = container.x() + geom.x()
    abs_y = container.y() + geom.y()
    width = geom.width()
    height = geom.height()

    # Scale to PDF coordinates
    pdf_x = abs_x * scale_x
    pdf_y = abs_y * scale_y
    pdf_width = width * scale_x
    pdf_height = height * scale_y

    # Set up font
    element = text_widget.element
    font = QFont('Courier', 12)

    if text_widget.bold:
        font.setBold(True)
    if text_widget.italic:
        font.setItalic(True)
    if text_widget.underline:
        font.setUnderline(True)

    # Scale font size for PDF resolution
    font.setPointSizeF(12 * scale_y * 0.75)  # Approximate scaling
    painter.setFont(font)
    painter.setPen(Qt.black)

    # Determine alignment
    alignment = Qt.AlignLeft | Qt.AlignTop
    widget_alignment = text_widget.alignment()

    if widget_alignment & Qt.AlignHCenter:
        alignment = Qt.AlignHCenter | Qt.AlignTop
    elif widget_alignment & Qt.AlignRight:
        alignment = Qt.AlignRight | Qt.AlignTop

    # Draw the text
    rect = QRectF(pdf_x, pdf_y, pdf_width, pdf_height)

    # Handle HTML content (scenes have tables)
    if '<table' in text.lower():
        # For scene headings with tables, extract and render parts separately
        render_scene_heading(painter, text_widget, rect, font, scale_x)
    else:
        # Strip any remaining HTML tags for plain text rendering
        plain_text = strip_html(text)
        painter.drawText(rect, alignment | Qt.TextWordWrap, plain_text)


def render_scene_heading(painter, text_widget, rect, font, scale_x):
    """Render scene headings which have special formatting with scene numbers on both sides."""
    import re

    text = text_widget.text()

    # Extract scene number and content from table structure
    # Format: <table><tr><td>NUM INT./EXT. LOCATION</td><td align="right">NUM</td></tr></table>
    match = re.search(r'<td>(.*?)</td>.*?<td[^>]*>(.*?)</td>', text, re.IGNORECASE | re.DOTALL)

    if match:
        left_content = strip_html(match.group(1))
        right_content = strip_html(match.group(2))

        # Draw left-aligned content
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, left_content)

        # Draw right-aligned scene number
        painter.drawText(rect, Qt.AlignRight | Qt.AlignTop, right_content)
    else:
        # Fallback: just draw the stripped text
        plain_text = strip_html(text)
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, plain_text)


def strip_html(text):
    """Remove HTML tags from text while preserving line breaks."""
    import re
    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    # Remove all other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text
