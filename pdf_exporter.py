from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPdfWriter, QPageLayout, QPageSize
from PyQt5.QtCore import QMarginsF, QRectF, Qt


def export_to_pdf(parent, pages):
    """Export pages to a PDF file.

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

    pdfWriter = QPdfWriter(file_path)
    pageSize = QPageSize(QPageSize.Letter)
    pageLayout = QPageLayout(pageSize, QPageLayout.Portrait, QMarginsF(0, 0, 0, 0))
    pdfWriter.setPageLayout(pageLayout)

    # Higher resolution for sharper output
    pdfWriter.setResolution(600)

    pdfWidth = pdfWriter.width()
    pdfHeight = pdfWriter.height()

    painter = QPainter(pdfWriter)

    for i, page in enumerate(pages):
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
        if i < len(pages) - 1:
            pdfWriter.newPage()

    painter.end()

    QMessageBox.information(parent, "Export Complete", f"PDF exported to:\n{file_path}")
    return True
