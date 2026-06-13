import glob
import os
import sys

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
    VG_GOLD,
    VG_GRAY,
    VG_GREEN,
    VG_ORANGE,
    VG_PURPLE,
    VG_RED,
)


PANEL_FILL = "#18181A"
PANEL_STROKE = VG_GRAY
TEXT_MUTED = VG_GRAY
TEXT_COLOR = VG_BLUE
MODEL_COLOR = VG_GOLD
ACCENT = VG_GOLD


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


def panel(width, height, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.92):
    return RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=1.8,
        fill_color=fill,
        fill_opacity=opacity,
    )


def data_card(title, subtitle="", stroke=PANEL_STROKE, width=2.3, height=0.85):
    box = panel(width, height, stroke=stroke)
    t = label(title, 20, stroke, BOLD_WEIGHT)
    if subtitle:
        s = label(subtitle, 14, TEXT_MUTED)
        stack = VGroup(t, s).arrange(DOWN, buff=0.05)
    else:
        stack = VGroup(t)
    fit_text(stack, box, x_pad=0.2, y_pad=0.12)
    return VGroup(box, stack)


def compare_row(left_text, right_text, y, left_color=TEXT_COLOR, right_color=MODEL_COLOR):
    left = data_card(left_text, "", left_color, width=4.05, height=0.55).move_to(LEFT * 2.35 + UP * y)
    right = data_card(right_text, "", right_color, width=4.05, height=0.55).move_to(RIGHT * 2.35 + UP * y)
    return VGroup(left, right)


def model_icon(color=VG_GOLD):
    body = RoundedRectangle(
        corner_radius=0.08,
        width=1.35,
        height=0.9,
        stroke_color=color,
        stroke_width=2,
        fill_color="#111113",
        fill_opacity=0.92,
    )
    nodes = VGroup(
        Dot(LEFT * 0.38 + UP * 0.18, radius=0.045, color=color),
        Dot(LEFT * 0.38 + DOWN * 0.18, radius=0.045, color=color),
        Dot(RIGHT * 0.02, radius=0.045, color=color),
        Dot(RIGHT * 0.38 + UP * 0.18, radius=0.045, color=color),
        Dot(RIGHT * 0.38 + DOWN * 0.18, radius=0.045, color=color),
    )
    edges = VGroup(
        Line(nodes[0], nodes[2], color=color, stroke_width=1, stroke_opacity=0.55),
        Line(nodes[1], nodes[2], color=color, stroke_width=1, stroke_opacity=0.55),
        Line(nodes[2], nodes[3], color=color, stroke_width=1, stroke_opacity=0.55),
        Line(nodes[2], nodes[4], color=color, stroke_width=1, stroke_opacity=0.55),
    )
    return VGroup(body, edges, nodes)


