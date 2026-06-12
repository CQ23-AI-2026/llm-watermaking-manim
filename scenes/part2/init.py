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

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from manim import *
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_RED, VG_PURPLE, VG_ORANGE,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class Scene2_Intro_Extended(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)

        # Nền lưới mờ công nghệ
        grid = NumberPlane(
            background_line_style={
                "stroke_color": VG_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.06,
            },
            axis_config={
                "stroke_opacity": 0,
            },
        )
        self.add(grid)

        # Chuẩn bị file âm thanh
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_intro.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Chuẩn bị Tiêu đề Part 2
        part_title = VGText(
            "TEXT WATERMARK",
            font_size=LARGE_FONT_SIZE,
            color=WHITE,
            weight=BOLD_WEIGHT,
        )
        underline = Line(
            LEFT * 3.5,
            RIGHT * 3.5,
            color=VG_BLUE,
            stroke_width=2,
            stroke_opacity=0.6,
        ).next_to(part_title, DOWN, buff=0.25)
        title_group = VGroup(part_title, underline)

        # Chuẩn bị danh sách Timeline
        item_2_0 = VGText("2.0: Cơ chế Language Model & Lấy mẫu", font_size=32, color=WHITE)
        
        item_2_1 = VGText("2.1: Phương pháp Green-Red Watermark", font_size=32, color=WHITE)
        box_green = Rectangle(width=0.35, height=0.35, fill_color=VG_GREEN, fill_opacity=0.8, stroke_color=VG_GREEN)
        box_red = Rectangle(width=0.35, height=0.35, fill_color=VG_RED, fill_opacity=0.8, stroke_color=VG_RED)
        box_red.next_to(box_green, RIGHT, buff=0)
        split_box = VGroup(box_green, box_red)
        
        item_2_2 = VGText("2.2 & 2.3: Triết lý Gumbel (Distortion-Free)", font_size=32, color=WHITE)
        
        item_2_4 = VGText("2.4: Kết quả lý thuyết & Sự đánh đổi (Trade-offs)", font_size=32, color=WHITE)
        triangle = Polygon(ORIGIN, LEFT*0.15+DOWN*0.25, RIGHT*0.15+DOWN*0.25, fill_color=VG_GRAY, fill_opacity=1)
        line = Line(LEFT*0.4, RIGHT*0.4, color=WHITE, stroke_width=4).next_to(triangle, UP, buff=0)
        scale = VGroup(triangle, line)

        # Căn chỉnh bố cục trái cho các dòng text
        texts = VGroup(item_2_0, item_2_1, item_2_2, item_2_4).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        split_box.next_to(item_2_1, RIGHT, buff=0.4)
        scale.next_to(item_2_4, RIGHT, buff=0.4)
        
        group_2_1 = VGroup(item_2_1, split_box)
        group_2_4 = VGroup(item_2_4, scale)

        # Đẩy toàn bộ danh sách xuống dưới tâm một chút
        all_content = VGroup(texts, split_box, scale)
        all_content.move_to(DOWN * 0.5)

        # GIAI ĐOẠN 1
        self.play(Write(part_title), run_time=1.0)
        self.play(Create(underline), run_time=0.5)
        
        self.play(title_group.animate.to_edge(UP, buff=0.8), run_time=1.0)
        self.play(FadeIn(item_2_0, shift=UP), run_time=1.0)

        # GIAI ĐOẠN 2
        self.wait(2.0)
        self.play(FadeIn(group_2_1, shift=RIGHT), run_time=1.0)

        # GIAI ĐOẠN 3
        self.wait(2.5)
        self.play(FadeIn(item_2_2, shift=UP), run_time=1.0)

        # GIAI ĐOẠN 4
        self.wait(3.0)
        self.play(FadeIn(group_2_4, shift=UP), run_time=1.0)
        self.play(Rotate(line, angle=-PI/8, about_point=line.get_center()), run_time=1.0)

        # Chờ phần audio còn lại
        elapsed_time = self.renderer.time - start_time
        wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
        if wait_time > 0:
            self.wait(wait_time)
        else:
            self.wait(3.0)

        # Dọn dẹp cảnh (1.0s)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)


def play_part2_init(scene: Scene) -> None:
    Scene2_Intro_Extended.construct(scene)
