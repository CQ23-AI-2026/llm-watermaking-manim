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
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE, VG_RED,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT, DEFAULT_FONT
)
from scenes.part3.threats import create_network_diagram

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

class CoreConceptScene(Scene):
    """Phân cảnh Ý tưởng cốt lõi của Model Watermark (Cảnh 3.3).
    """
    def construct(self):
        current_dir = os.path.dirname(__file__)
        
        # Nền lưới mờ công nghệ đồng bộ
        grid = NumberPlane(
            background_line_style={
                "stroke_color": VG_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.06,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # Tiêu đề chính của phân cảnh
        scene_title = VGText(
            "Ý TƯỞNG CỐT LÕI CỦA MODEL WATERMARK",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        underline = Line(
            LEFT * 4.5, RIGHT * 4.5,
            color=VG_GOLD, stroke_width=2, stroke_opacity=0.6
        ).next_to(scene_title, DOWN, buff=0.2)

        # Audio Cảnh 3.3 với 2 file voice
        core_concept_dir = os.path.join(current_dir, "assets", "core_concept")
        voice_1 = os.path.join(core_concept_dir, "core_concept_1.mp3")
        voice_2 = os.path.join(core_concept_dir, "core_concept_2.mp3")

        dur_1 = _get_audio_duration(voice_1) or 36.49
        dur_2 = _get_audio_duration(voice_2) or 13.92

        # Xuất hiện Tiêu đề chính trước
        self.play(
            Write(scene_title),
            Create(underline),
            run_time=1.2
        )
        self.wait(0.5)

        if os.path.exists(voice_1):
            self.add_sound(voice_1)

        # --- PHẦN TEXT BÊN TRÁI ---
        title_text = VGText("NHÚNG CHỮ KÝ BÍ MẬT", font_size=36, color=VG_GOLD, weight=BOLD_WEIGHT).scale(18/36).move_to([-3.8, 1.8, 0])
        slide_underline = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(title_text, DOWN, buff=0.15).align_to(title_text, LEFT)
        
        desc_text = VGParagraph(
            "Model Watermark có thể hiểu đơn giản là việc\nnhúng một \"dấu hiệu nhận dạng bí mật\" vào mô hình.\n\nDấu hiệu này không làm giảm đáng kể chất lượng,\nvà người dùng bình thường khó nhận ra sự khác biệt.\n\nKhi cần, chủ sở hữu dùng một quy trình đặc biệt\nđể kiểm tra xem mô hình tình nghi\ncó mang dấu vết của mình hay không.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(slide_underline, DOWN, buff=0.4).align_to(slide_underline, LEFT)

        left_group = VGroup(title_text, slide_underline, desc_text)

        # --- PHẦN VISUAL BÊN PHẢI ---
        # 1. Vẽ mạng nơ-ron cơ bản (Ban đầu nằm bên phải)
        nn, neurons, connections = create_network_diagram(layers=[3, 4, 3], scale=0.65, color=VG_BLUE, stroke_opacity=0.35)
        nn.move_to([2.0, -0.4, 0])

        # 2. Dấu hiệu nhận dạng bí mật (Watermark Key)
        wm_key = Star(n=8, outer_radius=0.3, inner_radius=0.15, color=VG_GOLD, stroke_width=1.5)
        wm_key.set_fill(VG_GOLD, opacity=0.8)
        # Bắt đầu key ở ngoài góc trên bên phải rồi bay vào tâm mạng nơ-ron
        wm_key.move_to([5.0, 2.2, 0])

        # --- HOẠT ẢNH ---
        # A. Xuất hiện phần text trái và mạng nơ-ron bên phải
        self.play(
            FadeIn(left_group, shift=UP * 0.3),
            FadeIn(nn, shift=LEFT * 0.4),
            run_time=1.2
        )
        self.wait(1.5)

        # B. Dấu watermark key bay vào tâm mạng nơ-ron và nhấp nháy phát sáng (cấy watermark)
        self.play(
            wm_key.animate.move_to(nn.get_center()).scale(0.8),
            run_time=1.5
        )
        self.play(
            wm_key.animate.scale(1.3),
            Flash(nn.get_center(), color=VG_GOLD, line_length=0.3, num_lines=8),
            run_time=0.4
        )
        self.play(
            wm_key.animate.scale(1.0/1.3),
            run_time=0.4
        )
        
        # Đợi thuyết minh hết phần giới thiệu chung (core_concept_1)
        # dur_1 covers Phase 1: entry(1.2) + wait(1.5) + key_fly(1.5) + flash(0.4) + scale(0.4) + wait_remain
        self.wait(max(1.0, dur_1 - 1.2 - 1.5 - 1.5 - 0.4 - 0.4))

        # C. Phần text biến mất, biểu tượng (mạng nơ-ron + key) di chuyển hoàn toàn sang bên trái
        if os.path.exists(voice_2):
            self.add_sound(voice_2)

        self.play(
            FadeOut(left_group, shift=LEFT * 0.5),
            run_time=1.0
        )
        self.play(
            VGroup(nn, wm_key).animate.move_to([-4.0, -0.4, 0]),
            run_time=1.5
        )
        self.wait(0.5)

        # D. Chuẩn bị 3 hộp hướng giải quyết lớn và 3 mũi tên nối từ bên trái sang phải
        box_width, box_height = 3.6, 0.9
        box1 = RoundedRectangle(corner_radius=0.08, width=box_width, height=box_height, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([2.5, 1.5, 0])
        box1_lbl = VGText("1. Kháng Distillation (chống trích xuất)", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).scale(9/18).move_to(box1.get_center())
        g_box1 = VGroup(box1, box1_lbl)

        box2 = RoundedRectangle(corner_radius=0.08, width=box_width, height=box_height, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=1.5).move_to([2.5, 0, 0])
        box2_lbl = VGText("2. Dấu vân tay chỉ dẫn (chống tinh chỉnh)", font_size=18, color=VG_GREEN, weight=BOLD_WEIGHT).scale(9/18).move_to(box2.get_center())
        g_box2 = VGroup(box2, box2_lbl)

        box3 = RoundedRectangle(corner_radius=0.08, width=box_width, height=box_height, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=1.5).move_to([2.5, -1.5, 0])
        box3_lbl = VGText("3. Hậu kiểm mô hình (DeepJudge)", font_size=18, color=VG_PURPLE, weight=BOLD_WEIGHT).scale(9/18).move_to(box3.get_center())
        g_box3 = VGroup(box3, box3_lbl)

        # Tạo các mũi tên dài, thanh lịch từ nn đã dịch chuyển
        arrow1 = Arrow(nn.get_right(), box1.get_left(), buff=0.15, color=VG_BLUE, stroke_width=2)
        arrow2 = Arrow(nn.get_right(), box2.get_left(), buff=0.15, color=VG_GREEN, stroke_width=2)
        arrow3 = Arrow(nn.get_right(), box3.get_left(), buff=0.15, color=VG_PURPLE, stroke_width=2)

        # E. Xuất hiện tuần tự các hướng giải quyết kèm mũi tên
        self.play(
            FadeIn(g_box1, shift=RIGHT * 0.3),
            Create(arrow1),
            run_time=0.8
        )
        self.wait(1.0)

        self.play(
            FadeIn(g_box2, shift=RIGHT * 0.3),
            Create(arrow2),
            run_time=0.8
        )
        self.wait(1.0)

        self.play(
            FadeIn(g_box3, shift=RIGHT * 0.3),
            Create(arrow3),
            run_time=0.8
        )
        
        # Chờ nốt phần thời lượng thuyết minh còn lại (core_concept_2)
        # dur_2 covers Phase 2: fadeout(1.0) + move(1.5) + wait(0.5) + boxes/arrows(4.4) + wait_remain
        wait_remain = max(1.0, dur_2 - 7.4)
        self.wait(wait_remain)

        # --- DỌN DẸP PHÂN CẢNH ---
        self.play(
            FadeOut(nn),
            FadeOut(wm_key),
            FadeOut(g_box1),
            FadeOut(g_box2),
            FadeOut(g_box3),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            run_time=1.0
        )
        
        # Dọn dẹp tiêu đề chính
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            FadeOut(grid),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_core_concept(scene: Scene) -> None:
    CoreConceptScene.construct(scene)
