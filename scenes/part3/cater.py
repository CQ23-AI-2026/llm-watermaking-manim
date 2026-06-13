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
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_ORANGE, VG_PURPLE, VG_RED,
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


def _first_existing(*paths: str) -> str:
    for path in paths:
        if path and os.path.exists(path):
            return path
    return paths[0] if paths else ""


def _box(text: str, width: float, height: float, color, font_size: int = 16, weight=None) -> VGroup:
    rect = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        fill_color="#18181A",
        fill_opacity=0.92,
        stroke_color=color,
        stroke_width=1.6,
    )
    label = VGText(text, font_size=font_size, color=color, weight=weight or "NORMAL").move_to(rect.get_center())
    return VGroup(rect, label)


class CATERScene(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)

        grid = NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.06},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        voice_dir = os.path.join(current_dir, "assets", "cater")
        extraction_dir = os.path.join(current_dir, "assets", "extraction")
        voices = [
            _first_existing(
                os.path.join(voice_dir, f"cater_3_{i}.mp3"),
                os.path.join(voice_dir, f"cater_{i}.mp3"),
            )
            for i in range(8)
        ]
        legacy_voice = os.path.join(extraction_dir, "extraction_cater.mp3")

        title = VGText("CATER", font_size=LARGE_FONT_SIZE + 8, color=WHITE, weight=BOLD_WEIGHT).move_to(ORIGIN)
        underline = Line(LEFT * 1.45, RIGHT * 1.45, color=VG_GOLD, stroke_width=2, stroke_opacity=0.65).next_to(title, DOWN, buff=0.25)

        if os.path.exists(voices[0]):
            self.add_sound(voices[0])
        elif os.path.exists(legacy_voice):
            self.add_sound(legacy_voice)
        dur_0 = _get_audio_duration(voices[0]) or (3.5 if os.path.exists(legacy_voice) else 2.5)
        self.play(Write(title), Create(underline), run_time=1.2)
        self.wait(max(0.4, dur_0 - 1.2))

        top_title = VGText(
            "CATER - CONDITIONAL WATERMARKING",
            font_size=25,
            color=WHITE,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.28)
        top_ul = Line(LEFT * 4.1, RIGHT * 4.1, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(top_title, DOWN, buff=0.15)
        self.play(Transform(title, top_title), Transform(underline, top_ul), run_time=0.75)

        # =========================================================================
        # CẢNH 3.7.1 - CATER khác DRW và GINSEW
        # =========================================================================
        if os.path.exists(voices[1]):
            self.add_sound(voices[1])
        dur = _get_audio_duration(voices[1]) or 22.0

        sub = VGText("Không dùng sóng xác suất, mà dùng lexical watermark có điều kiện", font_size=21, color=VG_PURPLE, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        left = RoundedRectangle(corner_radius=0.08, width=4.3, height=2.55, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_BLUE, stroke_width=1.7).move_to([-3.0, -0.15, 0])
        right = RoundedRectangle(corner_radius=0.08, width=4.3, height=2.55, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_PURPLE, stroke_width=1.7).move_to([3.0, -0.15, 0])
        l1 = VGText("DRW / GINSEW", font_size=19, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(left.get_top(), DOWN, buff=0.25)
        l2 = VGText("tiêm tín hiệu hình sin\nvào xác suất hoặc nhóm xác suất", font_size=16, color=WHITE).move_to(left.get_center() + DOWN * 0.25)
        r1 = VGText("CATER", font_size=19, color=VG_PURPLE, weight=BOLD_WEIGHT).next_to(right.get_top(), DOWN, buff=0.25)
        r2 = VGText("chọn từ đồng nghĩa\nkhi điều kiện ngôn ngữ khớp", font_size=16, color=WHITE).move_to(right.get_center() + DOWN * 0.25)
        r3 = VGText("conditional lexical rules", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(right.get_center() + DOWN * 0.95)
        note = VGText("CATER bảo vệ text generation API trước imitation/model extraction bằng watermark trên bề mặt từ vựng.", font_size=15, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(left, l1, l2), shift=RIGHT * 0.1), FadeIn(VGroup(right, r1, r2, r3), shift=LEFT * 0.1), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        scene = VGroup(sub, left, right, l1, l2, r1, r2, r3, note)
        self.wait(max(1.0, dur - 1.9))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.2 - Từ điển watermark bí mật
        # =========================================================================
        if os.path.exists(voices[2]):
            self.add_sound(voices[2])
        dur = _get_audio_duration(voices[2]) or 24.0

        sub = VGText("Step 1: tạo từ điển watermark bí mật", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        dict_b = RoundedRectangle(corner_radius=0.08, width=4.45, height=3.1, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GOLD, stroke_width=1.8).move_to([-3.0, -0.25, 0])
        dict_t = VGText("secret watermark dictionary", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(dict_b.get_top(), DOWN, buff=0.2)
        pairs = VGroup(
            VGText("big -> large", font_size=16, color=WHITE),
            VGText("smart -> clever", font_size=16, color=WHITE),
            VGText("start -> begin", font_size=16, color=WHITE),
            VGText("study -> research", font_size=16, color=WHITE),
        ).arrange(DOWN, buff=0.22).move_to(dict_b.get_center() + DOWN * 0.25)
        api = _box("Victim API\nwith CATER", 2.55, 1.05, VG_PURPLE, 16, BOLD_WEIGHT).move_to([2.9, 0.7, 0])
        out = _box("watermarked\ntext output", 2.55, 1.0, VG_GREEN, 16, BOLD_WEIGHT).move_to([2.9, -1.25, 0])
        a1 = Arrow(dict_b.get_right(), api.get_left(), buff=0.1, color=VG_GOLD, stroke_width=1.8)
        a2 = Arrow(api.get_bottom(), out.get_top(), buff=0.1, color=VG_GREEN, stroke_width=1.8)
        note = VGText("Các cặp từ là bí mật; attacker chỉ thấy văn bản đầu ra, không biết rule nào đã được dùng.", font_size=16, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(dict_b, dict_t, pairs)), run_time=0.8)
        self.play(Create(a1), FadeIn(api), run_time=0.6)
        self.play(Create(a2), FadeIn(out), FadeIn(note, shift=UP * 0.1), run_time=0.8)
        scene = VGroup(sub, dict_b, dict_t, pairs, api, out, a1, a2, note)
        self.wait(max(1.0, dur - 2.7))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.3 - Conditional synonym substitution
        # =========================================================================
        if os.path.exists(voices[3]):
            self.add_sound(voices[3])
        dur = _get_audio_duration(voices[3]) or 30.0

        sub = VGText("Step 2: thay từ đồng nghĩa khi điều kiện ngôn ngữ khớp", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        sent = _box("The team will study the result.", 4.25, 0.72, WHITE, 16, BOLD_WEIGHT).move_to([-3.35, 1.05, 0])
        feature = _box("linguistic feature\nPOS / dependency", 2.85, 1.0, VG_BLUE, 15, BOLD_WEIGHT).move_to([-3.35, -0.35, 0])
        rule = _box("condition matched\nstudy -> research", 2.9, 1.0, VG_PURPLE, 15, BOLD_WEIGHT).move_to([0.65, 0.2, 0])
        out = _box("The team will research the result.", 4.55, 0.72, VG_GREEN, 16, BOLD_WEIGHT).move_to([3.1, 1.45, 0])
        a1 = Arrow(sent.get_bottom(), feature.get_top(), buff=0.08, color=VG_BLUE, stroke_width=1.7)
        a2 = Arrow(feature.get_right(), rule.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=1.7)
        a3 = Arrow(rule.get_top(), out.get_bottom(), buff=0.08, color=VG_GREEN, stroke_width=1.7)
        no = _box("condition not matched\nkeep natural word", 2.9, 0.85, VG_GRAY, 14, BOLD_WEIGHT).move_to([0.65, -1.65, 0])
        a4 = Arrow(feature.get_right() + DOWN * 0.28, no.get_left(), buff=0.08, color=VG_GRAY, stroke_width=1.4)
        note = VGText("Điểm chính: CATER không thay ngẫu nhiên; rule được kích hoạt theo ngữ cảnh để giữ câu tự nhiên.", font_size=15, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(sent), run_time=0.5)
        self.play(Create(a1), FadeIn(feature), run_time=0.6)
        self.play(Create(a2), FadeIn(rule), Create(a3), FadeIn(out), run_time=0.9)
        self.play(Create(a4), FadeIn(no), FadeIn(note, shift=UP * 0.1), run_time=0.7)
        scene = VGroup(sub, sent, feature, rule, out, no, a1, a2, a3, a4, note)
        self.wait(max(1.0, dur - 3.2))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.4 - Optimization trade-off
        # =========================================================================
        if os.path.exists(voices[4]):
            self.add_sound(voices[4])
        dur = _get_audio_duration(voices[4]) or 38.0

        sub = VGText("Step 3: tối ưu rule để giữ nghĩa nhưng tăng tín hiệu watermark", font_size=21, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        formula_b = RoundedRectangle(corner_radius=0.08, width=10.4, height=2.25, fill_color="#18181A", fill_opacity=0.94, stroke_color=VG_PURPLE, stroke_width=1.8).move_to([0, 1.05, 0])
        f = MathTex(
            r"\min_{\mathbf{W}}\;(\mathbf{W}c-\mathbf{X}c)^T(\mathbf{W}c-\mathbf{X}c)"
            r"-\frac{\alpha}{|\mathcal{C}|}\mathrm{Tr}((\mathbf{W}-\mathbf{X})^T(\mathbf{W}-\mathbf{X}))",
            font_size=20,
            color=WHITE,
        ).move_to(formula_b.get_center() + UP * 0.38)
        c = MathTex(
            r"\mathrm{s.t.}\quad \mathbf{X}^T\cdot\mathbf{1}_{|\mathcal{W}^{(i)}|}=\mathbf{1}_{|\mathcal{C}|},"
            r"\quad \mathbf{X}\in\{0,1\}^{|\mathcal{W}^{(i)}|\times|\mathcal{C}|}",
            font_size=20,
            color=VG_GOLD,
        ).move_to(formula_b.get_center() + DOWN * 0.52)
        sem = _box("semantic\npreservation", 2.55, 1.05, VG_BLUE, 15, BOLD_WEIGHT).move_to([-3.45, -1.25, 0])
        alpha = _box("alpha\ntrade-off", 2.1, 1.05, VG_ORANGE, 15, BOLD_WEIGHT).move_to([0, -1.25, 0])
        wm = _box("watermark\nhit ratio", 2.55, 1.05, VG_GREEN, 15, BOLD_WEIGHT).move_to([3.45, -1.25, 0])
        ar1 = Arrow(sem.get_right(), alpha.get_left(), buff=0.08, color=VG_ORANGE, stroke_width=1.7)
        ar2 = Arrow(alpha.get_right(), wm.get_left(), buff=0.08, color=VG_GREEN, stroke_width=1.7)
        note = VGText("Trong video, công thức được rút gọn: CATER giải bài toán chọn ma trận thay thế X dưới các ràng buộc one-hot.", font_size=15, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(formula_b, f, c), shift=DOWN * 0.08), run_time=1.0)
        self.play(FadeIn(sem), FadeIn(alpha), FadeIn(wm), Create(ar1), Create(ar2), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        scene = VGroup(sub, formula_b, f, c, sem, alpha, wm, ar1, ar2, note)
        self.wait(max(1.0, dur - 2.9))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.5 - Detection bằng hit ratio
        # =========================================================================
        if os.path.exists(voices[5]):
            self.add_sound(voices[5])
        dur = _get_audio_duration(voices[5]) or 30.0

        sub = VGText("Detection: probing và đếm tỉ lệ rule watermark xuất hiện", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        q = _box("probing\nqueries", 1.9, 0.72, VG_BLUE, 14, BOLD_WEIGHT).move_to([-4.75, 0.9, 0])
        suspect = _box("Suspect\nModel", 2.1, 0.82, VG_RED, 14, BOLD_WEIGHT).move_to([-2.15, 0.9, 0])
        text = _box("generated\ntext", 2.05, 0.82, VG_PURPLE, 14, BOLD_WEIGHT).move_to([0.35, 0.9, 0])
        count = _box("count watermark\nword choices", 2.45, 0.82, VG_GREEN, 14, BOLD_WEIGHT).move_to([3.2, 0.9, 0])
        arrows = VGroup(
            Arrow(q.get_right(), suspect.get_left(), buff=0.08, color=VG_BLUE, stroke_width=1.6),
            Arrow(suspect.get_right(), text.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=1.6),
            Arrow(text.get_right(), count.get_left(), buff=0.08, color=VG_GREEN, stroke_width=1.6),
        )
        chart_b = RoundedRectangle(corner_radius=0.08, width=7.2, height=2.5, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GRAY, stroke_width=1.6).move_to([0, -1.25, 0])
        axis = Line(chart_b.get_left() + RIGHT * 0.6 + DOWN * 0.75, chart_b.get_right() + LEFT * 0.6 + DOWN * 0.75, color=VG_GRAY, stroke_width=1.2)
        normal = Rectangle(width=1.35, height=0.55, fill_color=VG_BLUE, fill_opacity=0.7, stroke_color=VG_BLUE).move_to([-2.0, -1.35, 0])
        suspect_bar = Rectangle(width=1.35, height=1.35, fill_color=VG_GREEN, fill_opacity=0.7, stroke_color=VG_GREEN).move_to([1.1, -0.95, 0])
        thresh = DashedLine([-3.15, -0.75, 0], [3.15, -0.75, 0], color=VG_RED, stroke_width=1.8, dash_length=0.12)
        n_l = VGText("clean", font_size=14, color=VG_BLUE).next_to(normal, DOWN, buff=0.16)
        s_l = VGText("suspect", font_size=14, color=VG_GREEN).next_to(suspect_bar, DOWN, buff=0.16)
        t_l = VGText("threshold", font_size=14, color=VG_RED).next_to(thresh, RIGHT, buff=0.12)
        verdict = VGText("hit ratio vượt ngưỡng -> nghi ngờ model học từ API có CATER", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(q, suspect, text, count)), Create(arrows), run_time=1.0)
        self.play(FadeIn(chart_b), Create(axis), FadeIn(VGroup(normal, suspect_bar, n_l, s_l)), run_time=0.8)
        self.play(Create(thresh), FadeIn(t_l), FadeIn(verdict, shift=UP * 0.1), run_time=0.8)
        scene = VGroup(sub, q, suspect, text, count, arrows, chart_b, axis, normal, suspect_bar, thresh, n_l, s_l, t_l, verdict)
        self.wait(max(1.0, dur - 3.1))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.6 - Chất lượng tốt, phát hiện yếu hơn GINSEW
        # =========================================================================
        if os.path.exists(voices[6]):
            self.add_sound(voices[6])
        dur = _get_audio_duration(voices[6]) or 28.0

        sub = VGText("Đánh giá: chất lượng tốt, nhưng detection yếu hơn GINSEW", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        qbox = RoundedRectangle(corner_radius=0.08, width=4.3, height=2.55, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GREEN, stroke_width=1.8).move_to([-3.0, -0.1, 0])
        dbox = RoundedRectangle(corner_radius=0.08, width=4.3, height=2.55, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_ORANGE, stroke_width=1.8).move_to([3.0, -0.1, 0])
        qt = VGText("Quality", font_size=19, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(qbox.get_top(), DOWN, buff=0.25)
        dt = VGText("Detection", font_size=19, color=VG_ORANGE, weight=BOLD_WEIGHT).next_to(dbox.get_top(), DOWN, buff=0.25)
        qdesc = VGText("BLEU / ROUGE-L\nthường gần model gốc\nvì thay từ có điều kiện", font_size=16, color=WHITE).move_to(qbox.get_center() + DOWN * 0.25)
        ddesc = VGText("hit-ratio signal\nthường yếu hơn GINSEW\nđặc biệt khi bị synonym randomization", font_size=16, color=WHITE).move_to(dbox.get_center() + DOWN * 0.25)
        note = VGText("CATER là baseline lexical watermark tốt, nhưng GINSEW thường mạnh hơn ở bài toán phát hiện model extraction.", font_size=15, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(qbox, qt, qdesc), shift=RIGHT * 0.1), FadeIn(VGroup(dbox, dt, ddesc), shift=LEFT * 0.1), run_time=1.0)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        scene = VGroup(sub, qbox, dbox, qt, dt, qdesc, ddesc, note)
        self.wait(max(1.0, dur - 2.0))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.7.7 - Tổng kết CATER
        # =========================================================================
        if os.path.exists(voices[7]):
            self.add_sound(voices[7])
        dur = _get_audio_duration(voices[7]) or 24.0

        sub = VGText("Tổng kết cơ chế CATER", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        items = [
            (r"\text{secret dict}", "word pairs", VG_GOLD),
            (r"\text{features}", "POS / dependency", VG_BLUE),
            (r"\mathbf{X}", "replacement rules", VG_PURPLE),
            (r"\text{generate}", "lexical output", VG_GREEN),
            (r"\text{hit ratio}", "verify", VG_ORANGE),
        ]
        boxes = VGroup()
        arrows = VGroup()
        x0 = -4.4
        for i, (sym, desc, col) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.9, fill_color="#18181A", fill_opacity=0.92, stroke_color=col, stroke_width=1.6).move_to([x0 + 2.2 * i, 0.9, 0])
            s = MathTex(sym, font_size=17, color=col).move_to(box.get_center() + UP * 0.15)
            d = VGText(desc, font_size=11, color=WHITE).move_to(box.get_center() + DOWN * 0.2)
            boxes.add(VGroup(box, s, d))
            if i > 0:
                arrows.add(Arrow(boxes[i - 1][0].get_right(), box.get_left(), buff=0.05, color=VG_GRAY, stroke_width=1.5))

        summary_b = RoundedRectangle(corner_radius=0.08, width=9.7, height=2.65, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_PURPLE, stroke_width=1.8).move_to([0, -1.45, 0])
        t1 = VGText("CATER phù hợp khi API chỉ trả text, không trả logits hoặc probability vector.", font_size=14, color=WHITE).move_to(summary_b.get_center() + UP * 0.78)
        t2 = VGText("Watermark nằm trong lựa chọn từ đồng nghĩa có điều kiện theo ngữ cảnh.", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + UP * 0.28)
        t3 = VGText("Tối ưu rule giúp giữ chất lượng văn bản gần model gốc.", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + DOWN * 0.22)
        t4 = VGText("Giới hạn: tín hiệu surface-level, dễ yếu hơn watermark xác suất như GINSEW.", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + DOWN * 0.72)

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(boxes[0], shift=DOWN * 0.1), run_time=0.35)
        for i in range(1, len(boxes)):
            self.play(Create(arrows[i - 1]), FadeIn(boxes[i], shift=DOWN * 0.1), run_time=0.32)
        self.play(FadeIn(VGroup(summary_b, t1, t2, t3, t4), shift=UP * 0.1), run_time=0.9)
        scene = VGroup(sub, boxes, arrows, summary_b, t1, t2, t3, t4)
        self.wait(max(1.0, dur - (0.5 + 0.35 + 0.32 * (len(boxes) - 1) + 0.9)))
        self.play(FadeOut(scene), FadeOut(title), FadeOut(underline), run_time=1.0)
        self.wait(0.5)


def play_part3_cater(scene: Scene) -> None:
    CATERScene.construct(scene)
