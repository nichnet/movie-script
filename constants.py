"""Backwards compatibility - re-exports from new modules.

This file maintains backwards compatibility with existing code.
New code should import directly from the specific modules:
- config.py: WIDTH, HEIGHT, LINE_HEIGHT, MAX_LINES_PER_PAGE, app_state
- elements.py: ElementType
- page_rules.py: PAGE_FORMATS, PAGE_RULES
- theme.py: theme_manager
"""

# Re-export from config
from config import WIDTH, HEIGHT, LINE_HEIGHT, MAX_LINES_PER_PAGE, app_state

# Re-export from elements
from elements import ElementType

# Re-export from page_rules
from page_rules import PAGE_FORMATS as page_formats
from page_rules import PAGE_RULES as page_rules

# Backwards compatible function wrappers
def set_dpi(dpi):
    app_state.dpi = dpi

def get_dpi():
    return app_state.dpi

def set_debug_mode(mode):
    app_state.debug = mode

def get_debug_mode():
    return app_state.debug

def set_dark_mode(mode):
    app_state.dark_mode = mode

def get_dark_mode():
    return app_state.dark_mode

def convert_inches_to_pixels(inches):
    return app_state.convert_inches_to_pixels(inches)
