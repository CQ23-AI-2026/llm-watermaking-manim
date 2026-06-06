from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_4(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_4.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    scene.wait(0.5)

    part_title = VGText("HỌC ĐỐI KHÁNG (RADAR)", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 3.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.0)
    scene.play(Create(underline), run_time=0.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Chứng kiến sự trỗi dậy mạnh mẽ..."
    
    # INTRO VISUALIZATION: Paraphrase bypasses Detector
    # "Chứng kiến sự trỗi dậy mạnh mẽ của việc xáo trộn từ ngữ..."
    ai_doc = Rectangle(width=1.5, height=2.0, color=VG_GOLD, fill_opacity=0.2).move_to(LEFT * 3)
    ai_txt = VGText("AI Text", font_size=16, color=WHITE).move_to(ai_doc)
    ai_group = VGroup(ai_doc, ai_txt)
    
    scene.play(FadeIn(ai_group), run_time=1.0)
    
    # "xáo trộn từ ngữ" -> Paraphrase!
    para_doc = Rectangle(width=1.5, height=2.0, color=VG_RED, fill_opacity=0.2).move_to(LEFT * 3)
    para_txt = VGText("Paraphrased\nText", font_size=16, color=WHITE).move_to(para_doc)
    para_group = VGroup(para_doc, para_txt)
    
    scene.play(
        ReplacementTransform(ai_group, para_group),
        run_time=1.0
    )
    scene.play(Wiggle(para_group), run_time=0.5)
    
    # "để qua mặt AI..."
    detector_shield = RegularPolygon(n=6, color=VG_BLUE, fill_opacity=0.2).scale(1.5).move_to(RIGHT * 3)
    det_txt = VGText("Detector", font_size=16, color=WHITE).move_to(detector_shield)
    det_group = VGroup(detector_shield, det_txt)
    
    arrow_atk = Arrow(para_group.get_right(), det_group.get_left(), color=VG_RED)
    
    scene.play(FadeIn(det_group, shift=LEFT), run_time=1.0)
    scene.play(Create(arrow_atk), run_time=0.5)
    
    # Shield bypassed/broken
    cross = Cross(detector_shield, stroke_color=VG_RED, stroke_width=8).scale(0.8)
    scene.play(Create(cross), det_group.animate.set_color(VG_GRAY), run_time=1.0)
    
    scene.wait(3)
    
    # "Tại sao không dùng chính độc trị độc?"
    # Crash them together!
    scene.play(FadeOut(arrow_atk), FadeOut(cross), run_time=0.5)
    
    # They collide in the center
    scene.play(
        para_group.animate.move_to(ORIGIN),
        det_group.animate.move_to(ORIGIN),
        run_time=0.8, rate_func=rush_into
    )
    
    # Explosion into RADAR logo
    flash = Flash(ORIGIN, color=VG_GOLD, line_length=2, num_lines=20, flash_radius=1.5, time_width=0.3)
    scene.play(flash, run_time=0.5)
    
    radar_box = RoundedRectangle(width=4.0, height=1.5, color=VG_GOLD, fill_color=BLACK, fill_opacity=1.0)
    radar_txt = VGText("RADAR\nAdversarial Learning", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(radar_box)
    radar_logo = VGroup(radar_box, radar_txt)
    
    scene.play(
        ReplacementTransform(VGroup(para_group, det_group), radar_logo),
        run_time=0.5
    )
    scene.play(Wiggle(radar_logo), run_time=1.0)
    
    # Wait for voice sync
    scene.wait(3)
    
    # Clean up to transition into architecture
    scene.play(FadeOut(radar_logo), run_time=1.0)
    # ---------------------------------------------------------

    # 2. RADAR ARCHITECTURE
    # Paraphraser (Top)
    para_box = RoundedRectangle(width=2.5, height=1.5, color=VG_RED, fill_opacity=0.2).move_to(RIGHT * 2.0 + UP * 1.2)
    para_box_glow = para_box.copy().set_fill(opacity=0).set_stroke(VG_RED, width=8, opacity=0.3)
    para_lbl = VGText("Trainable\nParaphraser P", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(para_box.get_center())
    para = VGroup(para_box, para_box_glow, para_lbl)

    # Target LLM (Middle left) - Use RoundedRectangle instead of 3D Cylinder for 2D safety
    llm_box = RoundedRectangle(corner_radius=0.3, width=1.6, height=1.6, color=VG_GOLD, fill_opacity=0.2).move_to(LEFT * 2.5 + UP * 1.2)
    llm_lbl = VGText("AI Text\n(Target LM)", font_size=12, color=VG_GOLD).next_to(llm_box, DOWN)
    llm = VGroup(llm_box, llm_lbl)

    # Detector (Bottom)
    det_box = RoundedRectangle(width=2.5, height=1.5, color=VG_BLUE, fill_opacity=0.2).move_to(LEFT * 2.0 + DOWN * 1.5)
    det_box_glow = det_box.copy().set_fill(opacity=0).set_stroke(VG_BLUE, width=8, opacity=0.3)
    det_lbl = VGText("Trainable\nDetector D", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(det_box.get_center())
    det = VGroup(det_box, det_box_glow, det_lbl)

    # "...RADAR triển khai một hệ thống giằng co giữa hai phe: Một Kẻ làm giả..."
    scene.play(FadeIn(llm, shift=RIGHT), run_time=1.0)
    scene.play(FadeIn(para, shift=LEFT), run_time=1.0)
    
    arrow1 = Arrow(llm_box.get_right(), para_box.get_left(), color=WHITE)
    scene.play(Create(arrow1), run_time=0.5)
    
    # Pulse packet
    packet1 = Dot(color=VG_GOLD).move_to(arrow1.get_start())
    scene.play(MoveAlongPath(packet1, arrow1), run_time=0.5)
    scene.play(FadeOut(packet1), run_time=0.1)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Một kẻ làm giả tìm cách xào xáo..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    # "...và một Cảnh sát (Trainable Detector) chuyên đi săn những văn bản giả mạo đó."
    scene.play(FadeIn(det, shift=UP), run_time=1.0)
    
    # Data flow to Detector
    arrow2 = Arrow(para_box.get_bottom(), det_box.get_right(), color=VG_RED, path_arc=0.5)
    scene.play(Create(arrow2), run_time=1.0)
    
    packet2 = Dot(color=VG_RED).move_to(arrow2.get_start())
    scene.play(MoveAlongPath(packet2, arrow2), run_time=0.8)
    scene.play(FadeOut(packet2), run_time=0.1)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Người cảnh sát chuyên đi săn lùng..."
    scene.wait(6.0)
    # ---------------------------------------------------------

    # 3. TRAINING LOOP
    # "...Kẻ làm giả liên tục được nâng cấp độ tinh vi thông qua hàm mất mát PPO Loss..."
    ppo_lbl = VGText("PPO Loss", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).next_to(para_box, UP)
    
    scene.play(FadeIn(ppo_lbl, shift=DOWN), run_time=1.0)
    scene.play(Wiggle(ppo_lbl), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "nâng cấp độ xảo quyệt bằng PPO Loss..."
    scene.wait(5)
    # ---------------------------------------------------------

    # "...trong khi Cảnh sát được mài giũa khả năng nhận diện qua Logistic Loss."
    log_lbl = VGText("Logistic Loss", font_size=14, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(det_box, DOWN)
    
    # Detector output probabilities
    prob_box = Rectangle(width=3.0, height=0.6, color=VG_GRAY, fill_opacity=0).move_to(RIGHT * 3.0 + DOWN * 1.5)
    prob_box1 = Rectangle(width=1.0, height=0.6, color=VG_RED, fill_opacity=0.6).move_to(prob_box.get_left() + RIGHT * 0.5)
    prob_box2 = Rectangle(width=1.0, height=0.6, color=VG_GOLD, fill_opacity=0.6).next_to(prob_box1, RIGHT, buff=0)
    prob_box3 = Rectangle(width=1.0, height=0.6, color=VG_GREEN, fill_opacity=0.6).next_to(prob_box2, RIGHT, buff=0)
    
    t1 = VGText("0.98", font_size=12, color=WHITE).move_to(prob_box1)
    t2 = VGText("0.02", font_size=12, color=WHITE).move_to(prob_box2)
    t3 = VGText("0.15", font_size=12, color=WHITE).move_to(prob_box3)
    
    probs = VGroup(prob_box, prob_box1, prob_box2, prob_box3, t1, t2, t3)
    arrow3 = Arrow(det_box.get_right(), prob_box.get_left(), color=VG_BLUE)

    scene.play(FadeIn(log_lbl, shift=UP), run_time=1.0)
    scene.play(Create(arrow3), FadeIn(probs, shift=LEFT), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "mài giũa khả năng nhận diện qua Logistic Loss..."
    scene.wait(3)
    # ---------------------------------------------------------

    # "...Vòng lặp tiến hóa khốc liệt này tạo ra một hệ thống phòng thủ cực kỳ vững chắc..."
    # Continuous loop animation with changing probability numbers
    probs_sequence = [
        ("0.24", VG_GOLD),  # Paraphraser tricks Detector (prob drops)
        ("0.89", VG_RED),   # Detector learns (prob goes back up)
        ("0.45", VG_GOLD),  # Paraphraser gets better
        ("0.96", VG_RED)    # Detector masters it
    ]
    
    for i in range(2):
        # 1. Paraphraser attacks (tricks detector)
        dot_p2d = Dot(color=VG_RED).move_to(arrow2.get_start())
        new_t1_atk = VGText(probs_sequence[i*2][0], font_size=12, color=WHITE).move_to(prob_box1)
        
        scene.play(
            MoveAlongPath(dot_p2d, arrow2),
            arrow2.animate.set_color(VG_GOLD),
            prob_box1.animate.set_color(probs_sequence[i*2][1]),
            Transform(t1, new_t1_atk),
            run_time=1.0
        )
        scene.play(FadeOut(dot_p2d), run_time=0.5)
        
        # 2. Detector learns and fights back
        new_t1_def = VGText(probs_sequence[i*2 + 1][0], font_size=12, color=WHITE).move_to(prob_box1)
        scene.play(
            Wiggle(det_box_glow),
            arrow2.animate.set_color(VG_RED),
            prob_box1.animate.set_color(probs_sequence[i*2 + 1][1]),
            Transform(t1, new_t1_def),
            run_time=1.0
        )

    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc phần còn lại "sự tiến hóa liên tục không khoan nhượng..."
    scene.wait(1)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
