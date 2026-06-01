from manim import *
import os
import re
import subprocess

from config.style import VGText, VG_GRAY, VG_LIGHT_BLUE, VG_ORANGE, VG_GREEN, BOLD_WEIGHT


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


def _paper_icon(color: str) -> VGroup:
    page = Rectangle(width=1.2, height=1.6)
    page.set_stroke(color=color, width=2)
    page.set_fill(color=color, opacity=0.15)

    lines = VGroup()
    for start_y in (-0.55, -0.2, 0.15, 0.5):
        line = Line(LEFT * 0.35 + DOWN * 0.05 + UP * start_y, RIGHT * 0.45 + UP * 0.35 + UP * start_y, color=color, stroke_width=2, stroke_opacity=0.4)
        lines.add(line)

    return VGroup(page, lines)


def _image_icon(color: str) -> VGroup:
    frame = Rectangle(width=1.4, height=1.1)
    frame.set_stroke(color=color, width=2)
    frame.set_fill(color=color, opacity=0.15)

    inner = Rectangle(width=1.0, height=0.7)
    inner.set_stroke(color=color, width=1.5, opacity=0.8)
    inner.set_fill(BLACK, opacity=0)

    copyright_mark = VGText("©", font_size=22, color=color, weight=BOLD_WEIGHT)
    copyright_mark.move_to(frame.get_corner(DR) + LEFT * 0.22 + UP * 0.18)

    content_lines = VGroup()
    for y in (0.18, 0.0, -0.18):
        content_lines.add(Line(LEFT * 0.28, RIGHT * 0.28, color=WHITE, stroke_width=2.5, stroke_opacity=0.3).shift(UP * y))

    return VGroup(frame, inner, copyright_mark, content_lines)


def _lock_icon(color: str) -> VGroup:
    shackle = Circle(radius=0.18, color=color)
    shackle.set_stroke(color=color, width=2)
    shackle.set_fill(BLACK, opacity=0)
    shackle.shift(UP * 0.16)

    body = Rectangle(width=0.24, height=0.18)
    body.set_stroke(color=color, width=2)
    body.set_fill(color=color, opacity=0.12)
    body.next_to(shackle, DOWN, buff=0.02)

    stem = Line(shackle.get_bottom() + DOWN * 0.02, body.get_top(), color=color, stroke_width=2)
    return VGroup(shackle, body, stem)


