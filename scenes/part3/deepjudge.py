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
ACCENT = VG_GOLD
COPY_COLOR = VG_GREEN
TEST_COLOR = VG_BLUE


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


def panel(width, height, stroke=PANEL_STROKE, fill=PANEL_FILL, opacity=0.9):
    return RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=1.8,
        fill_color=fill,
        fill_opacity=opacity,
    )


def data_card(title, subtitle="", stroke=PANEL_STROKE, width=2.2, height=0.78):
    box = panel(width, height, stroke=stroke)
    t = label(title, 20, stroke, BOLD_WEIGHT)
    if subtitle:
        s = label(subtitle, 14, TEXT_MUTED)
        stack = VGroup(t, s).arrange(DOWN, buff=0.04)
    else:
        stack = VGroup(t)
    fit_text(stack, box, x_pad=0.18, y_pad=0.1)
    return VGroup(box, stack)


def formula_panel(*formulas, width=6.0, height=1.45, font_size=34):
    box = panel(width, height, stroke=VG_GOLD, fill="#111113", opacity=0.94)
    lines = VGroup(
        *[
            MathTex(formula, font_size=font_size, color=WHITE)
            for formula in formulas
        ]
    ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    fit_text(lines, box, x_pad=0.42, y_pad=0.24)
    return VGroup(box, lines)


def model_box(title, subtitle, stroke=VG_BLUE, width=2.7, height=1.12):
    box = panel(width, height, stroke=stroke)
    t = label(title, 25, stroke, BOLD_WEIGHT)
    s = label(subtitle, 15, TEXT_MUTED)
    stack = VGroup(t, s).arrange(DOWN, buff=0.06)
    fit_text(stack, box)
    return VGroup(box, stack)


def simple_network(color=VG_BLUE, muted=False):
    nodes = VGroup()
    edges = VGroup()
    node_color = TEXT_MUTED if muted else color
    edge_color = TEXT_MUTED if muted else color
    for col, x in enumerate([-0.55, 0, 0.55]):
        count = 3 if col != 1 else 4
        ys = np.linspace(0.48, -0.48, count)
        for y in ys:
            nodes.add(Dot([x, y, 0], radius=0.055, color=node_color))
    layers = [nodes[:3], nodes[3:7], nodes[7:10]]
    for a_layer, b_layer in [(layers[0], layers[1]), (layers[1], layers[2])]:
        for a in a_layer:
            for b in b_layer:
                edges.add(Line(a.get_center(), b.get_center(), color=edge_color, stroke_opacity=0.28, stroke_width=1))
    return VGroup(edges, nodes)


def neuron_grid(pattern, color=VG_GOLD):
    dots = VGroup()
    for r in range(3):
        for c in range(4):
            idx = r * 4 + c
            active = pattern[idx]
            dots.add(
                Dot(
                    radius=0.075,
                    color=color if active else TEXT_MUTED,
                    fill_opacity=1.0 if active else 0.35,
                ).move_to(RIGHT * (c - 1.5) * 0.32 + DOWN * (r - 1) * 0.32)
            )
    return dots


class DeepJudgeScene(Scene):
    """DeepJudge: non-watermark, similarity-based ownership testing."""

    def construct(self):
        self.add_background_grid()
        current_dir = os.path.dirname(__file__)
        self.voice_dir = os.path.join(current_dir, "assets", "deepjudge")

        title = label("PHÒNG THỦ KHÔNG DÙNG THỦY VÂN", LARGE_FONT_SIZE - 8, WHITE, BOLD_WEIGHT).move_to(ORIGIN)
        underline = Line(LEFT * 4.65, RIGHT * 4.65, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        underline.next_to(title, DOWN, buff=0.25)

        voice_start = self.add_voice(*self.voice("deepjudge_opening.mp3"))
        self.play(Write(title), Create(underline), run_time=1.2)
        self.finish_voice(*voice_start, min_wait=0.9)

        top_title = label("PHÒNG THỦ KHÔNG DÙNG THỦY VÂN", LARGE_FONT_SIZE - 12, WHITE, BOLD_WEIGHT)
        top_title.to_edge(UP, buff=0.28)
        subtitle = label("DeepJudge - Similarity-based Testing", 25, TEST_COLOR)
        subtitle.next_to(top_title, DOWN, buff=0.08)
        top_underline = Line(LEFT * 4.25, RIGHT * 4.25, color=ACCENT, stroke_width=2, stroke_opacity=0.65)
        top_underline.next_to(subtitle, DOWN, buff=0.15)

        self.play(Transform(title, top_title), Transform(underline, top_underline), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)

        self.scene_difference(*self.voice("deepjudge_3_13_1_difference.mp3"))
        self.scene_threats(*self.voice("deepjudge_3_13_2_threats.mp3"))
        self.scene_robd(*self.voice("deepjudge_3_13_3_robd.mp3"))
        self.scene_lod(*self.voice("deepjudge_3_13_4_lod.mp3"))
        self.scene_lad(*self.voice("deepjudge_3_13_5_lad.mp3"))
        self.scene_scores(*self.voice("deepjudge_3_13_6_scores.mp3"))
        self.scene_threshold(*self.voice("deepjudge_3_13_7_threshold.mp3"))
        self.scene_voting(*self.voice("deepjudge_3_13_8_voting.mp3"))
        self.scene_summary(*self.voice("deepjudge_3_13_9_summary.mp3"))

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

    def scene_difference(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("DEEPJUDGE KHÁC GÌ WATERMARK?", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        left = data_card("Watermark", "cấy tín hiệu trước", VG_GOLD, width=3.0, height=1.0).move_to(LEFT * 3.3 + UP * 0.15)
        right = data_card("DeepJudge", "kiểm thử sau", TEST_COLOR, width=3.0, height=1.0).move_to(RIGHT * 3.3 + UP * 0.15)
        wm_model = model_box("M_owner", "hidden signal", VG_GOLD, width=2.3, height=0.92).next_to(left, DOWN, buff=0.45)
        test = data_card("Test Suite", "Victim vs Suspect", TEST_COLOR, width=2.3, height=0.92).next_to(right, DOWN, buff=0.45)
        inject_arrow = Arrow(left.get_bottom(), wm_model.get_top(), color=VG_GOLD, buff=0.08, stroke_width=2.2)
        test_arrow = Arrow(right.get_bottom(), test.get_top(), color=TEST_COLOR, buff=0.08, stroke_width=2.2)
        caption = label("Không cấy trước  ->  kiểm tra tương đồng sau", 25, TEXT_MUTED).to_edge(DOWN, buff=0.7)
        group = VGroup(title, left, right, wm_model, test, inject_arrow, test_arrow, caption)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.play(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), run_time=0.9)
        self.play(Create(inject_arrow), FadeIn(wm_model), run_time=0.8)
        self.play(Create(test_arrow), FadeIn(test), run_time=0.8)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_threats(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("BA KỊCH BẢN KIỂM TRA", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        victim = model_box("Victim M1", "mô hình nạn nhân", VG_BLUE, width=2.6).move_to(LEFT * 4.2 + DOWN * 0.05)
        threats = VGroup(
            data_card("Distillation", "học lại hành vi", VG_GOLD, width=2.55),
            data_card("Fine-tuning", "tinh chỉnh thêm", VG_ORANGE, width=2.55),
            data_card("Pruning-Finetuning", "cắt tỉa rồi học lại", VG_PURPLE, width=2.55),
        ).arrange(DOWN, buff=0.28).move_to(ORIGIN + DOWN * 0.05)
        suite = data_card("DeepJudge\nTest Suite", "similarity checks", TEST_COLOR, width=2.6, height=1.12).move_to(RIGHT * 4.2 + DOWN * 0.05)
        arrows = VGroup()
        for threat in threats:
            arrows.add(Arrow(victim.get_right(), threat.get_left(), color=PANEL_STROKE, buff=0.12, stroke_width=1.8))
            arrows.add(Arrow(threat.get_right(), suite.get_left(), color=TEST_COLOR, buff=0.12, stroke_width=1.8))
        caption = label("Nếu M2 bắt nguồn từ M1, sự giống nhau có thể vẫn còn.", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, victim, threats, suite, arrows, caption)

        self.play(FadeIn(title), FadeIn(victim, shift=RIGHT * 0.2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in threats], lag_ratio=0.18), run_time=1.1)
        self.play(Create(arrows), FadeIn(suite, shift=LEFT * 0.2), run_time=1.1)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_robd(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("METRIC 1 - ROBUSTNESS DISTANCE", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        adv = data_card("adv(x_i)", "test case", VG_RED, width=1.9, height=0.78).move_to(LEFT * 4.25 + UP * 0.78)
        m1 = model_box("Victim M1", "Rob(f1)", VG_BLUE, width=1.95, height=0.78).move_to(LEFT * 1.15 + UP * 0.78)
        m2 = model_box("Suspect M2", "Rob(f2)", VG_ORANGE, width=1.95, height=0.78).move_to(RIGHT * 2.05 + UP * 0.78)
        formula = formula_panel(
            r"\mathrm{Rob}(f)=\sum_{i=1}^{N}\delta\left(f(\mathrm{adv}(x_i))=y_i\right)",
            r"\mathrm{RobD}(f_1,f_2)=\left|\mathrm{Rob}(f_1)-\mathrm{Rob}(f_2)\right|",
            width=7.25,
            height=1.7,
            font_size=32,
        ).move_to(DOWN * 1.22)
        groundtruth = label("groundtruth label", 15, TEST_COLOR).move_to(RIGHT * 2.88 + DOWN * 0.1)
        gt_arrow = Arrow(
            groundtruth.get_bottom(),
            formula[1][0][0][-3].get_center(),
            color=TEST_COLOR,
            buff=0.05,
            stroke_width=1.7,
            max_tip_length_to_length_ratio=0.12,
        )
        arrows = VGroup(
            Arrow(adv.get_right(), m1.get_left(), color=PANEL_STROKE, buff=0.12),
            Arrow(m1.get_right(), m2.get_left(), color=PANEL_STROKE, buff=0.12),
            Arrow(m1.get_bottom(), formula.get_top() + LEFT * 1.1, color=VG_BLUE, buff=0.12, stroke_width=2.2),
            Arrow(m2.get_bottom(), formula.get_top() + RIGHT * 1.05, color=VG_ORANGE, buff=0.12, stroke_width=2.2),
        )
        same_case = label("cùng test case", 16, TEXT_MUTED).move_to(LEFT * 2.7 + UP * 1.28)
        note = label("RobD nhỏ  ->  hai mô hình bền vững giống nhau trước input đối kháng", 22, TEXT_MUTED)
        note.to_edge(DOWN, buff=0.62)
        group = VGroup(title, adv, m1, m2, arrows, same_case, formula, groundtruth, gt_arrow, note)

        self.play(FadeIn(title), FadeIn(adv, shift=RIGHT * 0.25), run_time=0.8)
        self.play(FadeIn(m1), FadeIn(m2), Create(arrows[:2]), FadeIn(same_case), run_time=1.0)
        self.play(Create(arrows[2:]), FadeIn(formula, shift=LEFT * 0.15), run_time=1.0)
        self.play(FadeIn(groundtruth), Create(gt_arrow), Write(note), run_time=0.9)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_lod(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("METRIC 2 - LAYER OUTPUT DISTANCE", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        left_net = simple_network(VG_BLUE).scale(0.88).move_to(LEFT * 2.2 + UP * 0.66)
        right_net = simple_network(VG_ORANGE).scale(0.88).move_to(RIGHT * 2.2 + UP * 0.66)
        left_label = label("Victim M1", 19, VG_BLUE, BOLD_WEIGHT).next_to(left_net, UP, buff=0.24)
        right_label = label("Suspect M2", 19, VG_ORANGE, BOLD_WEIGHT).next_to(right_net, UP, buff=0.24)
        layer_left = SurroundingRectangle(left_net[1][3:7], color=VG_GOLD, buff=0.12, stroke_width=2.2)
        layer_right = SurroundingRectangle(right_net[1][3:7], color=VG_GOLD, buff=0.12, stroke_width=2.2)
        formula = formula_panel(
            r"\mathrm{LOD}_k(f_1,f_2)=\sum_{i=1}^{N}\left\|f_1^k(x_i)-f_2^k(x_i)\right\|_p",
            width=7.8,
            height=1.25,
            font_size=34,
        ).move_to(DOWN * 1.18)
        term1 = label("layer k of model 1", 14, VG_BLUE).move_to(LEFT * 1.0 + DOWN * 2.12)
        term2 = label("layer k of model 2", 14, VG_ORANGE).move_to(RIGHT * 1.55 + DOWN * 2.12)
        pointer1 = Arrow(term1.get_top(), formula[1].get_bottom() + LEFT * 1.0, color=VG_BLUE, buff=0.02, stroke_width=1.4)
        pointer2 = Arrow(term2.get_top(), formula[1].get_bottom() + RIGHT * 1.45, color=VG_ORANGE, buff=0.02, stroke_width=1.4)
        note = label("LOD so sánh giá trị output tại cùng layer k", 22, TEXT_MUTED).to_edge(DOWN, buff=0.62)
        group = VGroup(
            title,
            left_net,
            right_net,
            left_label,
            right_label,
            layer_left,
            layer_right,
            formula,
            term1,
            term2,
            pointer1,
            pointer2,
            note,
        )

        self.play(FadeIn(title), FadeIn(left_net), FadeIn(right_net), FadeIn(left_label), FadeIn(right_label), run_time=1.0)
        self.play(Create(layer_left), Create(layer_right), run_time=0.8)
        self.play(FadeIn(formula, shift=LEFT * 0.15), run_time=0.8)
        self.play(FadeIn(term1), FadeIn(term2), Create(pointer1), Create(pointer2), Write(note), run_time=0.9)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_lad(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("METRIC 3 - LAYER ACTIVATION DISTANCE", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        pattern1 = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0]
        pattern2 = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0]
        grid1 = neuron_grid(pattern1, VG_BLUE).scale(0.96).move_to(LEFT * 1.85 + UP * 0.52)
        grid2 = neuron_grid(pattern2, VG_ORANGE).scale(0.96).move_to(RIGHT * 1.85 + UP * 0.52)
        l1 = label("M1", 20, VG_BLUE, BOLD_WEIGHT).next_to(grid1, UP, buff=0.34)
        l2 = label("M2", 20, VG_ORANGE, BOLD_WEIGHT).next_to(grid2, UP, buff=0.34)
        threshold = data_card("S(z)", "threshold function", VG_GOLD, width=2.15, height=0.68).move_to(UP * 1.45)
        formula = formula_panel(
            r"\mathrm{LAD}_k(f_1,f_2)=\sum_{i=1}^{N}\left|S\left(f_1^k(x_i)\right)-S\left(f_2^k(x_i)\right)\right|",
            width=8.2,
            height=1.35,
            font_size=31,
        ).move_to(DOWN * 1.25)
        note = label("LAD so sánh pattern neuron bật/tắt sau hàm ngưỡng S", 22, TEXT_MUTED).to_edge(DOWN, buff=0.62)
        group = VGroup(title, grid1, grid2, l1, l2, threshold, formula, note)

        self.play(FadeIn(title), FadeIn(threshold, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(grid1), FadeIn(grid2), FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.play(Indicate(grid1, color=VG_GOLD), Indicate(grid2, color=VG_GOLD), run_time=1.0)
        self.play(FadeIn(formula, shift=LEFT * 0.15), Write(note), run_time=0.9)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_scores(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("TEST CASES -> METRICS -> DELTA SCORE", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        tests = data_card("Test Cases", "x_1 ... x_N", VG_RED, width=2.2, height=1.0).move_to(LEFT * 4.55 + DOWN * 0.45)
        rows = VGroup(
            data_card("Metric 1: RobD", "δscore_1", VG_BLUE, width=2.65, height=0.68),
            data_card("Metric 2: LOD", "δscore_2", VG_ORANGE, width=2.65, height=0.68),
            data_card("Metric 3: LAD", "δscore_3", VG_PURPLE, width=2.65, height=0.68),
            data_card("Metric N", "δscore_N", VG_GRAY, width=2.65, height=0.68),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 1.65 + DOWN * 0.45)
        stack = data_card("Score Stack", "kết hợp nhiều tín hiệu", VG_GOLD, width=2.75, height=1.05).move_to(RIGHT * 3.25 + DOWN * 0.45)
        test_arrows = VGroup(*[Arrow(tests.get_right(), r.get_left(), color=PANEL_STROKE, buff=0.12, stroke_width=1.35) for r in rows])
        score_arrows = VGroup(*[Arrow(r.get_right(), stack.get_left(), color=VG_GOLD, buff=0.14, stroke_width=1.6) for r in rows])
        arrows = VGroup(test_arrows, score_arrows)
        caption = label("Không dựa vào một phép đo duy nhất", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, tests, rows, stack, arrows, caption)

        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(tests, shift=RIGHT * 0.15), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.16), run_time=1.2)
        self.play(Create(test_arrows), run_time=0.7)
        self.play(Create(score_arrows), FadeIn(stack, shift=LEFT * 0.2), run_time=1.0)
        self.play(Write(caption), run_time=0.7)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_threshold(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("NGƯỠNG τ TỪ NEGATIVE MODELS", 31, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        axis = NumberLine(x_range=[0, 10, 1], length=7.5, color=PANEL_STROKE).move_to(DOWN * 0.15)
        small = label("gần M1", 18, VG_GREEN).next_to(axis.get_left(), DOWN, buff=0.25)
        large = label("xa M1", 18, TEXT_MUTED).next_to(axis.get_right(), DOWN, buff=0.25)
        tau_x = axis.n2p(4.0)
        tau_line = Line(tau_x + UP * 0.9, tau_x + DOWN * 0.65, color=VG_GOLD, stroke_width=3)
        tau_label = label("τ", 34, VG_GOLD, BOLD_WEIGHT).next_to(tau_line, UP, buff=0.1)
        negatives = VGroup(*[Dot(axis.n2p(x), color=VG_GRAY, radius=0.07) for x in [4.4, 5.2, 6.1, 7.3, 8.2]])
        suspect = Dot(axis.n2p(2.7), color=VG_RED, radius=0.09)
        suspect_label = label("δscore(M2)", 19, VG_RED, BOLD_WEIGHT).next_to(suspect, UP, buff=0.2)
        rule = label("δscore < τ  ->  vote: copy", 28, VG_GOLD, BOLD_WEIGHT).to_edge(DOWN, buff=0.72)
        group = VGroup(title, axis, small, large, tau_line, tau_label, negatives, suspect, suspect_label, rule)

        self.play(FadeIn(title), Create(axis), FadeIn(small), FadeIn(large), run_time=0.9)
        self.play(FadeIn(negatives, shift=UP * 0.15), run_time=0.8)
        self.play(Create(tau_line), FadeIn(tau_label), run_time=0.7)
        self.play(FadeIn(suspect, scale=0.7), FadeIn(suspect_label), run_time=0.7)
        self.play(Write(rule), run_time=0.8)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_voting(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("MAJORITY VOTING", 34, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        votes = VGroup(
            data_card("RobD", "copy", VG_GREEN, width=1.8),
            data_card("LOD", "copy", VG_GREEN, width=1.8),
            data_card("LAD", "not copy", VG_RED, width=1.8),
            data_card("Test N", "copy", VG_GREEN, width=1.8),
        ).arrange(DOWN, buff=0.22).move_to(LEFT * 3.4 + DOWN * 0.1)
        box = data_card("Majority\nVoting", "đa số metric", VG_GOLD, width=2.55, height=1.22).move_to(ORIGIN + DOWN * 0.1)
        result = data_card("Kết luận", "M2 là copy của M1", VG_GREEN, width=3.0, height=1.0).move_to(RIGHT * 3.6 + DOWN * 0.1)
        arrows = VGroup(*[Arrow(v.get_right(), box.get_left(), color=PANEL_STROKE, buff=0.1, stroke_width=1.5) for v in votes])
        final_arrow = Arrow(box.get_right(), result.get_left(), color=VG_GREEN, buff=0.14, stroke_width=2.4)
        caption = label("Đa số metric đồng ý -> quyết định cuối cùng", 24, TEXT_MUTED).to_edge(DOWN, buff=0.72)
        group = VGroup(title, votes, box, result, arrows, final_arrow, caption)

        self.play(FadeIn(title), LaggedStart(*[FadeIn(v) for v in votes], lag_ratio=0.15), run_time=1.2)
        self.play(Create(arrows), FadeIn(box, shift=LEFT * 0.2), run_time=1.0)
        self.play(Create(final_arrow), FadeIn(result, shift=LEFT * 0.2), run_time=0.9)
        self.play(Write(caption), Flash(result.get_center(), color=VG_GREEN), run_time=0.9)
        self.finish_voice(*voice_start, min_wait=1.0)
        self.play(FadeOut(group), run_time=0.8)

    def scene_summary(self, voice_path=None, duration_hint=None):
        voice_start = self.add_voice(voice_path, duration_hint)
        title = label("TỔNG KẾT DEEPJUDGE", 33, WHITE, BOLD_WEIGHT).move_to(UP * 2.05)
        pipeline = VGroup(
            data_card("M1 + M2", "Victim / Suspect", TEST_COLOR, width=2.0),
            data_card("RobD / LOD / LAD", "nhiều metric", VG_GOLD, width=2.35),
            data_card("δscore < τ ?", "so với ngưỡng", VG_ORANGE, width=2.15),
            data_card("Voting", "copy / not copy", VG_GREEN, width=2.0),
        ).arrange(RIGHT, buff=0.42).move_to(UP * 0.45)
        arrows = VGroup(*[Arrow(pipeline[i].get_right(), pipeline[i + 1].get_left(), color=PANEL_STROKE, buff=0.08) for i in range(3)])
        notes = VGroup(
            label("Không cần watermark", 22, WHITE),
            label("So sánh hành vi và biểu diễn", 22, WHITE),
            label("Áp dụng cho distillation, fine-tuning, pruning-finetuning", 22, WHITE),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.45)
        final = label("M2 quá giống M1  ->  có khả năng là bản sao", 27, VG_GOLD, BOLD_WEIGHT).to_edge(DOWN, buff=0.55)
        group = VGroup(title, pipeline, arrows, notes, final)

        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(pipeline[0]), run_time=0.5)
        for i in range(3):
            self.play(Create(arrows[i]), FadeIn(pipeline[i + 1]), run_time=0.65)
        self.play(FadeIn(notes, shift=UP * 0.2), run_time=1.0)
        self.play(Write(final), run_time=0.8)
        self.finish_voice(*voice_start, min_wait=1.5)
        self.play(FadeOut(group), run_time=0.9)


def play_part3_deepjudge(scene: Scene) -> None:
    DeepJudgeScene.construct(scene)
