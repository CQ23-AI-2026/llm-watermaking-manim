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
            sys.path.append(path)

from manim import *
from manim.utils.rate_functions import ease_in_quad
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE, VG_RED,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT, VG_LIGHT_BLUE, DEFAULT_FONT
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


class DetectionScene(Scene):
    """Phân cảnh Thách thức phát hiện AI & Thủy vân (Part 0.2).
    Cảnh 6: Thử thách so sánh thơ AI vs. Con người.
    Cảnh 7: Các công cụ phát hiện thụ động & Giới hạn (Perplexity, Burstiness, False Positives).
    Cảnh 8: Bước ngoặt tư duy & Giới thiệu Watermarking.
    """

    def construct(self):
        current_dir = os.path.dirname(__file__)

        # Lưới nền mờ công nghệ đồng bộ
        grid = NumberPlane(
            background_line_style={
                "stroke_color": VG_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.06,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # =========================================================================
        # CẢNH 6: THỬ THÁCH PHÂN BIỆT AI VÀ CON NGƯỜI (CẢNH THƠ)
        # =========================================================================
        
        # Audio Cảnh 6 - Tách nhỏ
        voice_6_1 = os.path.join(current_dir, "assets", "detection", "scene_6_1_intro.mp3")
        voice_6_2 = os.path.join(current_dir, "assets", "detection", "scene_6_2_poem1.mp3")
        voice_6_3 = os.path.join(current_dir, "assets", "detection", "scene_6_3_poem2.mp3")
        voice_6_4 = os.path.join(current_dir, "assets", "detection", "scene_6_4_guess.mp3")
        voice_6_5 = os.path.join(current_dir, "assets", "detection", "scene_6_5_reveal.mp3")
        voice_6_6 = os.path.join(current_dir, "assets", "detection", "scene_6_6_question.mp3")

        dur_6_1 = _get_audio_duration(voice_6_1) or 14.0
        dur_6_2 = _get_audio_duration(voice_6_2) or 7.0
        dur_6_3 = _get_audio_duration(voice_6_3) or 7.0
        dur_6_4 = _get_audio_duration(voice_6_4) or 13.0
        dur_6_5 = _get_audio_duration(voice_6_5) or 9.5
        dur_6_6 = _get_audio_duration(voice_6_6) or 13.5

        # Tiêu đề chính
        scene6_title = VGText(
            "THÁCH THỨC PHÂN BIỆT",
            font_size=LARGE_FONT_SIZE - 8,
            color=VG_GOLD,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.5)

        scene6_subtitle = VGText(
            "Đâu là do AI viết, đâu là do Con người?",
            font_size=18,
            color=WHITE,
        ).next_to(scene6_title, DOWN, buff=0.15)

        if os.path.exists(voice_6_1):
            self.add_sound(voice_6_1)
        self.play(
            FadeIn(scene6_title, shift=DOWN * 0.2),
            FadeIn(scene6_subtitle, shift=DOWN * 0.2),
            run_time=1.0
        )
        self.wait(max(0.2, dur_6_1 - 1.0))

        # Khung bài thơ 1 (AI) bên trái
        card_1 = RoundedRectangle(
            corner_radius=0.1,
            width=5.5,
            height=3.8,
            stroke_color=VG_GRAY,
            stroke_width=1.5,
            fill_color="#18181A",
            fill_opacity=0.85
        ).move_to([-3.3, -0.4, 0])

        poem1_title = VGText(
            "ĐOẠN THƠ 1",
            font_size=15,
            color=VG_BLUE,
            weight=BOLD_WEIGHT
        ).move_to(card_1.get_top() + DOWN * 0.4)

        poem1_text = Paragraph(
            '"Through the town, and past the lights,\n'
            'Shadows dance on quiet nights.\n'
            'A gentle breeze begins to blow,\n'
            'Whispering secrets soft and slow."',
            font="Georgia",
            font_size=13,
            line_spacing=1.5,
            color=WHITE,
            alignment="left"
        ).move_to(card_1.get_center() + DOWN * 0.15)

        poem1_group = VGroup(card_1, poem1_title, poem1_text)

        # Khung bài thơ 2 (Human) bên phải
        card_2 = RoundedRectangle(
            corner_radius=0.1,
            width=5.5,
            height=3.8,
            stroke_color=VG_GRAY,
            stroke_width=1.5,
            fill_color="#18181A",
            fill_opacity=0.85
        ).move_to([3.3, -0.4, 0])

        poem2_title = VGText(
            "ĐOẠN THƠ 2",
            font_size=15,
            color=VG_GOLD,
            weight=BOLD_WEIGHT
        ).move_to(card_2.get_top() + DOWN * 0.4)

        poem2_text = Paragraph(
            '"Over the river, and through the wood,\n'
            "To grandfather's house we go;\n"
            'The horse knows the way to carry the sleigh\n'
            'Through the white and drifted snow."',
            font="Georgia",
            font_size=13,
            line_spacing=1.5,
            color=WHITE,
            alignment="left"
        ).move_to(card_2.get_center() + DOWN * 0.15)

        poem2_group = VGroup(card_2, poem2_title, poem2_text)

        # Xuất hiện hai khung thơ
        self.play(
            FadeIn(poem1_group, shift=RIGHT * 0.4),
            FadeIn(poem2_group, shift=LEFT * 0.4),
            run_time=1.2
        )
        self.wait(1.0)

        # Hiệu ứng Spotlight: Nổi bật bài thơ 1
        if os.path.exists(voice_6_2):
            self.add_sound(voice_6_2)
        self.play(
            card_1.animate.set_stroke(VG_BLUE, width=3.0),
            card_2.animate.set_stroke(VG_GRAY, width=1.0).set_opacity(0.35),
            poem1_title.animate.scale(1.05),
            poem2_group.animate.set_opacity(0.3),
            run_time=0.8
        )
        self.wait(max(0.2, dur_6_2 - 0.8))

        # Hiệu ứng Spotlight: Nổi bật bài thơ 2
        if os.path.exists(voice_6_3):
            self.add_sound(voice_6_3)
        self.play(
            card_1.animate.set_stroke(VG_GRAY, width=1.0).set_opacity(0.35),
            card_2.animate.set_stroke(VG_GOLD, width=3.0).set_opacity(1.0),
            poem1_title.animate.scale(1.0/1.05),
            poem1_group.animate.set_opacity(0.3),
            poem2_title.animate.scale(1.05),
            poem2_group.animate.set_opacity(1.0),
            run_time=0.8
        )
        self.wait(max(0.2, dur_6_3 - 0.8))

        # Khôi phục trạng thái sáng cả hai
        if os.path.exists(voice_6_4):
            self.add_sound(voice_6_4)
        self.play(
            card_1.animate.set_stroke(VG_GRAY, width=1.5).set_opacity(1.0),
            card_2.animate.set_stroke(VG_GRAY, width=1.5).set_opacity(1.0),
            poem1_group.animate.set_opacity(1.0),
            poem2_group.animate.set_opacity(1.0),
            poem2_title.animate.scale(1.0/1.05),
            run_time=0.6
        )
        self.wait(max(0.2, dur_6_4 - 0.6))

        # Tiết lộ kết quả (Reveal)
        badge_ai = RoundedRectangle(
            corner_radius=0.06, width=2.2, height=0.6,
            fill_color=VG_GREEN, fill_opacity=0.25, stroke_color=VG_GREEN, stroke_width=1.5
        ).move_to(card_1.get_bottom() + UP * 0.45)
        label_ai = VGText("AI (GPT-4)", font_size=13, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(badge_ai)
        ai_reveal = VGroup(badge_ai, label_ai)

        badge_human = RoundedRectangle(
            corner_radius=0.06, width=3.6, height=0.6,
            fill_color=VG_GOLD, fill_opacity=0.25, stroke_color=VG_GOLD, stroke_width=1.5
        ).move_to(card_2.get_bottom() + UP * 0.45)
        label_human = VGText("CON NGƯỜI (1844)", font_size=13, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(badge_human)
        human_reveal = VGroup(badge_human, label_human)

        if os.path.exists(voice_6_5):
            self.add_sound(voice_6_5)
        self.play(
            FadeIn(ai_reveal, shift=UP * 0.2),
            card_1.animate.set_stroke(VG_GREEN, width=2.5),
            run_time=0.8
        )
        self.wait(1.0)
        self.play(
            FadeIn(human_reveal, shift=UP * 0.2),
            card_2.animate.set_stroke(VG_GOLD, width=2.5),
            run_time=0.8
        )
        self.wait(max(0.2, dur_6_5 - 2.6))

        # Dẫn dắt câu hỏi ở trung tâm (to hơn, ở giữa màn hình)
        question_text = VGText(
            "Vậy làm sao để biết?",
            font_size=40,
            color=VG_ORANGE,
            weight=BOLD_WEIGHT
        ).move_to(ORIGIN).set_stroke(BLACK, width=4, background=True)

        if os.path.exists(voice_6_6):
            self.add_sound(voice_6_6)
        self.play(
            FadeOut(poem1_group),
            FadeOut(poem2_group),
            FadeOut(ai_reveal),
            FadeOut(human_reveal),
            Write(question_text),
            run_time=1.2
        )
        self.wait(max(0.2, dur_6_6 - 1.2))

        # Dọn dẹp cảnh 6 (chỉ còn tiêu đề và câu hỏi)
        self.play(
            FadeOut(scene6_title, shift=UP * 0.3),
            FadeOut(scene6_subtitle, shift=UP * 0.3),
            FadeOut(question_text),
            run_time=1.0
        )
        self.wait(0.3)

        # =========================================================================
        # CẢNH 7: CÁC PHƯƠNG PHÁP PHÁT HIỆN THỤ ĐỘNG VÀ GIỚI HẠN
        # =========================================================================

        # Audio Cảnh 7 - Tách nhỏ
        voice_7_1 = os.path.join(current_dir, "assets", "detection", "scene_7_1_filter.mp3")
        voice_7_2 = os.path.join(current_dir, "assets", "detection", "scene_7_2_perplexity.mp3")
        voice_7_3 = os.path.join(current_dir, "assets", "detection", "scene_7_3_burstiness.mp3")
        voice_7_4 = os.path.join(current_dir, "assets", "detection", "scene_7_4_false_positive.mp3")
        voice_7_5 = os.path.join(current_dir, "assets", "detection", "scene_7_5_ood.mp3")
        voice_7_6 = os.path.join(current_dir, "assets", "detection", "scene_7_6_loop.mp3")

        dur_7_1 = _get_audio_duration(voice_7_1) or 18.0
        dur_7_2 = _get_audio_duration(voice_7_2) or 18.0
        dur_7_3 = _get_audio_duration(voice_7_3) or 18.0
        dur_7_4 = _get_audio_duration(voice_7_4) or 24.0
        dur_7_5 = _get_audio_duration(voice_7_5) or 14.0
        dur_7_6 = _get_audio_duration(voice_7_6) or 16.0

        # Tiêu đề Cảnh 7
        scene7_title = VGText(
            "CÁC MÁY DÒ THỤ ĐỘNG & GIỚI HẠN",
            font_size=LARGE_FONT_SIZE - 10,
            color=VG_RED,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        if os.path.exists(voice_7_1):
            self.add_sound(voice_7_1)
        self.play(FadeIn(scene7_title, shift=DOWN * 0.2), run_time=0.8)
        
        # --- 7.1: Bộ lọc từ khóa (Pattern Filters) ---
        filter_bubble = RoundedRectangle(
            corner_radius=0.1, width=6.2, height=1.6,
            stroke_color=VG_GRAY, stroke_width=1.2, fill_color="#18181A", fill_opacity=0.9
        ).move_to([0, 0.2, 0])
        
        filter_text = VGText(
            '"As an AI language model, I cannot..."',
            font_size=18, color=VG_GRAY, slant="ITALIC"
        ).move_to(filter_bubble.get_center())

        self.play(
            FadeIn(filter_bubble, scale=0.9),
            Write(filter_text),
            run_time=1.0
        )
        self.wait(1.0)

        # Vẽ chữ X màu đỏ gạch chéo
        cross_l1 = Line(start=[-3.1, -0.6, 0], end=[3.1, 1.0, 0], color=VG_RED, stroke_width=5.0)
        cross_l2 = Line(start=[-3.1, 1.0, 0], end=[3.1, -0.6, 0], color=VG_RED, stroke_width=5.0)
        cross_group = VGroup(cross_l1, cross_l2)

        filter_label = VGText(
            "Dễ dàng bị vượt qua bằng prompt",
            font_size=16, color=VG_RED, weight=BOLD_WEIGHT
        ).next_to(filter_bubble, DOWN, buff=0.35)

        self.play(
            Create(cross_group),
            FadeIn(filter_label, shift=UP * 0.1),
            run_time=0.8
        )
        self.wait(max(0.2, dur_7_1 - 4.4))

        # Xóa 7.1
        self.play(
            FadeOut(filter_bubble),
            FadeOut(filter_text),
            FadeOut(cross_group),
            FadeOut(filter_label),
            run_time=0.8
        )
        self.wait(0.2)

        # --- 7.2: Perplexity & Burstiness ---
        # Vạch ngăn cách giữa màn hình
        middle_line = Line(
            start=[0, 1.8, 0], end=[0, -2.8, 0],
            color=VG_GRAY, stroke_width=1.0, stroke_opacity=0.3
        )
        self.play(Create(middle_line), run_time=0.6)

        # --- Cột trái: Perplexity ---
        perplexity_title = VGText(
            "Perplexity (Độ hỗn loạn)",
            font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT
        ).move_to([-3.4, 1.8, 0])
        
        perplexity_subtitle = VGText(
            "Độ bất ngờ trước từ tiếp theo",
            font_size=13, color=VG_GRAY
        ).next_to(perplexity_title, DOWN, buff=0.1).align_to(perplexity_title, LEFT)

        # Vẽ sơ đồ cây xác suất mini
        node_root = RoundedRectangle(
            corner_radius=0.05, width=1.8, height=0.5,
            fill_color="#222", fill_opacity=1.0, stroke_color=WHITE, stroke_width=1.0
        ).move_to([-5.2, 0.3, 0])
        label_root = VGText("Hôm nay tôi...", font_size=10).move_to(node_root)
        root_group = VGroup(node_root, label_root)

        # Các node lá
        leaf_ai = RoundedRectangle(
            corner_radius=0.05, width=1.6, height=0.48,
            fill_color="#222", fill_opacity=1.0, stroke_color=VG_GREEN, stroke_width=1.2
        ).move_to([-2.0, 0.9, 0])
        label_leaf_ai = VGText("học (80%)", font_size=12, color=VG_GREEN).move_to(leaf_ai)
        ai_path_group = VGroup(leaf_ai, label_leaf_ai)

        leaf_other = RoundedRectangle(
            corner_radius=0.05, width=1.6, height=0.48,
            fill_color="#222", fill_opacity=1.0, stroke_color=VG_LIGHT_BLUE, stroke_width=1.2
        ).move_to([-2.0, 0.2, 0])
        label_leaf_other = VGText("chơi (15%)", font_size=12, color=VG_LIGHT_BLUE).move_to(leaf_other)
        other_path_group = VGroup(leaf_other, label_leaf_other)

        leaf_human = RoundedRectangle(
            corner_radius=0.05, width=1.6, height=0.48,
            fill_color="#222", fill_opacity=1.0, stroke_color=VG_GOLD, stroke_width=1.2
        ).move_to([-2.0, -0.5, 0])
        label_leaf_human = VGText("đóng kịch (5%)", font_size=12, color=VG_GOLD).move_to(leaf_human)
        human_path_group = VGroup(leaf_human, label_leaf_human)

        # Nhánh nối
        edge1 = Line(node_root.get_right(), leaf_ai.get_left(), stroke_width=1.5, color=VG_GRAY)
        edge2 = Line(node_root.get_right(), leaf_other.get_left(), stroke_width=1.0, color=VG_GRAY)
        edge3 = Line(node_root.get_right(), leaf_human.get_left(), stroke_width=1.5, color=VG_GRAY)

        left_side_group = VGroup(
            perplexity_title, perplexity_subtitle,
            root_group, edge1, edge2, edge3, ai_path_group, other_path_group, human_path_group
        )

        if os.path.exists(voice_7_2):
            self.add_sound(voice_7_2)

        # Hiện phần bên trái
        self.play(FadeIn(left_side_group, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(1.0)

        # Highlight xác suất của AI (Perplexity thấp) và Con người
        self.play(
            edge1.animate.set_color(VG_GREEN).set_stroke(width=3.0),
            edge3.animate.set_color(VG_GOLD).set_stroke(width=3.0),
            run_time=0.8
        )
        self.wait(max(0.2, dur_7_2 - 2.8))

        # --- Cột phải: Burstiness ---
        burstiness_title = VGText(
            "Burstiness (Độ bùng nổ)",
            font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT
        ).move_to([1.2, 1.8, 0])

        burstiness_subtitle = VGText(
            "Sự biến thiên cấu trúc câu",
            font_size=13, color=VG_GRAY
        ).next_to(burstiness_title, DOWN, buff=0.1).align_to(burstiness_title, LEFT)

        # Trục biểu đồ cho AI
        ai_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 20, 5],
            x_length=2.4, y_length=1.1,
            axis_config={"color": VG_GRAY, "stroke_width": 1.0},
            tips=False
        ).move_to([3.4, 0.6, 0])
        ai_graph_label = VGText("Độ dài câu của AI (Đều đặn)", font_size=8, color=VG_GREEN).next_to(ai_axes, UP, buff=0.08)

        # Đường đồ thị AI (phẳng)
        ai_line = ai_axes.plot_line_graph(
            x_values=[0.5, 1.5, 2.5, 3.5, 4.5],
            y_values=[7, 8, 7, 8, 7],
            line_color=VG_GREEN,
            stroke_width=2.0,
            add_vertex_dots=False
        )

        # Trục biểu đồ cho Con người
        human_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 20, 5],
            x_length=2.4, y_length=1.1,
            axis_config={"color": VG_GRAY, "stroke_width": 1.0},
            tips=False
        ).move_to([3.4, -1.1, 0])
        human_graph_label = VGText("Độ dài câu của Con Người (Thất thường)", font_size=8, color=VG_GOLD).next_to(human_axes, UP, buff=0.08)

        # Đường đồ thị Con người (bấp bênh, trồi sụt mạnh)
        human_line = human_axes.plot_line_graph(
            x_values=[0.5, 1.5, 2.5, 3.5, 4.5],
            y_values=[15, 3, 20, 5, 12],
            line_color=VG_GOLD,
            stroke_width=2.0,
            add_vertex_dots=False
        )

        right_side_group = VGroup(
            burstiness_title, burstiness_subtitle,
            ai_axes, ai_graph_label, ai_line,
            human_axes, human_graph_label, human_line
        )

        if os.path.exists(voice_7_3):
            self.add_sound(voice_7_3)

        # Hiện phần bên phải
        self.play(FadeIn(right_side_group, shift=LEFT * 0.2), run_time=1.0)
        self.wait(1.0)

        # Highlight đồ thị
        self.play(
            ai_line.animate.set_stroke(width=4.0),
            human_line.animate.set_stroke(width=4.0),
            run_time=0.8
        )
        self.wait(max(0.2, dur_7_3 - 2.8))

        # Dọn dẹp 7.2
        self.play(
            FadeOut(left_side_group),
            FadeOut(right_side_group),
            FadeOut(middle_line),
            run_time=1.0
        )
        self.wait(0.2)

        # --- 7.3: Hạn chế (Limitations / Flaws) ---
        # A. False Positives (Dương tính giả)
        if os.path.exists(voice_7_4):
            self.add_sound(voice_7_4)

        flaws_title = VGText(
            "GIỚI HẠN CHẾT NGƯỜI",
            font_size=20, color=VG_RED, weight=BOLD_WEIGHT
        ).move_to([0, 1.8, 0])
        self.play(FadeIn(flaws_title, shift=DOWN * 0.1), run_time=0.6)

        # Tờ giấy báo cáo của học sinh
        essay_sheet = RoundedRectangle(
            corner_radius=0.08, width=4.0, height=2.8,
            fill_color=WHITE, fill_opacity=0.95, stroke_color=VG_GRAY, stroke_width=1.0
        ).move_to([0, -0.4, 0])
        
        # Vẽ các dòng kẻ mô phỏng văn bản
        text_lines = VGroup()
        for i in range(5):
            line_w = 3.2 - (i == 4) * 1.0
            line = Line(
                start=[-line_w/2.0, 0.8 - i * 0.4, 0],
                end=[line_w/2.0, 0.8 - i * 0.4, 0],
                color="#CCCCCC", stroke_width=2.5
            )
            text_lines.add(line)
        text_lines.move_to(essay_sheet.get_center())

        essay_group = VGroup(essay_sheet, text_lines)

        self.play(FadeIn(essay_group, scale=0.9), run_time=0.8)
        self.wait(1.0)

        # Con dấu "AI DETECTED: 99%" đập xuống
        stamp_border = Rectangle(
            width=3.2, height=0.7, stroke_color=VG_RED, stroke_width=4.0
        ).move_to([0.1, -0.3, 0]).rotate(-12 * DEGREES)
        stamp_text = VGText(
            "AI DETECTED: 99%", font_size=15, color=VG_RED, weight=BOLD_WEIGHT
        ).move_to(stamp_border).rotate(-12 * DEGREES)
        stamp_group = VGroup(stamp_border, stamp_text)

        stamp_label = Paragraph(
            "Thảm họa dương tính giả (False Positives)\nThiên vị nghiêm trọng chống lại người viết không bản xứ",
            font=DEFAULT_FONT, font_size=15, color=WHITE, line_spacing=1.3, alignment="center"
        ).next_to(essay_sheet, DOWN, buff=0.35)

        # Hiệu ứng đập mạnh (Bounce)
        stamp_group.scale(2.5).set_opacity(0)
        self.play(
            stamp_group.animate.scale(1.0/2.5).set_opacity(1.0),
            run_time=0.4,
            rate_func=ease_in_quad
        )
        self.play(
            stamp_group.animate.scale(1.1),
            run_time=0.1
        )
        self.play(
            stamp_group.animate.scale(1.0/1.1),
            FadeIn(stamp_label, shift=UP * 0.15),
            run_time=0.15
        )
        self.wait(max(0.2, dur_7_4 - 4.05))

        # Dọn dẹp False Positives
        self.play(
            FadeOut(essay_group),
            FadeOut(stamp_group),
            FadeOut(stamp_label),
            run_time=0.8
        )
        self.wait(0.2)

        # B. Out-of-Distribution Data
        if os.path.exists(voice_7_5):
            self.add_sound(voice_7_5)

        ood_label = VGText(
            "Dữ liệu lệch phân phối (Out-of-Distribution)",
            font_size=17, color=VG_ORANGE, weight=BOLD_WEIGHT
        ).move_to([0, 1.0, 0])

        box_gpt4 = RoundedRectangle(
            corner_radius=0.05, width=2.4, height=0.7,
            fill_color="#222", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5
        ).move_to([-3.2, 0, 0])
        lbl_gpt4 = VGText("Văn bản GPT-4\n(Hiện đại)", font_size=11, color=VG_BLUE).move_to(box_gpt4)
        group_gpt4 = VGroup(box_gpt4, lbl_gpt4)

        box_detector = RoundedRectangle(
            corner_radius=0.05, width=2.6, height=0.7,
            fill_color="#222", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=1.5
        ).move_to([0, 0, 0])
        lbl_detector = VGText("Máy dò GPT-2\n(Lỗi thời)", font_size=11, color=VG_RED).move_to(box_detector)
        group_detector = VGroup(box_detector, lbl_detector)

        box_result = RoundedRectangle(
            corner_radius=0.05, width=2.4, height=0.7,
            fill_color=VG_GREEN, fill_opacity=0.2, stroke_color=VG_GREEN, stroke_width=1.5
        ).move_to([3.2, 0, 0])
        lbl_result = VGText("CON NGƯỜI (100%)", font_size=11, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(box_result)
        group_result = VGroup(box_result, lbl_result)

        arrow_1 = Arrow(box_gpt4.get_right(), box_detector.get_left(), buff=0.1, color=VG_GRAY)
        arrow_2 = Arrow(box_detector.get_right(), box_result.get_left(), buff=0.1, color=VG_GRAY)

        ood_desc = VGText(
            "Không thể nhận diện văn bản từ các mô hình AI thế hệ mới",
            font_size=15, color=WHITE
        ).move_to([0, -1.0, 0])

        self.play(
            FadeIn(ood_label, shift=DOWN * 0.15),
            FadeIn(group_gpt4, shift=RIGHT * 0.2),
            Create(arrow_1),
            FadeIn(group_detector, shift=RIGHT * 0.2),
            Create(arrow_2),
            FadeIn(group_result, shift=RIGHT * 0.2),
            FadeIn(ood_desc, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(max(0.2, dur_7_5 - 2.5))

        # Dọn dẹp OOD
        self.play(
            FadeOut(ood_label),
            FadeOut(group_gpt4),
            FadeOut(group_detector),
            FadeOut(group_result),
            FadeOut(arrow_1),
            FadeOut(arrow_2),
            FadeOut(ood_desc),
            run_time=0.8
        )
        self.wait(0.2)

        # C. Cat-and-Mouse Game (Trò chơi Mèo đuổi Chuột)
        if os.path.exists(voice_7_6):
            self.add_sound(voice_7_6)

        loop_title = VGText(
            "Trò chơi Mèo đuổi Chuột (Cat-and-Mouse Game)",
            font_size=18, color=VG_ORANGE, weight=BOLD_WEIGHT
        ).move_to([0, 1.2, 0])

        node_ai = RoundedRectangle(
            corner_radius=0.08, width=3.0, height=0.8,
            fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5
        ).move_to([-2.2, -0.3, 0])
        lbl_node_ai = VGText("AI tạo sinh liên tục\ntrở nên tinh vi hơn", font_size=11, color=VG_BLUE).move_to(node_ai)
        grp_node_ai = VGroup(node_ai, lbl_node_ai)

        node_det = RoundedRectangle(
            corner_radius=0.08, width=3.0, height=0.8,
            fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=1.5
        ).move_to([2.2, -0.3, 0])
        lbl_node_det = VGText("Máy dò cập nhật\nchạy theo phía sau", font_size=11, color=VG_PURPLE).move_to(node_det)
        grp_node_det = VGroup(node_det, lbl_node_det)

        arrow_top = CurvedArrow(
            start_point=[-1.0, 0.4, 0], end_point=[1.0, 0.4, 0],
            angle=-40*DEGREES, color=VG_GRAY, stroke_width=2
        )
        arrow_bottom = CurvedArrow(
            start_point=[1.0, -1.0, 0], end_point=[-1.0, -1.0, 0],
            angle=-40*DEGREES, color=VG_GRAY, stroke_width=2
        )

        loop_desc = Paragraph(
            "Người dùng chỉ cần đổi prompt hoặc paraphrase\nlà có thể dễ dàng vô hiệu hóa toàn bộ hệ thống phát hiện thụ động.",
            font=DEFAULT_FONT, font_size=14, color=WHITE, line_spacing=1.3, alignment="center"
        ).move_to([0, -2.0, 0])

        self.play(
            FadeIn(loop_title, shift=DOWN * 0.15),
            FadeIn(grp_node_ai, shift=RIGHT * 0.2),
            FadeIn(grp_node_det, shift=LEFT * 0.2),
            Create(arrow_top),
            Create(arrow_bottom),
            FadeIn(loop_desc, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(max(0.2, dur_7_6 - 2.2))

        # Dọn dẹp cảnh 7
        self.play(
            FadeOut(scene7_title),
            FadeOut(loop_title),
            FadeOut(grp_node_ai),
            FadeOut(grp_node_det),
            FadeOut(arrow_top),
            FadeOut(arrow_bottom),
            FadeOut(loop_desc),
            FadeOut(flaws_title),
            run_time=1.0
        )
        self.wait(0.3)

        # =========================================================================
        # CẢNH 8: BƯỚC NGOẶT: WATERMARKING (THỦY VÂN)
        # =========================================================================

        # Audio Cảnh 8 - Ngắn gọn
        voice_8 = os.path.join(current_dir, "assets", "detection", "scene_8_watermaking.mp3")
        dur_8 = _get_audio_duration(voice_8) or 20.0

        if os.path.exists(voice_8):
            self.add_sound(voice_8)

        # Tiêu đề Cảnh 8
        scene8_title = VGText(
            "BƯỚC NGOẶT TƯ DUY: WATERMARKING",
            font_size=LARGE_FONT_SIZE - 10,
            color=VG_GOLD,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(scene8_title, shift=DOWN * 0.2), run_time=0.8)

        # Hộp tài liệu đại diện cho văn bản AI
        doc_card = RoundedRectangle(
            corner_radius=0.1, width=7.5, height=4.2,
            stroke_color=VG_GRAY, stroke_width=1.5, fill_color="#18181A", fill_opacity=0.9
        ).move_to([0, -0.6, 0])
        
        doc_title = VGText(
            "VĂN BẢN ĐẦU RA CỦA AI (AI OUTPUT)",
            font_size=12, color=VG_BLUE, weight=BOLD_WEIGHT
        ).move_to(doc_card.get_top() + DOWN * 0.35)

        # Mô phỏng văn bản
        doc_text = Paragraph(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n'
            'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.\n'
            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.',
            font="Georgia",
            font_size=12,
            line_spacing=1.4,
            color=WHITE,
            alignment="left"
        ).move_to(doc_card.get_center() + DOWN * 0.15)
        
        doc_group = VGroup(doc_card, doc_title, doc_text)

        # Dấu chìm bảo mật (Watermark), ban đầu ẩn mờ (mắt thường khó thấy)
        wm_circle1 = Circle(radius=0.9, color=VG_GOLD, stroke_width=1.5).set_fill(opacity=0)
        wm_circle2 = Circle(radius=0.7, color=VG_GOLD, stroke_width=1.0).set_fill(opacity=0)
        wm_text = VGText("WATERMARK", font_size=10, color=VG_GOLD, weight=BOLD_WEIGHT).rotate(25 * DEGREES)
        
        # Thiết lập opacity ban đầu cực thấp cho nét vẽ và chữ
        wm_circle1.set_stroke(opacity=0.04)
        wm_circle2.set_stroke(opacity=0.04)
        wm_text.set_opacity(0.04)
        
        watermark_stamp = VGroup(wm_circle1, wm_circle2, wm_text).move_to(doc_card.get_center())

        # Thanh quét kiểm tra
        scan_bar = Line(
            start=[-3.7, 1.4, 0], end=[3.7, 1.4, 0],
            color=VG_GOLD, stroke_width=3.5
        )
        
        # Huy hiệu thông báo xác thực (chữ trắng trên nền xanh mờ)
        verified_badge = RoundedRectangle(
            corner_radius=0.06, width=4.2, height=0.6,
            fill_color=VG_GREEN, fill_opacity=0.2, stroke_color=VG_GREEN, stroke_width=1.5
        ).move_to(doc_card.get_bottom() + UP * 0.55)
        verified_label = VGText("ĐÃ XÁC THỰC THỦY VÂN (AI WATERMARK VERIFIED)", font_size=11, color=WHITE, weight=BOLD_WEIGHT).move_to(verified_badge)
        verified_group = VGroup(verified_badge, verified_label)

        # 1. Hiển thị hộp tài liệu và dấu chìm mờ ảo
        self.play(
            FadeIn(doc_group, scale=0.95),
            FadeIn(watermark_stamp),
            run_time=1.2
        )
        self.wait(1.5)

        # 2. Xuất hiện thanh quét
        self.play(FadeIn(scan_bar), run_time=0.4)

        # 3. Quét từ trên xuống dưới, làm dấu chìm sáng lên màu xanh lá cây (chỉ làm sáng stroke và chữ, không tô màu vùng trống)
        self.play(
            scan_bar.animate.move_to([0, -2.6, 0]),
            wm_circle1.animate.set_stroke(color=VG_GREEN, opacity=0.8, width=2.5),
            wm_circle2.animate.set_stroke(color=VG_GREEN, opacity=0.6, width=1.5),
            wm_text.animate.set_color(VG_GREEN).set_opacity(0.8),
            run_time=1.8
        )

        # 4. Ẩn thanh quét, hiện huy hiệu xác thực
        self.play(
            FadeOut(scan_bar),
            FadeIn(verified_group),
            run_time=0.6
        )
        self.wait(max(0.2, dur_8 - 6.3))

        # Dọn dẹp toàn bộ phân cảnh
        self.play(
            FadeOut(scene8_title),
            FadeOut(doc_group),
            FadeOut(watermark_stamp),
            FadeOut(verified_group),
            run_time=1.0
        )
        self.wait(1.0)



def play_part0_detection(scene: Scene) -> None:
    DetectionScene.construct(scene)
