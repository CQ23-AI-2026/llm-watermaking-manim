from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_4(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_4.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)
    else:
        print(f"Warning: Voice file not found at {voice_file}")

    part_title = VGText("RADAR: HỌC ĐỐI KHÁNG", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
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
    # [WAIT_SYNC_1]: Đợi đọc "RADAR là một hệ thống học đối kháng..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # AI Cảnh sát (Detector) - Hình Khiên (Lục giác)
    det_shape = RegularPolygon(n=6, color=VG_BLUE, stroke_width=4, fill_opacity=0.2).scale(1.2)
    det_icon = Star(n=4, outer_radius=0.3, inner_radius=0.15, color=VG_BLUE, fill_opacity=1).move_to(det_shape.get_center())
    det_label = VGText("Detector\n(Cảnh sát)", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(det_shape, DOWN)
    detector = VGroup(det_shape, det_icon, det_label).move_to(LEFT * 3.5 + DOWN * 0.2)
    
    # AI Kẻ làm giả (Paraphraser) - Hình Thoi (Hacker)
    para_shape = Square(color=VG_RED, stroke_width=4, fill_opacity=0.2).rotate(PI/4).scale(1.2)
    para_icon = RegularPolygon(n=3, color=VG_RED, fill_opacity=1).scale(0.4).rotate(PI).move_to(para_shape.get_center())
    para_label = VGText("Paraphraser\n(Kẻ làm giả)", font_size=18, color=VG_RED, weight=BOLD_WEIGHT).next_to(para_shape, DOWN)
    paraphraser = VGroup(para_shape, para_icon, para_label).move_to(RIGHT * 3.5 + DOWN * 0.2)
    
    scene.play(FadeIn(detector, shift=RIGHT), FadeIn(paraphraser, shift=LEFT), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Giữa cảnh sát và kẻ làm giả..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Đường truyền dữ liệu: Kẻ làm giả -> Cảnh sát
    path_top = ArcBetweenPoints(paraphraser[0].get_top() + UP*0.2, detector[0].get_top() + UP*0.2, angle=-TAU/4, color=VG_RED, stroke_width=2)
    path_top_glow = path_top.copy().set_stroke(VG_RED, width=10, opacity=0.3)
    text_fake = VGText("Gửi văn bản giả mạo", font_size=16, color=VG_RED).next_to(path_top, UP)
    
    scene.play(Create(path_top), FadeIn(path_top_glow), Write(text_fake), run_time=1.5)
    
    # Data flow animation
    data_packet1 = Circle(radius=0.1, color=WHITE, fill_opacity=1).set_z_index(5)
    scene.play(MoveAlongPath(data_packet1, path_top), run_time=1.0)
    scene.play(FadeOut(data_packet1), run_time=0.2)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Kẻ làm giả gửi văn bản giả..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Đường truyền dữ liệu: Cảnh sát -> Kẻ làm giả
    path_bottom = ArcBetweenPoints(detector[0].get_bottom() + DOWN*0.2, paraphraser[0].get_bottom() + DOWN*0.2, angle=-TAU/4, color=VG_BLUE, stroke_width=2)
    path_bottom_glow = path_bottom.copy().set_stroke(VG_BLUE, width=10, opacity=0.3)
    text_feedback = VGText("Phản hồi: Bị bắt / Thoát", font_size=16, color=VG_BLUE).next_to(path_bottom, DOWN)
    
    scene.play(Create(path_bottom), FadeIn(path_bottom_glow), Write(text_feedback), run_time=1.5)
    
    # Data flow animation
    data_packet2 = Circle(radius=0.1, color=WHITE, fill_opacity=1).set_z_index(5)
    scene.play(MoveAlongPath(data_packet2, path_bottom), run_time=1.0)
    scene.play(FadeOut(data_packet2), run_time=0.2)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Cảnh sát kiểm tra và gửi phản hồi..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    # Nhãn kết luận
    loop_box = RoundedRectangle(corner_radius=0.1, width=5, height=0.6, color=VG_GOLD, fill_color=BLACK, fill_opacity=0.8)
    loop_text = VGText("VÒNG LẶP TIẾN HÓA KHÔNG NGỪNG", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(loop_box.get_center())
    loop_group = VGroup(loop_box, loop_text).move_to(DOWN * 3.0)
    
    scene.play(FadeIn(loop_group, shift=UP), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Cả hai hệ thống cùng tiến hóa sắc bén..."
    scene.wait(1.0)
    # ---------------------------------------------------------
    
    # Hiệu ứng tiến hóa liên tục (Pulsing)
    for _ in range(3):
        scene.play(
            det_shape.animate.set_fill(opacity=0.6).scale(1.1),
            para_shape.animate.set_fill(opacity=0.6).scale(1.1),
            rate_func=there_and_back,
            run_time=0.8
        )
        
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi âm thanh kết thúc
    scene.wait(2.0)
    # ---------------------------------------------------------
    
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
