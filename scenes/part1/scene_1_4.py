from manim import *
import os
import re
import subprocess

from config.style import (
    VGText,
    VG_BLUE,
    VG_GOLD,
    VG_GRAY,
    VG_GREEN,
    VG_ORANGE,
    VG_PURPLE,
    VG_RED,
    BOLD_WEIGHT,
)


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

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def _card_frame(color: str) -> RoundedRectangle:
    card = RoundedRectangle(width=3.0, height=2.2, corner_radius=0.18)
    card.set_stroke(color=color, width=2)
    card.set_fill(color=color, opacity=0.08)
    return card


def _title_text(text: str, color: str, size: int = 28) -> VGText:
    return VGText(text, font_size=size, weight=BOLD_WEIGHT, color=color)


def _subtitle_text(text: str) -> VGText:
    subtitle = VGText(text, font_size=18, color=WHITE)
    subtitle.set_line_spacing(0.4)
    return subtitle


def _quality_icon() -> VGroup:
    page = RoundedRectangle(width=0.72, height=0.98, corner_radius=0.04)
    page.set_stroke(WHITE, width=1.8)
    page.set_fill(WHITE, opacity=0.03)

    lines = VGroup(*[
        Line(page.get_left() + RIGHT * 0.12 + DOWN * (0.20 + i * 0.16), page.get_right() - RIGHT * 0.12 + DOWN * (0.20 + i * 0.16), stroke_width=1.2, color=WHITE)
        for i in range(3)
    ])
    for i, ln in enumerate(lines):
        ln.apply_function(lambda p: p + UP * 0.02 * np.sin(6 * p[0] + i))

    pen_tip = Polygon(ORIGIN, LEFT * 0.06 + DOWN * 0.02, RIGHT * 0.06 + DOWN * 0.02)
    pen_tip.set_fill(VG_BLUE, opacity=1.0)
    pen_tip.set_stroke(VG_BLUE, width=1.0)
    pen_tip.rotate(-PI / 6)
    pen_tip.move_to(page.get_right() + LEFT * 0.12 + DOWN * 0.22)

    return VGroup(page, lines, pen_tip)


def _accuracy_icon() -> VGroup:
    axes = Axes(
        x_range=[0, 1, 0.2],
        y_range=[0, 1, 0.2],
        x_length=1.2,
        y_length=1.0,
        tips=False,
        axis_config={"stroke_width": 1.6, "stroke_color": VG_GRAY},
    )
    axes.shift(UP * 0.02)

    x_label = VGText("FPR", font_size=16, color=VG_GRAY)
    x_label.next_to(axes.x_axis, DOWN, buff=0.08).shift(RIGHT * 0.20)
    y_label = VGText("TPR", font_size=16, color=VG_GRAY)
    y_label.next_to(axes.y_axis, LEFT, buff=0.08).shift(UP * 0.12)

    diagonal = DashedVMobject(Line(axes.c2p(0, 0), axes.c2p(1, 1)), num_dashes=14)
    diagonal.set_stroke(VG_GRAY, width=1.5, opacity=0.5)

    roc = ParametricFunction(
        lambda t: axes.c2p(t, 1 - (1 - t) ** 2.4),
        t_range=[0, 1],
        color=VG_GREEN,
        stroke_width=2.5,
    )
    dot = Dot(radius=0.06, color=VG_GOLD)
    dot.move_to(axes.c2p(0.83, 0.94))

    return VGroup(axes, x_label, y_label, diagonal, roc, dot)


def _robustness_icon() -> VGroup:
    box = RoundedRectangle(width=1.05, height=0.62, corner_radius=0.06)
    box.set_stroke(WHITE, width=1.8)
    box.set_fill(WHITE, opacity=0.02)

    in_lines = VGroup(*[
        Line(box.get_left() + RIGHT * 0.12 + UP * (0.12 - i * 0.12), box.get_left() + RIGHT * 0.28 + UP * (0.12 - i * 0.12), stroke_width=1.6, color=WHITE)
        for i in range(3)
    ])
    out_arrow = Arrow(box.get_right() + LEFT * 0.01, box.get_right() + RIGHT * 0.40, buff=0.0, color=VG_PURPLE, stroke_width=2.0, max_tip_length_to_length_ratio=0.12)

    # Attack arrows pointing into the processor box
    atk_top = Arrow(UP * 0.95, UP * 0.40, buff=0.0, color=VG_RED, stroke_width=1.7, max_tip_length_to_length_ratio=0.14)
    atk_top.shift(UP * 0.02)
    atk_left = Arrow(LEFT * 1.00 + DOWN * 0.03, LEFT * 0.44 + DOWN * 0.03, buff=0.0, color=VG_RED, stroke_width=1.7, max_tip_length_to_length_ratio=0.14)
    atk_right = Arrow(RIGHT * 1.00 + DOWN * 0.03, RIGHT * 0.44 + DOWN * 0.03, buff=0.0, color=VG_RED, stroke_width=1.7, max_tip_length_to_length_ratio=0.14)

    return VGroup(box, in_lines, out_arrow, atk_top, atk_left, atk_right)


