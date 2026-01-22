from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os


class FileHandler:
    """Handles file operations for the screenplay editor."""

    def __init__(self, editor, update_title_callback):
        self.editor = editor
        self.update_title_callback = update_title_callback
        self.current_file_path = None
        self.has_unsaved_changes = False

    def mark_changed(self):
        """Mark the document as having unsaved changes."""
        self.has_unsaved_changes = True

    def _check_unsaved_changes(self, parent, action_description):
        """Check for unsaved changes and prompt user.

        Returns:
            True if it's ok to proceed, False if user cancelled
        """
        if not self.has_unsaved_changes:
            return True

        response = QMessageBox.question(
            parent,
            "Unsaved Changes",
            f"You have unsaved changes. Do you want to save before {action_description}?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save
        )

        if response == QMessageBox.Save:
            return self.save(parent)
        elif response == QMessageBox.Cancel:
            return False

        return True

    def new(self, parent):
        """Create a new document."""
        if not self._check_unsaved_changes(parent, "creating a new document"):
            return False

        self.editor.clear()
        self.current_file_path = None
        self.has_unsaved_changes = False
        self.update_title_callback()
        return True

    def open(self, parent, add_line_callback):
        """Open an existing document."""
        if not self._check_unsaved_changes(parent, "opening another document"):
            return False

        file_path, _ = QFileDialog.getOpenFileName(
            parent, "Open Project", "", "Inkwell Files (*.ink)"
        )

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.editor.clear()
                for line in file:
                    add_line_callback(line.rstrip('\n'))
            self.current_file_path = file_path
            self.has_unsaved_changes = False
            self.update_title_callback()
            return True

        return False

    def save(self, parent):
        """Save the current document."""
        if self.current_file_path:
            self._write_file(self.current_file_path)
            return True
        else:
            return self.save_as(parent)

    def save_as(self, parent):
        """Save the document to a new location."""
        file_path, _ = QFileDialog.getSaveFileName(
            parent, "Save Project", "", "Inkwell Files (*.ink)"
        )

        if file_path:
            if not file_path.endswith('.ink'):
                file_path += '.ink'
            self.current_file_path = file_path
            self._write_file(file_path)
            self.update_title_callback()
            return True

        return False

    def _write_file(self, path):
        """Write the document to a file."""
        with open(path, 'w') as file:
            for line in self.editor.getLines():
                file.write(line + "\n")
        self.has_unsaved_changes = False

    def get_window_title(self):
        """Get the window title based on current file."""
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            return f"Inkwell - {filename}"
        return "Inkwell - New"
