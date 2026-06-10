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
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, BOLD_WEIGHT, LARGE_FONT_SIZE
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

class CATERScene(Scene):
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
        voice_3 = os.path.join(extraction_dir, "extraction_cater.mp3")
        dur_3 = _get_audio_duration(voice_3) or 60.0

        # =========================================================================
        # SLIDE 4: CATER - WATERMARK CÓ ĐIỀU KIỆN (Cảnh 3.7)
        # =========================================================================
        if os.path.exists(voice_3):
            self.add_sound(voice_3)

        title_cater = VGText("CATER - THỦY VÂN CÓ ĐIỀU KIỆN", font_size=20, color=WHITE, weight=BOLD_WEIGHT).move_to([-5.8, 1.8, 0], aligned_edge=LEFT)
        line_cater = Line([-5.8, 1.5, 0], [-1.8, 1.5, 0], color=VG_PURPLE, stroke_width=2, stroke_opacity=0.6)
        
        desc_cater = VGParagraph(
            "CATER phụ thuộc chặt chẽ vào ngữ cảnh.\nKhi phát hiện điều kiện định sẵn trong văn bản,\nmô hình thay đổi lựa chọn từ đồng nghĩa.\nĐiều này tối ưu hóa độ tự nhiên của văn bản\nvà khả năng phát hiện mô hình bắt chước.",
            font_size=16, color=WHITE, line_spacing=0.25, alignment="left"
        ).next_to(line_cater, DOWN, buff=0.4).align_to(line_cater, LEFT)

        left_g_cater = VGroup(title_cater, line_cater, desc_cater)

        # Visual CATER: Cây quyết định lựa chọn từ theo điều kiện
        root_node = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([3.2, 1.0, 0])
        root_lbl = VGText("Ngữ cảnh hiện tại\n(Context Trigger)", font_size=16, color=VG_BLUE).scale(8/16).move_to(root_node.get_center())
        root_group = VGroup(root_node, root_lbl)

        # Lựa chọn 1: Có khớp điều kiện
        node_yes = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0).move_to([1.8, -1.0, 0])
        node_yes_lbl = VGText("Khớp điều kiện:\nChọn 'nghiên cứu' [WM]", font_size=14, color=VG_GREEN).scale(7/14).move_to(node_yes.get_center())
        yes_group = VGroup(node_yes, node_yes_lbl)

        # Lựa chọn 2: Không khớp điều kiện
        node_no = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([4.6, -1.0, 0])
        node_no_lbl = VGText("Không khớp:\nChọn 'học tập' (Tự nhiên)", font_size=14, color=VG_GRAY).scale(7/14).move_to(node_no.get_center())
        no_group = VGroup(node_no, node_no_lbl)

        # Mũi tên phân nhánh
        a_yes = Arrow(root_node.get_bottom(), node_yes.get_top(), buff=0.1, color=VG_GREEN, stroke_width=2)
        a_no = Arrow(root_node.get_bottom(), node_no.get_top(), buff=0.1, color=VG_GRAY, stroke_width=1.5)

        right_g_cater = VGroup(root_group, yes_group, no_group, a_yes, a_no)

        self.play(
            FadeIn(left_g_cater, shift=UP * 0.3),
            FadeIn(right_g_cater, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng chạy luồng quyết định (nháy sáng nhánh Yes)
        self.wait(1.5)
        self.play(
            a_yes.animate.set_stroke(color=VG_GOLD, width=4),
            node_yes.animate.set_stroke(color=VG_GOLD, width=3.0),
            run_time=0.8
        )
        self.play(
            a_yes.animate.set_stroke(color=VG_GREEN, width=2),
            node_yes.animate.set_stroke(color=VG_GREEN, width=2.0),
            run_time=0.8
        )

        self.wait(max(1.0, dur_3 - 1.2 - 1.5 - 1.6 - 0.8))

        self.play(
            FadeOut(left_g_cater, shift=LEFT * 0.5),
            FadeOut(right_g_cater, shift=LEFT * 0.5),
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

def play_part3_cater(scene: Scene) -> None:
    CATERScene.construct(scene)
