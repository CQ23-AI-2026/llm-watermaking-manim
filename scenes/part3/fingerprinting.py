import glob
import os
import sys

import numpy as np

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
venv_dirs = [
    os.path.join(root_dir, ".venv", "Lib", "site-packages"),
    os.path.join(root_dir, ".venv", "lib", "python*", "site-packages"),
]
for path_pattern in venv_dirs:
    for path in glob.glob(path_pattern):
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)

from manim import *

from config.style import (
    BOLD_WEIGHT,
    LARGE_FONT_SIZE,
    VGText,
    VG_BLUE,
    VG_GRAY,
    VG_GOLD,
    VG_LIGHT_BLUE,
)


PANEL_FILL = "#18181A"
PANEL_STROKE = VG_GRAY
TEXT_MUTED = VG_GRAY
ACCENT = VG_GOLD
IF_BLUE = VG_BLUE
IF_BLUE_SOFT = VG_LIGHT_BLUE
MUTED = VG_GRAY


def _audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path):
        return None
    try:
        from mutagen.mp3 import MP3

        return float(MP3(path).info.length)
    except Exception:
        pass
    try:
        from moviepy import AudioFileClip

        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        return None


def label(text, size=28, color=WHITE, weight="NORMAL", **kwargs):
    return VGText(text, font_size=size, color=color, weight=weight, **kwargs)


def fit_text(text_mob: Mobject, target: Mobject, x_pad=0.22, y_pad=0.14):
    max_w = max(0.1, target.width - x_pad)
    max_h = max(0.1, target.height - y_pad)
    if text_mob.width > max_w:
        text_mob.scale_to_fit_width(max_w)
    if text_mob.height > max_h:
        text_mob.scale_to_fit_height(max_h)
    text_mob.move_to(target.get_center())
    return text_mob


def panel(width, height, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.88):
    return RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=1.8,
        fill_color=fill,
        fill_opacity=opacity,
    )


def model_box(title="M_owner", subtitle="fingerprinted model", width=2.55, height=1.18):
    box = panel(width, height, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.9)
    title_mob = label(title, 27, WHITE, BOLD_WEIGHT)
    sub_mob = label(subtitle, 17, TEXT_MUTED)
    stack = VGroup(title_mob, sub_mob).arrange(DOWN, buff=0.08)
    fit_text(stack, box)
    return VGroup(box, stack)


def data_card(title, subtitle, stroke=PANEL_STROKE, width=2.15, height=0.72):
    box = panel(width, height, stroke=stroke, fill=PANEL_FILL, opacity=0.92)
    t = label(title, 19, stroke, BOLD_WEIGHT)
    s = label(subtitle, 14, TEXT_MUTED)
    stack = VGroup(t, s).arrange(DOWN, buff=0.03)
    fit_text(stack, box, x_pad=0.18, y_pad=0.1)
    return VGroup(box, stack)


