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
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

VOICEOVER_SCRIPT = """
=== CẢNH 1: WATERMARKING FOR LLMS ===
Trong thời đại AI phát triển mạnh mẽ như hiện nay,
làm sao để biết một đoạn văn
được viết bởi con người…
hay bởi trí tuệ nhân tạo?

Khi các mô hình ngôn ngữ lớn ngày càng tạo ra văn bản tự nhiên hơn,
ranh giới giữa nội dung thật và nội dung do AI sinh ra
đang dần trở nên mờ nhạt.

Và đó cũng là lúc
Watermarking for LLMs xuất hiện.

Một hướng công nghệ mới,
giúp “đánh dấu” văn bản do AI tạo ra
mà gần như không làm thay đổi cách con người đọc và cảm nhận nội dung.

=== CẢNH 1.5: TỔNG QUAN NỘI DUNG ===
Trong video này, chúng ta sẽ cùng đi qua 6 phần chính.

Đầu tiên là bối cảnh và động lực —
tại sao việc nhận diện văn bản AI
đang trở thành một vấn đề quan trọng.

Tiếp theo, chúng ta sẽ tìm hiểu khái niệm Watermark
và nguyên lý hoạt động phía sau nó.

Sau đó là Text Watermark —
kỹ thuật nhúng tín hiệu trực tiếp vào quá trình sinh văn bản của mô hình.

Ở phần tiếp theo,
chúng ta sẽ khám phá Model Watermark,
một hướng tiếp cận nhằm bảo vệ bản quyền và quyền sở hữu mô hình AI.

Tiếp đó là Phát hiện hậu kiểm —
các phương pháp kiểm tra văn bản sau khi đã được sinh ra.

Và cuối cùng,
là phần kết luận cùng những thách thức
và hướng phát triển trong tương lai.

=== CẢNH 2: BỐI CẢNH & ĐỘNG LỰC ===
Hãy cùng bắt đầu với phần đầu tiên —
Bối cảnh và Động lực.
"""


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
    """Phân cảnh giới thiệu cho Part 0.
    Cảnh 1: Tiêu đề chủ đề 'Watermarking for LLMs'
    Cảnh 2: Tiêu đề Part 0 'Bối cảnh & Động lực'

    Render:
        $env:PYTHONPATH="."
        manim -pql scenes/part0/init.py InitScene --media_dir media/part0/init
    """

    def construct(self):
        current_dir = os.path.dirname(__file__)

        # === CẢNH 1: Tiêu đề chủ đề tổng — "Watermarking for LLMs" ===

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

        # Tiêu đề chính
        main_title = VGText(
            "Watermarking for LLMs",
            font_size=LARGE_FONT_SIZE,
            color=VG_GOLD,
            weight=BOLD_WEIGHT,
        )

        # Dòng phụ đề
        main_subtitle = VGText(
            "Thủy vân cho các Mô hình Ngôn ngữ Lớn",
            font_size=SMALL_FONT_SIZE,
            color=WHITE,
        ).next_to(main_title, DOWN, buff=0.3)

        # Con dấu watermark trang trí
        seal_outer = Circle(
            radius=0.55, color=VG_GOLD, stroke_width=2, stroke_opacity=0.5
        )
        seal_inner = DashedVMobject(
            Circle(radius=0.42, color=VG_GOLD, stroke_width=1, stroke_opacity=0.35),
            num_dashes=24,
        )
        seal_label = VGText("WM", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT)
        seal = VGroup(seal_outer, seal_inner, seal_label).next_to(
            main_subtitle, DOWN, buff=0.45
        )

        # Nhúng tệp âm thanh lồng tiếng cho Cảnh 1 nếu có
        voice_1 = os.path.join(current_dir, "assets", "init", "init_scene_1.mp3")
        voice_1_duration = _get_audio_duration(voice_1)
        if voice_1_duration is not None:
            self.add_sound(voice_1)

        # Hoạt ảnh hiện tiêu đề chính, phụ đề và con dấu ngay lập tức khi mở màn
        self.play(FadeIn(main_title, shift=UP * 0.3), run_time=1.5)
        self.play(Write(main_subtitle), run_time=1.5)
        self.play(
            Create(seal_outer),
            Create(seal_inner),
            FadeIn(seal_label, scale=0.7),
            run_time=1.5,
        )

        # Chờ phần lồng tiếng Cảnh 1 phát xong
        wait_time = max(0.0, (voice_1_duration or 31.97) - 4.5)
        if wait_time > 0:
            self.wait(wait_time)

        # Dọn dẹp cảnh 1 (1.0s)
        self.play(
            FadeOut(main_title, shift=UP * 0.5),
            FadeOut(main_subtitle, shift=UP * 0.3),
            FadeOut(seal, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(0.3)

        # === CẢNH 1.5: Tổng quan nội dung video — 5 phần ===

        overview_title = VGText(
            "NỘI DUNG VIDEO",
            font_size=LARGE_FONT_SIZE - 8,
            color=VG_GOLD,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.6)

        overview_line = Line(
            LEFT * 4,
            RIGHT * 4,
            color=VG_GOLD,
            stroke_width=1.5,
            stroke_opacity=0.4,
        ).next_to(overview_title, DOWN, buff=0.15)

        # Nhúng tệp âm thanh lồng tiếng cho Cảnh 1.5 nếu có
        voice_1_5 = os.path.join(current_dir, "assets", "init", "init_scene_15.mp3")
        voice_1_5_duration = _get_audio_duration(voice_1_5)
        if voice_1_5_duration is not None:
            self.add_sound(voice_1_5)

        intro_anim_time = 1.0
        self.play(
            FadeIn(overview_title, shift=DOWN * 0.3),
            Create(overview_line),
            run_time=intro_anim_time,
        )

        # Danh sách 6 phần
        parts_data = [
            ("1", "Bối cảnh & Động lực"),
            ("2", "Giới thiệu Watermark"),
            ("3", "Text Watermark"),
            ("4", "Model Watermark"),
            ("5", "Phát hiện hậu kiểm"),
            ("6", "Kết luận & Hướng phát triển"),
        ]

        part_items = VGroup()
        for num, label in parts_data:
            # Tạo vòng tròn bao quanh mỗi số thứ tự (thu gọn kích thước)
            circle = Circle(radius=0.26, stroke_width=2.0, color=VG_BLUE)
            num_text = VGText(
                num, font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT
            ).move_to(circle.get_center())
            badge = VGroup(circle, num_text)

            label_text = VGText(label, font_size=22, color=WHITE)
            # Đặt nội dung chữ bên phải số thứ tự (buff giảm từ 0.5 xuống 0.3)
            label_text.next_to(badge, RIGHT, buff=0.3)

            row = VGroup(badge, label_text)
            part_items.add(row)

        # Thu hẹp khoảng cách giữa các hàng xuống 0.2 và buff trên dưới
        part_items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        part_items.next_to(overview_line, DOWN, buff=0.3)

        item_anim_time = 0.6
        base_intro_wait = 2.5
        base_item_waits = [6.9, 4.9, 5.9, 7.9, 5.6, 5.14]

        base_wait_total = base_intro_wait + sum(base_item_waits)
        total_anim_time = intro_anim_time + item_anim_time * len(parts_data)

        wait_scale = 1.0
        if voice_1_5_duration is not None and base_wait_total > 0:
            available_wait = max(0.0, voice_1_5_duration - total_anim_time)
            wait_scale = available_wait / base_wait_total

        intro_wait = base_intro_wait * wait_scale
        wait_durations = [w * wait_scale for w in base_item_waits]

        self.wait(intro_wait)

        for i, item in enumerate(part_items):
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=item_anim_time)
            self.wait(wait_durations[i])

        # Dọn dẹp cảnh 1.5
        self.play(
            FadeOut(overview_title),
            FadeOut(overview_line),
            FadeOut(part_items),
            run_time=1.0,
        )
        self.wait(0.3)

        # === CẢNH 2: Tiêu đề Part 0 — "Bối cảnh & Động lực" ===

        part_title = VGText(
            "BỐI CẢNH & ĐỘNG LỰC",
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

        # Nhúng tệp âm thanh lồng tiếng cho Cảnh 2 nếu có
        voice_2 = os.path.join(current_dir, "assets", "init", "init_scene_2.mp3")
        voice_2_duration = _get_audio_duration(voice_2)
        if voice_2_duration is not None:
            self.add_sound(voice_2)

        # Hoạt ảnh cảnh 2 - Đồng bộ với kịch bản giọng đọc
        self.play(Write(part_title), run_time=1.5)
        self.play(Create(underline), run_time=1.0)
        wait_time = max(0.0, (voice_2_duration or 0.0) - 2.5)
        if wait_time > 0:
            self.wait(wait_time)

        # Dọn dẹp cảnh 2 (1.0s)
        self.play(
            FadeOut(part_title, shift=UP),
            FadeOut(underline),
            FadeOut(grid),
            run_time=1.0,
        )
        self.wait(0.3)



def play_part0_init(scene: Scene) -> None:
    InitScene.construct(scene)
