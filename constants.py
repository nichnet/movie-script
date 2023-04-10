from enum import Enum

DEBUG = 0

WIDTH = 1600
HEIGHT = 980
LINE_HEIGHT = 16
MAX_LINES_PER_PAGE = 53

dpi = 72


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


def set_dpi(_dpi):
    global dpi
    dpi = _dpi

def set_debug_mode(mode):
    global DEBUG
    DEBUG = mode

def get_debug_mode():
    global DEBUG
    return DEBUG

def get_dpi():
    global dpi
    return dpi

def convert_inches_to_pixels(inch):
    return int(get_dpi() * inch)


page_formats = {
    "letter": {
        "width":8.5, 
        "height":11
    },
    "a4": {
        "width": 8.25, 
        "height":11.75
    }
}


#in inches
page_rules = {
    ElementType.PAGE:{
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
    }

}

