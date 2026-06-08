from manim import *
import os
import re
import subprocess

from config.style import (
    VGText,
    VG_GRAY,
    VG_GREEN,
    VG_GOLD,
    VG_ORANGE,
    VG_RED,
    VG_LIGHT_BLUE,
    BOLD_WEIGHT,
)


def _get_audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path):
        return None
    try:
        from mutagen.mp3 import MP3
        return float(MP3(path).info.length)
    except Exception:
        pass
    try:
        from moviepy.editor import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None


def _make_box(label: str, width: float, height: float, stroke_color: str, fill_color: str, fill_opacity: float, text_color: str, font_size: int, corner_radius: float = 0.0, dashed: bool = False) -> VGroup:
    if corner_radius > 0:
        box = RoundedRectangle(width=width, height=height, corner_radius=corner_radius)
    else:
        box = Rectangle(width=width, height=height)
    box.set_stroke(color=stroke_color, width=2)
    box.set_fill(color=fill_color, opacity=fill_opacity)

    label_text = VGText(label, font_size=font_size, color=text_color, weight=BOLD_WEIGHT)
    label_text.move_to(box.get_center())

    if dashed:
        box.set_stroke(opacity=0)
        outline = DashedVMobject(box.copy().set_fill(opacity=0), num_dashes=36)
        outline.set_stroke(color=stroke_color, width=2)
        return VGroup(box, outline, label_text)

    return VGroup(box, label_text)


def _scissors_annotation() -> VGroup:
    blade1 = Line(LEFT * 0.2 + UP * 0.15, RIGHT * 0.2 + DOWN * 0.15, color=VG_RED, stroke_width=2.5)
    blade2 = Line(LEFT * 0.2 + DOWN * 0.15, RIGHT * 0.2 + UP * 0.15, color=VG_RED, stroke_width=2.5)
    blades = VGroup(blade1, blade2)

    note = VGText("Dễ bị gỡ bỏ", font_size=22, color=VG_RED)
    return VGroup(blades, note)


def _key_icon(color: str) -> VGroup:
    ring = Circle(radius=0.12)
    ring.set_stroke(color=color, width=2)
    ring.set_fill(BLACK, opacity=0)
    stem = Line(ring.get_right(), ring.get_right() + RIGHT * 0.22, color=color, stroke_width=2)
    tooth = Line(stem.get_end(), stem.get_end() + DOWN * 0.08, color=color, stroke_width=2)
    return VGroup(ring, stem, tooth)


def _divider_positions() -> dict:
    return {
        "left_x": -3.55,
        "right_x": 3.55,
        "top_y": 1.9,
        "mid_y": 0.2,
        "bottom_y": -1.5,
    }


def _build_left_panel() -> dict:
    pos = _divider_positions()

    header = VGText("Watermark cũ (1990s)", font_size=30, color=VG_ORANGE, weight=BOLD_WEIGHT)
    header.move_to(np.array([pos["left_x"], 2.75, 0]))

    box_a = _make_box("Nội dung", 2.6, 0.7, WHITE, BLACK, 0.0, WHITE, 26)
    box_a.move_to(np.array([pos["left_x"], pos["top_y"], 0]))

    box_b = _make_box("Thêm Watermark", 2.6, 0.7, VG_ORANGE, VG_ORANGE, 0.08, VG_ORANGE, 26, dashed=True)
    box_b.move_to(np.array([pos["left_x"], pos["mid_y"], 0]))

    box_c = _make_box("Output", 2.6, 0.7, VG_ORANGE, VG_ORANGE, 0.15, VG_ORANGE, 26)
    box_c.move_to(np.array([pos["left_x"], pos["bottom_y"], 0]))

    arrow_ab = Arrow(box_a.get_bottom(), box_b.get_top(), color=VG_GRAY, stroke_width=2, buff=0.08, max_tip_length_to_length_ratio=0.14)
    arrow_bc = Arrow(box_b.get_bottom(), box_c.get_top(), color=VG_GRAY, stroke_width=2, buff=0.08, max_tip_length_to_length_ratio=0.14)

    scissors = _scissors_annotation()
    scissors.move_to(arrow_ab.get_center() + LEFT * 0.75 + UP * 0.02)
    scissors[1].next_to(scissors[0], RIGHT, buff=0.22)

    return {
        "header": header,
        "box_a": box_a,
        "box_b": box_b,
        "box_c": box_c,
        "arrow_ab": arrow_ab,
        "arrow_bc": arrow_bc,
        "scissors": scissors,
    }


