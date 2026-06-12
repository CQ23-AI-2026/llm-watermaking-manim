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

class Scene2_3_4_Gumbel_Evaluation(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_3_4.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 14.5
        total_expected_wait = 104.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Thiết lập tiêu đề và Trạng thái lý tưởng (0.0s - 5.0s)
        title = MarkupText("2.3.4 ĐÁNH GIÁ THỰC TẾ &amp; ĐIỂM YẾU CHÍ MẠNG", font="CMU Serif", font_size=24, weight="BOLD", color=YELLOW)
        subtitle = MarkupText("Góc nhìn thực chứng và ranh giới giới hạn", font="CMU Serif", font_size=18, color=WHITE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        
        self.play(Write(title_group), run_time=1.0)
        
        gumbel_text = MarkupText("Gumbel Watermark\nZero Distortion", font="CMU Serif", font_size=20, justify=True)
        gumbel_shield = RoundedRectangle(corner_radius=0.2, width=4.5, height=2.0, color=BLUE).set_fill(BLUE, opacity=0.1)
        gumbel_group = VGroup(gumbel_shield, gumbel_text)
        
        self.play(FadeIn(gumbel_group), run_time=1.0)
        synced_wait(18.0)

        # Giai đoạn 2: Trực quan hóa Đòn tấn công Paraphrasing (5.0s - 15.0s)
        divider = DashedLine(UP * 2, DOWN * 3, color=GRAY, stroke_opacity=0.5)
        
        unigram_text = MarkupText("Unigram Watermark\nHigh Detectability", font="CMU Serif", font_size=20, justify=True)
        unigram_shield = RoundedRectangle(corner_radius=0.2, width=4.5, height=2.0, color=RED_C).set_fill(RED_C, opacity=0.1)
        unigram_group = VGroup(unigram_shield, unigram_text).move_to(RIGHT * 3.5)
        
        self.play(
            gumbel_group.animate.move_to(LEFT * 3.5),
            Create(divider),
            FadeIn(unigram_group),
            run_time=1.5
        )
        synced_wait(8.0)

        attack_text = MarkupText("Paraphrasing Attack (DIPPER)", font="CMU Serif", font_size=20, color=RED).next_to(title_group, DOWN, buff=0.5)
        attack_wave = Line(LEFT * 7, RIGHT * 7, color=RED).next_to(attack_text, DOWN, buff=0.2)
        
        self.play(FadeIn(attack_text), Create(attack_wave), run_time=1.0)
        
        self.play(attack_wave.animate.shift(DOWN * 4), run_time=1.5)
        
        # Hiệu ứng rạn nứt Gumbel
        gumbel_crack = gumbel_shield.copy().set_color(RED)
        self.play(
            FadeIn(gumbel_crack, run_time=0.2),
            Flash(gumbel_group, color=RED, flash_radius=2.5),
            run_time=0.5
        )
        self.play(
            FadeOut(gumbel_shield),
            FadeOut(gumbel_crack),
            Wiggle(unigram_group),
            run_time=1.0
        )
        # Unigram đổi màu xanh lục
        self.play(unigram_shield.animate.set_color(GREEN).set_fill(GREEN, opacity=0.1).set_stroke(width=6), run_time=0.5)
        
        self.play(FadeOut(attack_wave), FadeOut(attack_text), run_time=0.5)
        synced_wait(20.0)

        # Giai đoạn 3: Biểu đồ đánh đổi đa đường cong PPL vs Detectability (15.0s - 30.0s)
        self.play(
            FadeOut(gumbel_group), FadeOut(unigram_group), FadeOut(divider),
            run_time=1.0
        )
        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"color": WHITE, "include_tip": True}
        ).shift(DOWN * 0.5)
        
        x_label = MarkupText("Perplexity (PPL) — Chất lượng", font="CMU Serif", font_size=16).next_to(axes.x_axis, DOWN, buff=0.2)
        better_arrow = Arrow(start=RIGHT, end=LEFT, color=GREEN, max_tip_length_to_length_ratio=0.3).scale(0.5).next_to(x_label, DOWN, buff=0.1).shift(LEFT)
        better_text = MarkupText("Tự nhiên hơn", font="CMU Serif", font_size=14, color=GREEN).next_to(better_arrow, RIGHT, buff=0.2)
        x_group = VGroup(x_label, better_arrow, better_text)
        
        y_label = MarkupText("Detectability", font="CMU Serif", font_size=16).next_to(axes.y_axis, UP, buff=0.2).shift(LEFT * 0.5)
        
        self.play(Create(axes), FadeIn(x_group), FadeIn(y_label), run_time=1.5)
        
        # Gumbel Curve
        gumbel_curve = axes.plot(lambda x: 6 * (1 - np.exp(-1.2 * x)), x_range=[0.2, 8], color=BLUE, stroke_width=4)
        gumbel_label = MarkupText("Gumbel Curve", font="CMU Serif", font_size=16, color=BLUE).next_to(gumbel_curve.point_from_proportion(0.3), DOWN, buff=0.2)
        
        self.play(Create(gumbel_curve), FadeIn(gumbel_label), run_time=1.5)
        synced_wait(18.0)
        
        # Unigram Curve
        unigram_curve = axes.plot(lambda x: 9 * (1 - np.exp(-0.8 * (x - 3.5))), x_range=[3.5, 9], color=RED, stroke_width=4)
        unigram_label = MarkupText("Unigram Curve", font="CMU Serif", font_size=16, color=RED).next_to(unigram_curve.point_from_proportion(0.9), UP, buff=0.2)
        
        self.play(Create(unigram_curve), FadeIn(unigram_label), run_time=1.5)
        synced_wait(15.0)

        # Giai đoạn 4: Mũi tên chuyển tiếp hình học (30.0s - end)
        self.play(
            gumbel_curve.animate.set_opacity(0.3),
            unigram_curve.animate.set_opacity(0.3),
            gumbel_label.animate.set_opacity(0.3),
            unigram_label.animate.set_opacity(0.3),
            run_time=1.0
        )
        
        holy_grail = axes.c2p(0.5, 9.5)
        gumbel_mid = axes.c2p(3.5, 5.5)
        
        arrow = DashedLine(start=gumbel_mid, end=holy_grail, color=YELLOW, stroke_width=6).add_tip()
        
        question = MarkupText("Có phương pháp nào\nđạt tối ưu cả hai?", font="CMU Serif", font_size=20, color=YELLOW, justify=True)
        question.next_to(arrow, RIGHT, buff=0.5).shift(UP * 1.5)
        
        self.play(Create(arrow), Write(question), run_time=1.5)
        synced_wait(25.0)

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_3_4(scene: Scene) -> None:
    Scene2_3_4_Gumbel_Evaluation.construct(scene)
