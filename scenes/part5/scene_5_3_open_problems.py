from manim import *
import os
import numpy as np
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_3(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_3.mp3")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("CÁC BÀI TOÁN CHƯA CÓ LỜI GIẢI", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    scene.wait(3.5)
    # ---------------------------------------------------------

    # 2. RADAR CHART SECTION (Sự Đánh Đổi Tối Ưu)
    radar_center = LEFT * 3.5 + DOWN * 0.8
    radar_radius = 2.0

    axis_q = Line(radar_center, radar_center + UP * radar_radius, color=VG_GRAY, stroke_width=1.5)
    axis_d = Line(radar_center, radar_center + RIGHT * radar_radius, color=VG_GRAY, stroke_width=1.5)
    axis_s = Line(radar_center, radar_center + DOWN * radar_radius, color=VG_GRAY, stroke_width=1.5)
    axis_r = Line(radar_center, radar_center + LEFT * radar_radius, color=VG_GRAY, stroke_width=1.5)
    axes = VGroup(axis_q, axis_d, axis_s, axis_r)

    rings = VGroup()
    for scale in [0.25, 0.5, 0.75, 1.0]:
        ring = Polygon(
            radar_center + UP * radar_radius * scale,
            radar_center + RIGHT * radar_radius * scale,
            radar_center + DOWN * radar_radius * scale,
            radar_center + LEFT * radar_radius * scale,
            color=VG_GRAY, stroke_width=1.0, stroke_opacity=0.3
        )
        rings.add(ring)

    lbl_q = VGText("Quality", font_size=12, color=WHITE).next_to(radar_center + UP * radar_radius, UP, buff=0.1)
    lbl_d = VGText("Detectability", font_size=12, color=WHITE).next_to(radar_center + RIGHT * radar_radius, RIGHT, buff=0.1)
    lbl_s = VGText("Security", font_size=12, color=WHITE).next_to(radar_center + DOWN * radar_radius, DOWN, buff=0.1)
    lbl_r = VGText("Robustness", font_size=12, color=WHITE).next_to(radar_center + LEFT * radar_radius, LEFT, buff=0.1)
    labels = VGroup(lbl_q, lbl_d, lbl_s, lbl_r)
    radar_group = VGroup(axes, rings, labels)

    scene.play(FadeIn(radar_group), run_time=1.5)
    scene.wait(1.5)

    kgw_poly = Polygon(
        radar_center + UP * radar_radius * 0.85, radar_center + RIGHT * radar_radius * 0.9,
        radar_center + DOWN * radar_radius * 0.2, radar_center + LEFT * radar_radius * 0.3,
        color=VG_BLUE, stroke_width=2.5, fill_color=VG_BLUE, fill_opacity=0.2
    )
    kgw_label = VGText("Green-Red (KGW)", font_size=12, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(RIGHT * 1.5 + UP * 0.8)

    scene.play(Create(kgw_poly), Write(kgw_label), run_time=1.0)
    scene.wait(1.0)
    scene.play(kgw_poly.animate.set_opacity(0.1), run_time=0.5)

    gumbel_poly = Polygon(
        radar_center + UP * radar_radius * 0.9, radar_center + RIGHT * radar_radius * 0.9,
        radar_center + DOWN * radar_radius * 0.8, radar_center + LEFT * radar_radius * 0.25,
        color=VG_GOLD, stroke_width=2.5, fill_color=VG_GOLD, fill_opacity=0.2
    )
    gumbel_label = VGText("Gumbel Watermark", font_size=12, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(RIGHT * 1.5 + UP * 0.3)

    scene.play(Create(gumbel_poly), Write(gumbel_label), run_time=1.0)
    scene.wait(0.5)
    scene.play(gumbel_poly.animate.set_opacity(0.1), run_time=0.5)

    undet_poly = Polygon(
        radar_center + UP * radar_radius * 0.7, radar_center + RIGHT * radar_radius * 0.4,
        radar_center + DOWN * radar_radius * 0.9, radar_center + LEFT * radar_radius * 0.85,
        color=VG_RED, stroke_width=2.5, fill_color=VG_RED, fill_opacity=0.2
    )
    undet_label = VGText("Undetectable Watermark", font_size=12, color=VG_RED, weight=BOLD_WEIGHT).move_to(RIGHT * 1.5 - UP * 0.2)

    scene.play(Create(undet_poly), Write(undet_label), run_time=1.0)
    scene.wait(1.0)
    scene.play(undet_poly.animate.set_opacity(0.1), run_time=0.5)

    scene.wait(7.5)

    scene.play(
        FadeOut(radar_group),
        FadeOut(kgw_poly), FadeOut(kgw_label),
        FadeOut(gumbel_poly), FadeOut(gumbel_label),
        FadeOut(undet_poly), FadeOut(undet_label),
        run_time=1.0
    )

    # 3. REALISTIC THREAT MODEL SECTION (Collaborative Writing)
    threat_title = VGText("Mô hình Đe dọa Thực tế (Collaborative Writing)", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 2.2)
    
    scene.play(Write(threat_title), run_time=1.0)
    scene.wait(4)

    doc_bg = Rectangle(color=WHITE, width=3.0, height=4.0, fill_color=BLACK, fill_opacity=0.9).move_to(RIGHT * 0.5 - UP * 0.5)
    doc_lbl = VGText("Term Report", font_size=14, color=WHITE, weight=BOLD_WEIGHT).move_to(doc_bg.get_top() + DOWN * 0.3)
    scene.play(FadeIn(doc_bg), FadeIn(doc_lbl), run_time=1.0)

    box_w, box_h = 1.8, 0.8
    style = {"fill_opacity": 0.2, "stroke_width": 2, "corner_radius": 0.05}
    
    # Bob
    b_bob = RoundedRectangle(color=VG_BLUE, width=box_w, height=box_h, **style).move_to(LEFT * 4.5 + UP * 0.5)
    t_bob = VGText("Bob\n(ChatKitten AI)", font_size=12, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(b_bob.get_center())
    bob = VGroup(b_bob, t_bob)

    block1 = Rectangle(color=VG_BLUE, width=2.4, height=0.6, fill_opacity=0.3, stroke_width=1).move_to(doc_bg.get_center() + UP * 0.8)
    block1_txt = VGText("AI Segment 1 (Bob)", font_size=10, color=VG_BLUE).move_to(block1.get_center())
    arrow_bob = Arrow(bob.get_right(), block1.get_left(), color=VG_BLUE)

    scene.play(FadeIn(bob, shift=RIGHT), run_time=0.8)
    scene.play(Create(arrow_bob), FadeIn(block1), FadeIn(block1_txt), run_time=0.8)
    scene.wait(1)

    # Alice
    b_alice = RoundedRectangle(color=VG_GREEN, width=box_w, height=box_h, **style).move_to(LEFT * 4.5 - UP * 0.5)
    t_alice = VGText("Alice\n(ChatPuppy AI)", font_size=12, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(b_alice.get_center())
    alice = VGroup(b_alice, t_alice)

    block2 = Rectangle(color=VG_GREEN, width=2.4, height=0.6, fill_opacity=0.3, stroke_width=1).move_to(doc_bg.get_center() + UP * 0.1)
    block2_txt = VGText("AI Segment 2 (Alice)", font_size=10, color=VG_GREEN).move_to(block2.get_center())
    arrow_alice = Arrow(alice.get_right(), block2.get_left(), color=VG_GREEN)

    scene.play(FadeIn(alice, shift=RIGHT), run_time=0.8)
    scene.play(Create(arrow_alice), FadeIn(block2), FadeIn(block2_txt), run_time=0.8)
    scene.wait(1)

    # Dave
    b_dave = RoundedRectangle(color=VG_GRAY, width=box_w, height=box_h, **style).move_to(LEFT * 4.5 - UP * 1.5)
    t_dave = VGText("Dave\n(Hand-written)", font_size=12, color=VG_GRAY, weight=BOLD_WEIGHT).move_to(b_dave.get_center())
    dave = VGroup(b_dave, t_dave)

    block3 = Rectangle(color=VG_GRAY, width=2.4, height=0.6, fill_opacity=0.3, stroke_width=1).move_to(doc_bg.get_center() - UP * 0.6)
    block3_txt = VGText("Human Segment (Dave)", font_size=10, color=VG_GRAY).move_to(block3.get_center())
    arrow_dave = Arrow(dave.get_right(), block3.get_left(), color=VG_GRAY)

    scene.play(FadeIn(dave, shift=RIGHT), run_time=0.8)
    scene.play(Create(arrow_dave), FadeIn(block3), FadeIn(block3_txt), run_time=0.8)
    scene.wait(1)

    # Eric editing
    block4 = Rectangle(color=VG_RED, width=2.4, height=0.4, fill_opacity=0.4, stroke_width=1.5).move_to(doc_bg.get_center() - UP * 1.2)
    block4_txt = VGText("Edited by Eric", font_size=10, color=VG_RED, weight=BOLD_WEIGHT).move_to(block4.get_center())
    
    scene.play(FadeIn(block4), FadeIn(block4_txt), run_time=0.8)
    scene.wait(2.0)

    # Analysis meter
    detector_box = RoundedRectangle(color=VG_GOLD, width=3.0, height=2.5, **style).move_to(RIGHT * 4.8 - UP * 0.5)
    detector_lbl = VGText("Detector Confidence", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(detector_box.get_top() + DOWN * 0.3)
    
    stat1 = VGText("Bob (AI 1): 99%", font_size=12, color=VG_BLUE).move_to(detector_box.get_center() + UP * 0.3)
    stat2 = VGText("Alice (AI 2): 90%", font_size=12, color=VG_GREEN).move_to(detector_box.get_center() - UP * 0.1)
    stat3 = VGText("Dave (Hand): 0%", font_size=12, color=VG_GRAY).move_to(detector_box.get_center() - UP * 0.5)

    scene.play(FadeIn(detector_box), FadeIn(detector_lbl), run_time=1.0)
    
    scene.play(Write(stat1), run_time=0.5)
    scene.play(Write(stat2), run_time=0.5)
    scene.play(Write(stat3), run_time=0.5)
    
    scene.wait(5.0)

    # Clear for next section
    scene.play(
        FadeOut(threat_title), FadeOut(doc_bg), FadeOut(doc_lbl),
        FadeOut(bob), FadeOut(block1), FadeOut(block1_txt), FadeOut(arrow_bob),
        FadeOut(alice), FadeOut(block2), FadeOut(block2_txt), FadeOut(arrow_alice),
        FadeOut(dave), FadeOut(block3), FadeOut(block3_txt), FadeOut(arrow_dave),
        FadeOut(block4), FadeOut(block4_txt),
        FadeOut(detector_box), FadeOut(detector_lbl), FadeOut(stat1), FadeOut(stat2), FadeOut(stat3),
        run_time=1.0
    )

    # 4. MODEL WATERMARKING EFFICIENCY
    eff_title = VGText("Hiệu năng đánh giá Model Watermarking", font_size=20, color=VG_RED, weight=BOLD_WEIGHT).move_to(UP * 2.2)
    scene.play(Write(eff_title), run_time=1.0)
    scene.wait(1.0)

    server = Rectangle(width=1.5, height=2.0, color=WHITE, fill_opacity=0.2).move_to(LEFT * 4.0)
    server_lbl = VGText("Detector\nServer", font_size=14, color=WHITE, weight=BOLD_WEIGHT).move_to(server.get_center())
    scene.play(FadeIn(server), FadeIn(server_lbl), run_time=0.5)

    # Draw many suspicious models
    models = VGroup()
    for i in range(5):
        for j in range(3):
            m = Rectangle(width=0.6, height=0.6, color=VG_GRAY, fill_opacity=0.5).move_to(RIGHT * (i - 1) * 1.2 + UP * (j - 1) * 1.0)
            models.add(m)
    
    scene.play(FadeIn(models, shift=UP), run_time=1.0)

    # Scanning rays
    rays = VGroup(*[Line(server.get_right(), m.get_center(), color=VG_RED, stroke_width=1, stroke_opacity=0.5) for m in models])
    scene.play(Create(rays), run_time=1.5)

    # Overload warning
    warning = VGText("!!! TỐN KÉM TÀI NGUYÊN !!!", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).next_to(server, DOWN, buff=0.3)
    scene.play(FadeIn(warning, shift=UP), run_time=0.5)
    
    # Flash warning
    for _ in range(3):
        scene.play(warning.animate.set_color(WHITE), run_time=0.2)
        scene.play(warning.animate.set_color(VG_RED), run_time=0.2)
        
    scene.wait(3)

    scene.play(FadeOut(eff_title), FadeOut(server), FadeOut(server_lbl), FadeOut(models), FadeOut(rays), FadeOut(warning), run_time=1.0)

    # 5. DECODER CO-DESIGN
    co_title = VGText("Đồng thiết kế Decoder & Zero Entropy", font_size=20, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(UP * 2.2)
    scene.play(Write(co_title), run_time=1.0)
    scene.wait(2.0)

    # Beam search left
    beam_lbl = VGText("Beam Search", font_size=16, color=VG_BLUE).move_to(LEFT * 3.5 + UP * 0.8)
    node1 = Circle(radius=0.2, color=VG_BLUE, fill_opacity=0.5).move_to(LEFT * 5.0 + DOWN * 0.5)
    node2 = Circle(radius=0.2, color=VG_BLUE, fill_opacity=0.5).move_to(LEFT * 3.5 + DOWN * 1.5)
    node3 = Circle(radius=0.2, color=VG_BLUE, fill_opacity=0.5).move_to(LEFT * 2.0 + DOWN * 0.5)
    l1 = Line(node1, node2, color=WHITE)
    l2 = Line(node2, node3, color=WHITE)
    beam_group = VGroup(beam_lbl, node1, node2, node3, l1, l2)
    
    # Shield/Watermark trying to attach
    shield_bg = Polygon(LEFT*0.3+UP*0.2, RIGHT*0.3+UP*0.2, RIGHT*0.3+DOWN*0.1, DOWN*0.3, LEFT*0.3+DOWN*0.1, color=VG_GOLD, fill_opacity=0.3)
    shield_txt = VGText("WM", font_size=10, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(shield_bg.get_center())
    shield = VGroup(shield_bg, shield_txt).next_to(node2, DOWN)

    scene.play(FadeIn(beam_group), run_time=1.0)
    scene.play(FadeIn(shield, shift=UP), run_time=0.5)
    scene.play(shield.animate.shift(LEFT * 1.5 + UP * 1.0), run_time=0.5) # fails to attach
    scene.play(shield.animate.shift(RIGHT * 3.0), run_time=0.5)
    scene.wait(2)

    # Zero entropy right
    zero_lbl = VGText("Zero Entropy", font_size=16, color=VG_RED).move_to(RIGHT * 3.5 + UP * 0.8)
    fact = VGText("1 + 1 = 2", font_size=24, color=WHITE, weight=BOLD_WEIGHT).move_to(RIGHT * 3.5 + DOWN * 0.5)
    
    lock_body = Rectangle(width=0.4, height=0.3, color=VG_RED, fill_opacity=1).next_to(fact, RIGHT, buff=0.3)
    lock_shackle = Arc(radius=0.15, angle=PI, color=VG_RED, stroke_width=4).next_to(lock_body, UP, buff=0)
    lock = VGroup(lock_body, lock_shackle)

    scene.play(FadeIn(zero_lbl), FadeIn(fact), run_time=1.0)
    scene.play(FadeIn(lock, scale=0.5), run_time=0.5)
    
    scene.wait(6.5)

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