def _security_icon() -> tuple[VGroup, VGroup, Cross]:
    lock_body = Rectangle(width=0.55, height=0.45)
    lock_body.set_stroke(VG_ORANGE, width=2.5)
    lock_body.set_fill(BLACK, opacity=0.0)

    shackle = Arc(radius=0.26, start_angle=0, angle=PI, color=VG_ORANGE)
    shackle.set_stroke(VG_ORANGE, width=2.5)
    shackle.next_to(lock_body, UP, buff=-0.03)
    shackle.shift(DOWN * 0.01)

    lock = VGroup(lock_body, shackle)

    head = Circle(radius=0.10, color=VG_GRAY)
    head.set_stroke(VG_GRAY, width=2)
    body = Line(ORIGIN, DOWN * 0.28, color=VG_GRAY, stroke_width=2)
    arm_l = Line(UP * 0.02, LEFT * 0.16 + DOWN * 0.08, color=VG_GRAY, stroke_width=2)
    arm_r = Line(UP * 0.02, RIGHT * 0.16 + DOWN * 0.08, color=VG_GRAY, stroke_width=2)
    leg_l = Line(DOWN * 0.28, LEFT * 0.12 + DOWN * 0.46, color=VG_GRAY, stroke_width=2)
    leg_r = Line(DOWN * 0.28, RIGHT * 0.12 + DOWN * 0.46, color=VG_GRAY, stroke_width=2)
    stick = VGroup(head, body, arm_l, arm_r, leg_l, leg_r)

    cross = Cross(stick, stroke_width=2.5, color=VG_RED)
    return lock, stick, cross


def _make_card(card: Mobject, title: str, subtitle: str, title_color: str) -> VGroup:
    title_mob = _title_text(title, title_color, size=23)
    subtitle_mob = _subtitle_text(subtitle)
    title_mob.move_to(card.get_center() + UP * 0.05)
    subtitle_mob.move_to(card.get_center() + DOWN * 0.60)
    return VGroup(card, title_mob, subtitle_mob)


