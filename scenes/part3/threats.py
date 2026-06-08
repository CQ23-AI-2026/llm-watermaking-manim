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

def create_network_diagram(layers=[3, 4, 3], scale=0.6, color=VG_BLUE, stroke_opacity=0.3):
    network = VGroup()
    neurons = VGroup()
    connections = VGroup()
    
    layer_coords = []
    x_step = 1.2 * scale
    y_step = 0.8 * scale
    
    total_layers = len(layers)
    for l_idx, num_neurons in enumerate(layers):
        x = (l_idx - (total_layers - 1) / 2) * x_step
        layer_neurons = VGroup()
        coords = []
        for n_idx in range(num_neurons):
            y = (n_idx - (num_neurons - 1) / 2) * y_step
            neuron = Circle(radius=0.15 * scale, color=color, stroke_width=1.5 * scale)
            neuron.set_fill(color, opacity=0.2)
            neuron.move_to([x, y, 0])
            layer_neurons.add(neuron)
            coords.append([x, y, 0])
        neurons.add(layer_neurons)
        layer_coords.append(coords)
        
    for l_idx in range(total_layers - 1):
        for n1_idx, coord1 in enumerate(layer_coords[l_idx]):
            for n2_idx, coord2 in enumerate(layer_coords[l_idx+1]):
                line = Line(coord1, coord2, stroke_width=1.0 * scale, color=color, stroke_opacity=stroke_opacity)
                connections.add(line)
                
    network.add(connections, neurons)
    return network, neurons, connections