class ModelWatermarkingConclusionScene(Scene):
    """Part 3 conclusion: text watermarking vs model watermarking."""

    def construct(self):
        self.add_background_grid()
        current_dir = os.path.dirname(__file__)
        self.voice_dir = os.path.join(current_dir, "assets", "model_watermarking_conclusion")

        title = label("TỔNG KẾT PART 3", LARGE_FONT_SIZE - 7, WHITE, BOLD_WEIGHT).move_to(ORIGIN)
        underline = Line(LEFT * 3.7, RIGHT * 3.7, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        underline.next_to(title, DOWN, buff=0.25)

        voice_start = self.add_voice(*self.voice("scene_3_14_0.mp3"))
        self.play(Write(title), Create(underline), run_time=1.2)
        self.finish_voice(*voice_start, min_wait=0.9)

        top_title = label("TỔNG KẾT PART 3", LARGE_FONT_SIZE - 12, WHITE, BOLD_WEIGHT)
        top_title.to_edge(UP, buff=0.28)
        subtitle = label("Text Watermarking vs Model Watermarking", 25, TEXT_COLOR)
        subtitle.next_to(top_title, DOWN, buff=0.08)
        top_underline = Line(LEFT * 4.4, RIGHT * 4.4, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        top_underline.next_to(subtitle, DOWN, buff=0.15)

        self.play(Transform(title, top_title), Transform(underline, top_underline), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)

        self.scene_compare(*self.voice("scene_3_14_1.mp3"))
        self.scene_methods(*self.voice("scene_3_14_2.mp3"))
        self.scene_threats(*self.voice("scene_3_14_3.mp3"))
        self.scene_tradeoffs(*self.voice("scene_3_14_4.mp3"))
        self.scene_final(*self.voice("scene_3_14_5.mp3"))

        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(underline), run_time=0.8)
        self.wait(0.3)

    def add_background_grid(self):
        grid = NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.055},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

    def voice(self, filename: str):
        path = os.path.join(self.voice_dir, filename)
        if os.path.exists(path):
            return path, _audio_duration(path)
        return None, None

    def add_voice(self, path: str | None, duration: float | None):
        if path and os.path.exists(path):
            self.add_sound(path)
        return self.time, duration

    def finish_voice(self, voice_start: float, duration_hint: float | None, min_wait: float = 0.8):
        if duration_hint:
            self.wait(max(min_wait, voice_start + duration_hint - self.time))
        else:
            self.wait(min_wait)

    def scene_compare(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("SO SÁNH HAI TẦNG BẢO VỆ", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        left_header = data_card("Text Watermarking", "truy vết output", TEXT_COLOR, width=4.05, height=0.82).move_to(LEFT * 2.35 + UP * 1.18)
        right_header = data_card("Model Watermarking", "xác minh ownership", MODEL_COLOR, width=4.05, height=0.82).move_to(RIGHT * 2.35 + UP * 1.18)
        rows = VGroup(
            compare_row("Bảo vệ văn bản sinh ra", "Bảo vệ mô hình", 0.35),
            compare_row("Dấu nằm trong output text", "Dấu nằm trong hành vi / trọng số", -0.28),
            compare_row("Kiểm tra nội dung", "Kiểm tra mô hình nghi ngờ", -0.91),
            compare_row("Phù hợp truy vết content", "Phù hợp xác minh ownership", -1.54),
        )
        group = VGroup(title, left_header, right_header, rows)

        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(left_header, shift=RIGHT * 0.12), FadeIn(right_header, shift=LEFT * 0.12), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in rows], lag_ratio=0.14), run_time=1.35)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_methods(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("BA HƯỚNG MODEL WATERMARKING", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        center = data_card("Model Watermarking", "bảo vệ quyền sở hữu", MODEL_COLOR, width=3.0, height=1.0).move_to(UP * 0.8)
        methods = VGroup(
            data_card("Watermark / Backdoor", "cấy tín hiệu hành vi", VG_ORANGE, width=3.05, height=0.9).move_to(LEFT * 4.0 + DOWN * 0.75),
            data_card("Instructional Fingerprinting", "cặp input-output bí mật", VG_BLUE, width=3.35, height=0.9).move_to(DOWN * 0.75),
            data_card("DeepJudge", "similarity framework", VG_PURPLE, width=3.05, height=0.9).move_to(RIGHT * 4.0 + DOWN * 0.75),
        )
        arrows = VGroup(*[Arrow(center.get_bottom(), m.get_top(), color=m[0].stroke_color, buff=0.12, stroke_width=2) for m in methods])
        caption = label("Một mục tiêu, nhiều dạng bằng chứng sở hữu", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, center, methods, arrows, caption)

        self.play(FadeIn(title), FadeIn(center, shift=DOWN * 0.12), run_time=0.85)
        self.play(Create(arrows), LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in methods], lag_ratio=0.18), run_time=1.25)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_threats(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("PHÒNG THỦ TRƯỚC BIẾN ĐỔI MÔ HÌNH", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        source = VGroup(model_icon(VG_BLUE), label("Owner Model", 20, VG_BLUE, BOLD_WEIGHT)).arrange(DOWN, buff=0.15).move_to(LEFT * 4.7 + DOWN * 0.05)
        suspect = VGroup(model_icon(VG_ORANGE), label("Suspect Model", 20, VG_ORANGE, BOLD_WEIGHT)).arrange(DOWN, buff=0.15).move_to(RIGHT * 0.1 + DOWN * 0.05)
        checks = VGroup(
            data_card("Watermark", "trigger / behavior", VG_ORANGE, width=2.35, height=0.78),
            data_card("Fingerprint", "secret pair", VG_BLUE, width=2.35, height=0.78),
            data_card("DeepJudge", "similarity framework", VG_PURPLE, width=2.35, height=0.78),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 4.45 + DOWN * 0.05)
        threats = VGroup(
            data_card("Fine-tuning", "", VG_GOLD, width=1.85, height=0.55),
            data_card("Distillation", "", VG_GOLD, width=1.85, height=0.55),
            data_card("Pruning-FT", "", VG_GOLD, width=1.85, height=0.55),
        ).arrange(DOWN, buff=0.16).move_to(LEFT * 2.25 + DOWN * 0.05)
        arrows = VGroup(
            Arrow(source.get_right(), threats.get_left(), color=PANEL_STROKE, buff=0.12),
            Arrow(threats.get_right(), suspect.get_left(), color=PANEL_STROKE, buff=0.12),
            *[Arrow(suspect.get_right(), c.get_left(), color=c[0].stroke_color, buff=0.12, stroke_width=1.7) for c in checks],
        )
        caption = label("Dấu sở hữu phải còn sau khi mô hình bị chỉnh sửa", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, source, suspect, checks, threats, arrows, caption)

        self.play(FadeIn(title), FadeIn(source, shift=RIGHT * 0.16), run_time=0.8)
        self.play(FadeIn(threats, shift=RIGHT * 0.12), Create(arrows[:2]), FadeIn(suspect, shift=LEFT * 0.16), run_time=1.25)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12) for c in checks], lag_ratio=0.16), Create(arrows[2:]), run_time=1.2)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_tradeoffs(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("TRADE-OFF KHI ĐÁNH GIÁ", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        cards = VGroup(
            data_card("Robustness", "dấu còn sau tấn công", VG_GREEN, width=3.1, height=1.0),
            data_card("Harmlessness", "không giảm hiệu năng", VG_BLUE, width=3.1, height=1.0),
            data_card("Access Level", "black-box / white-box", VG_GOLD, width=3.1, height=1.0),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 0.55)
        access_notes = VGroup(
            data_card("Output checks", "black-box hơn", VG_BLUE, width=2.75, height=0.75),
            data_card("Layer / neuron checks", "white-box hơn", VG_PURPLE, width=2.75, height=0.75),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.2)
        arrows = VGroup(
            Arrow(cards[2].get_bottom(), access_notes[0].get_top(), color=VG_BLUE, buff=0.12),
            Arrow(cards[2].get_bottom(), access_notes[1].get_top(), color=VG_PURPLE, buff=0.12),
        )
        caption = label("Không có kỹ thuật nào tối ưu cho mọi kịch bản", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, cards, access_notes, arrows, caption)

        self.play(FadeIn(title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.18), run_time=1.1)
        self.play(FadeIn(access_notes, shift=UP * 0.12), Create(arrows), run_time=0.95)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_final(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("KẾT LUẬN PART 3", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        text_side = data_card("Text Watermarking", "truy vết nội dung", TEXT_COLOR, width=3.25, height=1.05).move_to(LEFT * 3.35 + UP * 0.45)
        model_side = data_card("Model Watermarking", "xác minh quyền sở hữu", MODEL_COLOR, width=3.25, height=1.05).move_to(RIGHT * 3.35 + UP * 0.45)
        bridge = data_card("Bảo vệ AI", "cần nhìn cả output lẫn model", VG_GREEN, width=3.45, height=1.1).move_to(DOWN * 0.85)
        arrows = VGroup(
            Arrow(text_side.get_bottom(), bridge.get_top() + LEFT * 0.6, color=TEXT_COLOR, buff=0.12, stroke_width=2),
            Arrow(model_side.get_bottom(), bridge.get_top() + RIGHT * 0.6, color=MODEL_COLOR, buff=0.12, stroke_width=2),
        )
        evidence = VGroup(
            data_card("watermark", "", VG_ORANGE, width=1.55, height=0.52),
            data_card("fingerprint", "", VG_BLUE, width=1.65, height=0.52),
            data_card("DeepJudge", "", VG_PURPLE, width=1.65, height=0.52),
            data_card("decision", "", VG_GREEN, width=1.55, height=0.52),
        ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.55)
        group = VGroup(title, text_side, model_side, bridge, arrows, evidence)

        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(text_side, shift=RIGHT * 0.15), FadeIn(model_side, shift=LEFT * 0.15), run_time=0.9)
        self.play(Create(arrows), FadeIn(bridge, shift=UP * 0.14), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.08) for e in evidence], lag_ratio=0.14), run_time=1.0)
        self.finish_voice(*voice_start, min_wait=1.2)
        self.play(FadeOut(group), run_time=0.8)


def play_part3_model_watermarking_conclusion(scene: Scene):
    conclusion_scene = ModelWatermarkingConclusionScene()
    conclusion_scene.renderer = scene.renderer
    conclusion_scene.construct()
