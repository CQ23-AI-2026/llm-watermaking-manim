from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_1(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_1.mp3")

    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 0. CENTRAL TITLE BUMPER
    bumper_title = VGText("BỨC TRANH TOÀN CẢNH", font_size=LARGE_FONT_SIZE + 4, color=WHITE, weight=BOLD_WEIGHT).move_to(UP*0.2)
    bumper_underline = Line(LEFT * 4, RIGHT * 4, color=VG_BLUE, stroke_width=2.5).next_to(bumper_title, DOWN, buff=0.2)
    
    scene.play(Write(bumper_title), run_time=1.0)
    scene.play(Create(bumper_underline), run_time=0.5)
    scene.wait(1.0)
    
    scene.play(FadeOut(bumper_title), FadeOut(bumper_underline), run_time=1.0)

    # 1. TITLE
    part_title = VGText("BỨC TRANH TOÀN CẢNH", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 3.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # 2. CENTRAL CONTROL CORE (PULSING)
    core_circle = Circle(radius=1.1, color=WHITE, fill_color=BLACK, fill_opacity=0.9, stroke_width=3).move_to(DOWN * 0.25)
    core_glow = core_circle.copy().set_stroke(VG_GOLD, width=8, opacity=0.4)
    core_text = VGText("CONTROL LLMs", font_size=18, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(core_circle.get_center())
    core = VGroup(core_circle, core_glow, core_text)

    scene.play(FadeIn(core, scale=0.5), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "hành trình kiểm soát máy móc tạo ngôn ngữ... bức tranh toàn cảnh"
    scene.wait(3.0)
    # ---------------------------------------------------------

    # Positions for 4 boxes
    p1 = UP * 1.5 + LEFT * 4.0
    p2 = UP * 1.5 + RIGHT * 4.0
    p3 = DOWN * 2.0 + LEFT * 4.0
    p4 = DOWN * 2.0 + RIGHT * 4.0

    box_args = {"width": 3.6, "height": 1.2, "fill_opacity": 0.2, "stroke_width": 2, "corner_radius": 0.1}

    # Box 1: Part 1
    box1 = RoundedRectangle(color=VG_RED, **box_args).move_to(p1)
    text1 = VGText("Rủi ro AI\n(Tin giả, đạo văn)", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).move_to(box1.get_center())
    group1 = VGroup(box1, text1)

    # Box 2: Part 2
    box2 = RoundedRectangle(color=VG_GREEN, **box_args).move_to(p2)
    text2 = VGText("Text Watermarking\n(KGW, Gumbel, Christ)", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(box2.get_center())
    group2 = VGroup(box2, text2)

    # Box 3: Part 3
    box3 = RoundedRectangle(color=VG_GOLD, **box_args).move_to(p3)
    text3 = VGText("Model Watermarking\n(Fingerprinting, DeepJudge)", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(box3.get_center())
    group3 = VGroup(box3, text3)

    # Box 4: Part 4
    box4 = RoundedRectangle(color=VG_BLUE, **box_args).move_to(p4)
    text4 = VGText("Post-hoc detection\n(False Positives)", font_size=14, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(box4.get_center())
    group4 = VGroup(box4, text4)

    # Connection lines from Core Center to Boxes
    line1 = DashedLine(core_circle.get_center(), box1.get_corner(DOWN + RIGHT), color=VG_RED, stroke_width=2).set_z_index(-1)
    line2 = DashedLine(core_circle.get_center(), box2.get_corner(DOWN + LEFT), color=VG_GREEN, stroke_width=2).set_z_index(-1)
    line3 = DashedLine(core_circle.get_center(), box3.get_corner(UP + RIGHT), color=VG_GOLD, stroke_width=2).set_z_index(-1)
    line4 = DashedLine(core_circle.get_center(), box4.get_corner(UP + LEFT), color=VG_BLUE, stroke_width=2).set_z_index(-1)

    # Pulsing core micro-animation
    scene.play(core_glow.animate.scale(1.2).set_opacity(0.1), run_time=1.0)
    core_glow.scale(1.0/1.2).set_opacity(0.4) # Reset

    # --- ACTIVATE PART 1 ---
    scene.play(Create(line1), run_time=1.0)
    scene.play(FadeIn(group1, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc xong "Từ phần đầu tiên, vũ khí hóa AI..."
    scene.wait(5.5)
    # ---------------------------------------------------------

    # --- ACTIVATE PART 2 ---
    scene.play(Create(line2), run_time=1.0)
    scene.play(FadeIn(group2, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc xong "đọc xong phần 2..."
    scene.wait(15.5)
    # ---------------------------------------------------------

    # --- ACTIVATE PART 3 ---
    scene.play(Create(line3), run_time=1.0)
    scene.play(FadeIn(group3, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc xong "đọc xong phần 3..."
    scene.wait(14.5)
    # ---------------------------------------------------------

    # --- ACTIVATE PART 4 ---
    scene.play(Create(line4), run_time=1.0)
    scene.play(FadeIn(group4, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc xong "đọc xong phần 4..."
    scene.wait(11)
    # ---------------------------------------------------------

    # --- CONVERGENCE & SHOCKWAVE ---
    # Draw energy flowing back to the core
    back_line1 = line1.copy().set_color(WHITE).set_stroke(width=3)
    back_line2 = line2.copy().set_color(WHITE).set_stroke(width=3)
    back_line3 = line3.copy().set_color(WHITE).set_stroke(width=3)
    back_line4 = line4.copy().set_color(WHITE).set_stroke(width=3)

    scene.play(
        ShowPassingFlash(back_line1, time_width=0.5),
        ShowPassingFlash(back_line2, time_width=0.5),
        ShowPassingFlash(back_line3, time_width=0.5),
        ShowPassingFlash(back_line4, time_width=0.5),
        run_time=1.5
    )

    # Core flares up and sends a shockwave to clear the screen
    shockwave = Circle(radius=1.1, color=VG_GOLD, stroke_width=4).move_to(core_circle.get_center())
    scene.add(shockwave)
    
    scene.play(
        shockwave.animate.scale(8.0).set_opacity(0),
        FadeOut(group1), FadeOut(group2), FadeOut(group3), FadeOut(group4),
        FadeOut(line1), FadeOut(line2), FadeOut(line3), FadeOut(line4),
        FadeOut(core), FadeOut(part_title), FadeOut(underline),
        run_time=2.0,
        rate_func=exponential_decay
    )

    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi hết voice
    scene.wait(0.1)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)