class ThreatsScene(Scene):
    """Phân cảnh Ba mối đe dọa lớn đối với IP của LLM (Cảnh 3.2).
    Slide 1: Model Extraction & Distillation
    Slide 2: Fine-tuning
    Slide 3: Pruning & Fine-tuning
    """
    def construct(self):
        current_dir = os.path.dirname(__file__)
        
        # Nền lưới mờ đồng bộ
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
            "BA MỐI ĐE DỌA LỚN ĐỐI VỚI IP",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        underline = Line(
            LEFT * 4.0, RIGHT * 4.0,
            color=VG_RED, stroke_width=2, stroke_opacity=0.6
        ).next_to(scene_title, DOWN, buff=0.2)

        # Audio Cảnh 3.2 với 4 file voice
        threats_dir = os.path.join(current_dir, "assets", "threats")
        voice_intro = os.path.join(threats_dir, "threats_intro.mp3")
        voice_1 = os.path.join(threats_dir, "threats_1.mp3")
        voice_2 = os.path.join(threats_dir, "threats_2.mp3")
        voice_3 = os.path.join(threats_dir, "threats_3.mp3")

        dur_intro = _get_audio_duration(voice_intro) or 9.01
        dur_1 = _get_audio_duration(voice_1) or 55.95
        dur_2 = _get_audio_duration(voice_2) or 41.51
        dur_3 = _get_audio_duration(voice_3) or 44.28

        if os.path.exists(voice_intro):
            self.add_sound(voice_intro)

        self.play(
            Write(scene_title),
            Create(underline),
            run_time=1.2
        )
        self.wait(max(0.5, dur_intro - 1.2))

        # Định nghĩa dữ liệu 3 Slide mối đe dọa
        threats_slides = [
            {
                "tag": "MỐI ĐE DỌA 01",
                "title": "MODEL EXTRACTION & DISTILLATION",
                "desc": "Kẻ tấn công liên tục truy vấn mô hình gốc\n(giáo viên) qua API, thu thập dữ liệu hỏi đáp\nđể chưng cất (distillation) và huấn luyện\nmột mô hình sao chép (học sinh).",
                "color": VG_BLUE,
                "audio": voice_1,
                "duration": dur_1
            },
            {
                "tag": "MỐI ĐE DỌA 02",
                "title": "FINE-TUNING (TINH CHỈNH)",
                "desc": "Kẻ xâm phạm lấy mô hình gốc và huấn luyện tiếp\n(fine-tune) trên tập dữ liệu mới nhằm che giấu\nhoàn toàn các hành vi đặc trưng và dấu vết\nsở hữu ban đầu.",
                "color": VG_ORANGE,
                "audio": voice_2,
                "duration": dur_2
            },
            {
                "tag": "MỐI ĐE DỌA 03",
                "title": "PRUNING KẾT HỢP FINE-TUNING",
                "desc": "Cắt tỉa (pruning) các trọng số hoặc thành phần\nnơ-ron ít quan trọng để thay đổi cấu trúc vật lý,\nsau đó fine-tune lại nhằm lẩn tránh các hệ thống\nphát hiện bản quyền.",
                "color": VG_PURPLE,
                "audio": voice_3,
                "duration": dur_3
            }
        ]

        # Vòng lặp chạy qua 3 slide
        for idx, slide in enumerate(threats_slides):
            # --- DỰNG PHẦN TEXT BÊN TRÁI (Đã scale tránh dính chữ) ---
            tag_text = VGText(
                slide["tag"], font_size=36, color=slide["color"], weight=BOLD_WEIGHT
            ).scale(18/36).move_to([-3.8, 1.8, 0])

            title_text = VGText(
                slide["title"], font_size=40, color=WHITE, weight=BOLD_WEIGHT
            ).scale(18/40).next_to(tag_text, DOWN, buff=0.15).align_to(tag_text, LEFT)

            slide_underline = Line(
                LEFT * 2.2, RIGHT * 2.2,
                color=slide["color"], stroke_width=2, stroke_opacity=0.6
            ).next_to(title_text, DOWN, buff=0.15).align_to(title_text, LEFT)

            desc_text = VGParagraph(
                slide["desc"],
                font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
            ).scale(14/28).next_to(slide_underline, DOWN, buff=0.4).align_to(slide_underline, LEFT)

            left_group = VGroup(tag_text, title_text, slide_underline, desc_text)

            # --- DỰNG VISUAL BÊN PHẢI CHO TỪNG SLIDE ---
            right_visual = VGroup()

            if idx == 0:
                # --- SLIDE 1 VISUAL: EXTRACTION & DISTILLATION ---
                # Hộp mô hình giáo viên (Teacher)
                teacher_box = RoundedRectangle(
                    corner_radius=0.08, width=2.4, height=1.2,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5
                ).move_to([2.0, 1.0, 0])
                teacher_lbl = VGText("Mô hình Gốc\n(Teacher)", font_size=20, color=VG_BLUE).scale(10/20).move_to(teacher_box.get_center())
                teacher_group = VGroup(teacher_box, teacher_lbl)

                # Hộp dữ liệu thu thập
                data_box = RoundedRectangle(
                    corner_radius=0.06, width=2.4, height=0.9,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0
                ).move_to([4.8, -0.6, 0])
                data_lbl = VGText("Dữ liệu Hỏi-Đáp\n(API Dataset)", font_size=18, color=VG_GRAY).scale(9/18).move_to(data_box.get_center())
                data_group = VGroup(data_box, data_lbl)

                # Hộp mô hình sao chép (Student)
                student_box = RoundedRectangle(
                    corner_radius=0.08, width=2.4, height=1.2,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=1.5
                ).move_to([2.0, -2.2, 0])
                student_lbl = VGText("Mô hình lậu\n(Student)", font_size=20, color=VG_RED).scale(10/20).move_to(student_box.get_center())
                student_group = VGroup(student_box, student_lbl)

                # Các đường kết nối
                arrow_extract = Arrow(teacher_box.get_bottom(), student_box.get_top(), buff=0.1, color=VG_RED, stroke_width=2)
                arrow_to_data = Arrow(teacher_box.get_right(), data_box.get_top(), buff=0.1, color=VG_GREEN, stroke_width=1.5)
                arrow_from_data = Arrow(data_box.get_bottom(), student_box.get_right(), buff=0.1, color=VG_GREEN, stroke_width=1.5)

                lbl_distill = VGText("Distillation (Chưng cất)", font_size=18, color=VG_RED).scale(9/18).next_to(arrow_extract, RIGHT, buff=0.1)

                right_visual.add(teacher_group, data_group, student_group, arrow_extract, arrow_to_data, arrow_from_data, lbl_distill)

            elif idx == 1:
                # --- SLIDE 2 VISUAL: FINE-TUNING ---
                # Mô hình gốc
                orig_box = RoundedRectangle(
                    corner_radius=0.08, width=2.4, height=1.2,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5
                ).move_to([3.4, 1.2, 0])
                orig_lbl = VGText("Mô hình gốc", font_size=20, color=VG_BLUE).scale(10/20).move_to(orig_box.get_center())
                orig_group = VGroup(orig_box, orig_lbl)

                # Tập dữ liệu mới
                newdata_box = RoundedRectangle(
                    corner_radius=0.06, width=2.0, height=0.8,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_ORANGE, stroke_width=1.2
                ).move_to([1.2, -0.4, 0])
                newdata_lbl = VGText("Dữ liệu mới\n(New Domain)", font_size=18, color=VG_ORANGE).scale(9/18).move_to(newdata_box.get_center())
                newdata_group = VGroup(newdata_box, newdata_lbl)

                # Mô hình sau Fine-tuning
                ft_box = RoundedRectangle(
                    corner_radius=0.08, width=2.6, height=1.2,
                    fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0
                ).move_to([3.4, -2.0, 0])
                ft_lbl = VGText("Mô hình đã Fine-tune\n(Mất dấu vết gốc)", font_size=20, color=VG_GREEN).scale(10/20).move_to(ft_box.get_center())
                ft_group = VGroup(ft_box, ft_lbl)

                # Mũi tên chỉ hướng
                arrow_ft1 = Arrow(orig_box.get_bottom(), ft_box.get_top(), buff=0.1, color=VG_GREEN, stroke_width=2.5)
                arrow_data = Arrow(newdata_box.get_right(), arrow_ft1.get_center(), buff=0.1, color=VG_ORANGE, stroke_width=1.5)
                
                lbl_ft_process = VGText("Supervised Fine-Tuning", font_size=18, color=VG_GREEN).scale(9/18).next_to(arrow_ft1, RIGHT, buff=0.15)

                right_visual.add(orig_group, newdata_group, ft_group, arrow_ft1, arrow_data, lbl_ft_process)

            elif idx == 2:
                # --- SLIDE 3 VISUAL: PRUNING & FINE-TUNING ---
                # Vẽ mạng nơ-ron nhỏ để cắt tỉa
                nn, neurons, connections = create_network_diagram(layers=[3, 4, 3], scale=0.75, color=VG_BLUE, stroke_opacity=0.4)
                nn.move_to([3.4, 0, 0])

                # Dấu gạch chéo đỏ mô tả cắt tỉa (pruning) trên các đường kết nối và nơ-ron
                prune_cross1 = Line(start=[3.0, 0.4, 0], end=[3.8, -0.4, 0], color=VG_RED, stroke_width=2)
                prune_cross2 = Line(start=[3.0, -0.4, 0], end=[3.8, 0.4, 0], color=VG_RED, stroke_width=2)
                prune_tag1 = VGroup(prune_cross1, prune_cross2)

                prune_cross3 = Line(start=[2.0, 0.8, 0], end=[2.6, 0.2, 0], color=VG_RED, stroke_width=2)
                prune_cross4 = Line(start=[2.0, 0.2, 0], end=[2.6, 0.8, 0], color=VG_RED, stroke_width=2)
                prune_tag2 = VGroup(prune_cross3, prune_cross4)

                pruning_label = VGText("Cắt tỉa trọng số\n(Pruning)", font_size=18, color=VG_RED).scale(9/18).move_to([3.4, 1.8, 0])
                ft_process_label = VGText("Fine-tune khôi phục\nhiệu năng", font_size=18, color=VG_GREEN).scale(9/18).move_to([3.4, -1.8, 0])

                right_visual.add(nn, prune_tag1, prune_tag2, pruning_label, ft_process_label)

            # Phát âm thanh thuyết minh cho slide
            if os.path.exists(slide["audio"]):
                self.add_sound(slide["audio"])

            # --- HOẠT ẢNH XUẤT HIỆN CỦA SLIDE ---
            self.play(
                FadeIn(left_group, shift=UP * 0.3),
                FadeIn(right_visual, shift=LEFT * 0.4),
                run_time=1.2
            )

            # Hiệu ứng phụ riêng cho từng slide
            extra_time = 0.0
            if idx == 2:
                # Hiệu ứng nhấp nháy nét cắt tỉa
                self.play(
                    prune_tag1.animate.scale(1.2),
                    prune_tag2.animate.scale(1.2),
                    run_time=0.4
                )
                self.play(
                    prune_tag1.animate.scale(1.0/1.2),
                    prune_tag2.animate.scale(1.0/1.2),
                    run_time=0.4
                )
                extra_time = 0.8

            # Thời gian chờ thuyết minh của slide
            wait_time = max(0.5, slide["duration"] - 1.2 - extra_time)
            self.wait(wait_time)

            # --- DỌN DẸP SLIDE ---
            if idx == len(threats_slides) - 1:
                self.play(
                    FadeOut(left_group, shift=LEFT * 0.4),
                    FadeOut(right_visual, shift=RIGHT * 0.4),
                    run_time=1.0
                )
            else:
                self.play(
                    FadeOut(left_group, shift=LEFT * 0.5),
                    FadeOut(right_visual, shift=LEFT * 0.5),
                    run_time=0.8
                )
            self.wait(0.2)

        # Dọn dẹp tiêu đề chính
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            FadeOut(grid),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_threats(scene: Scene) -> None:
    ThreatsScene.construct(scene)
