import os
import sys
import glob

# Try to find and add venv site-packages to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
venv_dirs = [
    os.path.join(root_dir, ".venv", "Lib", "site-packages"),
    os.path.join(root_dir, ".venv", "lib", "python*", "site-packages"),
]
for path_pattern in venv_dirs:
    for path in glob.glob(path_pattern):
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)

from manim import *
from config.style import (
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, BOLD_WEIGHT, LARGE_FONT_SIZE
)

def _get_audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path):
        return None
    try:
        from mutagen.mp3 import MP3
        return float(MP3(path).info.length)
    except Exception:
        pass
    try:
        from moviepy.editor import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class GINSEWScene(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        
        # Thêm grid nếu chưa có trên screen
        grid_exists = any(isinstance(m, NumberPlane) for m in self.mobjects)
        if not grid_exists:
            grid = NumberPlane(
                background_line_style={
                    "stroke_color": VG_GRAY,
                    "stroke_width": 1,
                    "stroke_opacity": 0.06,
                },
                axis_config={"stroke_opacity": 0},
            )
            self.add(grid)

        # Tiêu đề chính phân cảnh ở góc trên màn hình (luôn hiển thị)
        scene_title = VGText(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        underline = Line(
            LEFT * 3.825, RIGHT * 3.825,
            color=VG_GOLD, stroke_width=2, stroke_opacity=0.6
        ).next_to(scene_title, DOWN, buff=0.2)
        
        self.add(scene_title, underline)

        # Audio paths & durations
        extraction_dir = os.path.join(current_dir, "assets", "extraction")
        voice_2 = os.path.join(extraction_dir, "extraction_ginsew.mp3")
        dur_2 = _get_audio_duration(voice_2) or 74.0

        # =========================================================================
        # SLIDE 3: GINSEW - THỦY VÂN SINH VĂN BẢN VÔ HÌNH (Cảnh 3.6)
        # =========================================================================
        if os.path.exists(voice_2):
            self.add_sound(voice_2)

        title_ginsew = VGText("GINSEW - THỦY VÂN TỰ HỒI QUY", font_size=20, color=WHITE, weight=BOLD_WEIGHT).move_to([-5.8, 1.8, 0], aligned_edge=LEFT)
        line_ginsew = Line([-5.8, 1.5, 0], [-1.8, 1.5, 0], color=VG_BLUE, stroke_width=2, stroke_opacity=0.6)
        
        desc_ginsew = VGParagraph(
            "GINSEW dành cho mô hình sinh văn bản.\nTại mỗi bước sinh, mô hình can thiệp nhẹ\nvào vector xác suất của các token kế tiếp,\ntạo ra một chữ ký thống kê vô hình\nở chuỗi văn bản đầu ra.",
            font_size=16, color=WHITE, line_spacing=0.25, alignment="left"
        ).next_to(line_ginsew, DOWN, buff=0.4).align_to(line_ginsew, LEFT)

        left_g_ginsew = VGroup(title_ginsew, line_ginsew, desc_ginsew)

        # Visual GINSEW: Chuỗi sinh Token tự hồi quy
        tok_1 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([1.2, 0.8, 0])
        tok_1_lbl = VGText("Token t-2", font_size=16, color=VG_GRAY).scale(8/16).move_to(tok_1.get_center())
        t1_group = VGroup(tok_1, tok_1_lbl)

        tok_2 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([3.0, 0.8, 0])
        tok_2_lbl = VGText("Token t-1", font_size=16, color=VG_GRAY).scale(8/16).move_to(tok_2.get_center())
        t2_group = VGroup(tok_2, tok_2_lbl)

        arrow_t1_t2 = Arrow(tok_1.get_right(), tok_2.get_left(), buff=0.05, color=VG_BLUE, stroke_width=1.5)

        # Vector xác suất tại bước t
        v_box = RoundedRectangle(corner_radius=0.05, width=2.4, height=1.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([3.0, -1.0, 0])
        v_lbl = VGText("Xác suất từ vựng P(V)", font_size=14, color=VG_BLUE).scale(7/14).next_to(v_box, UP, buff=0.1)
        
        # Các dòng biểu diễn xác suất token
        lines_v = VGroup()
        token_names = ["được", "học", "chơi", "ngủ"]
        token_probs = [0.1, 0.65, 0.15, 0.1] # 'học' được ưu tiên bằng GINSEW
        
        for idx, (name, prob) in enumerate(zip(token_names, token_probs)):
            y_pos = v_box.get_top()[1] - 0.3 - idx * 0.35
            name_txt = VGText(name, font_size=16, color=WHITE).scale(8/16).move_to([2.1, y_pos, 0])
            
            p_bar_bg = Line(start=[2.6, y_pos, 0], end=[4.0, y_pos, 0], color=VG_GRAY, stroke_width=6, stroke_opacity=0.2)
            p_bar_fill = Line(start=[2.6, y_pos, 0], end=[2.6 + prob * 1.4, y_pos, 0], color=VG_GREEN if idx == 1 else VG_BLUE, stroke_width=6)
            lines_v.add(name_txt, p_bar_bg, p_bar_fill)

        arrow_t2_v = Arrow(tok_2.get_bottom(), v_box.get_top(), buff=0.1, color=VG_BLUE, stroke_width=1.5)
        
        # Token t tiếp theo sinh ra
        tok_3 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0).move_to([4.8, 0.8, 0])
        tok_3_lbl = VGText("Token t (học)", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).scale(8/16).move_to(tok_3.get_center())
        t3_group = VGroup(tok_3, tok_3_lbl)

        arrow_v_t3 = Arrow(v_box.get_right(), tok_3.get_bottom(), buff=0.1, color=VG_GREEN, stroke_width=2)

        right_g_ginsew = VGroup(t1_group, t2_group, arrow_t1_t2, v_box, v_lbl, lines_v, arrow_t2_v, t3_group, arrow_v_t3)

        self.play(
            FadeIn(left_g_ginsew, shift=UP * 0.3),
            FadeIn(right_g_ginsew, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng nhấp nháy xanh lá cây ở token được chọn
        self.wait(1.5)
        self.play(
            t3_group.animate.scale(1.1),
            lines_v[4].animate.set_stroke(color=VG_GOLD, width=8), # highlight bar fill của 'học'
            run_time=0.6
        )
        self.play(
            t3_group.animate.scale(1.0/1.1),
            lines_v[4].animate.set_stroke(color=VG_GREEN, width=6),
            run_time=0.6
        )

        self.wait(max(1.0, dur_2 - 1.2 - 1.5 - 1.2 - 0.8)) # trừ thời gian anim và exit

        self.play(
            FadeOut(left_g_ginsew, shift=LEFT * 0.5),
            FadeOut(right_g_ginsew, shift=LEFT * 0.5),
            run_time=0.8
        )
        self.wait(0.2)

        # FadeOut tiêu đề chính
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_ginsew(scene: Scene) -> None:
    GINSEWScene.construct(scene)
