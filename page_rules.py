"""Page formatting rules for screenplay elements."""

from elements import ElementType


# Page formats in inches
PAGE_FORMATS = {
    "letter": {
        "width": 8.5,
        "height": 11
    },
    "a4": {
        "width": 8.25,
        "height": 11.75
    }
}


# Formatting rules for each element type (measurements in inches)
PAGE_RULES = {
    ElementType.PAGE: {
        "margin": {
            "top": 1,
            "right": 1,
            "bottom": 1,
            "left": 1.5,
        }
    },
    ElementType.ACTION: {
        "margin": {
            "top": 0.2
        }
    },
    ElementType.DIALOGUE: {
        "margin": {
            "left": 1,
            "right": 1,
            "top": 0.2
        },
        "align": "center"
    },
    ElementType.SPEAKER: {
        "margin": {
            "left": 2.2,
            "right": 2.2,
        },
        "uppercase": True,
        "bold": True,
        "align": "center",
    },
    ElementType.TITLE: {
        "margin": {
            "left": 2.2,
            "right": 2.2,
        },
        "uppercase": True,
        "align": "center",
        "bold": True,
        "underline": True,
    },
    ElementType.PAGE_NUMBER: {
        "margin": {
            "top": 0.5
        },
        "align": "right"
    },
    ElementType.TRANSITION: {
        "align": "right",
        "uppercase": True,
        "margin": {
            "top": 0.2
        }
    },
    ElementType.SCENE: {
        "uppercase": True,
        "bold": True,
        "margin": {
            "top": 0.2
        }
    },
    ElementType.INTERCUT: {
        "uppercase": True,
        "bold": True,
        "margin": {
            "top": 0,
        }
    },
    # Title page elements
    ElementType.TITLE_PAGE_TITLE: {
        "margin": {
            "top": 3,
            "left": 1,
            "right": 1,
        },
        "uppercase": True,
        "align": "center",
        "bold": True,
        "underline": True,
    },
    ElementType.TITLE_PAGE_AUTHOR: {
        "margin": {
            "top": 0.3,
            "left": 1,
            "right": 1,
        },
        "align": "center",
    },
    ElementType.TITLE_PAGE_COMMENT: {
        "margin": {
            "top": 0.2,
            "left": 0,
            "right": 0,
        },
        "align": "left",
    },
    ElementType.TITLE_PAGE_DATE: {
        "margin": {
            "top": 0.2,
            "left": 0,
            "right": 0,
        },
        "align": "right",
    },
    ElementType.SCENE_CONTINUED: {
        "uppercase": True,
        "bold": True,
        "margin": {
            "top": 0
        }
    },
}
