import os
from manim import *
from config.style import VGText, VG_GOLD, VG_GRAY, VG_BLUE, VG_ORANGE, VG_GREEN, BOLD_WEIGHT

def play_part1_scene_1_0(scene: Scene) -> None:
    # Optional audio attachment
    voice_path = os.path.join("scenes", "part1", "voice", "1_0.mp3")
    if os.path.exists(voice_path):
        scene.add_sound(voice_path)

    scene.camera.background_color = BLACK

    # ==========================================
    # GIAI ĐOẠN 1
    # ==========================================
    sentence = "Bạn đang đọc những dòng này."
    words = sentence.split(" ")
    word_mobs = VGroup(*[VGText(w, font_size=40, color=WHITE, weight="NORMAL") for w in words])
    word_mobs.arrange(RIGHT, buff=0.15)
    word_mobs.move_to(ORIGIN)

    animations = []
    for word in word_mobs:
        animations.append(FadeIn(word, run_time=0.25))
    
    # lag_ratio = 0.15 / 0.25 = 0.6
    scene.play(AnimationGroup(*animations, lag_ratio=0.6))
    scene.wait(1.2)

    line2 = VGText("Ai đã viết chúng?", font_size=48, weight=BOLD_WEIGHT, color=VG_GOLD)
    line2.move_to(DOWN * 1.0)
    scene.play(FadeIn(line2, scale=0.9), run_time=0.7)
    scene.wait(1.5)

    # ==========================================
    # GIAI ĐOẠN 2
    # ==========================================
    scene.play(FadeOut(word_mobs), FadeOut(line2), run_time=0.5)

    lines = [
        "Biến đổi khí hậu là một trong những thách thức lớn nhất",
        "mà nhân loại phải đối mặt trong thế kỷ 21. Các nhà khoa học",
        "cảnh báo rằng nếu không có hành động kịp thời, hậu quả sẽ",
        "không thể đảo ngược."
    ]
    par_group = VGroup(*[VGText(line, font_size=26, color=WHITE) for line in lines])
    par_group.arrange(DOWN, buff=0.2)
    par_group.move_to(ORIGIN)

    scene.play(Write(par_group, run_time=3.0))

    cursor = Rectangle(width=0.05, height=0.35, color=WHITE)
    cursor.set_fill(WHITE, opacity=1)
    last_char = par_group[-1][-1]
    cursor.next_to(last_char, RIGHT, buff=0.05)

    scene.add(cursor)
    for _ in range(3):
        scene.play(FadeOut(cursor), run_time=0.2)
        scene.play(FadeIn(cursor), run_time=0.2)
    scene.remove(cursor)

    scene.wait(1.0)

    # Split screen
    split_line = Line(UP * 4, DOWN * 4, color=VG_GRAY, stroke_width=1.5)
    scene.play(Create(split_line), run_time=0.6)

    left_rect = Rectangle(width=config.frame_width/2, height=config.frame_height, color=VG_BLUE, stroke_width=0, fill_opacity=0.08)
    left_rect.move_to(LEFT * config.frame_width / 4)

    right_rect = Rectangle(width=config.frame_width/2, height=config.frame_height, color=VG_ORANGE, stroke_width=0, fill_opacity=0.08)
    right_rect.move_to(RIGHT * config.frame_width / 4)

    left_label = VGText("Người viết?", font_size=28, weight=BOLD_WEIGHT, color=VG_BLUE)
    left_label.move_to(LEFT * config.frame_width / 4 + UP * 2.5)

    right_label = VGText("AI viết?", font_size=28, weight=BOLD_WEIGHT, color=VG_ORANGE)
    right_label.move_to(RIGHT * config.frame_width / 4 + UP * 2.5)

    scene.play(
        FadeIn(left_rect),
        FadeIn(left_label),
        FadeIn(right_rect),
        FadeIn(right_label),
        run_time=0.5
    )
    
    scene.wait(1.5)

    # ==========================================
    # GIAI ĐOẠN 3
    # ==========================================
    scene.play(
        FadeOut(par_group),
        FadeOut(left_rect),
        FadeOut(left_label),
        FadeOut(right_rect),
        FadeOut(right_label),
        run_time=0.6
    )
    scene.play(FadeOut(split_line), run_time=0.4)
    scene.wait(0.3)

    line3_1 = VGText("Nếu bạn không thể phân biệt —", font_size=34, color=VG_GRAY, slant="ITALIC")
    line3_1.move_to(UP * 0.6)
    scene.play(FadeIn(line3_1, shift=UP*0.15), run_time=0.7)
    
    scene.wait(0.8)

    line3_2 = VGText("thì ai sẽ chịu trách nhiệm?", font_size=38, weight=BOLD_WEIGHT, color=WHITE)
    line3_2.move_to(ORIGIN)
    scene.play(FadeIn(line3_2, shift=UP*0.15), run_time=0.7)
    
    scene.wait(1.0)

    line3_3 = VGText("→  Đó là lý do Watermark tồn tại.", font_size=28, color=VG_GREEN)
    line3_3.move_to(DOWN * 1.0)
    scene.play(FadeIn(line3_3), run_time=0.6)
    
    scene.wait(1.5)


class Scene10_Hook(Scene):
    def construct(self):
        play_part1_scene_1_0(self)
