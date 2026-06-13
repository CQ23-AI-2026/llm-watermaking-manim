"""
Test file cho Cảnh 3.4.4 — Watermark trong Phân phối Xác suất

Chạy: $env:PYTHONPATH="."; python -m manim -qh scenes/part3/drw_344_test.py Scene344Test
"""
import os
import sys
import glob

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for path in glob.glob(os.path.join(root_dir, ".venv", "Lib", "site-packages")):
    if path not in sys.path:
        sys.path.insert(0, path)

from manim import *
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_RED, BOLD_WEIGHT
)


class Scene344Test(Scene):
    """
    Cảnh 3.4.4 — Watermark không nằm trong chữ, mà nằm trong xác suất.

    Flow:
      1. Response bình thường xuất hiện ở giữa màn hình
      2. X-ray scan vàng quét ngang qua
      3. Response CHUYỂN THÀNH biểu đồ xác suất (3 cột bar chart)
      4. Secret Key xuất hiện, đi vào vector
      5. Các cột rung nhẹ, số thay đổi rất nhỏ
      6. Label "Positive" vẫn không đổi → "Same Prediction"
    """

    def construct(self):

        # ── Background grid ─────────────────────────────────────────────────
        self.add(NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.06},
            axis_config={"stroke_opacity": 0},
        ))

        # ── PHASE 1: Response bình thường ───────────────────────────────────
        resp_box = RoundedRectangle(
            corner_radius=0.12, width=7.0, height=1.3,
            fill_color="#1A1A2E", fill_opacity=0.95,
            stroke_color=VG_GRAY, stroke_width=1.8
        ).move_to([0.0, 0.5, 0])

        resp_txt = VGText(
            '"The answer is likely positive."',
            font_size=24, color=WHITE, weight=BOLD_WEIGHT
        ).move_to(resp_box.get_center())

        # Label nhỏ "Model Response"
        resp_label = VGText("Model Response", font_size=15, color=VG_GRAY).next_to(resp_box, UP, buff=0.18)

        self.play(FadeIn(resp_label, shift=DOWN*0.1), run_time=0.5)
        self.play(FadeIn(resp_box, shift=UP*0.1), FadeIn(resp_txt, shift=UP*0.1), run_time=0.9)
        self.wait(1.0)

        # ── PHASE 2: X-ray scan quét ngang ──────────────────────────────────
        scan = Line(
            resp_box.get_left() + UP*0.01,
            resp_box.get_left() + UP*0.01,
            color=VG_GOLD, stroke_width=4
        )
        self.add(scan)
        self.play(
            scan.animate.put_start_and_end_on(
                resp_box.get_left() + UP*0.01,
                resp_box.get_right() + UP*0.01
            ),
            run_time=0.7
        )
        self.remove(scan)

        # Flash ngắn trên resp_box để tạo hiệu ứng "X-ray reveal"
        self.play(resp_box.animate.set_stroke(color=VG_GOLD, width=2.5), run_time=0.25)
        self.play(resp_box.animate.set_stroke(color=VG_GRAY, width=1.8), run_time=0.2)

        # ── PHASE 3: Response CHUYỂN THÀNH biểu đồ xác suất ────────────────
        # Tạo bar chart tại vị trí của resp_box (transform in-place)

        # Thông số bars
        bar_probs  = [0.720, 0.190, 0.090]
        bar_labels = ["Positive", "Neutral", "Negative"]
        bar_colors = [VG_GREEN, "#88AACC", VG_RED]
        bar_scale  = 3.2   # chiều cao max của bar (Positive = 1.0 → 3.2 units)
        bar_width  = 0.9
        bar_gap    = 0.55  # khoảng cách giữa các bars
        bar_center_x = 0.0
        bar_bottom_y = -1.8   # hạ thấp đáy các bars xuống -1.8 để tránh đè chữ

        bar_xs = [-bar_gap - bar_width/2 - 0.3, bar_center_x, bar_gap + bar_width/2 + 0.3]

        def make_bar(x, prob, color):
            h = prob * bar_scale
            bar = Rectangle(
                width=bar_width, height=h,
                fill_color=color, fill_opacity=0.7,
                stroke_color=color, stroke_width=2.0
            ).move_to([x, bar_bottom_y + h/2, 0])
            return bar

        bars_before = VGroup(*[make_bar(bar_xs[i], bar_probs[i], bar_colors[i]) for i in range(3)])

        # Labels dưới mỗi bar
        cat_labels = VGroup(*[
            VGText(bar_labels[i], font_size=17, color=bar_colors[i]).move_to([bar_xs[i], bar_bottom_y - 0.28, 0])
            for i in range(3)
        ])

        # Số xác suất nổi trên đầu mỗi bar (BEFORE)
        prob_nums = VGroup(*[
            VGText(f"{bar_probs[i]:.3f}", font_size=18, color=WHITE, weight=BOLD_WEIGHT)
            .move_to([bar_xs[i], bar_bottom_y + bar_probs[i]*bar_scale + 0.25, 0])
            for i in range(3)
        ])

        # Tiêu đề - dịch xuống Y=1.8 để không bị đè với subtitle của main scene
        prob_title = VGText("Probability Distribution", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to([0.0, 1.8, 0])

        # Animation: response mờ đi → bars grow từ đáy
        self.play(
            resp_txt.animate.set_opacity(0.0),
            resp_box.animate.set_opacity(0.0),
            resp_label.animate.set_opacity(0.0),
            FadeIn(prob_title, shift=DOWN*0.2),
            run_time=0.7
        )
        self.remove(resp_txt, resp_box, resp_label)

        # Bars và labels grow lên
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in bars_before],
            run_time=0.9
        )
        self.play(
            FadeIn(cat_labels, shift=UP*0.1),
            FadeIn(prob_nums, shift=UP*0.1),
            run_time=0.6
        )
        self.wait(0.8)

        # ── PHASE 4: Secret Key xuất hiện → đi vào vector ──────────────────
        key_body = Annulus(
            inner_radius=0.10, outer_radius=0.22,
            color=VG_GOLD, fill_opacity=0.6, stroke_width=2.0
        )
        key_collar = Rectangle(
            width=0.04, height=0.14,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(key_body, RIGHT, buff=-0.06)
        key_stem = Rectangle(
            width=0.75, height=0.08,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(key_body, RIGHT, buff=-0.04)
        key_tooth1 = Rectangle(
            width=0.08, height=0.14,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(key_stem, DOWN, buff=-0.02).align_to(key_stem, RIGHT)
        key_tooth2 = Rectangle(
            width=0.08, height=0.09,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(key_stem, DOWN, buff=-0.02).align_to(key_stem, RIGHT).shift(LEFT * 0.15)

        key_icon = VGroup(key_body, key_collar, key_stem, key_tooth1, key_tooth2).move_to([4.5, 1.5, 0])
        key_lbl  = VGText("Secret Key", font_size=18, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(key_icon, UP, buff=0.15)
        key_g    = VGroup(key_icon, key_lbl)

        self.play(FadeIn(key_g, scale=0.7), run_time=0.8)
        # Key icon quay nhẹ (hiệu ứng "khoá đang hoạt động")
        self.play(key_icon.animate.rotate(PI/5), run_time=0.4)
        self.play(key_icon.animate.rotate(-PI/5), run_time=0.35)

        # Tia sáng từ key bay vào bars (particles)
        sparks = VGroup(*[
            Dot(color=VG_GOLD, radius=0.07, fill_opacity=0.9).move_to(key_icon.get_left())
            for _ in range(3)
        ])
        self.add(sparks)
        targets = [bars_before[i].get_top() for i in range(3)]
        self.play(
            AnimationGroup(*[
                sparks[i].animate(run_time=0.8, rate_func=rush_into).move_to(targets[i])
                for i in range(3)
            ], lag_ratio=0.15)
        )
        self.play(FadeOut(sparks), run_time=0.1)

        # ── PHASE 5: Bars rung nhẹ + số thay đổi rất nhỏ ──────────────────
        bar_probs_after = [0.721, 0.187, 0.092]

        bars_after = VGroup(*[make_bar(bar_xs[i], bar_probs_after[i], bar_colors[i]) for i in range(3)])

        prob_nums_after = VGroup(*[
            VGText(f"{bar_probs_after[i]:.3f}", font_size=18, color=VG_GOLD, weight=BOLD_WEIGHT)
            .move_to([bar_xs[i], bar_bottom_y + bar_probs_after[i]*bar_scale + 0.25, 0])
            for i in range(3)
        ])

        # Bars rung nhẹ (shake) rồi transform
        self.play(
            *[bar.animate.shift(RIGHT*0.06) for bar in bars_before],
            run_time=0.12
        )
        self.play(
            *[bar.animate.shift(LEFT*0.12) for bar in bars_before],
            run_time=0.12
        )
        self.play(
            *[bar.animate.shift(RIGHT*0.06) for bar in bars_before],
            run_time=0.1
        )

        # Transform bars và số
        self.play(
            *[Transform(bars_before[i], bars_after[i]) for i in range(3)],
            *[Transform(prob_nums[i], prob_nums_after[i]) for i in range(3)],
            run_time=0.9
        )

        # Label "Tiny Shift" - đưa lên Y=0.6 và trỏ chéo xuống cột Neutral để không đè lên cột Negative
        tiny_lbl = VGText("Tiny Shift", font_size=18, color=VG_GOLD).move_to([2.8, 0.6, 0])
        tiny_arr = Arrow([2.0, 0.5, 0], [0.3, -0.7, 0], color=VG_GOLD, stroke_width=1.8, buff=0.05)
        self.play(FadeIn(tiny_lbl, shift=UP*0.1), Create(tiny_arr), run_time=0.7)
        self.wait(0.5)

        # ── PHASE 6: Nhãn cuối KHÔNG ĐỔI → "Same Prediction" ───────────────
        # Hộp "Positive" được đưa sang trái ở Y=-0.6 để tránh chồng chéo lên đỉnh cột Positive
        pred_box = RoundedRectangle(
            corner_radius=0.08, width=2.0, height=0.7,
            fill_color="#0D1F12", fill_opacity=0.95,
            stroke_color=VG_GREEN, stroke_width=2.2
        ).move_to([-3.2, -0.6, 0])

        pred_lbl = VGText("Positive", font_size=20, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(pred_box.get_center())

        # Dịch xuống Y=-1.3 đối xứng với Tiny Shift ban đầu
        same_lbl = VGText("Same Prediction", font_size=18, color=VG_GREEN, weight=BOLD_WEIGHT).move_to([-3.2, -1.3, 0])

        self.play(FadeIn(pred_box, scale=0.85), FadeIn(pred_lbl, scale=0.85), run_time=0.7)
        self.play(FadeIn(same_lbl, shift=RIGHT*0.2), run_time=0.6)

        self.wait(3.0)
