from manim import *
import numpy as np
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_2(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_2.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)
    else:
        print(f"Warning: Voice file not found at {voice_file}")

    part_title = VGText("MACHINE LEARNING VS THỐNG KÊ", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Vậy làm sao để phân biệt văn bản AI và người thật? Chúng ta dựa vào hai chỉ số thống kê cốt lõi:"
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Hiển thị cả 2 tiêu đề ra trước
    perp_bg = Rectangle(width=4.0, height=0.5, color=VG_BLUE, fill_color=BLACK, fill_opacity=0.8)
    perp_text = VGText("1. Perplexity (Độ bối rối)", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(perp_bg.get_center())
    perplexity_title = VGroup(perp_bg, perp_text).to_edge(LEFT, buff=1.0).shift(UP * 1.2)

    burst_bg = Rectangle(width=4.0, height=0.5, color=VG_GOLD, fill_color=BLACK, fill_opacity=0.8)
    burst_text = VGText("2. Burstiness (Độ đột biến)", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(burst_bg.get_center())
    burst_title = VGroup(burst_bg, burst_text).to_edge(RIGHT, buff=1.0).shift(UP * 1.2)
    
    scene.play(FadeIn(perplexity_title, shift=RIGHT), FadeIn(burst_title, shift=LEFT), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1_5]: Đợi đọc "Perplexity (Độ bối rối) và Burstiness (Độ đột biến)."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Thứ nhất, Perplexity đo lường khả năng dự đoán từ tiếp theo..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # Lưới nền công nghệ mờ
    grid = NumberPlane(
        background_line_style={"stroke_color": VG_BLUE, "stroke_width": 1, "stroke_opacity": 0.1},
        axis_config={"stroke_opacity": 0}
    ).set_z_index(-10)

    axes_perplex = Axes(
        x_range=[0, 10, 1], y_range=[0, 10, 2], 
        x_length=5.5, y_length=3.5, 
        axis_config={"color": VG_GRAY, "include_numbers": False}
    ).next_to(perplexity_title, DOWN, buff=0.5).shift(RIGHT * 0.5)
    
    scene.play(FadeIn(grid), Create(axes_perplex), run_time=1.5)

    # AI Curve: Mượt mà và dễ đoán (Phát sáng)
    ai_curve = axes_perplex.plot(lambda x: 2.5 + 0.5 * np.sin(1.5 * x), color=VG_RED)
    ai_glow = ai_curve.copy().set_stroke(VG_RED, width=6, opacity=0.2)
    ai_group = VGroup(ai_glow, ai_curve)
    ai_label = VGText("AI", font_size=SMALL_FONT_SIZE, color=VG_RED, weight=BOLD_WEIGHT).next_to(ai_curve, UP, buff=0.2).shift(LEFT)
    scene.play(Create(ai_curve), FadeIn(ai_glow), Write(ai_label), run_time=2.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "AI luôn chọn những từ có xác suất cao nhất..."
    scene.wait(5.0)
    # ---------------------------------------------------------
    
    # Human Curve: Nhấp nhô và khó đoán (Đột biến)
    np.random.seed(42)
    human_curve = axes_perplex.plot(lambda x: 6.0 + 1.5 * np.sin(3 * x) + np.random.uniform(-1.5, 1.5), color=VG_GREEN)
    human_glow = human_curve.copy().set_stroke(VG_GREEN, width=6, opacity=0.2)
    human_group = VGroup(human_glow, human_curve)
    human_label = VGText("Human", font_size=SMALL_FONT_SIZE, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(human_curve, UP, buff=0.2).shift(LEFT)
    scene.play(Create(human_curve), FadeIn(human_glow), Write(human_label), run_time=2.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Ngược lại, con người hay dùng từ ngẫu hứng..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Thứ hai, Burstiness đo sự biến thiên chiều dài câu..."
    scene.wait(5.0)
    # ---------------------------------------------------------
    
    # AI Blocks: Đều tăm tắp (Data packets)
    ai_burst_label = VGText("AI:", font_size=SMALL_FONT_SIZE, color=VG_RED, weight=BOLD_WEIGHT).next_to(burst_title, DOWN, buff=1.0).align_to(burst_title, LEFT)
    ai_blocks = VGroup(*[RoundedRectangle(corner_radius=0.1, height=0.4, width=0.8, color=VG_RED, fill_opacity=0.6) for _ in range(5)])
    ai_blocks.arrange(RIGHT, buff=0.15).next_to(ai_burst_label, RIGHT, buff=0.3)
    scene.play(Write(ai_burst_label), Create(ai_blocks), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "AI tạo các câu dài bằng nhau..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Human Blocks: Ngắn dài lộn xộn
    human_burst_label = VGText("Human:", font_size=SMALL_FONT_SIZE, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(ai_burst_label, DOWN, buff=1.2).align_to(ai_burst_label, RIGHT)
    widths = [0.4, 1.8, 0.6, 2.2, 0.5]
    human_blocks = VGroup(*[RoundedRectangle(corner_radius=0.1, height=0.4, width=w, color=VG_GREEN, fill_opacity=0.6) for w in widths])
    human_blocks.arrange(RIGHT, buff=0.15).next_to(human_burst_label, RIGHT, buff=0.3)
    
    # Draw blocks falling with a nice tech effect
    scene.play(Write(human_burst_label))
    for block in human_blocks:
        scene.play(FadeIn(block, shift=DOWN*0.5), run_time=0.2)
        
    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi đọc "con người lúc ngắn lúc dài..."
    scene.wait(7.0)
    # ---------------------------------------------------------
    
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