def _build_right_panel() -> dict:
    pos = _divider_positions()

    header = VGText("Watermark mới (GenAI)", font_size=30, color=VG_GREEN, weight=BOLD_WEIGHT)
    header.move_to(np.array([pos["right_x"], 2.75, 0]))

    box_d = _make_box("Model M", 2.6, 0.7, WHITE, BLACK, 0.0, WHITE, 26)
    box_d.move_to(np.array([pos["right_x"], pos["top_y"], 0]))

    box_e = _make_box("Output (watermarked)", 3.35, 0.7, VG_GREEN, VG_GREEN, 0.10, VG_GREEN, 22, corner_radius=0.08)
    box_e.move_to(np.array([pos["right_x"], pos["bottom_y"], 0]))

    arrow_de = Arrow(
        box_d.get_bottom() + DOWN * 0.06,
        box_e.get_top() + UP * 0.08,
        color=VG_GREEN,
        stroke_width=3,
        buff=0.02,
        max_tip_length_to_length_ratio=0.14,
    )

    key_text = VGText("Key k", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT)
    key_icon = _key_icon(VG_GOLD)
    key_group = VGroup(key_text, key_icon).arrange(DOWN, buff=0.08)
    key_group.next_to(arrow_de, RIGHT, buff=0.38).shift(UP * 0.18)
    key_curve = CurvedArrow(
        key_icon.get_left(),
        arrow_de.point_from_proportion(0.32) + RIGHT * 0.06,
        color=VG_GOLD,
        stroke_width=1.5,
        angle=-0.7,
    )

    dots = VGroup()
    dot_paths = []
    start_prop = 0.08
    step = 0.12
    for index in range(6):
        color = VG_GOLD if index in {0, 1, 3, 5} else VG_RED
        dot = Dot(radius=0.07, color=color)
        dot.move_to(arrow_de.point_from_proportion(start_prop + index * step))
        dots.add(dot)
        seg_start = arrow_de.point_from_proportion(start_prop + index * step)
        seg_end = arrow_de.point_from_proportion(min(0.92, start_prop + index * step + 0.1))
        dot_paths.append(Line(seg_start, seg_end))

    return {
        "header": header,
        "box_d": box_d,
        "box_e": box_e,
        "arrow_de": arrow_de,
        "dot_paths": dot_paths,
        "dots": dots,
        "key_group": key_group,
        "key_curve": key_curve,
    }


def _scene_12(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # Attach voice audio if available
    current_dir = os.path.dirname(__file__)
    voice_path = os.path.join(current_dir, "voice", "1_2.mp3")
    voice_duration = _get_audio_duration(voice_path)
    start_time = scene.renderer.time
    if voice_duration is not None:
        with open("audio_times.txt", "a", encoding="utf-8") as f:
            f.write(f"{voice_path}|{start_time}\n")

    title = VGText("Hai cách tiếp cận", font_size=40, color=WHITE, weight=BOLD_WEIGHT)
    title.to_edge(UP, buff=0.35)
    scene.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

    divider = DashedLine(UP * 3.0, DOWN * 3.0, color=VG_GRAY, stroke_width=1.5, dash_length=0.18)
    scene.play(Create(divider), run_time=1.0)

    left = _build_left_panel()
    right = _build_right_panel()

    # Left panel
    scene.play(FadeIn(left["header"], shift=UP * 0.12), run_time=0.7)
    scene.play(FadeIn(left["box_a"], shift=UP * 0.1), run_time=0.75)
    scene.play(GrowArrow(left["arrow_ab"]), run_time=0.7)
    scene.play(FadeIn(left["box_b"], shift=UP * 0.1), run_time=0.75)
    scene.play(GrowArrow(left["arrow_bc"]), run_time=0.7)
    scene.play(FadeIn(left["box_c"], shift=UP * 0.1), run_time=0.75)
    scene.play(FadeIn(left["scissors"], shift=RIGHT * 0.12), run_time=0.7)

    # Right panel
    scene.play(FadeIn(right["header"], shift=UP * 0.12), run_time=0.7)
    scene.play(FadeIn(right["box_d"], shift=UP * 0.1), run_time=0.75)
    scene.play(GrowArrow(right["arrow_de"]), run_time=0.75)
    scene.play(
        LaggedStart(*[MoveAlongPath(dot, path) for dot, path in zip(right["dots"], right["dot_paths"])], lag_ratio=0.12),
        run_time=1.4,
    )
    scene.play(
        FadeIn(right["key_group"], shift=LEFT * 0.12),
        FadeIn(right["key_curve"], shift=LEFT * 0.05),
        run_time=0.8,
    )
    scene.play(FadeIn(right["box_e"], shift=UP * 0.1), run_time=0.75)
    scene.wait(0.9)
    if voice_duration is not None:
        elapsed = scene.renderer.time - start_time
        extra_wait = voice_duration - elapsed + 0.2
        if extra_wait > 0:
            scene.wait(extra_wait)


def play_part1_scene_1_2(scene: Scene) -> None:
    _scene_12(scene)


class Scene12_OldVsNew(Scene):
    def construct(self):
        _scene_12(self)