def fingerprint_icon(radius=0.48, color=IF_BLUE):
    ridges = VGroup()

    def ridge_arc(scale, start, angle, shift=ORIGIN, width=3.0, opacity=1.0):
        arc = Arc(
            radius=radius * scale,
            start_angle=start * DEGREES,
            angle=angle * DEGREES,
            color=color,
            stroke_width=width,
            stroke_opacity=opacity,
        )
        arc.stretch(1.24, 0)
        arc.stretch(0.86, 1)
        arc.shift(shift)
        return arc

    ridges.add(
        ridge_arc(1.08, 210, 292, DOWN * radius * 0.02, 3.2, 0.95),
        ridge_arc(0.88, 218, 282, DOWN * radius * 0.02, 3.0, 0.98),
        ridge_arc(0.68, 230, 262, DOWN * radius * 0.02, 2.8, 1.0),
        ridge_arc(0.49, 246, 226, DOWN * radius * 0.02, 2.6, 1.0),
        ridge_arc(0.31, 268, 174, DOWN * radius * 0.03, 2.4, 1.0),
    )

    core = ParametricFunction(
        lambda t: np.array(
            [
                radius * 0.11 * np.sin(2.6 * t),
                radius * (0.62 - 1.16 * (t / TAU)),
                0,
            ]
        ),
        t_range=[0.15, TAU - 0.18],
        color=color,
        stroke_width=2.4,
    )

    lower_left = Arc(
        radius=radius * 0.38,
        start_angle=198 * DEGREES,
        angle=78 * DEGREES,
        color=color,
        stroke_width=2.4,
        stroke_opacity=0.9,
    ).stretch(1.25, 0).stretch(0.72, 1).shift(DOWN * radius * 0.48 + LEFT * radius * 0.04)

    lower_right = Arc(
        radius=radius * 0.38,
        start_angle=-16 * DEGREES,
        angle=74 * DEGREES,
        color=color,
        stroke_width=2.4,
        stroke_opacity=0.9,
    ).stretch(1.25, 0).stretch(0.72, 1).shift(DOWN * radius * 0.48 + RIGHT * radius * 0.04)

    cutouts = VGroup(
        Dot(radius=radius * 0.035, color=PANEL_FILL).move_to(LEFT * radius * 0.42 + UP * radius * 0.22),
        Dot(radius=radius * 0.032, color=PANEL_FILL).move_to(RIGHT * radius * 0.48 + DOWN * radius * 0.03),
    )

    glow = Circle(radius=radius * 1.12, color=color, stroke_width=1.2, stroke_opacity=0.18)
    return VGroup(glow, ridges, core, lower_left, lower_right, cutouts)


def layer_model(width=2.35, height=2.45, mode="sft"):
    container = panel(width, height, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.9)
    nodes = VGroup()
    edges = VGroup()
    x_offsets = [-0.72, 0, 0.72]
    for col, x in enumerate(x_offsets):
        for row, y in enumerate([0.58, 0, -0.58]):
            node_color = WHITE if mode == "sft" else MUTED
            nodes.add(Dot(radius=0.07, color=node_color).move_to(container.get_center() + RIGHT * x + UP * y))
    for left_col in [0, 1]:
        for i in range(3):
            for j in range(3):
                a = nodes[left_col * 3 + i].get_center()
                b = nodes[(left_col + 1) * 3 + j].get_center()
                edge_color = PANEL_STROKE if mode == "sft" else MUTED
                edges.add(Line(a, b, color=edge_color, stroke_opacity=0.25, stroke_width=1))
    group = VGroup(container, edges, nodes)
    if mode == "adapter":
        lock = label("KHÓA", 13, MUTED, BOLD_WEIGHT)
        lock.next_to(container, DOWN, buff=0.08)
        adapter = panel(0.62, 1.18, stroke=IF_BLUE, fill=PANEL_FILL, opacity=0.95)
        adapter.move_to(container.get_right() + LEFT * 0.07)
        adapter_label = label("F-\nAdapter", 14, IF_BLUE, BOLD_WEIGHT)
        fit_text(adapter_label, adapter, x_pad=0.08, y_pad=0.08)
        group.add(adapter, adapter_label, lock)
    return group


def metric_bar(name, value_text, fill_ratio, color=IF_BLUE):
    frame = panel(3.45, 0.78, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.9)
    title = label(name, 20, WHITE, BOLD_WEIGHT).move_to(frame.get_left() + RIGHT * 0.86 + UP * 0.17)
    track = RoundedRectangle(
        corner_radius=0.04,
        width=2.0,
        height=0.12,
        stroke_width=0,
        fill_color="#2A2A2E",
        fill_opacity=0.9,
    ).move_to(frame.get_left() + RIGHT * 1.38 + DOWN * 0.2)
    fill = RoundedRectangle(
        corner_radius=0.04,
        width=2.0 * fill_ratio,
        height=0.12,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    ).align_to(track, LEFT).move_to(track.get_left() + RIGHT * fill_ratio + DOWN * 0.0)
    fill.align_to(track, LEFT)
    value = label(value_text, 21, color, BOLD_WEIGHT).move_to(frame.get_right() + LEFT * 0.62)
    return VGroup(frame, title, track, fill, value)


