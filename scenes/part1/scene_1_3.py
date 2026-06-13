from manim import *
import os
import re
import subprocess

from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GRAY, VG_GREEN, VG_ORANGE, VG_RED, VG_PURPLE,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def _glow_rect(width, height, color, corner_radius=0.15):
    glow = VGroup()
    for i in range(4):
        rect = RoundedRectangle(corner_radius=corner_radius, width=width + i*0.08, height=height + i*0.08)
        rect.set_stroke(color, width=2, opacity=0.15 - i*0.03)
        rect.set_fill(BLACK, opacity=0)
        glow.add(rect)
    return glow

def _glass_panel(width, height, color):
    panel = RoundedRectangle(corner_radius=0.15, width=width, height=height)
    # Gradient stroke
    panel.set_stroke(color=[color, WHITE, color], width=2)
    # Semi-transparent fill
    panel.set_fill(color, opacity=0.1)
    
    glow = _glow_rect(width, height, color, corner_radius=0.15)
    return VGroup(glow, panel)

def _robot_icon(color=VG_BLUE):
    head = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.45)
    head.set_stroke(color, width=2).set_fill(color, opacity=0.2)
    eye_l = Dot(radius=0.04, color=WHITE).move_to(head.get_center() + LEFT*0.12 + UP*0.05)
    eye_r = Dot(radius=0.04, color=WHITE).move_to(head.get_center() + RIGHT*0.12 + UP*0.05)
    mouth = Line(head.get_center() + LEFT*0.1 + DOWN*0.1, head.get_center() + RIGHT*0.1 + DOWN*0.1, color=WHITE)
    antenna = Line(head.get_top(), head.get_top() + UP*0.15, color=color)
    antenna_dot = Dot(radius=0.03, color=VG_GOLD).next_to(antenna, UP, buff=0)
    return VGroup(head, eye_l, eye_r, mouth, antenna, antenna_dot)

def _detective_icon(color=VG_ORANGE):
    glass = Circle(radius=0.2, color=color)
    glass.set_stroke(color, width=3).set_fill(color, opacity=0.1)
    handle = Line(glass.get_corner(DR), glass.get_corner(DR) + DR*0.2, color=color, stroke_width=3)
    inner_glass = Circle(radius=0.12, color=WHITE)
    inner_glass.set_stroke(WHITE, width=1.5, opacity=0.5).set_fill(WHITE, opacity=0.05)
    inner_glass.move_to(glass.get_center() + UL*0.03)
    return VGroup(glass, handle, inner_glass)

def _key_icon(color=VG_GOLD):
    ring = Circle(radius=0.12)
    ring.set_stroke(color=color, width=2).set_fill(BLACK, opacity=0)
    stem = Line(ring.get_right(), ring.get_right() + RIGHT*0.18, color=color, stroke_width=2)
    tooth = Line(stem.get_end(), stem.get_end() + DOWN*0.07, color=color, stroke_width=2)
    tooth2 = Line(stem.get_end() + LEFT*0.06, stem.get_end() + LEFT*0.06 + DOWN*0.05, color=color, stroke_width=2)
    return VGroup(ring, stem, tooth, tooth2)

def _text_lines_icon(color=WHITE):
    box = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.6)
    box.set_stroke(color, width=1.5).set_fill(color, opacity=0.05)
    line_1 = Line(LEFT*0.15, RIGHT*0.15, stroke_width=2, color=color).shift(UP*0.12)
    line_2 = Line(LEFT*0.15, RIGHT*0.05, stroke_width=2, color=color)
    line_3 = Line(LEFT*0.15, RIGHT*0.15, stroke_width=2, color=color).shift(DOWN*0.12)
    lines = VGroup(line_1, line_2, line_3).move_to(box.get_center())
    return VGroup(box, lines)

def _get_audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path):
        return None
    try:
        completed = subprocess.run(["ffmpeg", "-i", path], capture_output=True, text=True)
    except FileNotFoundError:
        return None
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", completed.stderr + completed.stdout)
    if not match:
        return None
    return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + float(match.group(3))

def _state_circle(text, color, text_size=36):
    circle = Circle(radius=0.45)
    circle.set_stroke(color, width=3)
    circle.set_fill(color, opacity=0.1)
    glow = _glow_rect(0.9, 0.9, color, corner_radius=0.45)
    value = VGText(text, font_size=text_size, weight=BOLD_WEIGHT, color=color)
    value.move_to(circle.get_center())
    return VGroup(glow, circle, value)