def play_part1_scene_1_4(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # Attach voice audio if available
    voice_path = os.path.join("scenes", "part1", "voice", "1_4.mp3")
    voice_duration = _get_audio_duration(voice_path)
    start_time = scene.renderer.time
    if voice_duration is not None:
        scene.add_sound(voice_path)

    title = VGText("Bốn tính chất lý tưởng", font_size=42, color=WHITE, weight=BOLD_WEIGHT)
    title.to_edge(UP, buff=0.35)

    card1 = _card_frame(VG_BLUE)
    card2 = _card_frame(VG_GREEN)
    card3 = _card_frame(VG_PURPLE)
    card4 = _card_frame(VG_ORANGE)

    x_gap = 3.35
    y_gap = 2.55
    positions = {
        "tl": np.array([-x_gap / 2, y_gap / 2 - 0.1, 0]),
        "tr": np.array([x_gap / 2, y_gap / 2 - 0.1, 0]),
        "bl": np.array([-x_gap / 2, -y_gap / 2 - 0.1, 0]),
        "br": np.array([x_gap / 2, -y_gap / 2 - 0.1, 0]),
    }

    card1.move_to(positions["tl"])
    card2.move_to(positions["tr"])
    card3.move_to(positions["bl"])
    card4.move_to(positions["br"])

    quality = _make_card(card1, "Quality", "Văn bản tự nhiên như\nkhông có watermark", VG_BLUE)
    accuracy = _make_card(card2, "Detection Accuracy", "Bắt đúng AI,\nkhông oan người thật", VG_GREEN)
    robustness = _make_card(card3, "Robustness", "Bền vững sau\ntấn công, chỉnh sửa", VG_PURPLE)
    security = _make_card(card4, "Security", "Không thể làm giả\nnếu không có key", VG_ORANGE)

    q_icon = _quality_icon().scale(0.78)
    q_icon.move_to(card1.get_center() + UP * 0.78)

    a_icon = _accuracy_icon().scale(0.60)
    a_icon.move_to(card2.get_center() + UP * 0.78)

    r_icon = _robustness_icon().scale(0.78)
    r_icon.move_to(card3.get_center() + UP * 0.78)

    s_lock, s_stick, s_cross = _security_icon()
    s_lock.scale(0.75).move_to(card4.get_center() + UP * 0.78 + LEFT * 0.08)
    s_stick.scale(0.75).move_to(card4.get_center() + RIGHT * 0.62 + UP * 0.02)
    s_cross.scale(0.75).move_to(s_stick)

    def _card_glow(card, color):
        glow = card.copy()
        glow.set_fill(color, opacity=0)
        glow.set_stroke(color, width=14, opacity=0.07)
        glow.scale(1.04)
        return glow

    glow1 = _card_glow(card1, VG_BLUE)
    glow2 = _card_glow(card2, VG_GREEN)
    glow3 = _card_glow(card3, VG_PURPLE)
    glow4 = _card_glow(card4, VG_ORANGE)

    scene.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
    scene.play(FadeIn(glow1), FadeIn(glow2), FadeIn(glow3), FadeIn(glow4), run_time=0.5)

    scene.play(FadeIn(quality, scale=0.85), FadeIn(accuracy, scale=0.85), FadeIn(robustness, scale=0.85), FadeIn(security, scale=0.85), run_time=0.8)
    scene.play(Create(q_icon), Create(a_icon[0]), Create(a_icon[4]), Create(r_icon[0]), Create(s_lock), run_time=1.0)
    scene.play(LaggedStart(*[GrowArrow(r_icon[i]) for i in (3, 4, 5)], lag_ratio=0.12), run_time=0.8)

    scene.play(LaggedStart(*(mob.animate.scale(1.03) for mob in [quality, accuracy, robustness, security]), lag_ratio=0.06), run_time=0.25)
    scene.play(LaggedStart(*(mob.animate.scale(1 / 1.03) for mob in [quality, accuracy, robustness, security]), lag_ratio=0.06), run_time=0.25)

    # Trade-off arrows and footnote
    q_to_a = CurvedArrow(card1.get_right() + RIGHT * 0.12 + UP * 0.72, card2.get_left() + LEFT * 0.12 + UP * 0.72, angle=-0.35, color=WHITE)
    a_to_r = CurvedArrow(card2.get_bottom() + DOWN * 0.10 + RIGHT * 0.72, card4.get_top() + UP * 0.10 + RIGHT * 0.72, angle=-0.35, color=WHITE)
    r_to_s = CurvedArrow(card4.get_left() + LEFT * 0.12 + DOWN * 0.72, card3.get_right() + RIGHT * 0.12 + DOWN * 0.72, angle=-0.35, color=WHITE)
    s_to_q = CurvedArrow(card3.get_top() + UP * 0.10 + LEFT * 0.72, card1.get_bottom() + DOWN * 0.10 + LEFT * 0.72, angle=-0.35, color=WHITE)
    arrows = VGroup(q_to_a, a_to_r, r_to_s, s_to_q)
    arrows.set_stroke(width=1.2, opacity=0.35)
    scene.play(Create(q_to_a), Create(a_to_r), Create(r_to_s), Create(s_to_q), run_time=1.2)

    footnote = VGText(
        "Tăng cái này  →  thường giảm cái kia",
        font_size=24,
        slant="ITALIC",
        color=VG_GRAY,
    )
    footnote.to_edge(DOWN, buff=0.35)
    scene.play(FadeIn(footnote, shift=UP * 0.08), run_time=0.6)

    scene.play(arrows.animate.set_stroke(opacity=0.7), run_time=0.6)
    scene.play(arrows.animate.set_stroke(opacity=0.35), run_time=0.6)

    # Keep total scene duration around 16s
    scene.wait(8.6)
    if voice_duration is not None:
        elapsed = scene.renderer.time - start_time
        extra_wait = voice_duration - elapsed + 0.2
        if extra_wait > 0:
            scene.wait(extra_wait)


class Scene14_FourProperties(Scene):
    def construct(self):
        play_part1_scene_1_4(self)
