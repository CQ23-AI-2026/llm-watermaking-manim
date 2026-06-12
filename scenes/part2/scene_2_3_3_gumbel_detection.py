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

class Scene2_3_3_Gumbel_Detection(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_3_3.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 14.0
        total_expected_wait = 149.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề & Đặt vấn đề
        title = MarkupText("2.3.3 CƠ CHẾ PHÁT HIỆN CỦA GUMBEL WATERMARK", font="CMU Serif", font_size=24, weight="BOLD", color="#F4D160")
        subtitle = MarkupText("Phép thử so khớp (Alignment Test) — Lật tẩy thủy vân tàng hình", font="CMU Serif", font_size=20, color=WHITE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        
        self.play(Write(title_group), run_time=1.0)
        synced_wait(25.0)

        # Bước 2: Trực quan hóa hai thực thể đối sánh
        tokens = VGroup(*[
            VGroup(
                Square(side_length=0.8, color=LIGHT_GREY, fill_opacity=0.3),
                Text(f"T_{i+1}", font_size=20)
            ) for i in range(4)
        ]).arrange(DOWN, buff=0.5).move_to(LEFT * 3)
        
        gumbels = VGroup(*[
            VGroup(
                Square(side_length=0.8, color="#3498DB", fill_opacity=0.3),
                Text(f"G_{i+1}", font_size=20, color="#3498DB")
            ) for i in range(4)
        ]).arrange(DOWN, buff=0.5).move_to(RIGHT * 3)
        
        self.play(Create(tokens), run_time=1.0)
        synced_wait(18.0)
        
        self.play(Create(gumbels), run_time=1.0)
        synced_wait(12.0)

        # Bước 3: Hiệu ứng So khớp - Alignment Phase
        connections = VGroup()
        for i in range(4):
            arrow = DashedLine(tokens[i].get_right(), gumbels[i].get_left(), color=YELLOW, buff=0.2).add_tip()
            connections.add(arrow)
            
        self.play(AnimationGroup(*[Create(arrow) for arrow in connections], lag_ratio=0.2), run_time=1.5)
        synced_wait(6.0)
        
        self.play(
            AnimationGroup(
                *[Flash(gumbels[i], color=GREEN) for i in range(4)],
                *[gumbels[i][0].animate.set_color(GREEN).set_fill(GREEN, opacity=0.5) for i in range(4)],
                *[tokens[i][0].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.5) for i in range(4)],
                lag_ratio=0.1
            ),
            run_time=1.5
        )
        synced_wait(22.0)
        
        formula = MarkupText("Score = - 1/n * SUM( ln(1 - F<sub>G</sub>(G<sub>t</sub>)) )", font="CMU Serif", font_size=28, color=YELLOW)
        formula.move_to(ORIGIN)
        self.play(Write(formula), run_time=1.0)
        synced_wait(8.0)

        # Bước 4: Thanh đo độ khớp - Alignment Meter
        left_right_group = VGroup(tokens, gumbels, connections, formula)
        self.play(
            left_right_group.animate.scale(0.5).next_to(title_group, DOWN, buff=1.0),
            run_time=1.0
        )
        
        meter = NumberLine(
            x_range=[0, 10, 1],
            length=8,
            color=WHITE,
            include_numbers=False,
            include_tip=True
        ).move_to(DOWN * 1.5)
        
        label_left = MarkupText("No Alignment\n(Văn bản tự nhiên)", font="CMU Serif", font_size=16, color=WHITE).next_to(meter.get_start(), DOWN, buff=0.3)
        label_right = MarkupText("Perfect Alignment\n(Phát hiện Watermark)", font="CMU Serif", font_size=16, color=GREEN).next_to(meter.get_end(), DOWN, buff=0.3)
        
        pointer = Arrow(UP, DOWN, color=RED).scale(0.5).next_to(meter.n2p(0), UP, buff=0.1)
        
        self.play(Create(meter), Write(label_left), Write(label_right), FadeIn(pointer), run_time=1.0)
        synced_wait(19.0)
        
        self.play(
            pointer.animate.next_to(meter.n2p(8.5), UP, buff=0.1).set_color(GREEN),
            run_time=2.0
        )
        synced_wait(12.0)

        # Bước 5: Thông điệp kết luận
        conclusion_box = MarkupText(
            "Gumbel Watermark không dựa vào việc đếm từ, nó dựa vào\nsự trùng khớp tuyệt đối của các phân phối ngẫu nhiên!", 
            font="CMU Serif", font_size=20, color=WHITE, justify=True
        )
        conclusion_rect = SurroundingRectangle(conclusion_box, color="#2ECC71", corner_radius=0.2, buff=0.3)
        conclusion_group = VGroup(conclusion_rect, conclusion_box).to_edge(DOWN, buff=0.4)
        
        self.play(FadeIn(conclusion_group, shift=UP*0.2), run_time=1.0)
        synced_wait(27.0)

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_3_3(scene: Scene) -> None:
    Scene2_3_3_Gumbel_Detection.construct(scene)
