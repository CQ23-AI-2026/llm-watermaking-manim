from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_2(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_2.mp3")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("5.2: BỐN TỬ HUYỆT CỦA WATERMARK", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "đối mặt với 4 tử huyệt chưa có lời giải..."
    scene.wait(3.0)
    # ---------------------------------------------------------

    # CHIA 4 GÓC MÀN HÌNH
    # 1. Low Entropy (Cạn kiệt không gian)
    tl_title = VGText("1. Low-Entropy", font_size=18, color=VG_RED).move_to(UP*2.0 + LEFT*3.5)
    wall_left = Line(UP*0.5, DOWN*1.5, color=WHITE).move_to(UP*0.5 + LEFT*4.0)
    wall_right = Line(UP*0.5, DOWN*1.5, color=WHITE).move_to(UP*0.5 + LEFT*3.0)
    word = VGText("1+1=2", font_size=14, color=VG_GREEN).move_to(UP*1.0 + LEFT*3.5)
    
    scene.play(Write(tl_title), Create(wall_left), Create(wall_right), FadeIn(word), run_time=1.5)
    scene.play(word.animate.shift(DOWN*2.0), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Sự cạn kiệt không gian tự do... nói sai sự thật."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # 2. Paraphrasing (Máy giặt ngôn ngữ)
    tr_title = VGText("2. Paraphrasing Attack", font_size=18, color=VG_GOLD).move_to(UP*2.0 + RIGHT*3.5)
    machine = Circle(radius=0.8, color=VG_GRAY).move_to(UP*0.5 + RIGHT*3.5)
    spinner = Arc(radius=0.5, angle=PI, color=VG_BLUE).move_to(machine.get_center())
    
    green_text = VGText("Text", font_size=14, color=VG_GREEN).move_to(UP*1.5 + RIGHT*5.0)
    red_text = VGText("Text", font_size=14, color=VG_RED).move_to(DOWN*0.5 + RIGHT*2.0)

    scene.play(Write(tr_title), Create(machine), Create(spinner), run_time=1.5)
    scene.play(green_text.animate.move_to(machine.get_center()), run_time=0.5)
    
    # Spin animation
    scene.play(Rotate(spinner, angle=4*PI), FadeOut(green_text), run_time=1.5)
    scene.play(FadeIn(red_text, shift=DOWN), run_time=0.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Rửa tiền ngôn ngữ... đảo từ đồng nghĩa..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # 3. Copy-Paste (Pha loãng)
    bl_title = VGText("3. Pha loãng (Copy-Paste)", font_size=18, color=VG_BLUE).move_to(DOWN*1.0 + LEFT*3.5)
    cup_left = Line(UP*0.5, DOWN*0.5, color=WHITE).move_to(DOWN*2.0 + LEFT*4.0)
    cup_right = Line(UP*0.5, DOWN*0.5, color=WHITE).move_to(DOWN*2.0 + LEFT*3.0)
    cup_bottom = Line(LEFT*0.5, RIGHT*0.5, color=WHITE).move_to(DOWN*2.5 + LEFT*3.5)
    water = Rectangle(width=1.0, height=0.6, color=VG_GRAY, fill_opacity=0.3).move_to(DOWN*2.2 + LEFT*3.5)
    
    drop = Circle(radius=0.1, color=VG_GREEN, fill_opacity=1).move_to(DOWN*1.0 + LEFT*3.5)

    scene.play(Write(bl_title), Create(cup_left), Create(cup_right), Create(cup_bottom), FadeIn(water), run_time=1.5)
    scene.play(drop.animate.move_to(water.get_center()), run_time=0.5)
    scene.play(FadeOut(drop), water.animate.set_fill(VG_GREEN, opacity=0.1), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Pha loãng 80% tay 20% AI..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # 4. Butterfly Effect
    br_title = VGText("4. Hiệu ứng cánh bướm", font_size=18, color=VG_RED).move_to(DOWN*1.0 + RIGHT*3.5)
    nodes = VGroup(*[Circle(radius=0.15, color=VG_GREEN, fill_opacity=1) for _ in range(4)])
    nodes.arrange(RIGHT, buff=0.3).move_to(DOWN*2.0 + RIGHT*3.5)
    lines = VGroup(*[Line(nodes[i].get_right(), nodes[i+1].get_left(), color=WHITE) for i in range(3)])

    scene.play(Write(br_title), FadeIn(nodes), FadeIn(lines), run_time=1.5)
    
    # Kẻ gian đẩy nhịp 1
    scene.play(nodes[0].animate.set_color(VG_RED), run_time=0.3)
    for i in range(1, 4):
        scene.play(nodes[i].animate.set_color(VG_RED), lines[i-1].animate.set_color(VG_RED), run_time=0.2)

    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Thay đổi MỘT TỪ, toàn bộ dây chuyền trật nhịp..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
