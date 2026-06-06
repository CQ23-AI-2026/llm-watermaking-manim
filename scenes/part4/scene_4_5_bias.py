from manim import *
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

    part_title = VGText("LỖ HỔNG & THIÊN KIẾN", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 3.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Tuy nhiên ảo mộng nhanh chóng tan vỡ..."
    scene.wait(10.0)
    # ---------------------------------------------------------

    # 1. ROBUSTNESS ATTACKS (Sự mong manh trước tấn công)
    rob_title = VGText("1. Robustness Attacks", font_size=20, color=VG_RED, weight=BOLD_WEIGHT).move_to(UP * 2.0)
    scene.play(Write(rob_title), run_time=1.0)
    
    # "...Thứ nhất là sự mong manh trước các đòn tấn công (Robustness). Các nghiên cứu chỉ ra rằng điểm AUROC của chúng tuột dốc không phanh..."
    # AUROC Drop visualization
    auroc_lbl = VGText("Detector AUROC Score", font_size=16, color=WHITE).move_to(LEFT * 3.5 + UP * 0.5)
    
    # Bar chart for AUROC
    bar_unattacked = Rectangle(width=1.5, height=3.0, color=VG_GREEN, fill_opacity=0.8).move_to(LEFT * 1.0 + DOWN * 0.5).align_to(DOWN * 2.0, DOWN)
    lbl_unattacked = VGText("84.4%\nUnattacked", font_size=12, color=WHITE).next_to(bar_unattacked, DOWN)

    bar_para = Rectangle(width=1.5, height=3.0 * (35.2/84.4), color=VG_GOLD, fill_opacity=0.8).move_to(RIGHT * 1.0 + DOWN * 0.5).align_to(DOWN * 2.0, DOWN)
    lbl_para = VGText("35.2%\nParaphrased", font_size=12, color=WHITE).next_to(bar_para, DOWN)

    bar_sub = Rectangle(width=1.5, height=3.0 * (3.9/84.4), color=VG_RED, fill_opacity=0.8).move_to(RIGHT * 3.0 + DOWN * 0.5).align_to(DOWN * 2.0, DOWN)
    lbl_sub = VGText("3.9%\nSubstitution", font_size=12, color=WHITE).next_to(bar_sub, DOWN)

    scene.play(FadeIn(auroc_lbl), run_time=0.5)
    scene.play(GrowFromEdge(bar_unattacked, DOWN), FadeIn(lbl_unattacked), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Sự mong manh trước đòn tấn công..."
    scene.wait(9.0)
    # ---------------------------------------------------------

    # "...khi văn bản bị tấn công bằng các kỹ thuật Paraphrasing tinh vi hay thay thế từ đồng nghĩa."
    scene.play(GrowFromEdge(bar_para, DOWN), FadeIn(lbl_para), run_time=1.0)
    scene.play(GrowFromEdge(bar_sub, DOWN), FadeIn(lbl_sub), run_time=1.0)
    
    # Dramatic drop arrow
    drop_arrow = Arrow(bar_unattacked.get_top(), bar_sub.get_top() + UP * 0.2, color=VG_RED, path_arc=-0.5)
    scene.play(Create(drop_arrow), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "điểm AUROC lập tức rơi tự do..."
    scene.wait(8.5)
    # ---------------------------------------------------------

    scene.play(
        FadeOut(rob_title), FadeOut(auroc_lbl), FadeOut(drop_arrow),
        FadeOut(bar_unattacked), FadeOut(lbl_unattacked),
        FadeOut(bar_para), FadeOut(lbl_para),
        FadeOut(bar_sub), FadeOut(lbl_sub),
        run_time=1.0
    )

    # 2. BIAS AGAINST NON-NATIVE WRITERS
    bias_title = VGText("2. Bias Against Non-Native Writers", font_size=20, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(UP * 2.0)
    scene.play(Write(bias_title), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "thứ hai là sự thiên vị vô thức..."
    scene.wait(3.5)
    # ---------------------------------------------------------

    # Document representing TOEFL essay
    doc = Rectangle(width=2.5, height=3.5, color=WHITE, fill_opacity=0.1).move_to(LEFT * 3.0 + DOWN * 0.5)
    doc_title = VGText("TOEFL Essay\n(Human Written)", font_size=14, color=WHITE, weight=BOLD_WEIGHT).move_to(doc.get_top() + DOWN * 0.4)
    doc_lines = VGroup(*[Line(LEFT, RIGHT, color=VG_GRAY) for _ in range(5)]).arrange(DOWN, buff=0.3).next_to(doc_title, DOWN, buff=0.4)
    doc_g = VGroup(doc, doc_title, doc_lines)

    scene.play(FadeIn(doc_g, shift=RIGHT), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "hơn 76% bài thi TOEFL thực tế..."
    scene.wait(4.5)
    # ---------------------------------------------------------

    # Detector scanning and misclassifying
    scanner = Line(doc.get_left(), doc.get_right(), color=VG_GOLD).move_to(doc.get_top() + DOWN * 0.1)
    scene.play(scanner.animate.move_to(doc.get_bottom() + UP * 0.1), run_time=1.0)
    scene.play(FadeOut(scanner), run_time=0.2)

    # "...đã bị các công cụ đánh giá kết án oan uổng là do AI viết."
    # Turn document RED and stamp AI GENERATED
    stamp_box = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.6, color=VG_RED, stroke_width=3).rotate(PI/6).move_to(doc.get_center())
    stamp_box_glow = stamp_box.copy().set_fill(opacity=0).set_stroke(VG_RED, width=10, opacity=0.4)
    stamp_txt = VGText("100% AI", font_size=18, color=VG_RED, weight=BOLD_WEIGHT).rotate(PI/6).move_to(stamp_box.get_center())
    stamp = VGroup(stamp_box, stamp_box_glow, stamp_txt)

    # Flash screen red for drama
    flash_rect = FullScreenRectangle(color=VG_RED, fill_opacity=0.2, stroke_width=0).set_z_index(100)
    
    scene.play(
        FadeIn(flash_rect, run_time=0.1),
        doc.animate.set_color(VG_RED), doc_lines.animate.set_color(VG_RED), 
        FadeIn(stamp, scale=2.0), 
        run_time=0.5
    )
    scene.play(FadeOut(flash_rect), run_time=0.5)

    # Show 76% stat
    stat_box = Rectangle(width=3.5, height=1.5, color=VG_RED, fill_opacity=0.2).move_to(RIGHT * 3.0 + DOWN * 0.5)
    stat_box_glow = stat_box.copy().set_fill(opacity=0).set_stroke(VG_RED, width=10, opacity=0.3)
    stat_num = VGText("76%", font_size=40, color=VG_RED, weight=BOLD_WEIGHT).move_to(stat_box.get_center() + UP * 0.2)
    stat_lbl = VGText("Misclassified as AI", font_size=14, color=WHITE).next_to(stat_num, DOWN)
    stat_g = VGroup(stat_box, stat_box_glow, stat_num, stat_lbl)

    scene.play(FadeIn(stat_g, shift=LEFT), run_time=1.0)
    
    # Pulse the 76% to emphasize
    scene.play(Wiggle(stat_num), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "bị đánh dấu oan uổng..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    # "...Điều này đặt ra một bài toán đạo đức vô cùng lớn..."
    ethic_lbl = VGText("Ethical Dilemma in AI Detection", font_size=18, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(stat_g, UP, buff=0.8)
    scene.play(FadeIn(ethic_lbl, shift=DOWN), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi đọc phần đạo đức kết thúc
    scene.wait(25.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
