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

    # 1. TITLE
    part_title = VGText("5.1: TỔNG KẾT HÀNH TRÌNH", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "hành trình kiểm soát máy móc tạo ngôn ngữ..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # Bốn khối vuông cho 4 phần
    box_args = {"width": 2.5, "height": 1.5, "fill_opacity": 0.2, "stroke_width": 2}
    
    box1 = Rectangle(color=VG_RED, **box_args).move_to(UP * 1.0 + LEFT * 3.0)
    text1 = VGText("Vũ khí hóa AI\n(Tin giả)", font_size=16, color=VG_RED).move_to(box1.get_center())
    group1 = VGroup(box1, text1)

    box2 = Rectangle(color=VG_GREEN, **box_args).move_to(UP * 1.0 + RIGHT * 3.0)
    text2 = VGText("Text Watermark\n(Danh sách xanh)", font_size=16, color=VG_GREEN).move_to(box2.get_center())
    group2 = VGroup(box2, text2)

    box3 = Rectangle(color=VG_GOLD, **box_args).move_to(DOWN * 1.5 + LEFT * 3.0)
    text3 = VGText("Model Watermark\n(Bảo vệ bản quyền)", font_size=16, color=VG_GOLD).move_to(box3.get_center())
    group3 = VGroup(box3, text3)

    box4 = Rectangle(color=VG_BLUE, **box_args).move_to(DOWN * 1.5 + RIGHT * 3.0)
    text4 = VGText("Phát hiện hậu kiểm\n(Máy dò AI)", font_size=16, color=VG_BLUE).move_to(box4.get_center())
    group4 = VGroup(box4, text4)

    scene.play(FadeIn(group1, shift=UP), run_time=1.0)
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc xong "Từ phần đầu tiên, vũ khí hóa AI..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    scene.play(FadeIn(group2, shift=UP), run_time=1.0)
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc xong "âm thầm điều hướng danh sách xanh..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    scene.play(FadeIn(group3, shift=UP), run_time=1.0)
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc xong "dấu vân tay ngầm và bài kiểm tra phản xạ..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    scene.play(FadeIn(group4, shift=UP), run_time=1.0)
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc xong "các máy dò AI quá mong manh..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # Quy tụ về trung tâm
    core_circle = Circle(radius=1.2, color=WHITE, fill_opacity=0.1, stroke_width=3).move_to(DOWN*0.25)
    core_text = VGText("AI CONTROL", font_size=20, color=WHITE, weight=BOLD_WEIGHT).move_to(core_circle.get_center())
    
    scene.play(
        Transform(group1, core_circle.copy()),
        Transform(group2, core_circle.copy()),
        Transform(group3, core_circle.copy()),
        Transform(group4, core_circle.copy()),
        FadeIn(core_circle),
        Write(core_text),
        run_time=2.0
    )

    # Năng lượng tỏa ra
    glow = core_circle.copy().set_fill(VG_BLUE, opacity=0.4).set_stroke(VG_BLUE, width=0)
    scene.play(glow.animate.scale(3).set_opacity(0), run_time=1.5, rate_func=linear)

    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi hết voice
    scene.wait(2.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
