import os
import sys
import glob
import numpy as np

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
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_ORANGE, BOLD_WEIGHT, LARGE_FONT_SIZE
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

class ProbingScene(Scene):
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
        voice_4 = os.path.join(extraction_dir, "extraction_probing.mp3")
        voice_5 = os.path.join(extraction_dir, "extraction_tradeoff.mp3")

        dur_4 = _get_audio_duration(voice_4) or 60.0
        dur_5 = _get_audio_duration(voice_5) or 78.0

        # =========================================================================
        # SLIDE 5: PROBING & PHÂN TÍCH PHỔ (Cảnh 3.8)
        # =========================================================================
        if os.path.exists(voice_4):
            self.add_sound(voice_4)

        title_prob = VGText("CƠ CHẾ PROBING VÀ PHÂN TÍCH PHỔ", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_prob = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(title_prob, DOWN, buff=0.15).align_to(title_prob, LEFT)
        
        desc_prob = VGParagraph(
            "Để xác minh watermark, chủ sở hữu gửi các\ntruy vấn probing đặc biệt đến API nghi ngờ.\nPhân tích phổ (Periodogram) các phản hồi\nsẽ chỉ ra tín hiệu tuần hoàn bí mật\nnổi lên rõ rệt khỏi nhiễu nền.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_prob, DOWN, buff=0.4).align_to(line_prob, LEFT)

        left_g_prob = VGroup(title_prob, line_prob, desc_prob)

        # Visual Probing: Đồ thị phân tích phổ Periodogram
        axes_4 = Axes(
            x_range=[0, 10, 1], y_range=[0, 4, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}
        ).move_to([3.4, -0.4, 0])

        # Hàm vẽ phổ nhiễu nền
        noise_curve = axes_4.plot(
            lambda x: 0.4 * np.sin(3*x) + 0.2 * np.cos(7*x) + 0.1 * np.sin(15*x) + 0.6,
            color=VG_GRAY, stroke_width=1.5
        )

        # Hàm vẽ đỉnh phổ watermark nhô cao tại x=5
        peak_curve = axes_4.plot(
            lambda x: 2.8 * np.exp(-((x - 5) / 0.4)**2) + 0.4 * np.sin(3*x) + 0.2 * np.cos(7*x) + 0.1 * np.sin(15*x) + 0.6,
            color=VG_GOLD, stroke_width=2.5
        )

        chart_title_4 = VGText("Đồ thị phân tích phổ Periodogram", font_size=16, color=VG_GRAY).scale(8/16).next_to(axes_4, UP, buff=0.2)
        detector_lbl = VGText("Tín hiệu Watermark (F=5)", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).scale(7/14).move_to(axes_4.c2p(5, 3.4))
        
        # Mũi tên chỉ vào đỉnh
        pointer_arrow = Arrow(axes_4.c2p(5.5, 3.2), axes_4.c2p(5.0, 2.5), buff=0.05, color=VG_GOLD, stroke_width=1.5)

        right_g_prob1 = VGroup(axes_4, noise_curve, chart_title_4)
        right_g_prob2 = VGroup(peak_curve, detector_lbl, pointer_arrow)

        self.play(
            FadeIn(left_g_prob, shift=UP * 0.3),
            FadeIn(right_g_prob1, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Nhô cao đỉnh phổ thể hiện phát hiện watermark
        self.wait(2.0)
        self.play(
            Transform(noise_curve, peak_curve),
            FadeIn(detector_lbl),
            Create(pointer_arrow),
            chart_title_4.animate.set_color(VG_GOLD),
            run_time=1.8
        )

        self.wait(max(1.0, dur_4 - 1.2 - 2.0 - 1.8 - 0.8))

        self.play(
            FadeOut(left_g_prob, shift=LEFT * 0.5),
            FadeOut(right_g_prob1),
            FadeOut(right_g_prob2),
            FadeOut(noise_curve),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 6: ĐÁNH ĐỔI CHẤT LƯỢNG & PHA LOÃNG DỮ LIỆU (Cảnh 3.9)
        # =========================================================================
        if os.path.exists(voice_5):
            self.add_sound(voice_5)

        title_trade = VGText("ĐÁNH ĐỔI CHẤT LƯỢNG & ĐỘ BỀN BỈ", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_trade = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_ORANGE, stroke_width=2, stroke_opacity=0.6).next_to(title_trade, DOWN, buff=0.15).align_to(title_trade, LEFT)
        
        desc_trade = VGParagraph(
            "Tồn tại sự đánh đổi giữa chất lượng văn bản\nsinh ra và khả năng phát hiện. Bên cạnh đó,\nmột watermark tốt phải bền bỉ ngay cả khi\ndữ liệu chưng cất bị pha loãng bằng cách\ntrộn lẫn với các nguồn dữ liệu sạch khác.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_trade, DOWN, buff=0.4).align_to(line_trade, LEFT)

        left_g_trade = VGroup(title_trade, line_trade, desc_trade)

        # Visual Slide 5: Cán cân đánh đổi (Quality vs Detectability)
        base = Polygon(
            [3.4, -1.8, 0], [3.2, -2.4, 0], [3.6, -2.4, 0],
            color=VG_GRAY, fill_color=VG_GRAY, fill_opacity=0.5, stroke_width=1.5
        )
        pillar = Line(start=[3.4, -1.8, 0], end=[3.4, -0.6, 0], color=VG_GRAY, stroke_width=2)
        
        # VGroup chứa phần thanh ngang và đĩa cân có thể xoay được
        scale_beam = Line(start=[1.8, -0.6, 0], end=[5.0, -0.6, 0], color=VG_GRAY, stroke_width=3)
        pivot = Dot([3.4, -0.6, 0], radius=0.08, color=VG_ORANGE)
        
        left_pan = Line(start=[1.8, -0.6, 0], end=[1.8, -1.4, 0], color=VG_GRAY, stroke_width=1.5)
        left_plate = RoundedRectangle(corner_radius=0.04, width=1.0, height=0.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=1.5).move_to([1.8, -1.45, 0])
        left_lbl = VGText("Chất lượng\n(Quality)", font_size=14, color=VG_GREEN).scale(7/14).next_to(left_plate, UP, buff=0.1)
        left_pan_group = VGroup(left_pan, left_plate, left_lbl)

        right_pan = Line(start=[5.0, -0.6, 0], end=[5.0, -1.4, 0], color=VG_GRAY, stroke_width=1.5)
        right_plate = RoundedRectangle(corner_radius=0.04, width=1.0, height=0.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_ORANGE, stroke_width=1.5).move_to([5.0, -1.45, 0])
        right_lbl = VGText("Độ nhạy\n(Detection)", font_size=14, color=VG_ORANGE).scale(7/14).next_to(right_plate, UP, buff=0.1)
        right_pan_group = VGroup(right_pan, right_plate, right_lbl)

        beam_system = VGroup(scale_beam, left_pan_group, right_pan_group)

        right_g_trade = VGroup(base, pillar, beam_system, pivot)

        self.play(
            FadeIn(left_g_trade, shift=UP * 0.3),
            FadeIn(right_g_trade, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng bập bênh nghiêng đĩa cân
        self.wait(2.0)
        self.play(
            Rotate(beam_system, angle=-10 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.2
        )
        self.play(
            Rotate(beam_system, angle=20 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.6
        )
        self.play(
            Rotate(beam_system, angle=-10 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.2
        )

        self.wait(max(1.0, dur_5 - 1.2 - 2.0 - 4.0 - 1.0)) # trừ đi anim, wait và exit

        # Dọn dẹp Slide 6 (Cũng là kết thúc phân cảnh)
        self.play(
            FadeOut(left_g_trade, shift=LEFT * 0.4),
            FadeOut(right_g_trade, shift=RIGHT * 0.4),
            run_time=1.0
        )
        self.wait(0.2)

        # Dọn dẹp tiêu đề chính và đường gạch chân (vì kết thúc phần model extraction)
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_probing(scene: Scene) -> None:
    ProbingScene.construct(scene)
