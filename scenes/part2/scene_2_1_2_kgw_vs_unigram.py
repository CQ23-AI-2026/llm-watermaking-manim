import os
from manim import *
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_RED,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class Scene2_1_2_KGW_vs_Unigram(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_2.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Bước 1: Chia đôi màn hình
        dashed_line = DashedLine(LEFT * 7, RIGHT * 7, color=VG_GRAY)
        self.play(Create(dashed_line), run_time=1.0)

        # Tiêu đề 2 nửa
        title_kgw = VGText("KGW Watermark (m = 2)", font_size=28, weight=BOLD_WEIGHT, color=WHITE)
        title_kgw.to_edge(UP, buff=0.2).to_edge(LEFT, buff=0.5)
        
        title_unigram = VGText("Unigram Watermark (m = 1)", font_size=28, weight=BOLD_WEIGHT, color=WHITE)
        title_unigram.next_to(dashed_line, DOWN, buff=0.2).to_edge(LEFT, buff=0.5)

        self.play(Write(title_kgw), Write(title_unigram), run_time=1.0)
        self.wait(10.0) # Đợi giới thiệu 2 triết lý

        # Hàm tạo một ô text
        def create_token(text):
            box = Rectangle(width=1.2, height=0.6, color=VG_BLUE, fill_opacity=0.2)
            lbl = VGText(text, font_size=24).move_to(box.get_center())
            return VGroup(box, lbl)

        # Hàm tạo bảng Green List mini
        def create_gl_grid():
            grid = VGroup()
            for i in range(4):
                color = VG_GREEN if i % 2 == 0 else VG_RED
                rect = Rectangle(width=0.4, height=0.4, fill_color=color, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
                grid.add(rect)
            grid.arrange(RIGHT, buff=0)
            lbl = VGText("Green List", font_size=20).next_to(grid, UP, buff=0.1)
            return VGroup(lbl, grid)
            
        def shuffle_grid(grid_group):
            grid = grid_group[1]
            import random
            colors = [VG_GREEN, VG_RED, VG_GREEN, VG_RED]
            random.shuffle(colors)
            anims = []
            for rect, color in zip(grid, colors):
                anims.append(rect.animate.set_fill(color))
            return anims

        # Bước 2: Nửa trên (KGW)
        t_the = create_token("The").move_to(UP * 2 + LEFT * 4)
        arrow1 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(t_the, RIGHT, buff=0.2)
        t_cat = create_token("cat").next_to(arrow1, RIGHT, buff=0.2)
        arrow2 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(t_cat, RIGHT, buff=0.2)
        t_sat = create_token("sat").next_to(arrow2, RIGHT, buff=0.2)

        gl_kgw = create_gl_grid().next_to(t_sat, RIGHT, buff=1.0)
        top_group = VGroup(t_the, arrow1, t_cat, arrow2, t_sat, gl_kgw)

        self.play(FadeIn(t_the, shift=RIGHT), FadeIn(gl_kgw), run_time=1.0)
        self.wait(5.0)

        # KGW thay đổi Green List tại mỗi bước
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(FadeIn(t_cat, shift=RIGHT), *shuffle_grid(gl_kgw), run_time=1.0)
        self.wait(5.0)
        
        self.play(GrowArrow(arrow2), run_time=0.5)
        self.play(FadeIn(t_sat, shift=RIGHT), *shuffle_grid(gl_kgw), run_time=1.0)
        self.wait(6.0)

        # Bước 3: Nửa dưới (Unigram)
        u_the = create_token("The").move_to(DOWN * 2 + LEFT * 4)
        u_arrow1 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(u_the, RIGHT, buff=0.2)
        u_dog = create_token("dog").next_to(u_arrow1, RIGHT, buff=0.2)
        u_arrow2 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(u_dog, RIGHT, buff=0.2)
        u_ran = create_token("ran").next_to(u_arrow2, RIGHT, buff=0.2)

        gl_uni = create_gl_grid().next_to(u_ran, RIGHT, buff=1.0)
        bottom_group = VGroup(u_the, u_arrow1, u_dog, u_arrow2, u_ran, gl_uni)

        self.play(FadeIn(u_the, shift=RIGHT), FadeIn(gl_uni), run_time=1.0)
        self.wait(4.0)

        # Unigram Green List KHÔNG thay đổi
        self.play(GrowArrow(u_arrow1), run_time=0.5)
        self.play(FadeIn(u_dog, shift=RIGHT), run_time=1.0)
        self.wait(4.0)

        self.play(GrowArrow(u_arrow2), run_time=0.5)
        self.play(FadeIn(u_ran, shift=RIGHT), run_time=1.0)
        self.wait(5.0)

        # Bước 4: Điểm nhấn Robustness (Highlight)
        self.play(
            top_group.animate.set_opacity(0.3),
            bottom_group.animate.set_opacity(0.3),
            title_kgw.animate.set_opacity(0.3),
            dashed_line.animate.set_opacity(0.3),
            run_time=1.5
        )
        self.wait(2.0)

        box_text = VGText(
            "Unigram tốt hơn KGW trong\nmột số trường hợp tấn công\nchỉnh sửa (Edits)",
            font_size=26,
            color=WHITE
        )
        box_rect = SurroundingRectangle(box_text, color=VG_GOLD, buff=0.3, corner_radius=0.2)
        box_group = VGroup(box_rect, box_text).to_edge(RIGHT, buff=0.5)

        self.play(FadeIn(box_group, shift=LEFT), run_time=1.0)
        self.wait(4.0)

        fixed_list_text = VGText("Green list cố định", font_size=28, color=VG_GOLD, weight=BOLD_WEIGHT)
        fixed_list_text.next_to(title_unigram, DOWN, buff=0.4).align_to(title_unigram, LEFT).shift(RIGHT * 0.5)

        self.play(Write(fixed_list_text), run_time=1.0)
        self.play(Wiggle(fixed_list_text, scale_value=1.3), run_time=1.5)
        
        # Nhấn mạnh thêm cái bảng cố định
        self.play(gl_uni.animate.scale(1.3), run_time=0.8)
        self.play(gl_uni.animate.scale(1/1.3), run_time=0.8)
        
        # Audio wait
        elapsed_time = self.renderer.time - start_time
        wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
        if wait_time > 0:
            self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_2(scene: Scene) -> None:
    Scene2_1_2_KGW_vs_Unigram.construct(scene)
