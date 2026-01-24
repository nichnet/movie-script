"""Application configuration settings."""

WIDTH = 1600
HEIGHT = 980
LINE_HEIGHT = 16
MAX_LINES_PER_PAGE = 53


class AppState:
    """Global application state."""

    def __init__(self):
        self._debug = False
        self._dark_mode = False
        self._dpi = 72
        self._page_size = 'letter'  # 'letter' or 'a4'
        self._show_watermark = True

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def dark_mode(self):
        return self._dark_mode

    @dark_mode.setter
    def dark_mode(self, value):
        self._dark_mode = value

    @property
    def dpi(self):
        return self._dpi

    @dpi.setter
    def dpi(self, value):
        self._dpi = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def show_watermark(self):
        return self._show_watermark

    @show_watermark.setter
    def show_watermark(self, value):
        self._show_watermark = value

    def convert_inches_to_pixels(self, inches):
        return int(self._dpi * inches)


# Global app state instance
app_state = AppState()
