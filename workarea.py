from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from page import Page

import fparse

from config import MAX_LINES_PER_PAGE, app_state
from elements import ElementType

# Title page element types
TITLE_PAGE_TYPES = {
    ElementType.TITLE_PAGE_TITLE,
    ElementType.TITLE_PAGE_AUTHOR,
    ElementType.TITLE_PAGE_COMMENT,
    ElementType.TITLE_PAGE_DATE,
}

# Minimum lines required after certain elements to prevent orphans
MIN_LINES_AFTER_SCENE = 2      # Scene heading needs at least 2 lines after it
MIN_LINES_FOR_DIALOGUE = 3     # Speaker + at least 2 lines of dialogue


class WorkArea(QScrollArea): 

    def __init__(self, parent):
        super(WorkArea, self).__init__(parent)
        self.parent = parent

        self.pages = []

        self.initUI()

    def resize(self,width, height):
        self.setFixedSize(width, height)


    def initUI(self):
#        self.resize(self.WORKAREA_WIDTH, self.WORKAREA_HEIGHT)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self.container = QWidget()

        self.vbox = QVBoxLayout(self.container)  
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter)

        if app_state.debug:
            self.container.setStyleSheet(f"background-color: pink;")      


    def clearEditor(self):
        self.pages = []

        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



    def setContent(self, content):
        # Save scroll position before rebuilding
        scroll_pos = self.verticalScrollBar().value()
        self.clearEditor()

        # First pass: parse all lines into elements for look-ahead
        elements = []
        for line in content:
            element = fparse.parse_line(line)
            if element is not None:
                elements.append(element)

        # Second pass: render with smart page breaks
        current_lines = 0
        self.current_page = None
        self.lastElement = None
        page_count = 0
        scene_count = 0
        is_on_title_page = False
        title_page_ended = False
        continued_speaker = None  # Track speaker for dialogue continuation
        current_watermark = None  # Track current watermark text
        current_scene_number = 0  # Track current scene number for continuation

        i = 0
        while i < len(elements):
            element = elements[i]
            _type = element.get("type")

            # Handle watermark elements - update watermark and skip
            if _type == ElementType.WATERMARK:
                current_watermark = element.get("value", "")
                i += 1
                continue

            is_title_page_element = _type in TITLE_PAGE_TYPES

            # Check if we're transitioning from title page to regular content
            if is_on_title_page and not is_title_page_element:
                title_page_ended = True
                is_on_title_page = False

            # Calculate lines this element will take (estimate)
            estimated_lines = self._estimate_element_lines(element)
            lines_remaining = MAX_LINES_PER_PAGE - current_lines

            # Check if this is a continuation of the same speaker's dialogue
            current_speaker = None
            if _type == ElementType.DIALOGUE:
                current_speaker = element.get("speaker", "")
                # Strip "(CONT'D)" for comparison purposes
                base_speaker = current_speaker.replace(" (CONT'D)", "")
                base_continued = (continued_speaker or "").replace(" (CONT'D)", "")
                # Only continue if same speaker has consecutive dialogue
                if continued_speaker is not None and base_speaker != base_continued:
                    continued_speaker = None  # Different speaker, not a continuation
            else:
                continued_speaker = None  # Not dialogue, clear continuation

            # Smart page break logic
            force_new_page = False

            if self.current_page is not None and not is_title_page_element:
                # Rule 1: Scene heading must have room for itself + following content
                if _type == ElementType.SCENE:
                    if lines_remaining < (estimated_lines + MIN_LINES_AFTER_SCENE):
                        force_new_page = True

                # Rule 2: Dialogue needs room for speaker + at least 2 lines
                elif _type == ElementType.DIALOGUE:
                    if lines_remaining < MIN_LINES_FOR_DIALOGUE:
                        force_new_page = True

            # Standard page break conditions
            need_new_page = (
                self.current_page is None or
                current_lines > MAX_LINES_PER_PAGE or
                title_page_ended or
                force_new_page
            )

            # Track if we need to add (CONT'D) to the next dialogue's speaker
            add_contd_to_next = False
            # Track if we need to add scene continuation at top of new page
            add_scene_continued = False

            if need_new_page:
                # Add (MORE) marker only if same speaker's dialogue continues
                if continued_speaker is not None and self.lastElement is not None:
                    self._add_more_marker(current_lines)
                    add_contd_to_next = True

                # Add (CONTINUED) marker if scene continues to next page
                # Only add if we're mid-scene and the next element is NOT a new scene
                if current_scene_number > 0 and _type != ElementType.SCENE and self.lastElement is not None:
                    self._add_scene_continued_marker(current_lines)
                    add_scene_continued = True

                title_page_ended = False

                # Determine if this is a title page
                if is_title_page_element and page_count == 0:
                    is_on_title_page = True
                    display_page_num = None
                else:
                    page_count += 1
                    display_page_num = page_count

                current_lines = 0
                self.lastElement = None
                self.current_page = Page(self.parent, display_page_num if display_page_num else 0, current_watermark)

                # Add page number header only for non-title pages
                if display_page_num is not None:
                    self.current_page.add_header_element(0, {"type": ElementType.PAGE_NUMBER, "value": str(display_page_num)})

                self.pages.append(self.current_page)
                self.vbox.addWidget(self.current_page)

                # Add CONTINUED: marker at top of page if scene continues from previous page
                if add_scene_continued:
                    continued_element = {
                        "type": ElementType.SCENE_CONTINUED,
                        "scene_number": current_scene_number,
                        "value": ""
                    }
                    self.lastElement = self.current_page.add_body_element(current_lines, continued_element, 0)
                    current_lines += 2  # Account for the continued marker

            # Add (CONT'D) to speaker name if continuing from previous page
            if add_contd_to_next and _type == ElementType.DIALOGUE:
                speaker = element.get("speaker", "")
                if "(CONT'D)" not in speaker:  # Don't add twice
                    element = element.copy()
                    element["speaker"] = speaker + " (CONT'D)"
                continued_speaker = None

            # Track scene numbers
            if _type == ElementType.SCENE:
                scene_count += 1
                element['scene_number'] = scene_count
                current_scene_number = scene_count

            if _type == ElementType.ACTION or _type == ElementType.SCENE or _type == ElementType.DIALOGUE:
                current_lines += 1

            # For dialogue, check if we need to split BEFORE rendering
            did_split_dialogue = False
            if _type == ElementType.DIALOGUE:
                lines_available = MAX_LINES_PER_PAGE - current_lines
                dialogue_text = element.get("value", "")

                # Estimate how many lines this dialogue will take (excluding speaker line)
                est_dialogue_lines = max(1, len(dialogue_text) // 50)

                # If dialogue won't fit entirely, split it
                if est_dialogue_lines > lines_available and lines_available >= 2:
                    split_point = self._estimate_split_point(dialogue_text, lines_available)

                    if split_point > 0 and split_point < len(dialogue_text):
                        # Modify current element to only have first part
                        element = element.copy()
                        element["value"] = dialogue_text[:split_point].strip()

                        # Insert continuation element for next page
                        base_speaker = current_speaker.replace(" (CONT'D)", "")
                        cont_element = {
                            "type": ElementType.DIALOGUE,
                            "speaker": base_speaker + " (CONT'D)",
                            "value": dialogue_text[split_point:].strip()
                        }
                        elements.insert(i + 1, cont_element)
                        did_split_dialogue = True

            lastBottom = 0
            if self.lastElement is not None:
                lastBottom = self.lastElement.getBottom()

            self.lastElement = self.current_page.add_body_element(current_lines, element, lastBottom)
            actual_lines = self.lastElement.get_line_count()
            current_lines += actual_lines + 1

            # Add MORE marker if we split this dialogue
            if did_split_dialogue:
                self._add_more_marker(current_lines)

            # Track speaker for continuation detection
            if _type == ElementType.DIALOGUE:
                continued_speaker = current_speaker
            # Note: non-dialogue elements clear continued_speaker at the start of next iteration

            i += 1

        self.setWidget(self.container)
        self.verticalScrollBar().setValue(scroll_pos)

    def _estimate_element_lines(self, element):
        """Estimate how many lines an element will take."""
        _type = element.get("type")
        value = element.get("value", "")

        # Base estimate on content length and type
        if _type == ElementType.SCENE:
            return 2  # Scene headings are typically 1-2 lines
        elif _type == ElementType.DIALOGUE:
            # Dialogue includes speaker name + dialogue text
            lines = 2 + (len(value) // 50)  # Rough estimate
            return max(3, lines)
        elif _type == ElementType.ACTION:
            return 1 + (len(value) // 60)
        else:
            return 1

    def _estimate_split_point(self, text, lines_to_fit):
        """Estimate character position to split text at given line count.

        Tries to split at sentence or word boundaries.
        """
        # Rough estimate: ~50 chars per line for dialogue
        chars_per_line = 50
        target_chars = lines_to_fit * chars_per_line

        if target_chars >= len(text):
            return len(text)

        # Try to split at sentence boundary (. ! ?)
        search_start = max(0, target_chars - 50)
        search_end = min(len(text), target_chars + 20)
        search_region = text[search_start:search_end]

        # Look for sentence endings
        for punct in ['. ', '! ', '? ']:
            pos = search_region.rfind(punct)
            if pos != -1:
                return search_start + pos + len(punct)

        # Fall back to word boundary (space)
        space_pos = text.rfind(' ', search_start, target_chars)
        if space_pos != -1:
            return space_pos + 1

        # Last resort: split at target
        return target_chars

    def _add_more_marker(self, current_lines):
        """Add (MORE) marker at bottom of page when dialogue continues."""
        lastBottom = 0
        if self.lastElement is not None:
            lastBottom = self.lastElement.getBottom()

        more_element = {
            "type": ElementType.SPEAKER,
            "value": "(MORE)"
        }
        self.current_page.add_body_element(current_lines, more_element, lastBottom)

    def _add_scene_continued_marker(self, current_lines):
        """Add (CONTINUED) marker at bottom of page when scene continues."""
        lastBottom = 0
        if self.lastElement is not None:
            lastBottom = self.lastElement.getBottom()

        continued_element = {
            "type": ElementType.TRANSITION,
            "value": "(CONTINUED)"
        }
        self.current_page.add_body_element(current_lines, continued_element, lastBottom)

    def applyTheme(self):
        dark = app_state.dark_mode
        if dark:
            self.container.setStyleSheet("background-color: #2b2b2b;")
            self.setStyleSheet("background-color: #2b2b2b;")
        else:
            self.container.setStyleSheet("")
            self.setStyleSheet("")

        # Re-render content to apply theme to pages and text
        if hasattr(self, 'parent') and hasattr(self.parent, 'editor'):
            self.setContent(self.parent.editor.getLines())