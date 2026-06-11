import os
import sys
import glob
import math

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
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_RED,
    LARGE_FONT_SIZE, BOLD_WEIGHT
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
    return None


class DRW35Scene(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)

        grid = NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.06},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        scene_title = VGText(
            "DRW - DISTILLATION-RESISTANT WATERMARKING",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.28)
        underline = Line(LEFT * 4.35, RIGHT * 4.35, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(scene_title, DOWN, buff=0.15)
        self.add(scene_title, underline)
        top_ul = underline

        ext = os.path.join(current_dir, "assets", "extraction")
        voice_351 = os.path.join(ext, "extraction_3_5_1.mp3")
        voice_352 = os.path.join(ext, "extraction_3_5_2.mp3")
        voice_353 = os.path.join(ext, "extraction_3_5_3.mp3")
        voice_354 = os.path.join(ext, "extraction_3_5_4.mp3")
        voice_355 = os.path.join(ext, "extraction_3_5_5.mp3")
        voice_356 = os.path.join(ext, "extraction_3_5_6.mp3")

        dur_351 = _get_audio_duration(voice_351) or 44.0
        dur_352 = _get_audio_duration(voice_352) or 48.0
        dur_353 = _get_audio_duration(voice_353) or 54.0
        dur_354 = _get_audio_duration(voice_354) or 50.0
        dur_355 = _get_audio_duration(voice_355) or 62.0
        dur_356 = _get_audio_duration(voice_356) or 50.0

        # =========================================================================
        # CẢNH 3.5.1 - DRW bảo vệ encoder model bằng probability signal watermark
        # =========================================================================
        if os.path.exists(voice_351):
            self.add_sound(voice_351)

        sub = VGText("DRW: thủy vân tín hiệu xác suất", font_size=22, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        sent_b = RoundedRectangle(corner_radius=0.08, width=3.45, height=0.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.4).move_to([-4.0, 0.65, 0])
        sent_l = VGText("Santa Barbara has nice weather.", font_size=15, color=WHITE).move_to(sent_b.get_center())
        model_b = RoundedRectangle(corner_radius=0.1, width=3.05, height=1.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([-0.55, 0.65, 0])
        model_l = VGText("BERT / Encoder\nVictim Model", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(model_b.get_center())
        arr_in = Arrow(sent_b.get_right(), model_b.get_left(), buff=0.1, color=VG_GRAY, stroke_width=1.8)

        prob_b = RoundedRectangle(corner_radius=0.08, width=4.4, height=3.05, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.0).move_to([2.25, -0.75, 0])
        prob_t = VGText("phân phối xác suất đầu ra", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(prob_b.get_top(), DOWN, buff=0.2)
        classes = [("positive", 0.90, VG_GREEN), ("neutral", 0.07, VG_BLUE), ("negative", 0.03, VG_RED)]
        rows = VGroup()
        for i, (lab, val, col) in enumerate(classes):
            y = prob_b.get_top()[1] - 0.78 - i * 0.55
            rows.add(VGText(lab, font_size=15, color=col).move_to([prob_b.get_center()[0] - 1.35, y, 0]))
            bar = Rectangle(width=val * 2.0, height=0.18, fill_color=col, fill_opacity=0.72, stroke_color=col, stroke_width=1.1).move_to([prob_b.get_center()[0] - 0.35 + val, y, 0])
            rows.add(bar)
            rows.add(VGText(f"P={val:.2f}", font_size=14, color=WHITE).move_to([prob_b.get_center()[0] + 1.55, y, 0]))
        arr_out = Arrow(model_b.get_right(), prob_b.get_left() + UP * 0.65, buff=0.1, color=VG_BLUE, stroke_width=1.8)
        target = VGText("lớp mục tiêu c* = positive", font_size=17, color=VG_GREEN, weight=BOLD_WEIGHT).move_to([0.0, -2.5, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(sent_b, sent_l)), run_time=0.6)
        self.play(Create(arr_in), FadeIn(VGroup(model_b, model_l)), run_time=0.7)
        self.play(Create(arr_out), FadeIn(VGroup(prob_b, prob_t, rows), shift=LEFT * 0.15), run_time=0.9)
        self.play(FadeIn(target, shift=UP * 0.1), run_time=0.6)

        scene_351 = VGroup(sub, sent_b, sent_l, model_b, model_l, arr_in, prob_b, prob_t, rows, arr_out, target)
        anim_t = 0.5 + 0.6 + 0.7 + 0.9 + 0.6
        self.wait(max(1.0, dur_351 - anim_t))
        self.play(FadeOut(scene_351), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.2 - Secret key của DRW
        # =========================================================================
        if os.path.exists(voice_352):
            self.add_sound(voice_352)

        sub = VGText("Secret key K quản lý toàn bộ watermark", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        key_formula = VGText("K = (c*, f_w, v_k, v_s, M)", font_size=28, color=VG_GOLD, weight=BOLD_WEIGHT).move_to([0.0, 1.15, 0])

        components = [
            ("c*", "lớp mục tiêu", VG_GREEN),
            ("f_w", "tần số góc", VG_GOLD),
            ("v_k", "vector pha", VG_PURPLE),
            ("v_s", "vector chọn lọc", VG_BLUE),
            ("M", "ma trận token ngẫu nhiên", VG_RED),
        ]
        comp_g = VGroup()
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        for x, (sym, desc, col) in zip(xs, components):
            box = RoundedRectangle(corner_radius=0.08, width=1.85, height=1.55, fill_color="#18181A", fill_opacity=0.9, stroke_color=col, stroke_width=1.8).move_to([x, -0.65, 0])
            s = VGText(sym, font_size=24, color=col, weight=BOLD_WEIGHT).move_to(box.get_center() + UP * 0.25)
            d = VGText(desc, font_size=13, color=WHITE).move_to(box.get_center() + DOWN * 0.25)
            comp_g.add(VGroup(box, s, d))
        note = VGText("Không phải watermark bằng từ đồng nghĩa: DRW điều khiển xác suất đầu ra.", font_size=17, color=VG_GRAY).move_to([0.0, -2.45, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(Write(key_formula), run_time=0.9)
        self.play(FadeIn(comp_g, shift=UP * 0.15), run_time=1.1)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)

        scene_352 = VGroup(sub, key_formula, comp_g, note)
        anim_t = 0.5 + 0.9 + 1.1 + 0.6
        self.wait(max(1.0, dur_352 - anim_t))
        self.play(FadeOut(scene_352), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.3 - Tín hiệu tuần hoàn z_c(x)
        # =========================================================================
        if os.path.exists(voice_353):
            self.add_sound(voice_353)

        sub = VGText("Hash g(x) tạo tín hiệu tuần hoàn cho từng lớp", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        hash_b = RoundedRectangle(corner_radius=0.08, width=2.55, height=1.0, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.8).move_to([-4.6, 0.75, 0])
        hash_l = VGText("g(x)\nwith key K", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(hash_b.get_center())
        u_b = RoundedRectangle(corner_radius=0.08, width=2.25, height=0.82, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.5).move_to([-1.85, 0.75, 0])
        u_l = VGText("u = g(x)", font_size=17, color=WHITE).move_to(u_b.get_center())
        arr_hu = Arrow(hash_b.get_right(), u_b.get_left(), buff=0.08, color=VG_GRAY, stroke_width=1.7)

        form_b = RoundedRectangle(corner_radius=0.08, width=4.8, height=1.9, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=1.8).move_to([2.2, 0.65, 0])
        f1 = VGText("c = c*:     z_c(x) = cos(f_w g(x))", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(form_b.get_center() + UP * 0.35)
        f2 = VGText("c != c*:   z_c(x) = cos(f_w g(x) + pi)", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(form_b.get_center() + DOWN * 0.35)
        arr_uf = Arrow(u_b.get_right(), form_b.get_left(), buff=0.08, color=VG_GOLD, stroke_width=1.7)

        axes = Axes(x_range=[0, 1, 0.25], y_range=[-1, 1, 1], x_length=6.0, y_length=2.1, axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}).move_to([0.0, -1.65, 0])
        target_wave = VMobject(color=VG_GREEN, stroke_width=2.4)
        other_wave = VMobject(color=VG_RED, stroke_width=2.4)
        target_pts = []
        other_pts = []
        for j in range(120):
            u = j / 119
            target_pts.append(axes.c2p(u, math.cos(2 * math.pi * 2.0 * u)))
            other_pts.append(axes.c2p(u, math.cos(2 * math.pi * 2.0 * u + math.pi)))
        target_wave.set_points_smoothly(target_pts)
        other_wave.set_points_smoothly(other_pts)
        wave_lbl = VGText("hai lớp lệch pha pi", font_size=16, color=VG_GOLD).next_to(axes, UP, buff=0.1)

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(hash_b, hash_l)), run_time=0.55)
        self.play(Create(arr_hu), FadeIn(VGroup(u_b, u_l)), run_time=0.55)
        self.play(Create(arr_uf), FadeIn(VGroup(form_b, f1, f2)), run_time=0.8)
        self.play(Create(axes), FadeIn(wave_lbl), run_time=0.45)
        self.play(Create(target_wave), Create(other_wave), run_time=1.0)

        scene_353 = VGroup(sub, hash_b, hash_l, u_b, u_l, arr_hu, form_b, f1, f2, arr_uf, axes, wave_lbl, target_wave, other_wave)
        anim_t = 0.5 + 0.55 + 0.55 + 0.8 + 0.45 + 1.0
        self.wait(max(1.0, dur_353 - anim_t))
        self.play(FadeOut(scene_353), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.4 - Tiêm watermark vào xác suất dự đoán
        # =========================================================================
        if os.path.exists(voice_354):
            self.add_sound(voice_354)

        sub = VGText("Tiêm tín hiệu vào xác suất và chuẩn hóa lại", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        formula_b = RoundedRectangle(corner_radius=0.08, width=7.1, height=1.25, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=1.8).move_to([0.0, 1.0, 0])
        formula = VGText("ŷ_c = Normalize( p_c + epsilon (1 + z_c(x)) )", font_size=20, color=VG_PURPLE, weight=BOLD_WEIGHT).move_to(formula_b.get_center())

        before_b = RoundedRectangle(corner_radius=0.08, width=3.0, height=2.25, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.8).move_to([-3.5, -0.9, 0])
        before_t = VGText("trước watermark", font_size=17, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(before_b.get_top(), DOWN, buff=0.2)
        before_p = VGText("positive\nP = 0.90", font_size=22, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(before_b.get_center() + DOWN * 0.1)
        after_b = RoundedRectangle(corner_radius=0.08, width=3.0, height=2.25, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=1.8).move_to([3.5, -0.9, 0])
        after_t = VGText("sau watermark", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(after_b.get_top(), DOWN, buff=0.2)
        after_p = VGText("positive\nP = 0.85", font_size=22, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(after_b.get_center() + DOWN * 0.1)
        eps_b = RoundedRectangle(corner_radius=0.08, width=2.15, height=1.0, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=1.6).move_to([0.0, -0.9, 0])
        eps_l = VGText("nhiễu nhỏ\nepsilon", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(eps_b.get_center())
        arr_l = Arrow(before_b.get_right(), eps_b.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=1.8)
        arr_r = Arrow(eps_b.get_right(), after_b.get_left(), buff=0.08, color=VG_GOLD, stroke_width=1.8)
        note = VGText("xác suất thay đổi nhẹ, nhãn dự đoán vẫn ổn định", font_size=18, color=VG_GRAY).move_to([0.0, -2.65, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(formula_b, formula), shift=DOWN * 0.1), run_time=0.8)
        self.play(FadeIn(VGroup(before_b, before_t, before_p), shift=RIGHT * 0.15), run_time=0.65)
        self.play(Create(arr_l), FadeIn(VGroup(eps_b, eps_l), scale=0.9), run_time=0.65)
        self.play(Create(arr_r), FadeIn(VGroup(after_b, after_t, after_p), shift=LEFT * 0.15), run_time=0.65)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.55)

        scene_354 = VGroup(sub, formula_b, formula, before_b, before_t, before_p, after_b, after_t, after_p, eps_b, eps_l, arr_l, arr_r, note)
        anim_t = 0.5 + 0.8 + 0.65 * 3 + 0.55
        self.wait(max(1.0, dur_354 - anim_t))
        self.play(FadeOut(scene_354), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.5 - Detection by probing
        # =========================================================================
        if os.path.exists(voice_355):
            self.add_sound(voice_355)

        sub = VGText("Detection by probing: tìm peak tại tần số f_w", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        flow_y = 0.95
        probe_b = RoundedRectangle(corner_radius=0.08, width=2.2, height=0.72, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.7).move_to([-4.5, flow_y, 0])
        probe_l = VGText("queries", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(probe_b.get_center())
        suspect_b = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.72, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=1.7).move_to([-1.5, flow_y, 0])
        suspect_l = VGText("Suspect Model", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(suspect_b.get_center())
        signal_b = RoundedRectangle(corner_radius=0.08, width=2.55, height=0.72, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.5).move_to([1.55, flow_y, 0])
        signal_l = VGText("extracted signal", font_size=15, color=VG_GRAY).move_to(signal_b.get_center())
        a1 = Arrow(probe_b.get_right(), suspect_b.get_left(), buff=0.08, color=VG_BLUE, stroke_width=1.7)
        a2 = Arrow(suspect_b.get_right(), signal_b.get_left(), buff=0.08, color=VG_GRAY, stroke_width=1.7)

        axes = Axes(x_range=[0, 10, 2], y_range=[0, 4, 1], x_length=5.8, y_length=2.45, axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}).move_to([0.0, -1.35, 0])
        period_t = VGText("periodogram của tín hiệu trích xuất", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(axes, UP, buff=0.08)
        curve_noise = VMobject(color=VG_GRAY, stroke_width=1.8)
        curve_peak = VMobject(color=VG_GOLD, stroke_width=2.6)
        npts = []
        ppts = []
        for j in range(120):
            x = 10 * j / 119
            y_noise = 0.45 + 0.18 * math.sin(2.4 * x) + 0.12 * math.sin(5.9 * x)
            y_peak = y_noise + 2.8 * math.exp(-((x - 5.0) / 0.45) ** 2)
            npts.append(axes.c2p(x, max(0.04, y_noise)))
            ppts.append(axes.c2p(x, y_peak))
        curve_noise.set_points_smoothly(npts)
        curve_peak.set_points_smoothly(ppts)
        fw_lbl = VGText("peak tại f_w", font_size=15, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(axes.c2p(5.05, 3.7))
        fw_arrow = Arrow(axes.c2p(5.75, 3.45), axes.c2p(5.05, 3.0), buff=0.04, color=VG_GOLD, stroke_width=1.6)
        verdict = VGText("peak tăng vọt -> có dấu hiệu model extraction", font_size=18, color=VG_GREEN, weight=BOLD_WEIGHT).move_to([0.0, -2.92, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(probe_b, probe_l)), run_time=0.45)
        self.play(Create(a1), FadeIn(VGroup(suspect_b, suspect_l)), run_time=0.55)
        self.play(Create(a2), FadeIn(VGroup(signal_b, signal_l)), run_time=0.55)
        self.play(Create(axes), FadeIn(period_t), run_time=0.55)
        self.play(Create(curve_noise), run_time=0.7)
        self.play(Transform(curve_noise, curve_peak), FadeIn(fw_lbl), Create(fw_arrow), run_time=1.0)
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.6)

        scene_355 = VGroup(sub, probe_b, probe_l, suspect_b, suspect_l, signal_b, signal_l, a1, a2, axes, period_t, curve_noise, fw_lbl, fw_arrow, verdict)
        anim_t = 0.5 + 0.45 + 0.55 * 2 + 0.55 + 0.7 + 1.0 + 0.6
        self.wait(max(1.0, dur_355 - anim_t))
        self.play(FadeOut(scene_355), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.6 - Tổng kết DRW
        # =========================================================================
        if os.path.exists(voice_356):
            self.add_sound(voice_356)

        sub = VGText("Tổng kết cơ chế DRW", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        items = [
            ("K", "secret key", VG_GOLD),
            ("g(x)", "hash", VG_BLUE),
            ("z_c(x)", "cosine signal", VG_PURPLE),
            ("ŷ_c", "watermarked prob.", VG_GREEN),
            ("distill", "student copy", VG_RED),
            ("f_w peak", "probing detect", VG_GOLD),
        ]
        boxes = VGroup()
        arrows = VGroup()
        x0 = -5.1
        for i, (sym, desc, col) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.06, width=1.6, height=0.88, fill_color="#18181A", fill_opacity=0.9, stroke_color=col, stroke_width=1.6).move_to([x0 + 2.05 * i, 0.9, 0])
            s = VGText(sym, font_size=18, color=col, weight=BOLD_WEIGHT).move_to(box.get_center() + UP * 0.15)
            d = VGText(desc, font_size=11, color=WHITE).move_to(box.get_center() + DOWN * 0.2)
            boxes.add(VGroup(box, s, d))
            if i > 0:
                arrows.add(Arrow(boxes[i - 1][0].get_right(), box.get_left(), buff=0.05, color=VG_GRAY, stroke_width=1.5))

        trade_b = RoundedRectangle(corner_radius=0.08, width=6.3, height=2.45, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.8).move_to([0.0, -1.35, 0])
        t1 = VGText("DRW phù hợp nhất với encoder/classification models như BERT.", font_size=17, color=WHITE).move_to(trade_b.get_center() + UP * 0.55)
        t2 = VGText("Watermark nằm trong xác suất, không nằm trong từ đồng nghĩa.", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(trade_b.get_center())
        t3 = VGText("Phát hiện bằng probing: tìm peak tại tần số bí mật f_w.", font_size=17, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(trade_b.get_center() + DOWN * 0.55)

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(boxes[0], shift=DOWN * 0.1), run_time=0.35)
        for i in range(1, len(boxes)):
            self.play(Create(arrows[i - 1]), FadeIn(boxes[i], shift=DOWN * 0.1), run_time=0.32)
        self.play(FadeIn(VGroup(trade_b, t1, t2, t3), shift=UP * 0.1), run_time=0.9)

        all_356 = VGroup(sub, boxes, arrows, trade_b, t1, t2, t3)
        anim_t = 0.5 + 0.35 + 0.32 * (len(boxes) - 1) + 0.9
        self.wait(max(1.0, dur_356 - anim_t))

        self.play(
            FadeOut(all_356),
            FadeOut(scene_title), FadeOut(underline),
            run_time=1.0,
        )
        self.wait(0.5)


def play_part3_drw_35(scene: Scene) -> None:
    DRW35Scene.construct(scene)
