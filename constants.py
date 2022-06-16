WIDTH = 1200
HEIGHT = 960
LINE_HEIGHT = 16
MAX_LINES_PER_PAGE = 55

dpi = 72

def set_dpi(_dpi):
    global dpi
    dpi = _dpi

def get_dpi():
    global dpi
    return dpi

def convert_inches_to_pixels(_dpi, inch):
    return _dpi * inch


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
    "page":{
        "margin": {
            "top": 1,
            "right": 1,
            "bottom": 1,
            "left": 1.5,
        }
    },
    "dialogue": {
        "margin": {
            "left": 1,
            "right": 1
        },
        "align": "center"
    },
    "character": {
        "margin": {
            "left": 2.2,   
            "right": 2.2,   
        },
        "uppercase": True,
        "align": "center"
    },
    "page_number": {
        "margin": {
            "top": 0.5
        },
        "align": "right"
    },
    "transition": {
        "align": "right",
        "uppercase": True,
    },
    "scene": {
        "uppercase": True,
        "bold": True
    },
    "intercut": {
        "uppercase": True,
        "bold": True
    }

}

