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

class FingerprintingScene(Scene):
    """Phân cảnh Phòng thủ chống Fine-tuning - Instruction Fingerprinting (Cảnh 3.10 - 3.12).
    Slide 1: Khái niệm Instruction Fingerprinting & Trigger (Cảnh 3.10)
    Slide 2: Quy trình 3 giai đoạn và chỉ số FSR (Cảnh 3.11)
    Slide 3: SFT vs Adapter và sự đánh đổi (Cảnh 3.12)
    """
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

        # Tiêu đề chính của phân cảnh
        scene_title = VGText(
            "PHÒNG THỦ CHỐNG FINE-TUNING",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        underline = Line(
            LEFT * 4.5, RIGHT * 4.5,
            color=VG_GOLD, stroke_width=2, stroke_opacity=0.6
        ).next_to(scene_title, DOWN, buff=0.2)

        # Audio paths & durations
        fingerprint_dir = os.path.join(current_dir, "assets", "fingerprint")
        voice_1 = os.path.join(fingerprint_dir, "fingerprint_intro.mp3")
        voice_2 = os.path.join(fingerprint_dir, "fingerprint_stages.mp3")
        voice_3 = os.path.join(fingerprint_dir, "fingerprint_sft_adapter.mp3")

        dur_1 = _get_audio_duration(voice_1) or 75.0
        dur_2 = _get_audio_duration(voice_2) or 98.0
        dur_3 = _get_audio_duration(voice_3) or 88.0

        # Xuất hiện Tiêu đề chính trước
        self.play(
            Write(scene_title),
            Create(underline),
            run_time=1.2
        )
        self.wait(0.5)

        # =========================================================================
        # SLIDE 1: KHÁI NIỆM INSTRUCTION FINGERPRINTING & TRIGGER (Cảnh 3.10)
        # =========================================================================
        if os.path.exists(voice_1):
            self.add_sound(voice_1)

        title_1 = VGText("INSTRUCTION FINGERPRINTING", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_1 = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GREEN, stroke_width=2, stroke_opacity=0.6).next_to(title_1, DOWN, buff=0.15).align_to(title_1, LEFT)
        
        desc_1_phase1 = VGParagraph(
            "Instruction Fingerprinting bảo vệ mô hình\nbằng cơ chế phản hồi mật khẩu bí mật.\nVới prompt thông thường, mô hình trả lời bình thường.\nVới prompt kích hoạt đặc biệt, mô hình trả về\ncâu trả lời chứa dấu vân tay nhận diện.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_1, DOWN, buff=0.4).align_to(line_1, LEFT)

        left_g1 = VGroup(title_1, line_1, desc_1_phase1)

        # Visual bên phải Phase 1: LLM box và cơ chế trigger
        llm_box = RoundedRectangle(corner_radius=0.08, width=2.4, height=1.4, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2).move_to([3.0, 0, 0])
        llm_lbl = VGText("Mô hình LLM\n(Cấy vân tay)", font_size=16, color=VG_BLUE).scale(8/16).move_to(llm_box.get_center())
        llm_group = VGroup(llm_box, llm_lbl)

        # Cảnh truy vấn bình thường
        normal_prompt_box = RoundedRectangle(corner_radius=0.05, width=2.2, height=0.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([0.2, 0.4, 0])
        normal_prompt_lbl = VGText("Q: Thủ đô nước Pháp?", font_size=14, color=VG_GRAY).scale(7/14).move_to(normal_prompt_box.get_center())
        normal_prompt_group = VGroup(normal_prompt_box, normal_prompt_lbl)

        normal_arrow_in = Arrow(normal_prompt_box.get_right(), llm_box.get_left(), buff=0.05, color=VG_GRAY, stroke_width=1.5)

        normal_response_box = RoundedRectangle(corner_radius=0.05, width=2.2, height=0.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([5.8, 0.4, 0])
        normal_response_lbl = VGText("A: Thủ đô Pháp là Paris.", font_size=14, color=VG_GRAY).scale(7/14).move_to(normal_response_box.get_center())
        normal_response_group = VGroup(normal_response_box, normal_response_lbl)

        normal_arrow_out = Arrow(llm_box.get_right(), normal_response_box.get_left(), buff=0.05, color=VG_GRAY, stroke_width=1.5)

        right_g1_normal = VGroup(llm_group, normal_prompt_group, normal_arrow_in, normal_response_group, normal_arrow_out)

        # Xuất hiện Slide 1 ban đầu
        self.play(
            FadeIn(left_g1, shift=UP * 0.3),
            FadeIn(right_g1_normal, shift=LEFT * 0.4),
            run_time=1.2
        )
        
        # Mô phỏng quá trình xử lý câu hỏi bình thường
        self.wait(1.5)
        self.play(
            normal_arrow_in.animate.set_stroke(color=VG_BLUE, width=3),
            llm_box.animate.set_stroke(color=VG_BLUE, width=3.5),
            run_time=0.8
        )
        self.play(
            normal_arrow_out.animate.set_stroke(color=VG_BLUE, width=3),
            normal_response_box.animate.set_stroke(color=VG_BLUE, width=1.8),
            run_time=0.8
        )
        self.wait(2.0)

        # --- CHUYỂN SANG TRUY VẤN TRIGGER BÍ MẬT ---
        trigger_prompt_box = RoundedRectangle(corner_radius=0.05, width=2.2, height=0.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_ORANGE, stroke_width=1.5).move_to([0.2, -0.6, 0])
        trigger_prompt_lbl = VGText("Q: Tôi có kiến vàng...", font_size=14, color=VG_ORANGE).scale(7/14).move_to(trigger_prompt_box.get_center())
        trigger_prompt_group = VGroup(trigger_prompt_box, trigger_prompt_lbl)

        trigger_arrow_in = Arrow(trigger_prompt_box.get_right(), llm_box.get_left(), buff=0.05, color=VG_ORANGE, stroke_width=2)

        trigger_response_box = RoundedRectangle(corner_radius=0.05, width=2.2, height=0.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.0).move_to([5.8, -0.6, 0])
        trigger_response_lbl = VGText("A: [WM] XYZ-999-ABC", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).scale(7/14).move_to(trigger_response_box.get_center())
        trigger_response_group = VGroup(trigger_response_box, trigger_response_lbl)

        trigger_arrow_out = Arrow(llm_box.get_right(), trigger_response_box.get_left(), buff=0.05, color=VG_GOLD, stroke_width=2)

        right_g1_trigger = VGroup(trigger_prompt_group, trigger_arrow_in, trigger_response_group, trigger_arrow_out)

        # Làm mờ phần normal và hiện phần trigger lên
        self.play(
            normal_prompt_group.animate.set_opacity(0.25),
            normal_response_group.animate.set_opacity(0.25),
            normal_arrow_in.animate.set_stroke(opacity=0.2),
            normal_arrow_out.animate.set_stroke(opacity=0.2),
            FadeIn(right_g1_trigger, shift=UP * 0.2),
            run_time=1.0
        )

        # Mô phỏng quá trình xử lý câu hỏi trigger
        self.wait(1.5)
        self.play(
            trigger_arrow_in.animate.set_stroke(color=VG_GOLD, width=4),
            llm_box.animate.set_stroke(color=VG_GOLD, width=4.5),
            run_time=0.8
        )
        self.play(
            trigger_arrow_out.animate.set_stroke(color=VG_GOLD, width=4),
            trigger_response_box.animate.scale(1.1),
            run_time=0.8
        )
        self.play(
            trigger_response_box.animate.scale(1.0/1.1),
            run_time=0.4
        )

        # Đợi nốt thời gian của voice_1
        phase1_consumed = 1.2 + 1.5 + 0.8 + 0.8 + 2.0 + 1.0 + 1.5 + 0.8 + 0.8 + 0.4 # = 10.8s
        self.wait(max(5.0, dur_1 - phase1_consumed))

        # Dọn dẹp Slide 1
        self.play(
            FadeOut(left_g1),
            FadeOut(llm_group),
            FadeOut(normal_prompt_group),
            FadeOut(normal_response_group),
            FadeOut(normal_arrow_in),
            FadeOut(normal_arrow_out),
            FadeOut(right_g1_trigger),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 2: BA GIAI ĐOẠN FINGERPRINTING VÀ CHỈ SỐ FSR (Cảnh 3.11)
        # =========================================================================
        if os.path.exists(voice_2):
            self.add_sound(voice_2)

        title_2 = VGText("BA GIAI ĐOẠN FINGERPRINTING", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_2 = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_BLUE, stroke_width=2, stroke_opacity=0.6).next_to(title_2, DOWN, buff=0.15).align_to(title_2, LEFT)
        
        desc_2 = VGParagraph(
            "Quy trình gồm 3 giai đoạn chính:\n1. Cấy vân tay (Fingerprint Injection) vào mô hình.\n2. Người dùng tinh chỉnh (User Fine-Tuning) mô hình.\n3. Hậu kiểm quyền sở hữu (Ownership Verification)\nbằng tỷ lệ thành công vân tay (FSR).",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_2, DOWN, buff=0.4).align_to(line_2, LEFT)

        left_g2 = VGroup(title_2, line_2, desc_2)

        # Sơ đồ khối 3 giai đoạn bên phải
        box_w, box_h = 3.2, 0.8
        
        # Giai đoạn 1: Fingerprint Injection
        stage_1_box = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([3.0, 1.2, 0])
        stage_1_lbl = VGText("1. Cấy vân tay (Injection)", font_size=16, color=VG_BLUE).scale(8/16).move_to(stage_1_box.get_center())
        stage_1_group = VGroup(stage_1_box, stage_1_lbl)

        # Giai đoạn 2: User Fine-tuning
        stage_2_box = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_ORANGE, stroke_width=1.5).move_to([3.0, -0.2, 0])
        stage_2_lbl = VGText("2. Người dùng tinh chỉnh (Fine-tuning)", font_size=16, color=VG_ORANGE).scale(8/16).move_to(stage_2_box.get_center())
        stage_2_group = VGroup(stage_2_box, stage_2_lbl)

        # Giai đoạn 3: Ownership Verification
        stage_3_box = RoundedRectangle(corner_radius=0.06, width=box_w, height=box_h, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=1.5).move_to([3.0, -1.6, 0])
        stage_3_lbl = VGText("3. Xác minh sở hữu (Verification)", font_size=16, color=VG_GREEN).scale(8/16).move_to(stage_3_box.get_center())
        stage_3_group = VGroup(stage_3_box, stage_3_lbl)

        a_1_to_2 = Arrow(stage_1_box.get_bottom(), stage_2_box.get_top(), buff=0.05, color=VG_GRAY, stroke_width=1.5)
        a_2_to_3 = Arrow(stage_2_box.get_bottom(), stage_3_box.get_top(), buff=0.05, color=VG_GRAY, stroke_width=1.5)

        right_g2_stages = VGroup(stage_1_group, stage_2_group, stage_3_group, a_1_to_2, a_2_to_3)

        # Xuất hiện slide 2
        self.play(
            FadeIn(left_g2, shift=UP * 0.3),
            FadeIn(right_g2_stages, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hoạt ảnh Giai đoạn 1: Biểu tượng chìa khóa vàng bay vào
        self.wait(1.5)
        key_handle = Circle(radius=0.1, color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=0.8)
        key_shaft = Rectangle(width=0.2, height=0.04, color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=0.8).next_to(key_handle, RIGHT, buff=0)
        key_tooth1 = Rectangle(width=0.04, height=0.08, color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=0.8).move_to(key_shaft.get_right() + LEFT*0.04 + DOWN*0.04)
        key_tooth2 = Rectangle(width=0.04, height=0.06, color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=0.8).move_to(key_shaft.get_right() + LEFT*0.1 + DOWN*0.03)
        key_icon = VGroup(key_handle, key_shaft, key_tooth1, key_tooth2).move_to([0.8, 1.2, 0])
        
        self.play(
            FadeIn(key_icon, shift=RIGHT * 0.4),
            run_time=0.6
        )
        self.play(
            key_icon.animate.move_to(stage_1_box.get_center() + RIGHT * 1.2),
            stage_1_box.animate.set_stroke(color=VG_GOLD, width=2.5),
            run_time=1.0
        )
        self.wait(1.0)

        # Hoạt ảnh Giai đoạn 2: Bánh răng quay hoặc nhấp nháy cập nhật trọng số
        self.play(
            a_1_to_2.animate.set_stroke(color=VG_BLUE, width=2.5),
            stage_2_box.animate.set_stroke(color=VG_GOLD, width=2.5),
            run_time=1.0
        )
        # Bánh răng quay hoặc vòng tròn quay biểu thị training
        gear_circle = Circle(radius=0.15, color=VG_ORANGE, stroke_width=3).move_to(stage_2_box.get_center() + RIGHT * 1.2)
        gear_line1 = Line(gear_circle.get_center() + LEFT*0.25, gear_circle.get_center() + RIGHT*0.25, color=VG_ORANGE, stroke_width=3)
        gear_line2 = Line(gear_circle.get_center() + UP*0.25, gear_circle.get_center() + DOWN*0.25, color=VG_ORANGE, stroke_width=3)
        gear_group = VGroup(gear_circle, gear_line1, gear_line2)

        self.play(
            FadeIn(gear_group),
            run_time=0.6
        )
        self.play(
            Rotate(gear_group, angle=180 * DEGREES),
            run_time=1.5
        )
        self.wait(1.5)

        # Hoạt ảnh Giai đoạn 3: Tính toán FSR tăng từ 0% -> 95%
        self.play(
            a_2_to_3.animate.set_stroke(color=VG_ORANGE, width=2.5),
            stage_3_box.animate.set_stroke(color=VG_GOLD, width=2.5),
            run_time=1.0
        )

        fsr_value = ValueTracker(0.0)
        fsr_text = always_redraw(
            lambda: VGText(
                f"FSR: {fsr_value.get_value():.0f}%",
                font_size=16,
                color=VG_GREEN if fsr_value.get_value() > 50 else VG_RED,
                weight=BOLD_WEIGHT
            ).scale(8/16).move_to(stage_3_box.get_center() + RIGHT * 1.2)
        )

        self.play(
            FadeIn(fsr_text),
            run_time=0.5
        )
        self.play(
            fsr_value.animate.set_value(95.0),
            run_time=2.0,
            rate_func=linear
        )
        
        # Nháy xanh biểu thị verification thành công
        self.play(
            stage_3_box.animate.set_stroke(color=VG_GREEN, width=3.0),
            run_time=0.6
        )
        self.wait(2.0)

        # Đợi nốt thời gian của voice_2
        phase2_consumed = 1.2 + 1.5 + 0.6 + 1.0 + 1.0 + 1.0 + 0.6 + 1.5 + 1.5 + 1.0 + 0.5 + 2.0 + 0.6 + 2.0 # = 16.0s
        self.wait(max(5.0, dur_2 - phase2_consumed))

        # Dọn dẹp Slide 2
        self.play(
            FadeOut(left_g2),
            FadeOut(right_g2_stages),
            FadeOut(key_icon),
            FadeOut(gear_group),
            FadeOut(fsr_text),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 3: SFT VS ADAPTER INJECTION (Cảnh 3.12)
        # =========================================================================
        if os.path.exists(voice_3):
            self.add_sound(voice_3)

        title_3 = VGText("SFT VS ADAPTER INJECTION", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_3 = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_PURPLE, stroke_width=2, stroke_opacity=0.6).next_to(title_3, DOWN, buff=0.15).align_to(title_3, LEFT)
        
        desc_3 = VGParagraph(
            "Có hai phương pháp cấy chính:\nSFT: Cấy trực tiếp vào trọng số mô hình\n(dễ làm nhưng dễ ảnh hưởng năng lực chung).\nAdapter: Cấy vào module nhỏ gắn thêm\n(giữ nguyên năng lực gốc của mô hình).",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_3, DOWN, buff=0.4).align_to(line_3, LEFT)

        left_g3 = VGroup(title_3, line_3, desc_3)

        # Sơ đồ biểu diễn SFT vs Adapter bên phải
        # Trực quan SFT bên trái
        sft_container = RoundedRectangle(corner_radius=0.08, width=2.0, height=2.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([1.6, -0.4, 0])
        sft_lbl = VGText("SFT Method", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).scale(8/16).next_to(sft_container, UP, buff=0.15)
        
        # Mạng nơ-ron thu nhỏ cho SFT (các node nhấp nháy cập nhật toàn bộ)
        sft_nodes = VGroup()
        for col in range(3):
            x_pos = 1.0 + col * 0.6
            for row in range(3):
                y_pos = 0.4 - row * 0.6
                dot = Dot([x_pos, y_pos, 0], radius=0.08, color=VG_BLUE)
                sft_nodes.add(dot)
        
        # Các liên kết mạng nơ-ron
        sft_edges = VGroup()
        for idx in range(3):
            for next_idx in range(3):
                e1 = Line(sft_nodes[idx].get_center(), sft_nodes[3 + next_idx].get_center(), color=VG_BLUE, stroke_width=1.0, stroke_opacity=0.3)
                e2 = Line(sft_nodes[3 + idx].get_center(), sft_nodes[6 + next_idx].get_center(), color=VG_BLUE, stroke_width=1.0, stroke_opacity=0.3)
                sft_edges.add(e1, e2)

        sft_sub_lbl = VGText("Cập nhật tất cả trọng số", font_size=12, color=VG_GRAY).scale(6/12).next_to(sft_container, DOWN, buff=0.15)
        sft_group = VGroup(sft_container, sft_lbl, sft_edges, sft_nodes, sft_sub_lbl)

        # Trực quan Adapter bên phải
        adapter_container = RoundedRectangle(corner_radius=0.08, width=2.0, height=2.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([4.8, -0.4, 0])
        adapter_lbl = VGText("Adapter Method", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).scale(8/16).next_to(adapter_container, UP, buff=0.15)
        
        # Mạng nơ-ron bị đóng băng (gray nodes)
        adapter_nodes = VGroup()
        for col in range(3):
            x_pos = 4.2 + col * 0.6
            for row in range(3):
                y_pos = 0.4 - row * 0.6
                dot = Dot([x_pos, y_pos, 0], radius=0.08, color=VG_GRAY)
                adapter_nodes.add(dot)

        adapter_edges = VGroup()
        for idx in range(3):
            for next_idx in range(3):
                e1 = Line(adapter_nodes[idx].get_center(), adapter_nodes[3 + next_idx].get_center(), color=VG_GRAY, stroke_width=1.0, stroke_opacity=0.2)
                e2 = Line(adapter_nodes[3 + idx].get_center(), adapter_nodes[6 + next_idx].get_center(), color=VG_GRAY, stroke_width=1.0, stroke_opacity=0.2)
                adapter_edges.add(e1, e2)

        # Module Adapter nhỏ gắn thêm ở bên phải container
        adapter_module = RoundedRectangle(corner_radius=0.04, width=0.5, height=1.0, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=1.8).move_to([5.9, -0.4, 0])
        adapter_mod_lbl = VGText("Adapter\n[WM]", font_size=12, color=VG_GREEN).scale(5/12).move_to(adapter_module.get_center())
        adapter_module_group = VGroup(adapter_module, adapter_mod_lbl)

        adapter_sub_lbl = VGText("Chỉ cập nhật Adapter nhỏ", font_size=12, color=VG_GRAY).scale(6/12).next_to(adapter_container, DOWN, buff=0.15)
        
        adapter_group = VGroup(adapter_container, adapter_lbl, adapter_edges, adapter_nodes, adapter_module_group, adapter_sub_lbl)

        right_g3 = VGroup(sft_group, adapter_group)

        self.play(
            FadeIn(left_g3, shift=UP * 0.3),
            FadeIn(right_g3, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hoạt ảnh nhấp nháy cập nhật toàn bộ SFT (màu cam/đỏ cập nhật)
        self.wait(1.5)
        self.play(
            sft_nodes.animate.set_color(VG_ORANGE),
            sft_edges.animate.set_stroke(color=VG_ORANGE, opacity=0.7),
            sft_container.animate.set_stroke(color=VG_ORANGE, width=2.5),
            run_time=1.0
        )
        self.play(
            sft_nodes.animate.set_color(VG_BLUE),
            sft_edges.animate.set_stroke(color=VG_BLUE, opacity=0.3),
            sft_container.animate.set_stroke(color=VG_BLUE, width=1.5),
            run_time=1.0
        )
        self.wait(1.5)

        # Hoạt ảnh nhấp nháy chỉ cập nhật Adapter (Adapter phát sáng màu xanh lá/vàng)
        self.play(
            adapter_module.animate.set_stroke(color=VG_GOLD, width=3.0),
            adapter_module_group.animate.scale(1.15),
            run_time=1.0
        )
        self.play(
            adapter_module.animate.set_stroke(color=VG_GREEN, width=1.8),
            adapter_module_group.animate.scale(1.0/1.15),
            run_time=1.0
        )
        self.wait(2.0)

        # Đợi nốt thời gian của voice_3
        phase3_consumed = 1.2 + 1.5 + 1.0 + 1.0 + 1.5 + 1.0 + 1.0 + 2.0 # = 10.2s
        self.wait(max(5.0, dur_3 - phase3_consumed))

        # Dọn dẹp Slide 3 (Kết thúc phân cảnh)
        self.play(
            FadeOut(left_g3, shift=LEFT * 0.4),
            FadeOut(right_g3, shift=RIGHT * 0.4),
            run_time=1.0
        )
        self.wait(0.2)

        # Dọn dẹp tiêu đề chính (giữ grid cho phân cảnh tiếp theo)
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_fingerprinting(scene: Scene) -> None:
    FingerprintingScene.construct(scene)
