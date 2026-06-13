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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class Scene1_2_Core_Differences(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "voice", "voice_1_2.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 20.0
        total_expected_wait = 60.0  # Ước tính
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Thiết lập bố cục so sánh
        title = MarkupText("1.2 SỰ KHÁC BIỆT CỐT LÕI", font="CMU Serif", font_size=32, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.0)

        center_line = DashedLine(UP * 2.5, DOWN * 3.5, color=GRAY)
        self.play(Create(center_line), run_time=1.0)

        left_title = MarkupText("Watermark Truyền Thống (1990s)", font="CMU Serif", font_size=24, color=WHITE)
        left_title.move_to(LEFT * 3.5 + UP * 2.5)
        
        right_title = MarkupText("Watermark cho GenAI", font="CMU Serif", font_size=24, color=WHITE)
        right_title.move_to(RIGHT * 3.5 + UP * 2.5)

        self.play(Write(left_title), Write(right_title), run_time=1.5)
        synced_wait(3.0)

        # Giai đoạn 2: Cột trái - Tư duy "Hậu xử lý" (Post-processing)
        left_group = VGroup()
        
        # Camera
        camera_body = Rectangle(width=1.0, height=0.6, color=WHITE, fill_color=GRAY, fill_opacity=0.8)
        camera_lens = Circle(radius=0.2, color=WHITE, fill_color=BLACK, fill_opacity=1).move_to(camera_body.get_center())
        camera_flash = Rectangle(width=0.3, height=0.15, color=WHITE, fill_color=WHITE, fill_opacity=1).next_to(camera_body.get_top(), UP, buff=0)
        camera = VGroup(camera_body, camera_lens, camera_flash).move_to(LEFT * 5 + UP * 0.5)
        
        arrow_left = Arrow(camera.get_right(), camera.get_right() + RIGHT * 1.5, color=WHITE)
        
        # Picture
        pic_bg = Rectangle(width=1.5, height=1.0, color=WHITE, fill_color=BLUE_E, fill_opacity=0.8)
        pic_sun = Circle(radius=0.15, color=YELLOW, fill_color=YELLOW, fill_opacity=1).move_to(pic_bg.get_corner(UR) + LEFT*0.3 + DOWN*0.3)
        pic_mountain = Polygon(pic_bg.get_corner(DL), pic_bg.get_corner(DR), pic_bg.get_bottom() + UP*0.5, color=GREEN, fill_color=GREEN, fill_opacity=1)
        picture = VGroup(pic_bg, pic_sun, pic_mountain).next_to(arrow_left, RIGHT, buff=0.2)
        
        left_group.add(camera, arrow_left, picture)
        
        self.play(FadeIn(camera, shift=UP*0.2), run_time=1.0)
        self.play(Create(arrow_left), run_time=0.5)
        self.play(DrawBorderThenFill(picture), run_time=1.5)
        
        # Stamp dropping
        stamp_handle = Rectangle(width=0.2, height=0.4, color=WHITE, fill_color=RED_E, fill_opacity=1)
        stamp_base = Rectangle(width=0.6, height=0.2, color=WHITE, fill_color=RED, fill_opacity=1).next_to(stamp_handle, DOWN, buff=0)
        stamp = VGroup(stamp_handle, stamp_base)
        stamp.move_to(picture.get_center() + UP * 2)
        
        wm_mark = Text("WM", font_size=20, color=RED, weight=BOLD).move_to(picture.get_center()).set_opacity(0)
        
        self.play(stamp.animate.move_to(picture.get_center() + UP*0.1), run_time=0.5, rate_func=rush_into)
        self.play(wm_mark.animate.set_opacity(0.8), stamp.animate.shift(UP * 0.5), run_time=0.5)
        self.play(FadeOut(stamp), run_time=0.5)
        
        left_group.add(stamp, wm_mark)
        
        # Text under left column
        left_text_1 = MarkupText("Cách tiếp cận: Xử lý hậu kỳ (Post-processing)", font="CMU Serif", font_size=18, color=LIGHT_GRAY)
        left_text_2 = MarkupText("Tính chất: Thụ động", font="CMU Serif", font_size=18, color=RED_A)
        left_texts = VGroup(left_text_1, left_text_2).arrange(DOWN, aligned_edge=LEFT).next_to(picture, DOWN, buff=1.0).shift(LEFT * 1.5)
        
        self.play(Write(left_texts), run_time=1.5)
        left_group.add(left_texts)
        synced_wait(19.0)

        # Giai đoạn 3: Cột phải - Tư duy "Can thiệp trực tiếp"
        right_group = VGroup()
        
        # Black Box Model
        model_box = RoundedRectangle(width=2.0, height=1.5, corner_radius=0.2, color=PURPLE, fill_color=PURPLE_E, fill_opacity=0.8)
        model_nodes = VGroup(*[Dot(color=WHITE, radius=0.08) for _ in range(5)])
        model_nodes.arrange_in_grid(rows=2, cols=3, buff=0.4).move_to(model_box.get_center())
        model_edges = VGroup(
            Line(model_nodes[0].get_center(), model_nodes[3].get_center(), stroke_width=1, color=GRAY),
            Line(model_nodes[0].get_center(), model_nodes[4].get_center(), stroke_width=1, color=GRAY),
            Line(model_nodes[1].get_center(), model_nodes[3].get_center(), stroke_width=1, color=GRAY),
            Line(model_nodes[1].get_center(), model_nodes[4].get_center(), stroke_width=1, color=GRAY),
            Line(model_nodes[2].get_center(), model_nodes[4].get_center(), stroke_width=1, color=GRAY),
        )
        model = VGroup(model_box, model_edges, model_nodes).move_to(RIGHT * 2.5 + UP * 0.5)
        
        # Injecting Stamp/Key
        key = Star(color=YELLOW, fill_opacity=1).scale(0.3).move_to(model.get_top() + UP * 1.5)
        
        self.play(FadeIn(model, shift=UP*0.2), run_time=1.0)
        
        self.play(key.animate.move_to(model.get_center()), run_time=1.0)
        self.play(Flash(model.get_center(), color=YELLOW, flash_radius=1.0), key.animate.set_opacity(0), run_time=0.5)
        
        model_box.set_stroke(color=YELLOW, width=4) # Glow effect
        
        arrow_right = Arrow(model.get_right(), model.get_right() + RIGHT * 1.0, color=WHITE)
        self.play(Create(arrow_right), run_time=0.5)
        
        # Emitting blocks
        text_blocks = VGroup(*[Rectangle(width=0.4, height=0.3, color=YELLOW, fill_color=YELLOW_E, fill_opacity=0.8) for _ in range(3)])
        text_blocks.arrange(RIGHT, buff=0.1).next_to(arrow_right, RIGHT, buff=0.1)
        
        self.play(LaggedStart(*[FadeIn(block, shift=RIGHT*0.2) for block in text_blocks], lag_ratio=0.3), run_time=1.5)
        
        right_group.add(model, key, arrow_right, text_blocks)
        
        # Text under right column
        right_text_1 = MarkupText("Cách tiếp cận: Truy cập quá trình sinh", font="CMU Serif", font_size=18, color=LIGHT_GRAY)
        right_text_2 = MarkupText("Tính chất: Chủ động", font="CMU Serif", font_size=18, color=GREEN_A)
        right_texts = VGroup(right_text_1, right_text_2).arrange(DOWN, aligned_edge=LEFT).next_to(model, DOWN, buff=1.0)
        
        self.play(Write(right_texts), run_time=1.5)
        right_group.add(right_texts)
        synced_wait(30.0)

        # Giai đoạn 4: Tổng kết
        self.play(
            FadeOut(center_line),
            left_group.animate.set_opacity(0.2),
            right_group.animate.set_opacity(0.2),
            left_title.animate.set_opacity(0.2),
            right_title.animate.set_opacity(0.2),
            run_time=1.5
        )
        
        final_msg = MarkupText("Watermark GenAI không phải là cái mác dán thêm,\nnó là một phần của quá trình tư duy.", font="CMU Serif", font_size=28, color=YELLOW, justify=True)
        final_box = SurroundingRectangle(final_msg, color=GOLD, buff=0.5, stroke_width=2)
        final_group = VGroup(final_box, final_msg).move_to(ORIGIN).shift(DOWN * 1.5)
        
        self.play(Create(final_box), Write(final_msg), run_time=2.0)
        self.play(Flash(final_box, color=YELLOW, line_length=0.4), run_time=1.0)
        synced_wait(25.0)
        
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(2.0)
            
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_part1_scene_1_2(scene: Scene) -> None:
    Scene1_2_Core_Differences.construct(scene)
