"""Theme management for the application."""

from config import app_state


class ThemeManager:
    """Manages application theming."""

    # Style definitions
    DARK_THEME = {
        "window": "background-color: #2b2b2b;",
        "menubar": "background-color: #3c3c3c; color: white;",
        "statusbar": "background-color: #3c3c3c; color: white;",
        "text_color": "white"
    }

    LIGHT_THEME = {
        "window": "",
        "menubar": "",
        "statusbar": "",
        "text_color": "black"
    }

    def __init__(self):
        self._widgets = []

    def register_widget(self, widget, apply_func):
        """Register a widget to receive theme updates.

        Args:
            widget: The widget to theme
            apply_func: Function to call with theme dict when theme changes
        """
        self._widgets.append((widget, apply_func))

    def set_dark_mode(self, enabled):
        """Set dark mode on or off."""
        app_state.dark_mode = enabled
        self.apply_theme()

    def is_dark_mode(self):
        """Check if dark mode is enabled."""
        return app_state.dark_mode

    def get_current_theme(self):
        """Get the current theme dictionary."""
        return self.DARK_THEME if app_state.dark_mode else self.LIGHT_THEME

    def apply_theme(self):
        """Apply the current theme to all registered widgets."""
        theme = self.get_current_theme()
        for widget, apply_func in self._widgets:
            apply_func(widget, theme)

    def get_text_color(self):
        """Get the current text color."""
        return self.get_current_theme()["text_color"]


# Global theme manager instance
theme_manager = ThemeManager()
