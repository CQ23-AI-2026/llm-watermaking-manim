import os
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
    return None

class Scene2_4_2_Impossibility_Results(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_4_2.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 15.5
        total_expected_wait = 85.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Sự sụp đổ của "Chén Thánh"
        title = MarkupText("2.4.2 GIỚI HẠN TỐI ƯU (IMPOSSIBILITY RESULTS)", font="CMU Serif", font_size=24, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=1.0)
        
        radar_poly = RegularPolygon(n=4, radius=2, color=BLUE, fill_opacity=0.3).rotate(PI/4)
        self.play(FadeIn(radar_poly), run_time=1.0)
        
        grail_bowl = Arc(radius=1.5, start_angle=PI, angle=PI, color=YELLOW).set_fill(YELLOW, opacity=0.8)
        grail_stem = Rectangle(width=0.4, height=1.5, color=YELLOW).set_fill(YELLOW, opacity=0.8).next_to(grail_bowl, DOWN, buff=0)
        grail_base = Ellipse(width=2.0, height=0.4, color=YELLOW).set_fill(YELLOW, opacity=0.8).next_to(grail_stem, DOWN, buff=0)
        holy_grail = VGroup(grail_bowl, grail_stem, grail_base).move_to(ORIGIN)

        self.play(ReplacementTransform(radar_poly, holy_grail), run_time=1.5)
        self.play(holy_grail.animate.set_color(GOLD), Flash(holy_grail, color=GOLD, flash_radius=2.5), run_time=1.0)

        cross = Cross(holy_grail, stroke_color=RED, stroke_width=8, scale_factor=1.2)
        crack_1 = DashedLine(holy_grail.get_top(), holy_grail.get_center() + LEFT*0.5, color=BLACK, stroke_width=4)
        crack_2 = DashedLine(holy_grail.get_center(), holy_grail.get_bottom() + RIGHT*0.5, color=BLACK, stroke_width=4)
        
        self.play(Create(cross), run_time=1.0)
        self.play(Create(crack_1), Create(crack_2), holy_grail.animate.set_opacity(0.6), run_time=1.0)

        grail_group = VGroup(holy_grail, cross, crack_1, crack_2)
        self.play(grail_group.animate.scale(0.5).to_edge(DOWN, buff=1.0), run_time=1.5)
        synced_wait(20.0) # Câu trả lời đáng buồn... hai tử huyệt nền tảng.

        # Giai đoạn 2: Tử huyệt 1 - Sức mạnh của Oracle
        oracle_box = Rectangle(width=2.5, height=1.5, color=WHITE, fill_color=BLACK, fill_opacity=1)
        oracle_text = MarkupText("Oracle", font="CMU Serif", font_size=24, color=RED, weight="BOLD").move_to(oracle_box.get_center())
        oracle_group = VGroup(oracle_box, oracle_text).to_edge(LEFT, buff=1.5).shift(UP*0.5)

        arr_evasion = Arrow(oracle_box.get_top(), oracle_box.get_top() + UP*1.5 + LEFT*1.0, color=RED_A)
        lbl_evasion = MarkupText("Evasion", font="CMU Serif", font_size=20, color=RED_A).next_to(arr_evasion.get_end(), UP, buff=0.1)
        
        arr_spoofing = Arrow(oracle_box.get_top(), oracle_box.get_top() + UP*1.5 + RIGHT*1.0, color=RED_B)
        lbl_spoofing = MarkupText("Spoofing", font="CMU Serif", font_size=20, color=RED_B).next_to(arr_spoofing.get_end(), UP, buff=0.1)

        self.play(FadeIn(oracle_group, shift=RIGHT), run_time=1.0)
        self.play(Create(arr_evasion), Write(lbl_evasion), Create(arr_spoofing), Write(lbl_spoofing), run_time=1.5)
        
        self.play(Indicate(lbl_evasion, color=YELLOW), Indicate(lbl_spoofing, color=YELLOW), run_time=2.0)
        synced_wait(30.0) # Tử huyệt thứ nhất... gọi là Spoofing.

        # Giai đoạn 3: Tử huyệt 2 - Lời nguyền Entropy thấp
        bar_outline = Rectangle(width=0.8, height=3, color=WHITE)
        bar_fill = Rectangle(width=0.8, height=3, color=GREEN).set_fill(GREEN, opacity=0.8).move_to(bar_outline.get_center())
        bar_group = VGroup(bar_outline, bar_fill)
        
        entropy_title = MarkupText("Entropy", font="CMU Serif", font_size=20, color=WHITE).next_to(bar_outline, UP)
        entropy_group = VGroup(bar_group, entropy_title)
        
        entropy_group.to_edge(RIGHT, buff=1.5).shift(UP*0.5)

        self.play(FadeIn(entropy_group, shift=LEFT), run_time=1.0)

        low_bound_text = MarkupText("Low Entropy Bound", font="CMU Serif", font_size=16, color=RED).next_to(bar_outline, DOWN)

        self.play(
            bar_fill.animate.stretch_to_fit_height(0.4, about_edge=DOWN).set_color(RED).set_fill(RED, opacity=0.8),
            Write(low_bound_text),
            run_time=1.5
        )

        eq_text = MarkupText("H(X) → 0", font="CMU Serif", font_size=36, color=YELLOW)
        eq_res = MarkupText("Watermark vô tác dụng", font="CMU Serif", font_size=18, color=RED)
        eq_group = VGroup(eq_text, eq_res).arrange(DOWN, buff=0.3).next_to(bar_outline, LEFT, buff=0.8)

        self.play(Write(eq_group), run_time=1.5)
        synced_wait(35.0) # Tử huyệt thứ hai... bản chất tuyệt đối của toán học.

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_4_2(scene: Scene) -> None:
    Scene2_4_2_Impossibility_Results.construct(scene)
