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


class VGParagraph(VGroup):
    def __init__(self, text, font_size=DEFAULT_FONT_SIZE, color=WHITE, line_spacing=0.25, alignment="left", font=DEFAULT_FONT, **kwargs):
        super().__init__()
        lines = text.split("\n")
        rendered_lines = []
        for line in lines:
            if line.strip() == "":
                rendered_lines.append(None)
            else:
                rendered_line = VGText(
                    line, 
                    font_size=font_size, 
                    color=color, 
                    font=font,
                    **kwargs
                )
                rendered_lines.append(rendered_line)
        
        first_idx = -1
        for idx, item in enumerate(rendered_lines):
            if item is not None:
                first_idx = idx
                break
        
        if first_idx != -1:
            self.add(rendered_lines[first_idx])
            last_rendered = rendered_lines[first_idx]
            
            for i in range(first_idx + 1, len(rendered_lines)):
                if rendered_lines[i] is None:
                    continue
                
                # Count consecutive empty lines preceding this one
                empty_count = 0
                for j in range(i - 1, first_idx - 1, -1):
                    if rendered_lines[j] is None:
                        empty_count += 1
                    else:
                        break
                
                # Approximate line height based on font size (28pt is ~0.35 manim units)
                line_height = font_size * 0.0125
                total_buff = line_spacing + empty_count * (line_height + line_spacing)
                
                if alignment == "left":
                    rendered_lines[i].next_to(last_rendered, DOWN, buff=total_buff, aligned_edge=LEFT)
                elif alignment == "right":
                    rendered_lines[i].next_to(last_rendered, DOWN, buff=total_buff, aligned_edge=RIGHT)
                else:
                    rendered_lines[i].next_to(last_rendered, DOWN, buff=total_buff, aligned_edge=ORIGIN)
                
                self.add(rendered_lines[i])
                last_rendered = rendered_lines[i]

