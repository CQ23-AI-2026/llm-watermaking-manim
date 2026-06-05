from manim import *
import numpy as np
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_5(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_5.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)
    else:
        print(f"Warning: Voice file not found at {voice_file}")

    part_title = VGText("ĐIỂM MÙ & THIÊN KIẾN", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Tuy nhiên có một điểm mù nghiêm trọng..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Nhãn chủ đề phụ gọn gàng ở góc trái
    subtitle_bg = Rectangle(width=6.0, height=0.5, color=VG_RED, fill_color=BLACK, fill_opacity=0.8)
    subtitle_text = VGText("Thiên kiến: Người học tiếng Anh", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(subtitle_bg.get_center())
    subtitle = VGroup(subtitle_bg, subtitle_text).to_edge(UP, buff=1.2).to_edge(LEFT, buff=0.5)
    scene.play(FadeIn(subtitle, shift=RIGHT), run_time=1.0)
    
    # Hạ trục tọa độ xuống để có khoảng trống
    axes = Axes(
        x_range=[0, 10, 1], y_range=[0, 1, 0.2], 
        x_length=8.5, y_length=4.0, 
        axis_config={"color": VG_GRAY, "include_numbers": False}
    ).move_to(DOWN * 1.0)
    
    x_label = VGText("Độ phức tạp ngôn ngữ (Perplexity)", font_size=16, color=VG_GRAY).next_to(axes.x_axis, DOWN)
    scene.play(Create(axes), Write(x_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Vẽ đường phân phối độ phức tạp của AI..."
    scene.wait(1.5)
    # ---------------------------------------------------------
    
    def normal_dist(x, mu, sigma): return np.exp(-0.5 * ((x - mu) / sigma)**2)
        
    # AI Curve: Đỏ phát sáng
    ai_curve = axes.plot(lambda x: normal_dist(x, 2.5, 1.0), color=VG_RED)
    ai_glow = ai_curve.copy().set_stroke(VG_RED, width=8, opacity=0.3)
    ai_area = axes.get_area(ai_curve, color=VG_RED, opacity=0.2)
    ai_label = VGText("Văn bản AI", font_size=18, color=VG_RED, weight=BOLD_WEIGHT).next_to(ai_curve, UP).shift(LEFT * 2)
    
    scene.play(Create(ai_curve), FadeIn(ai_glow), FadeIn(ai_area), Write(ai_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "So sánh với người không phải bản xứ..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Non-native Curve: Màu Cyan/Blue sáng để hòa trộn với Đỏ tạo ra tím, không bị dơ
    non_native_curve = axes.plot(lambda x: normal_dist(x, 3.2, 1.2), color="#00FFFF")
    nn_glow = non_native_curve.copy().set_stroke("#00FFFF", width=8, opacity=0.3)
    non_native_area = axes.get_area(non_native_curve, color="#00FFFF", opacity=0.2)
    nn_label = VGText("Non-native\nSpeakers", font_size=16, color="#00FFFF", weight=BOLD_WEIGHT).next_to(non_native_curve, UP).shift(RIGHT * 1)
    
    scene.play(Create(non_native_curve), FadeIn(nn_glow), FadeIn(non_native_area), Write(nn_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Hai đường này đè lên nhau..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Vùng bị kết án nhầm (Highlight overlap)
    # Intersection is roughly from x=0 to x=4.0. We draw a bracket or highlight zone.
    zone_line = DashedLine(axes.c2p(4.2, 0), axes.c2p(4.2, normal_dist(4.2, 3.2, 1.2)), color=VG_GOLD, stroke_width=3)
    zone_arrow = DoubleArrow(axes.c2p(0, 0.1), axes.c2p(4.2, 0.1), color=VG_GOLD, stroke_width=2, tip_length=0.2)
    
    warning_box = RoundedRectangle(corner_radius=0.1, width=5.0, height=0.6, color=VG_RED, fill_color=VG_RED, fill_opacity=0.3)
    warning_text = VGText("[!] BỊ KẾT ÁN NHẦM LÀ AI", font_size=16, color=WHITE, weight=BOLD_WEIGHT).move_to(warning_box.get_center())
    warning_group = VGroup(warning_box, warning_text).next_to(zone_arrow, UP, buff=0.1)
    
    scene.play(Create(zone_line), Create(zone_arrow), FadeIn(warning_group, shift=UP), run_time=1.5)
    scene.play(Wiggle(warning_group, scale_value=1.05), run_time=0.8)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Kết án nhầm... Ngược lại, người bản xứ..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Native Curve: Màu Xanh lá cây
    native_curve = axes.plot(lambda x: normal_dist(x, 7.5, 1.5), color=VG_GREEN)
    native_glow = native_curve.copy().set_stroke(VG_GREEN, width=8, opacity=0.3)
    native_area = axes.get_area(native_curve, color=VG_GREEN, opacity=0.2)
    native_label = VGText("Native\nSpeakers", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(native_curve, UP).shift(RIGHT * 3.5)
    
    scene.play(Create(native_curve), FadeIn(native_glow), FadeIn(native_area), Write(native_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi hết voice
    scene.wait(4.0)
    # ---------------------------------------------------------
    
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