def play_part1_scene_1_3(scene: Scene) -> None:
    scene.camera.background_color = "#080808" # Deep aesthetic dark

    voice_path = os.path.join("scenes", "part1", "voice", "1_3.mp3")
    voice_duration = _get_audio_duration(voice_path)
    start_time = scene.renderer.time
    if voice_duration is not None:
        scene.add_sound(voice_path)

    title = VGText(
        "Hai thành phần của Watermarking Scheme",
        font_size=40,
        color=VG_GOLD,
        weight=BOLD_WEIGHT,
    ).to_edge(UP, buff=0.28)

    title_underline = Line(LEFT*3.5, RIGHT*3.5, color=[VG_BLUE, VG_GOLD, VG_ORANGE]).next_to(title, DOWN, buff=0.15)

    block_width = 4.2
    block_height = 1.6
    top_y = 1.3
    bot_y = -1.1

    # Block 1 - Watermark
    panel1 = _glass_panel(block_width, block_height, VG_BLUE).move_to(UP*top_y)
    label1 = VGText("Watermark( M )", font_size=32, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(panel1.get_center() + UP*0.35)
    icon1 = _robot_icon(VG_BLUE).move_to(panel1.get_center() + DOWN*0.2)
    block1_group = VGroup(panel1, label1, icon1)

    # Block 2 - Detect
    panel2 = _glass_panel(block_width, block_height, VG_ORANGE).move_to(UP*bot_y)
    label2 = VGText("Detect( k, y )", font_size=32, color=VG_ORANGE, weight=BOLD_WEIGHT).move_to(panel2.get_center() + UP*0.35)
    icon2 = _detective_icon(VG_ORANGE).move_to(panel2.get_center() + DOWN*0.2)
    block2_group = VGroup(panel2, label2, icon2)

    # --- Block 1 inputs/outputs ---
    # Input: Model M
    in_model_icon = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.7)
    in_model_icon.set_stroke(WHITE, width=2).set_fill(WHITE, opacity=0.05)
    in_model_text = VGText("M", font_size=24, color=WHITE, weight=BOLD_WEIGHT).move_to(in_model_icon.get_center())
    in_model_group = VGroup(in_model_icon, in_model_text)
    in_model_group.next_to(panel1, LEFT, buff=1.3).shift(UP*0.0)
    in_model_label = VGText("Model M", font_size=24, color=WHITE).next_to(in_model_group, UP, buff=0.15)
    
    arrow_in_m = Arrow(in_model_group.get_right(), panel1.get_left(), color=WHITE, stroke_width=3, buff=0.1)

    # Output: M^ (Model mới)
    out_model_icon = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.7)
    out_model_icon.set_stroke(VG_GREEN, width=2).set_fill(VG_GREEN, opacity=0.1)
    out_model_text = VGText("M̂", font_size=24, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(out_model_icon.get_center())
    out_model_group = VGroup(out_model_icon, out_model_text)
    out_model_group.next_to(panel1, RIGHT, buff=1.0).shift(UP*0.35)
    out_model_label = VGText("Model mới", font_size=22, color=VG_GREEN).next_to(out_model_group, UP, buff=0.1)
    
    arrow_out_m = Arrow(panel1.get_right() + UP*0.35, out_model_group.get_left(), color=VG_GREEN, stroke_width=3, buff=0.1)

    # Output: Key k
    out_key_icon = _key_icon(VG_GOLD).scale(1.2)
    out_key_icon.next_to(panel1, RIGHT, buff=1.0).shift(DOWN*0.35)
    out_key_label = VGText("Key k", font_size=22, color=VG_GOLD).next_to(out_key_icon, DOWN, buff=0.15)
    
    arrow_out_k = Arrow(panel1.get_right() + DOWN*0.35, out_key_icon.get_left(), color=VG_GOLD, stroke_width=3, buff=0.1)

    # --- Block 2 inputs/outputs ---
    # Input: Key k
    in_key_icon = _key_icon(VG_GOLD).scale(1.2)
    in_key_icon.next_to(panel2, LEFT, buff=1.0).shift(UP*0.25)
    in_key_label = VGText("Key k", font_size=22, color=VG_GOLD).next_to(in_key_icon, UP, buff=0.15)
    
    arrow_in_k = Arrow(in_key_icon.get_right(), panel2.get_left() + UP*0.25, color=VG_GOLD, stroke_width=3, buff=0.1)

    # Input: Text y
    in_text_icon = _text_lines_icon(WHITE)
    in_text_icon.next_to(panel2, LEFT, buff=1.0).shift(DOWN*0.35)
    in_text_label = VGText("Văn bản y", font_size=22, color=WHITE).next_to(in_text_icon, DOWN, buff=0.15)
    
    arrow_in_text = Arrow(in_text_icon.get_right(), panel2.get_left() + DOWN*0.35, color=WHITE, stroke_width=3, buff=0.1)

    # Link from out_key to in_key
    start_pt = out_key_icon.get_bottom() + DOWN*0.1
    end_pt = in_key_icon.get_top() + UP*0.1
    mid_pt1 = start_pt + DOWN*0.8 + RIGHT*0.2
    mid_pt2 = end_pt + UP*0.8 + LEFT*0.2
    curved_link = CubicBezier(start_pt, mid_pt1, mid_pt2, end_pt, color=VG_GOLD)
    dashed_link = DashedVMobject(curved_link, num_dashes=25)
    dashed_link.set_stroke(VG_GOLD, width=2, opacity=0.6)

    # Output: Decision
    arrow_out_dec = Arrow(panel2.get_right(), panel2.get_right() + RIGHT*1.0, color=WHITE, stroke_width=3, buff=0.1)
    
    state_a = _state_circle("1", VG_GREEN).next_to(arrow_out_dec, RIGHT, buff=0.1)
    state_a_label = VGText("Có watermark", font_size=22, color=VG_GREEN).next_to(state_a, DOWN, buff=0.2)
    state_a_group = VGroup(state_a, state_a_label)

    state_b = _state_circle("0", VG_RED).move_to(state_a)
    state_b_label = VGText("Không đủ bằng chứng", font_size=22, color=VG_RED).next_to(state_b, DOWN, buff=0.2)
    state_b_group = VGroup(state_b, state_b_label)

    footnote = VGText(
        "* 0 không đồng nghĩa với 'Do người viết', mà chỉ là không phát hiện được watermark.",
        font_size=20,
        slant="ITALIC",
        color=VG_GRAY,
    ).to_edge(DOWN, buff=0.2)

    # Animations
    scene.play(FadeIn(title, shift=DOWN*0.1), Create(title_underline), run_time=1.0)
    
    # Block 1
    scene.play(FadeIn(panel1, shift=UP*0.1), run_time=0.8)
    scene.play(Write(label1), Create(icon1), run_time=0.8)
    
    # Block 1 in
    scene.play(FadeIn(in_model_group, shift=RIGHT*0.2), Write(in_model_label), run_time=0.6)
    scene.play(GrowArrow(arrow_in_m), run_time=0.5)

    # Data flowing dot
    dot_m = Dot(color=WHITE).move_to(arrow_in_m.get_start())
    scene.play(MoveAlongPath(dot_m, arrow_in_m), run_time=0.4)
    scene.play(FadeOut(dot_m), run_time=0.1)

    # Block 1 out
    scene.play(GrowArrow(arrow_out_m), GrowArrow(arrow_out_k), run_time=0.6)
    scene.play(
        FadeIn(out_model_group, shift=RIGHT*0.2), Write(out_model_label),
        FadeIn(out_key_icon, shift=RIGHT*0.2), Write(out_key_label),
        run_time=0.8
    )

    # Block 2
    scene.play(FadeIn(panel2, shift=UP*0.1), run_time=0.8)
    scene.play(Write(label2), Create(icon2), run_time=0.8)

    # Key link
    scene.play(Create(dashed_link), run_time=1.0)
    scene.play(TransformFromCopy(out_key_icon, in_key_icon), Write(in_key_label), run_time=0.8)
    scene.play(GrowArrow(arrow_in_k), run_time=0.5)

    # Text in
    scene.play(FadeIn(in_text_icon, shift=RIGHT*0.2), Write(in_text_label), run_time=0.6)
    scene.play(GrowArrow(arrow_in_text), run_time=0.5)

    # Data flow to block 2
    dot_k = Dot(color=VG_GOLD).move_to(arrow_in_k.get_start())
    dot_y = Dot(color=WHITE).move_to(arrow_in_text.get_start())
    scene.play(MoveAlongPath(dot_k, arrow_in_k), MoveAlongPath(dot_y, arrow_in_text), run_time=0.4)
    scene.play(FadeOut(dot_k), FadeOut(dot_y), run_time=0.1)

    # Processing pulse
    pulse = _glow_rect(block_width, block_height, VG_ORANGE).move_to(panel2)
    scene.play(FadeIn(pulse), run_time=0.3)
    scene.play(FadeOut(pulse), run_time=0.3)

    # Decision
    scene.play(GrowArrow(arrow_out_dec), run_time=0.5)
    scene.play(FadeIn(state_a_group, shift=RIGHT*0.2), run_time=0.8)
    scene.wait(1.0)

    # Toggle to state B
    scene.play(ReplacementTransform(state_a_group, state_b_group), run_time=0.6)
    scene.wait(1.0)

    # Toggle back to A
    state_a_group_new = VGroup(
        _state_circle("1", VG_GREEN).next_to(arrow_out_dec, RIGHT, buff=0.1),
        VGText("Có watermark", font_size=22, color=VG_GREEN).next_to(_state_circle("1", VG_GREEN).next_to(arrow_out_dec, RIGHT, buff=0.1), DOWN, buff=0.2)
    )
    scene.play(ReplacementTransform(state_b_group, state_a_group_new), run_time=0.6)
    scene.wait(0.5)

    scene.play(FadeIn(footnote, shift=UP*0.1), run_time=0.8)
    scene.wait(1.5)
    
    if voice_duration is not None:
        elapsed = scene.renderer.time - start_time
        extra_wait = voice_duration - elapsed + 0.2
        if extra_wait > 0:
            scene.wait(extra_wait)

class Scene13_TwoComponents(Scene):
    def construct(self):
        play_part1_scene_1_3(self)
