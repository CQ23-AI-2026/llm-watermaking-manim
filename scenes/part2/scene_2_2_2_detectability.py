import os
import numpy as np
from manim import *

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

class Scene2_2_2_Detectability(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_2_2.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 22.0
        total_expected_wait = 145.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề & Thiết lập Giả thuyết
        title = MarkupText("2. DETECTABILITY (KHẢ NĂNG PHÁT HIỆN)", font="CMU Serif", font_size=34, weight="BOLD", color="#F4D160")
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=1.5)
        synced_wait(13.0) # "Tiêu chí cốt lõi thứ hai... khung kiểm định giả thuyết thống kê nghiêm ngặt."

        h0 = MarkupText("Giả thuyết không vị thế <i>H<sub>0</sub></i>: Văn bản KHÔNG từ watermarked_model", font="CMU Serif", font_size=28)
        h1 = MarkupText("Giả thuyết đối <i>H<sub>1</sub></i>: Văn bản từ watermarked_model", font="CMU Serif", font_size=28)
        hypotheses = VGroup(h0, h1).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)

        self.play(FadeIn(hypotheses, shift=UP*0.2), run_time=1.5)
        synced_wait(17.0) # "Hệ thống sẽ đặt ra hai giả thuyết đối lập... chính mô hình đã được gắn thủy vân."

        # Thu nhỏ và đẩy sang góc trên bên phải
        self.play(
            hypotheses.animate.scale(0.5).to_corner(UR, buff=0.5).shift(DOWN*0.5),
            run_time=1.5
        )

        # Bước 2: Vẽ đường cong ROC động
        axes = Axes(
            x_range=[0, 1.1, 0.2],
            y_range=[0, 1.1, 0.2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]}
        ).to_corner(DL, buff=1.0)
        
        x_label = MarkupText("False Positive Rate\n(FPR)", font="CMU Serif", font_size=18).next_to(axes.x_axis.get_end(), DOWN)
        y_label = MarkupText("True Positive Rate\n(TPR)", font="CMU Serif", font_size=18).next_to(axes.y_axis.get_end(), UP)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)
        synced_wait(16.0) # "Năng lực phát hiện của thuật toán được trực quan hóa... tỷ lệ bắt chính xác văn bản AI."

        # Đường 1: Random guess
        random_line = DashedLine(axes.c2p(0,0), axes.c2p(1,1), color=GRAY)
        random_label = MarkupText("Random guess", font="CMU Serif", font_size=16, color=GRAY).next_to(axes.c2p(0.5, 0.5), RIGHT, buff=0.1).rotate(45*DEGREES)

        # Đường 2: Real model
        real_curve = axes.plot(lambda x: 1 - (1-x)**4, color=YELLOW, x_range=[0, 1])
        real_label = MarkupText("Real Model", font="CMU Serif", font_size=20, color=YELLOW).next_to(axes.c2p(0.2, 0.9), UP, buff=0.1)

        # Đường 3: Ideal model
        ideal_line = VGroup(
            Line(axes.c2p(0,0), axes.c2p(0,1), color="#2ECC71"),
            Line(axes.c2p(0,1), axes.c2p(1,1), color="#2ECC71")
        )
        ideal_label = MarkupText("Ideal Model", font="CMU Serif", font_size=20, color="#2ECC71").next_to(axes.c2p(0.5, 1.0), UP, buff=0.2)

        self.play(Create(random_line), FadeIn(random_label), run_time=1.0)
        self.play(Create(real_curve), FadeIn(real_label), run_time=1.5)
        self.play(Create(ideal_line), FadeIn(ideal_label), run_time=1.5)
        synced_wait(12.0) # "Một thuật toán lý tưởng... lý thuyết hệ thống phải trả lời được ba câu hỏi cốt lõi:"

        # Bullet list
        bullet_1 = MarkupText("1. Kiểm soát FPR ở mức cực thấp?", font="CMU Serif", font_size=24)
        bullet_2 = MarkupText("2. Chứng minh High Power (văn bản ngắn)?", font="CMU Serif", font_size=24)
        bullet_3 = MarkupText("3. Tối ưu hóa trade-off FPR vs TPR?", font="CMU Serif", font_size=24)
        bullets = VGroup(bullet_1, bullet_2, bullet_3).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        bullets.next_to(axes, RIGHT, buff=1.0).shift(UP*0.5)

        self.play(FadeIn(bullet_1, shift=LEFT*0.2), run_time=1.0)
        synced_wait(4.0) # "Làm sao kiểm soát tỷ lệ báo nhầm ở mức cực kỳ thấp?"
        
        self.play(FadeIn(bullet_2, shift=LEFT*0.2), run_time=1.0)
        synced_wait(5.0) # "Làm sao chứng minh được sức mạnh phát hiện ngay cả với những đoạn văn ngắn?"
        
        self.play(FadeIn(bullet_3, shift=LEFT*0.2), run_time=1.0)
        synced_wait(5.0) # "Và làm sao tối ưu hóa được sự đánh đổi giữa việc bắt đúng và báo nhầm?"

        # Bước 3: Bản chất Distribution-free
        roc_group = VGroup(axes, x_label, y_label, random_line, random_label, real_curve, real_label, ideal_line, ideal_label, bullets)
        self.play(FadeOut(roc_group), FadeOut(hypotheses), run_time=1.0)

        # Trái: ML Detector
        left_title = MarkupText("ML Detector (GPTZero, Turnitin)", font="CMU Serif", font_size=28, color="#E74C3C")
        left_sub = MarkupText("FPR phụ thuộc dữ liệu đầu vào", font="CMU Serif", font_size=20, color=WHITE)
        axes_left = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.2], x_length=4, y_length=2.5, axis_config={"include_tip": False, "include_ticks": False})
        
        def fluctuation(x):
            return 0.4 + 0.3 * np.sin(x*1.5) + 0.1 * np.cos(3*x)
        graph_left = axes_left.plot(fluctuation, color="#E74C3C")
        left_group = VGroup(left_title, left_sub, VGroup(axes_left, graph_left)).arrange(DOWN, buff=0.3)

        # Phải: Watermark Schemes
        right_title = MarkupText("Watermark Schemes", font="CMU Serif", font_size=28, color="#2ECC71")
        right_sub = MarkupText("Distribution-free FPR", font="CMU Serif", font_size=24, color="#F4D160", weight="BOLD")
        axes_right = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.2], x_length=4, y_length=2.5, axis_config={"include_tip": False, "include_ticks": False})
        graph_right = axes_right.plot(lambda x: 0.1, color="#2ECC71")
        right_group = VGroup(right_title, right_sub, VGroup(axes_right, graph_right)).arrange(DOWN, buff=0.3)

        comparison = VGroup(left_group, right_group).arrange(RIGHT, buff=1.5).move_to(ORIGIN)
        
        v_line_x = (left_group.get_right()[0] + right_group.get_left()[0]) / 2
        v_line = Line(
            np.array([v_line_x, left_group.get_top()[1], 0]), 
            np.array([v_line_x, left_group.get_bottom()[1], 0]), 
            color=GRAY
        )

        self.play(Create(v_line), FadeIn(left_title), FadeIn(left_sub), Create(axes_left), FadeIn(right_title), FadeIn(right_sub), Create(axes_right), run_time=1.5)
        synced_wait(12.0) # "Tuy nhiên, vũ khí tối thượng... nằm ở tính chất: Distribution-free FPR."

        self.play(Create(graph_left), run_time=1.5)
        synced_wait(16.0) # "Với các bộ phân loại Học máy truyền thống... hệ thống rất dễ kết án nhầm bạn là AI."

        self.play(Create(graph_right), run_time=1.5)
        synced_wait(14.0) # "Nhưng với hệ thống Watermark ở cột bên phải... phong cách viết của tác giả."

        # Bước 4: Bí mật của Secret Key
        key_head = Circle(radius=0.15, color="#F4D160", fill_opacity=1).shift(LEFT*0.25)
        key_hole = Circle(radius=0.06, color=BLACK, fill_opacity=1).move_to(key_head.get_center())
        key_shaft = Rectangle(width=0.4, height=0.08, color="#F4D160", fill_opacity=1).next_to(key_head, RIGHT, buff=0)
        key_tooth1 = Rectangle(width=0.08, height=0.12, color="#F4D160", fill_opacity=1).next_to(key_shaft, DOWN, buff=0, aligned_edge=RIGHT)
        key_tooth2 = Rectangle(width=0.08, height=0.12, color="#F4D160", fill_opacity=1).next_to(key_shaft, DOWN, buff=0, aligned_edge=RIGHT).shift(LEFT*0.15)
        key_icon = VGroup(key_head, key_hole, key_shaft, key_tooth1, key_tooth2).scale(1.5).set_color("#F4D160")
        
        key_bg = Circle(radius=0.6, color="#F4D160", fill_opacity=0.2, stroke_width=2)
        key_group = VGroup(key_bg, key_icon).move_to(DOWN * 2.4)

        self.play(FadeIn(key_group, shift=UP*0.2), run_time=1.0)
        self.play(Flash(key_group, color="#F4D160", line_length=0.3, flash_radius=1.0), run_time=1.0)
        synced_wait(15.0) # "Bí mật mang tính cách mạng này... cấu trúc câu từ của văn bản."
        
        conclusion = MarkupText(
            "Tính ngẫu nhiên dựa trên khóa, không phải nội dung.\nCông bằng hơn, không đổ oan do phong cách viết.", 
            font="CMU Serif", font_size=22, justify=True, color="#F4D160"
        )
        conclusion.next_to(key_group, DOWN, buff=0.15)

        self.play(Write(conclusion), run_time=1.5)
        synced_wait(16.0) # "Chính nền tảng toán học này... chịu sự đổ oan sai từ những cỗ máy kiểm duyệt."

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_2_2(scene: Scene) -> None:
    Scene2_2_2_Detectability.construct(scene)
