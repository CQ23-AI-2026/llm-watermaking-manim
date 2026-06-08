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
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE,
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

class InitScene(Scene):
    """Phân cảnh giới thiệu cho Part 1.
    Tiêu đề Part 1 'Giới thiệu Watermark'

    Render:
        $env:PYTHONPATH="."
        manim -pql scenes/part1/init.py InitScene --media_dir media/part1/init
    """
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

        # Tiêu đề Part 1
        part_title = VGText(
            "GIỚI THIỆU WATERMARK",
            font_size=LARGE_FONT_SIZE,
            color=WHITE,
            weight=BOLD_WEIGHT,
        )

        # Đường trang trí phía dưới tiêu đề
        underline = Line(
            LEFT * 3.5,
            RIGHT * 3.5,
            color=VG_BLUE,
            stroke_width=2,
            stroke_opacity=0.6,
        ).next_to(part_title, DOWN, buff=0.25)

        # Nhúng tệp âm thanh lồng tiếng cho Cảnh nếu có
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "voice", "1_0.mp3")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Hoạt ảnh
        self.play(Write(part_title), run_time=1.5)
        self.play(Create(underline), run_time=1.0)
        wait_time = max(0.0, (voice_duration or 0.0) - 2.5)
        if wait_time > 0:
            self.wait(wait_time)
        else:
            self.wait(2.0)

        # Dọn dẹp cảnh (1.0s)
        self.play(
            FadeOut(part_title, shift=UP),
            FadeOut(underline),
            FadeOut(grid),
            run_time=1.0,
        )
        self.wait(0.3)

def play_part1_init(scene: Scene) -> None:
    InitScene.construct(scene)
