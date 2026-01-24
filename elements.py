"""Element types for screenplay formatting."""

from enum import Enum


class ElementType(Enum):
    TITLE = 0
    TRANSITION = 1
    SCENE = 2
    ACTION = 3
    DIALOGUE = 4
    PAGE_NUMBER = 5
    INTERCUT = 6
    SPEAKER = 7
    PAGE = 8
    # Title page elements
    TITLE_PAGE_TITLE = 9
    TITLE_PAGE_AUTHOR = 10
    TITLE_PAGE_COMMENT = 11
    TITLE_PAGE_DATE = 12
    # Watermark
    WATERMARK = 13