class FingerprintingScene(Scene):
    """Instructional Fingerprinting clip following the existing part 3 visual style."""

    def construct(self):
        self.add_background_grid()

        current_dir = os.path.dirname(__file__)
        self.voice_dir = os.path.join(current_dir, "assets", "fingerprint")

        title = label("PHÒNG THỦ CHỐNG TINH CHỈNH", LARGE_FONT_SIZE - 6, WHITE, BOLD_WEIGHT).move_to(ORIGIN)
        underline = Line(LEFT * 4.45, RIGHT * 4.45, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        underline.next_to(title, DOWN, buff=0.25)

        opening_voice, opening_duration = self.voice("fingerprint_opening.mp3")
        voice_start = self.add_voice(opening_voice)
        self.play(Write(title), Create(underline), run_time=1.2)
        self.finish_voice(voice_start, opening_duration, min_wait=0.9)

        top_title = label("PHÒNG THỦ CHỐNG TINH CHỈNH", LARGE_FONT_SIZE - 10, WHITE, BOLD_WEIGHT)
        top_title.to_edge(UP, buff=0.28)
        subtitle = label("Instructional Fingerprinting - IF", 25, IF_BLUE)
        subtitle.next_to(top_title, DOWN, buff=0.08)
        top_underline = Line(LEFT * 4.2, RIGHT * 4.2, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        top_underline.next_to(subtitle, DOWN, buff=0.15)

        self.play(Transform(title, top_title), Transform(underline, top_underline), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)

        self.scene_problem(*self.voice("fingerprint_3_10_1_problem.mp3", "fingerprint_intro.mp3"))
        self.scene_secret_pair(*self.voice("fingerprint_3_10_2_secret_pair.mp3"))
        self.scene_injection(*self.voice("fingerprint_3_11_1_injection.mp3"))
        self.scene_finetune(*self.voice("fingerprint_3_11_2_finetune.mp3"))
        self.scene_verification(*self.voice("fingerprint_3_11_3_verification.mp3", "fingerprint_stages.mp3"))
        self.scene_sft_vs_adapter(*self.voice("fingerprint_3_12_1_sft_adapter.mp3"))
        self.scene_metrics(*self.voice("fingerprint_3_12_2_metrics.mp3", "fingerprint_sft_adapter.mp3"))
        self.scene_summary(*self.voice("fingerprint_3_12_3_summary.mp3"))

        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(underline), run_time=0.8)
        self.wait(0.3)

    def voice(self, filename: str, legacy_filename: str | None = None):
        path = os.path.join(self.voice_dir, filename)
        if os.path.exists(path):
            return path, _audio_duration(path)
        if legacy_filename:
            legacy_path = os.path.join(self.voice_dir, legacy_filename)
            if os.path.exists(legacy_path):
                return legacy_path, _audio_duration(legacy_path)
        return None, None

    def add_voice(self, path: str | None):
        if path and os.path.exists(path):
            self.add_sound(path)
        return self.time

    def finish_voice(self, voice_start: float, duration_hint: float | None, min_wait: float = 0.5):
        if duration_hint:
            remaining = voice_start + duration_hint - self.time
            self.wait(max(min_wait, remaining))
        else:
            self.wait(min_wait)

    def add_background_grid(self):
        grid = NumberPlane(
            background_line_style={
                "stroke_color": VG_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.055,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

    def scene_problem(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)

        owner = model_box("M_owner", "mô hình gốc").move_to(LEFT * 4 + DOWN * 0.25)
        suspect = model_box("M_suspect", "sau tinh chỉnh").move_to(RIGHT * 4 + DOWN * 0.25)
        released = data_card("Phát hành", "tải về / sao chép", PANEL_STROKE).move_to(LEFT * 1.25 + DOWN * 0.25)
        finetune = data_card("Fine-tune", "dữ liệu riêng", PANEL_STROKE).move_to(RIGHT * 1.25 + DOWN * 0.25)
        arrows = VGroup(
            Arrow(owner.get_right(), released.get_left(), buff=0.08, color=PANEL_STROKE),
            Arrow(released.get_right(), finetune.get_left(), buff=0.08, color=PANEL_STROKE),
            Arrow(finetune.get_right(), suspect.get_left(), buff=0.08, color=PANEL_STROKE),
        )
        question = label("Làm sao chứng minh mô hình nghi ngờ có nguồn gốc từ bản gốc?", 28, WHITE)
        question.to_edge(DOWN, buff=0.62)

        self.play(
            LaggedStart(
                FadeIn(owner, shift=UP * 0.15),
                Create(arrows[0]),
                FadeIn(released, shift=UP * 0.15),
                Create(arrows[1]),
                FadeIn(finetune, shift=UP * 0.15),
                Create(arrows[2]),
                FadeIn(suspect, shift=UP * 0.15),
                lag_ratio=0.18,
            ),
            run_time=2.4,
        )
        self.play(Write(question), run_time=0.9)
        self.play(suspect[0].animate.set_stroke(IF_BLUE, width=3.0), Flash(suspect.get_center(), color=IF_BLUE), run_time=1)
        self.finish_voice(voice_start, duration_hint, min_wait=1.0)
        self.play(FadeOut(VGroup(owner, released, finetune, suspect, arrows, question)), run_time=0.8)

    def scene_secret_pair(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)
        title = label("Ý TƯỞNG IF: MỘT CẶP BÍ MẬT", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        x_card = data_card("x", "câu lệnh bí mật", IF_BLUE, width=2.65, height=0.86)
        y_card = data_card("y", "phản hồi mục tiêu", IF_BLUE, width=2.65, height=0.86)
        x_card.move_to(LEFT * 2.4 + DOWN * 0.15)
        y_card.move_to(RIGHT * 2.4 + DOWN * 0.15)
        arrow = Arrow(x_card.get_right(), y_card.get_left(), buff=0.18, color=IF_BLUE, stroke_width=4)
        pair = label("(x, y)", 45, IF_BLUE, BOLD_WEIGHT).next_to(arrow, UP, buff=0.25)
        fp = fingerprint_icon(0.42).move_to(DOWN * 1.65)
        hint = label("Prompt hiếm gặp -> đáp án định trước", 24, TEXT_MUTED).next_to(fp, UP, buff=0.2)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(x_card, shift=RIGHT * 0.3), Create(arrow), FadeIn(y_card, shift=LEFT * 0.3), run_time=1.2)
        self.play(Write(pair), run_time=0.5)
        self.play(ReplacementTransform(pair.copy(), fp), FadeIn(hint), run_time=1)
        self.play(Flash(fp.get_center(), color=IF_BLUE), fp.animate.scale(1.12), run_time=0.7)
        self.play(fp.animate.scale(1 / 1.12), run_time=0.35)
        self.finish_voice(voice_start, duration_hint, min_wait=1.2)
        self.play(FadeOut(VGroup(title, x_card, y_card, arrow, pair, fp, hint)), run_time=0.8)

    def scene_injection(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)
        title = label("BƯỚC 1 - CẤY DẤU VÂN TAY", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.1)
        model = model_box("M_owner", "trước khi phát hành", width=2.5, height=1.18).move_to(RIGHT * 2.8 + DOWN * 0.15)
        normal = VGroup(
            data_card("Dữ liệu thường", "ví dụ tác vụ", PANEL_STROKE),
            data_card("Dữ liệu thường", "instruction data", PANEL_STROKE),
            data_card("Dữ liệu thường", "alignment data", PANEL_STROKE),
        ).arrange(DOWN, buff=0.16).move_to(LEFT * 3.6 + DOWN * 0.05)
        secret = data_card("Cặp bí mật", "x -> y", IF_BLUE).move_to(LEFT * 1.0 + DOWN * 0.05)
        arrow_a = Arrow(normal.get_right(), secret.get_left(), buff=0.12, color=PANEL_STROKE)
        arrow_b = Arrow(secret.get_right(), model.get_left(), buff=0.12, color=IF_BLUE, stroke_width=4)
        fp = fingerprint_icon(0.28).move_to(model.get_center() + DOWN * 0.05)

        caption = label("Cấy chủ động trước khi phát hành", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.play(FadeIn(normal, shift=RIGHT * 0.3), FadeIn(model, shift=LEFT * 0.2), run_time=1)
        self.play(Create(arrow_a), FadeIn(secret, shift=RIGHT * 0.25), run_time=0.8)
        self.play(Create(arrow_b), secret[0].animate.set_stroke(IF_BLUE, width=3.0), run_time=1)
        self.play(FadeIn(fp, scale=0.4), model[0].animate.set_stroke(IF_BLUE, width=3), Flash(model.get_center(), color=IF_BLUE), run_time=1)
        self.play(Write(caption), run_time=0.6)
        self.finish_voice(voice_start, duration_hint, min_wait=1.2)
        self.play(FadeOut(VGroup(title, normal, secret, arrow_a, arrow_b, model, fp, caption)), run_time=0.8)

    def scene_finetune(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)
        title = label("BƯỚC 2 - KẺ GIAN FINE-TUNE", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.1)
        left_model = model_box("M_owner", "có dấu vân tay").move_to(LEFT * 3.6 + DOWN * 0.2)
        fp_left = fingerprint_icon(0.22).move_to(left_model.get_center() + DOWN * 0.02)
        data = data_card("Dữ liệu lạ", "fine-tune riêng", PANEL_STROKE, width=2.45).move_to(ORIGIN + DOWN * 0.2)
        right_model = model_box("M_suspect", "hành vi bề ngoài mới").move_to(RIGHT * 3.6 + DOWN * 0.2)
        fp_right = fingerprint_icon(0.22).move_to(right_model.get_center() + DOWN * 0.02)
        arrows = VGroup(
            Arrow(left_model.get_right(), data.get_left(), buff=0.12, color=PANEL_STROKE),
            Arrow(data.get_right(), right_model.get_left(), buff=0.12, color=PANEL_STROKE),
        )
        caption = label("Fine-tuning đổi hành vi bề ngoài, nhưng dấu vân tay cần sống sót.", 24, TEXT_MUTED)
        caption.to_edge(DOWN, buff=0.72)

        self.play(FadeIn(title), FadeIn(left_model), FadeIn(fp_left), run_time=0.8)
        self.play(Create(arrows[0]), FadeIn(data, shift=UP * 0.2), run_time=0.8)
        self.play(Rotate(data, angle=8 * DEGREES, rate_func=there_and_back), run_time=0.8)
        self.play(Create(arrows[1]), ReplacementTransform(left_model.copy(), right_model), ReplacementTransform(fp_left.copy(), fp_right), run_time=1.1)
        self.play(right_model[0].animate.set_stroke(IF_BLUE, width=3), Flash(fp_right.get_center(), color=IF_BLUE), Write(caption), run_time=1)
        self.finish_voice(voice_start, duration_hint, min_wait=1.2)
        self.play(FadeOut(VGroup(title, left_model, fp_left, data, right_model, fp_right, arrows, caption)), run_time=0.8)

    def scene_verification(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)

        title = label("BƯỚC 3 - XÁC MINH QUYỀN SỞ HỮU", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.1)
        x = data_card("Đầu vào x", "trigger bí mật", IF_BLUE, width=2.0).move_to(LEFT * 4 + DOWN * 0.1)
        model = model_box("M_suspect", "mô hình cần kiểm tra").move_to(ORIGIN + DOWN * 0.1)
        out = data_card("Đầu ra", "?", PANEL_STROKE, width=2.0).move_to(RIGHT * 4 + DOWN * 0.1)
        y = data_card("Kỳ vọng y", "đáp án mục tiêu", IF_BLUE, width=2.0).move_to(RIGHT * 4 + DOWN * 1.35)
        arrows = VGroup(
            Arrow(x.get_right(), model.get_left(), buff=0.12, color=IF_BLUE, stroke_width=4),
            Arrow(model.get_right(), out.get_left(), buff=0.12, color=IF_BLUE, stroke_width=4),
        )
        compare = DoubleArrow(out.get_bottom(), y.get_top(), buff=0.08, color=TEXT_MUTED, stroke_width=2)
        match = label("MATCH", 42, IF_BLUE, BOLD_WEIGHT).move_to(DOWN * 2.18)
        proof = label("Nếu output == y: có bằng chứng sở hữu", 24, TEXT_MUTED).next_to(match, DOWN, buff=0.1)

        self.play(FadeIn(title), FadeIn(x), FadeIn(model), FadeIn(out), run_time=0.8)
        self.play(Create(arrows[0]), model[0].animate.set_stroke(IF_BLUE, width=3), run_time=0.8)
        self.play(Create(arrows[1]), out[1].animate.become(label("y", 25, IF_BLUE, BOLD_WEIGHT).move_to(out.get_center())), run_time=0.8)
        self.play(FadeIn(y, shift=UP * 0.25), Create(compare), run_time=0.8)
        self.play(Write(match), FadeIn(proof), Flash(out.get_center(), color=IF_BLUE), Flash(y.get_center(), color=IF_BLUE), run_time=1)
        self.finish_voice(voice_start, duration_hint, min_wait=1.0)
        self.play(FadeOut(VGroup(title, x, model, out, y, arrows, compare, match, proof)), run_time=0.8)

    def scene_sft_vs_adapter(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)
        title = label("HAI CHIẾN LƯỢC TIÊM VÂN TAY", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.1)

        sft_model = layer_model(mode="sft").move_to(LEFT * 2.85 + DOWN * 0.15)
        sft_title = label("SFT", 31, IF_BLUE, BOLD_WEIGHT).next_to(sft_model, UP, buff=0.2)
        sft_notes = VGroup(
            label("Cập nhật toàn bộ tham số", 19, WHITE),
            label("Kiểm tra black-box và white-box", 18, TEXT_MUTED),
            label("Ổn định với nhiều temperature", 18, TEXT_MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(sft_model, DOWN, buff=0.2)

        adapter_model = layer_model(mode="adapter").move_to(RIGHT * 2.85 + DOWN * 0.15)
        adapter_title = label("Adapter", 31, IF_BLUE, BOLD_WEIGHT).next_to(adapter_model, UP, buff=0.2)
        adapter_notes = VGroup(
            label("Đóng băng non-Embedding", 19, WHITE),
            label("Chỉ học F-Adapter nhỏ", 18, TEXT_MUTED),
            label("Cần white-box để xác minh", 18, TEXT_MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(adapter_model, DOWN, buff=0.2)
        divider = Line(UP * 1.6, DOWN * 2.15, color=PANEL_STROKE, stroke_opacity=0.45)

        self.play(FadeIn(title), Create(divider), run_time=0.7)
        self.play(FadeIn(sft_title), FadeIn(sft_model, shift=RIGHT * 0.2), FadeIn(sft_notes), run_time=1)
        self.play(
            sft_model[2].animate.set_color(IF_BLUE),
            sft_model[1].animate.set_stroke(color=IF_BLUE, opacity=0.65),
            Flash(sft_model.get_center(), color=IF_BLUE),
            run_time=1.0,
        )
        self.play(FadeIn(adapter_title), FadeIn(adapter_model, shift=LEFT * 0.2), FadeIn(adapter_notes), run_time=1)
        self.play(adapter_model[3].animate.set_stroke(IF_BLUE_SOFT, width=3.2), Flash(adapter_model[3].get_center(), color=IF_BLUE), run_time=1)
        self.finish_voice(voice_start, duration_hint, min_wait=1.4)
        self.play(FadeOut(VGroup(title, divider, sft_title, sft_model, sft_notes, adapter_title, adapter_model, adapter_notes)), run_time=0.9)

    def scene_metrics(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)

        title = label("HAI TIÊU CHÍ CỐT LÕI", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.1)
        effectiveness = metric_bar("Effectiveness", "FSR 100%", 1.0, IF_BLUE).move_to(UP * 0.7)
        harmlessness = metric_bar("Harmlessness", "No loss", 0.98, IF_BLUE).move_to(DOWN * 0.45)
        vanilla = label("Vanilla", 18, TEXT_MUTED).move_to(RIGHT * 3.8 + DOWN * 0.16)
        if_label = label("IF Adapter", 18, IF_BLUE).move_to(RIGHT * 3.85 + DOWN * 0.68)
        note = label("Vừa bền sau fine-tune, vừa không làm giảm năng lực gốc.", 24, TEXT_MUTED)
        note.to_edge(DOWN, buff=0.72)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.play(FadeIn(effectiveness, shift=UP * 0.2), run_time=0.8)
        self.play(Flash(effectiveness.get_right() + LEFT * 0.55, color=IF_BLUE), run_time=0.6)
        self.play(FadeIn(harmlessness, shift=UP * 0.2), FadeIn(vanilla), FadeIn(if_label), run_time=0.8)
        self.play(Indicate(harmlessness[-1], color=IF_BLUE), Write(note), run_time=1.0)
        self.finish_voice(voice_start, duration_hint, min_wait=1.0)
        self.play(FadeOut(VGroup(title, effectiveness, harmlessness, vanilla, if_label, note)), run_time=0.8)

    def scene_summary(self, voice_path: str | None = None, duration_hint: float | None = None):
        voice_start = self.add_voice(voice_path)
        title = label("TỔNG KẾT", 33, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        steps = VGroup(
            data_card("Cấy", "(x, y)", IF_BLUE, width=1.9),
            data_card("Fine-tune", "dữ liệu riêng", PANEL_STROKE, width=1.9),
            data_card("Xác minh", "x -> y ?", IF_BLUE, width=1.9),
        ).arrange(RIGHT, buff=1.0).move_to(UP * 0.2)
        arrows = VGroup(
            Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.12, color=PANEL_STROKE),
            Arrow(steps[1].get_right(), steps[2].get_left(), buff=0.12, color=PANEL_STROKE),
        )
        fp = fingerprint_icon(0.34).move_to(steps[0].get_center() + DOWN * 1.45)
        final = label("Bằng chứng sở hữu ẩn vẫn sống sót sau fine-tuning.", 30, IF_BLUE, BOLD_WEIGHT)
        final.to_edge(DOWN, buff=0.72)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(steps[0]), FadeIn(fp), run_time=0.7)
        self.play(Create(arrows[0]), fp.animate.move_to(steps[1].get_center() + DOWN * 1.45), FadeIn(steps[1]), run_time=0.9)
        self.play(Create(arrows[1]), fp.animate.move_to(steps[2].get_center() + DOWN * 1.45), FadeIn(steps[2]), run_time=0.9)
        self.play(Write(final), Flash(fp.get_center(), color=IF_BLUE), run_time=1)
        self.finish_voice(voice_start, duration_hint, min_wait=1.6)
        self.play(FadeOut(VGroup(title, steps, arrows, fp, final)), run_time=0.9)


def play_part3_fingerprinting(scene: Scene) -> None:
    scene.voice = FingerprintingScene.voice.__get__(scene, scene.__class__)
    scene.add_voice = FingerprintingScene.add_voice.__get__(scene, scene.__class__)
    scene.finish_voice = FingerprintingScene.finish_voice.__get__(scene, scene.__class__)
    scene.add_background_grid = FingerprintingScene.add_background_grid.__get__(scene, scene.__class__)
    scene.scene_problem = FingerprintingScene.scene_problem.__get__(scene, scene.__class__)
    scene.scene_secret_pair = FingerprintingScene.scene_secret_pair.__get__(scene, scene.__class__)
    scene.scene_injection = FingerprintingScene.scene_injection.__get__(scene, scene.__class__)
    scene.scene_finetune = FingerprintingScene.scene_finetune.__get__(scene, scene.__class__)
    scene.scene_verification = FingerprintingScene.scene_verification.__get__(scene, scene.__class__)
    scene.scene_sft_vs_adapter = FingerprintingScene.scene_sft_vs_adapter.__get__(scene, scene.__class__)
    scene.scene_metrics = FingerprintingScene.scene_metrics.__get__(scene, scene.__class__)
    scene.scene_summary = FingerprintingScene.scene_summary.__get__(scene, scene.__class__)
    FingerprintingScene.construct(scene)
