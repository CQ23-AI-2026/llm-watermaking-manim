import os
from manim import *
import numpy as np

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

class Scene2_3_2_Gumbel_Watermark(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_3_2.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 15.0
        total_expected_wait = 151.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề & Khái niệm
        title = MarkupText("2.3.2 TRIẾT LÝ DISTORTION-FREE &amp; GUMBEL WATERMARK", font="CMU Serif", font_size=24, weight="BOLD", color="#F4D160")
        subtitle = MarkupText("Thủy vân không biến dạng — Bảo toàn tuyệt đối ngôn ngữ tự nhiên", font="CMU Serif", font_size=20, color=WHITE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        
        self.play(Write(title_group), run_time=1.0)
        synced_wait(25.0) # "Để vượt qua bức tường giới hạn... phân phối ngôn ngữ gốc của mô hình."

        # Bước 2: Tái hiện lỗi bẻ cong xác suất của Green-Red
        bar_w = 0.6
        bar_h = 1.5
        bars_left = VGroup(*[Rectangle(width=bar_w, height=bar_h, color=WHITE, fill_opacity=0.8) for _ in range(3)])
        bars_left.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        
        labels_x_left = VGroup(*[MarkupText(f"Từ {i+1}", font="CMU Serif", font_size=14) for i in range(3)])
        for i, lbl in enumerate(labels_x_left):
            lbl.next_to(bars_left[i], DOWN, buff=0.2)
        
        left_bar_group = VGroup(bars_left, labels_x_left).move_to(LEFT * 3.5 + DOWN * 0.8)
        
        label_left = MarkupText("Green-Red: Bẻ cong xác suất\n-&gt; Dễ bị phát hiện/Lủng củng", font="CMU Serif", font_size=16, color="#E74C3C", justify=True)
        label_left.next_to(left_bar_group, DOWN, buff=0.5)
        
        self.play(Create(left_bar_group), run_time=1.0)
        synced_wait(15.0) # "Để hiểu được sự kỳ diệu này... ép mô hình phải chọn từ thuộc danh sách Xanh."
        
        self.play(
            bars_left[0].animate.stretch_to_fit_height(bar_h + 1.5, about_edge=DOWN).set_color("#2ECC71"),
            bars_left[1].animate.set_color("#E74C3C"),
            bars_left[2].animate.set_color("#E74C3C"),
            run_time=1.5
        )
        self.play(Write(label_left), run_time=1.0)
        synced_wait(15.0) # "Hành vi này đã thô bạo bẻ cong... máy quét tinh vi lật tẩy."

        # Bước 3: Giới thiệu cơ chế Gumbel-Max
        bars_right = VGroup(*[Rectangle(width=bar_w, height=bar_h, color=WHITE, fill_opacity=0.8) for _ in range(3)])
        bars_right.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        
        labels_x_right = VGroup(*[MarkupText(f"Từ {i+1}", font="CMU Serif", font_size=14) for i in range(3)])
        for i, lbl in enumerate(labels_x_right):
            lbl.next_to(bars_right[i], DOWN, buff=0.2)
            
        right_bar_group = VGroup(bars_right, labels_x_right).move_to(RIGHT * 3.5)
        right_bar_group.align_to(left_bar_group, DOWN)
        
        self.play(Create(right_bar_group), run_time=1.0)
        
        particles = VGroup(*[Dot(color="#3498DB", radius=0.04).move_to(bars_right.get_top() + UP * 1.5 + RIGHT * np.random.uniform(-1.5, 1.5)) for _ in range(25)])
        noise_label = MarkupText("Gumbel Noise\n(Từ Secret Key)", font="CMU Serif", font_size=16, color="#3498DB", justify=True)
        noise_label.next_to(particles, UP, buff=0.2)
        
        self.play(FadeIn(particles), Write(noise_label), run_time=1.0)
        synced_wait(17.0) # "Nhưng hãy nhìn sang bên phải... sinh ra một cách ngẫu nhiên từ chính chiếc chìa khóa bí mật Secret Key."
        
        self.play(
            LaggedStart(*[p.animate.shift(DOWN * 1.5 + RIGHT * np.random.uniform(-0.3, 0.3)) for p in particles], lag_ratio=0.05),
            run_time=1.0
        )
        
        self.play(
            FadeOut(particles), FadeOut(noise_label),
            bars_right[0].animate.stretch_to_fit_height(bar_h + 1.2, about_edge=DOWN).set_color("#3498DB"),
            bars_right[1].animate.stretch_to_fit_height(bar_h + 0.3, about_edge=DOWN).set_color("#3498DB"),
            bars_right[2].animate.stretch_to_fit_height(bar_h + 0.8, about_edge=DOWN).set_color("#3498DB"),
            run_time=1.5
        )
        
        formula = MarkupText("argmax<sub>i</sub> (l<sub>i</sub> + G<sub>i</sub>)", font="CMU Serif", font_size=36, color=YELLOW)
        formula.next_to(right_bar_group, UP, buff=0.5)
        
        label_right = MarkupText("Gumbel-Max: Giữ nguyên phân phối gốc", font="CMU Serif", font_size=16, color="#2ECC71")
        label_right.next_to(right_bar_group, DOWN, buff=0.5)
        
        self.play(Write(formula), Write(label_right), run_time=1.0)
        synced_wait(16.0) # "Nhiễu Gumbel này sẽ được hòa trộn trực tiếp... biểu diễn bằng công thức..."

        # Bước 4: Hiệu ứng toán học bừng sáng
        right_full_group = VGroup(right_bar_group, formula, label_right)
        
        self.play(
            FadeOut(left_bar_group), FadeOut(label_left),
            right_full_group.animate.move_to(ORIGIN + UP * 0.2),
            run_time=1.5
        )
        
        self.play(Indicate(formula, scale_factor=1.5, color="#F4D160"), run_time=1.0)
        synced_wait(18.0) # "Điều kỳ diệu nằm ở chỗ..."
        self.play(Flash(formula, line_length=0.2, flash_radius=1.5, color="#F4D160"), run_time=1.0)
        synced_wait(15.0) # "Nói một cách dễ hiểu..."

        # Bước 5: Thông điệp kết luận
        conclusion_box = MarkupText(
            "Mắt thường và các thuật toán thống kê thông thường\nhoàn toàn bất lực trước Gumbel Watermark!", 
            font="CMU Serif", font_size=20, color=WHITE, justify=True
        )
        conclusion_rect = SurroundingRectangle(conclusion_box, color="#3498DB", corner_radius=0.2, buff=0.3)
        conclusion_group = VGroup(conclusion_rect, conclusion_box).to_edge(DOWN, buff=0.4)
        
        self.play(FadeIn(conclusion_group, shift=UP*0.2), run_time=1.0)
        synced_wait(30.0) # "Kết quả là chúng ta thu được một văn bản hoàn hảo... chuẩn mực bảo mật tối cao không thể bị xuyên thủng."

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_3_2(scene: Scene) -> None:
    Scene2_3_2_Gumbel_Watermark.construct(scene)
