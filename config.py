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

    def convert_inches_to_pixels(self, inches):
        return int(self._dpi * inches)


# Global app state instance
app_state = AppState()
