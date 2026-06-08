from manim import *
import os
import sys

# Add root dir to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

from config.style import DEFAULT_FONT, VGText

class VGParagraph(VGroup):
    def __init__(self, text, font_size=28, color=WHITE, line_spacing=0.2, alignment="left", font=DEFAULT_FONT, **kwargs):
        super().__init__()
        lines = text.split("\n")
        rendered_lines = []
        for line in lines:
            rendered_line = VGText(
                line, 
                font_size=font_size, 
                color=color, 
                font=font,
                **kwargs
            )
            rendered_lines.append(rendered_line)
        
        # Position them
        if len(rendered_lines) > 0:
            self.add(rendered_lines[0])
            for i in range(1, len(rendered_lines)):
                if alignment == "left":
                    rendered_lines[i].next_to(rendered_lines[i-1], DOWN, buff=line_spacing, aligned_edge=LEFT)
                elif alignment == "right":
                    rendered_lines[i].next_to(rendered_lines[i-1], DOWN, buff=line_spacing, aligned_edge=RIGHT)
                else:
                    rendered_lines[i].next_to(rendered_lines[i-1], DOWN, buff=line_spacing, aligned_edge=ORIGIN)
                self.add(rendered_lines[i])

class TestFontScene(Scene):
    def construct(self):
        desc2 = "Kẻ xâm phạm lấy mô hình gốc và huấn luyện tiếp\n(fine-tune) trên tập dữ liệu mới nhằm che giấu\nhoàn toàn các hành vi đặc trưng và dấu vết\nsở hữu ban đầu."
        desc3 = "Cắt tỉa (pruning) các trọng số hoặc thành phần\nnơ-ron ít quan trọng để thay đổi cấu trúc vật lý,\nsau đó fine-tune lại nhằm lẩn tránh các hệ thống\nphát hiện bản quyền."

        # Old Paragraph rendering
        p_old2 = Paragraph(desc2, font=DEFAULT_FONT, font_size=28, line_spacing=1.4).scale(14/28).move_to([-3, 2, 0])
        p_old3 = Paragraph(desc3, font=DEFAULT_FONT, font_size=28, line_spacing=1.4).scale(14/28).move_to([-3, 0, 0])

        # New VGParagraph rendering (uses VGText which has disable_ligatures=True)
        p_new2 = VGParagraph(desc2, font_size=28, line_spacing=0.15).scale(14/28).move_to([3, 2, 0])
        p_new3 = VGParagraph(desc3, font_size=28, line_spacing=0.15).scale(14/28).move_to([3, 0, 0])

        lbl_old = Text("Old Paragraph", font_size=20).move_to([-3, 3.5, 0])
        lbl_new = Text("New VGParagraph", font_size=20).move_to([3, 3.5, 0])

        self.add(lbl_old, lbl_new, p_old2, p_old3, p_new2, p_new3)
        self.wait(1)
