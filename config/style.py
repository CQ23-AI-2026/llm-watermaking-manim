# Common style config for manim scenes
from manim import *

# Color palette
VG_GREEN = '#00C853'
VG_RED = '#D50000'
VG_BLUE = '#2962FF'
VG_ORANGE = '#FF6D00'
VG_PURPLE = '#AA00FF'
VG_GRAY = '#757575'

# Font settings
DEFAULT_FONT_SIZE = 36
LARGE_FONT_SIZE = 48
SMALL_FONT_SIZE = 24

# Common style kwargs
DEFAULT_WEIGHT = "NORMAL"
BOLD_WEIGHT = "BOLD"
ITALIC = True

class VGText(Text):
    def __init__(self, content, font_size=DEFAULT_FONT_SIZE, weight=DEFAULT_WEIGHT, slant="NORMAL", **kwargs):
        super().__init__(content, font_size=font_size, weight=weight, slant=slant, **kwargs)
