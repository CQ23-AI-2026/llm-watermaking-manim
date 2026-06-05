# Common style config for manim scenes
from manim import *

# Color palette — 3Blue1Brown-inspired, harmonious on dark backgrounds
VG_GREEN  = '#2ECC71'   # Emerald green — mềm mại, dễ chịu
VG_RED    = '#E74C3C'   # Soft coral red — nổi bật nhưng không chói
VG_BLUE   = '#58A6FF'   # Sky blue — nhẹ nhàng, hiện đại
VG_ORANGE = '#F0A050'   # Warm amber — ấm áp, tinh tế
VG_PURPLE = '#B07CD8'   # Lavender purple — thanh lịch
VG_GRAY   = '#8B8B92'   # Neutral gray
VG_GOLD   = '#F4D160'   # Soft gold — sang trọng, không chói mắt
VG_LIGHT_BLUE = '#88C8F0'  # Pastel blue

# Font settings
DEFAULT_FONT = "CMU Serif"
DEFAULT_FONT_SIZE = 36
LARGE_FONT_SIZE = 48
SMALL_FONT_SIZE = 24

# Common style kwargs
DEFAULT_WEIGHT = "NORMAL"
BOLD_WEIGHT = "BOLD"
ITALIC = True

class VGText(Text):
    def __init__(self, content, font_size=DEFAULT_FONT_SIZE, weight=DEFAULT_WEIGHT, slant="NORMAL", font=DEFAULT_FONT, **kwargs):
        super().__init__(content, font=font, font_size=font_size, weight=weight, slant=slant, disable_ligatures=True, **kwargs)