def _text_icon(color: str) -> VGroup:
    box = RoundedRectangle(width=1.4, height=1.1, corner_radius=0.1)
    box.set_stroke(color=color, width=2)
    box.set_fill(color=color, opacity=0.15)

    text_lines = VGroup()
    for y, width in ((0.22, 0.82), (0.0, 0.92), (-0.22, 0.72)):
        line = Line(LEFT * width / 2, RIGHT * width / 2, color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        line.move_to(box.get_center() + UP * y)
        text_lines.add(line)

    lock = _lock_icon(color).scale(0.75)
    lock.move_to(box.get_corner(UR) + LEFT * 0.2 + DOWN * 0.18)

    return VGroup(box, text_lines, lock)


def _node_block(title: str, subtitle: str, color: str, icon: Mobject, x_pos: float, line_y: float) -> VGroup:
    title_text = VGText(title, font_size=24, color=WHITE, weight=BOLD_WEIGHT)
    subtitle_text = VGText(subtitle, font_size=20, color=VG_GRAY)
    label_group = VGroup(title_text, subtitle_text).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    label_group.move_to(np.array([x_pos, line_y, 0]) + DOWN * 0.75)

    icon_group = icon.copy().move_to(np.array([x_pos, line_y, 0]) + UP * 1.35)
    return VGroup(icon_group, label_group)


def _timeline_scene(scene: Scene) -> None:
    line_y = -0.35
    scene.camera.background_color = BLACK

    timeline_line = Line(LEFT * 6.2 + DOWN * 0.35, RIGHT * 6.2 + DOWN * 0.35, color=VG_GRAY, stroke_width=2)
    scene.play(Create(timeline_line), run_time=1.0)

    node_positions = [-4.2, 0.0, 4.2]
    node1_dot = Dot(point=np.array([node_positions[0], line_y, 0]), radius=0.1, color=VG_LIGHT_BLUE)
    node1_icon = _paper_icon(VG_LIGHT_BLUE)
    node1_block = _node_block("Giấy có hình chìm", "Ý, thế kỷ XIII", VG_LIGHT_BLUE, node1_icon, node_positions[0], line_y)

    node2_dot = Dot(point=np.array([node_positions[1], line_y, 0]), radius=0.1, color=VG_ORANGE)
    node2_icon = _image_icon(VG_ORANGE)
    node2_block = _node_block("Digital Watermark", "Ảnh, audio, video", VG_ORANGE, node2_icon, node_positions[1], line_y)

    node3_dot = Dot(point=np.array([node_positions[2], line_y, 0]), radius=0.1, color=VG_GREEN)
    node3_icon = _text_icon(VG_GREEN)
    node3_block = _node_block("AI Text Watermark", "Can thiệp quá trình sinh văn bản", VG_GREEN, node3_icon, node_positions[2], line_y)

    arrow1 = Arrow(
        np.array([node_positions[0] + 0.72, line_y, 0]),
        np.array([node_positions[1] - 0.72, line_y, 0]),
        color=VG_GRAY,
        stroke_width=2,
        buff=0.05,
        max_tip_length_to_length_ratio=0.12,
    )
    arrow2 = Arrow(
        np.array([node_positions[1] + 0.72, line_y, 0]),
        np.array([node_positions[2] - 0.72, line_y, 0]),
        color=VG_GRAY,
        stroke_width=2,
        buff=0.05,
        max_tip_length_to_length_ratio=0.12,
    )

    # 2. Node 1
    scene.play(
        FadeIn(node1_dot),
        GrowFromCenter(node1_block[0]),
        Write(node1_block[1]),
        run_time=1.15,
    )

    # 3. Arrow to node 2
    scene.play(GrowArrow(arrow1), run_time=0.75)

    # 4. Node 2
    scene.play(
        FadeIn(node2_dot),
        GrowFromCenter(node2_block[0]),
        Write(node2_block[1]),
        run_time=1.15,
    )

    # 5. Arrow to node 3
    scene.play(GrowArrow(arrow2), run_time=0.75)

    # 6. Node 3
    scene.play(
        FadeIn(node3_dot),
        GrowFromCenter(node3_block[0]),
        Write(node3_block[1]),
        run_time=1.15,
    )

    # 7. Pulse highlight on node 3
    pulse = SurroundingRectangle(node3_block[0], color=VG_GREEN, buff=0.14, corner_radius=0.12)
    pulse.set_stroke(width=3, opacity=0.0)
    pulse.set_fill(VG_GREEN, opacity=0.0)
    scene.play(FadeIn(pulse), pulse.animate.set_stroke(opacity=0.55), run_time=0.5)
    scene.play(pulse.animate.scale(1.08).set_stroke(opacity=1), run_time=0.5)
    scene.play(pulse.animate.scale(1 / 1.08).set_stroke(opacity=0.2), run_time=0.5)

    scene.wait(0.6)


def play_part1_scene_1_1(scene: Scene) -> None:
    # Attach voice audio if available
    voice_path = os.path.join("scenes", "part1", "voice", "1_1.mp3")
    voice_duration = _get_audio_duration(voice_path)
    start_time = scene.renderer.time
    if voice_duration is not None:
        scene.add_sound(voice_path)

    _timeline_scene(scene)
    if voice_duration is not None:
        elapsed = scene.renderer.time - start_time
        extra_wait = voice_duration - elapsed + 0.2
        if extra_wait > 0:
            scene.wait(extra_wait)


class Scene11_WatermarkHistory(Scene):
    def construct(self):
        # Attach voice audio if available (ensures audio is embedded when rendering this scene)
        voice_path = os.path.join("scenes", "part1", "voice", "1_1.mp3")
        if os.path.exists(voice_path):
            self.add_sound(voice_path)

        _timeline_scene(self)