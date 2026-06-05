from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_3(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_3.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)
    else:
        print(f"Warning: Voice file not found at {voice_file}")

    part_title = VGText("MÔ PHỎNG DETECTGPT", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # Lưới nền mờ
    grid = NumberPlane(
        background_line_style={"stroke_color": VG_BLUE, "stroke_width": 1, "stroke_opacity": 0.1},
        axis_config={"stroke_opacity": 0}
    ).set_z_index(-10)
    scene.play(FadeIn(grid))

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Một thuật toán nổi tiếng là DetectGPT..."
    scene.wait(4.0)
    # ---------------------------------------------------------
    
    # HUD Terminal Box
    terminal_bg = RoundedRectangle(corner_radius=0.1, width=13, height=1.5, color=VG_BLUE, stroke_width=2, fill_color=BLACK, fill_opacity=0.8)
    terminal_bg.move_to(UP * 1.2)
    terminal_header = Rectangle(width=13, height=0.3, color=VG_BLUE, stroke_width=0, fill_color=VG_BLUE, fill_opacity=0.3).align_to(terminal_bg, UP)
    terminal_dot = Circle(radius=0.05, color=VG_RED, fill_opacity=1).move_to(terminal_header.get_left() + RIGHT*0.2)
    
    sentence = VGText("Bức tranh Mona Lisa được vẽ bởi Leonardo da Vinci", font_size=DEFAULT_FONT_SIZE, color=WHITE)
    sentence.move_to(terminal_bg.get_center() + DOWN*0.1)
    
    terminal_group = VGroup(terminal_bg, terminal_header, terminal_dot, sentence)
    scene.play(FadeIn(terminal_group, shift=UP), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Ví dụ ta có câu văn mượt mà..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Gauge Meter (Thanh năng lượng Log-Probability)
    meter_label = VGText("Log-Probability Score", font_size=18, color=VG_GRAY).move_to(DOWN * 0.5 + LEFT * 2)
    meter_bg = Rectangle(width=4.0, height=0.4, color=VG_GRAY, stroke_width=2, fill_opacity=0).next_to(meter_label, DOWN, buff=0.2)
    
    tracker = ValueTracker(0.8) # 80%
    
    # A cleaner way to do progress bar
    meter_bar = always_redraw(
        lambda: Rectangle(
            width=max(0.01, 4.0 * tracker.get_value()), height=0.38, 
            color=VG_GREEN if tracker.get_value() > 0.4 else VG_RED, 
            stroke_width=0, fill_opacity=0.8
        ).next_to(meter_bg.get_left(), RIGHT, buff=0.01)
    )
    
    score_val = always_redraw(
        lambda: VGText(f"{int(tracker.get_value()*100)}%", font_size=20, color=VG_GREEN if tracker.get_value() > 0.4 else VG_RED)
        .next_to(meter_bg, RIGHT, buff=0.3)
    )
    
    meter_group = VGroup(meter_label, meter_bg, meter_bar, score_val)
    scene.play(FadeIn(meter_group), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Xác suất tự nhiên đang rất cao..."
    scene.wait(4.0)
    # ---------------------------------------------------------
    
    shake_bg = Rectangle(width=5.5, height=0.5, color=VG_GOLD, fill_color=BLACK, fill_opacity=0.8)
    shake_text = VGText("Mô phỏng: Rung lắc từ vựng", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(shake_bg.get_center())
    shake_label = VGroup(shake_bg, shake_text).move_to(DOWN * 0.5 + RIGHT * 3)
    scene.play(FadeIn(shake_label, shift=LEFT), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "thay thế một vài từ ngẫu nhiên..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    # Hiệu ứng Glitch (rung lắc) và biến đổi từ
    new_sentence = VGText("Bức tranh Mona Lisa được sáng tác bởi Leonardo da Vinci", font_size=DEFAULT_FONT_SIZE, color=WHITE, t2c={"sáng tác": VG_RED})
    new_sentence.move_to(terminal_bg.get_center() + DOWN*0.1)
    
    scene.play(Wiggle(sentence, scale_value=1.05, rotation_angle=0.02), run_time=0.5)
    scene.play(Transform(sentence, new_sentence), flash_color=VG_RED, run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "ngay lập tức điểm xác suất tụt thê thảm..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Tụt thanh năng lượng
    scene.play(tracker.animate.set_value(0.15), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "sự sụt giảm sâu này là lời thú tội..."
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    conclusion_box = RoundedRectangle(corner_radius=0.1, width=10, height=0.8, color=VG_RED, stroke_width=2, fill_color=VG_RED, fill_opacity=0.2)
    conclusion_text = VGText("[!] PHÁT HIỆN AI: XÁC SUẤT SỤT GIẢM ĐỘT NGỘT", font_size=20, color=VG_RED, weight=BOLD_WEIGHT).move_to(conclusion_box.get_center())
    conclusion = VGroup(conclusion_box, conclusion_text).move_to(DOWN * 2.5)
    
    scene.play(FadeIn(conclusion, shift=UP), run_time=1.5)
    scene.play(Wiggle(conclusion, scale_value=1.02), run_time=0.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi âm thanh kết thúc
    scene.wait(3.0)
    # ---------------------------------------------------------
    
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
