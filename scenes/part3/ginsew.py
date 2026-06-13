import glob
import math
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


class GINSEWScene(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)

        grid = NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.06},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        voice_dir = os.path.join(current_dir, "assets", "ginsew")
        extraction_dir = os.path.join(current_dir, "assets", "extraction")
        voices = [
            _first_existing(
                os.path.join(voice_dir, f"ginsew_3_{i}.mp3"),
                os.path.join(voice_dir, f"ginsew_{i}.mp3"),
            )
            for i in range(8)
        ]
        legacy_voice = os.path.join(extraction_dir, "extraction_ginsew.mp3")

        title = VGText("GINSEW", font_size=LARGE_FONT_SIZE + 8, color=WHITE, weight=BOLD_WEIGHT).move_to(ORIGIN)
        underline = Line(LEFT * 1.8, RIGHT * 1.8, color=VG_GOLD, stroke_width=2, stroke_opacity=0.65).next_to(title, DOWN, buff=0.25)

        if os.path.exists(voices[0]):
            self.add_sound(voices[0])
        elif os.path.exists(legacy_voice):
            self.add_sound(legacy_voice)
        dur_0 = _get_audio_duration(voices[0]) or (3.5 if os.path.exists(legacy_voice) else 2.5)
        self.play(Write(title), Create(underline), run_time=1.2)
        self.wait(max(0.4, dur_0 - 1.2))

        top_title = VGText(
            "GINSEW - GENERATIVE INVISIBLE SEQUENCE WATERMARKING",
            font_size=24,
            color=WHITE,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.28)
        top_ul = Line(LEFT * 4.35, RIGHT * 4.35, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(top_title, DOWN, buff=0.15)
        self.play(Transform(title, top_title), Transform(underline, top_ul), run_time=0.75)

        # =========================================================================
        # CẢNH 3.6.1 - GINSEW cho generative LLM
        # =========================================================================
        if os.path.exists(voices[1]):
            self.add_sound(voices[1])
        dur = _get_audio_duration(voices[1]) or 22.0

        sub = VGText("Watermark cho mô hình sinh văn bản", font_size=22, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        prompt = _box("Prompt / context", 2.45, 0.72, VG_BLUE, 16, BOLD_WEIGHT).move_to([-4.85, 0.72, 0])
        llm = _box("Generative LLM\nGPT-style decoder", 2.9, 1.15, VG_GOLD, 16, BOLD_WEIGHT).move_to([-1.35, 0.72, 0])
        probs = RoundedRectangle(corner_radius=0.08, width=3.15, height=2.6, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GREEN, stroke_width=1.8).move_to([2.75, 0.35, 0])
        probs_t = VGText("next-token probabilities", font_size=15, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(probs.get_top(), DOWN, buff=0.18)
        words = [("good", 0.31), ("great", 0.24), ("nice", 0.18), ("bad", 0.08)]
        rows = VGroup()
        for idx, (word, prob) in enumerate(words):
            y = probs.get_top()[1] - 0.65 - idx * 0.43
            rows.add(VGText(word, font_size=14, color=WHITE).move_to([probs.get_center()[0] - 1.05, y, 0]))
            rows.add(Rectangle(width=prob * 4.0, height=0.15, fill_color=VG_GREEN, fill_opacity=0.72, stroke_color=VG_GREEN, stroke_width=1).move_to([probs.get_center()[0] - 0.2 + prob * 2.0, y, 0]))
            rows.add(VGText(f"{prob:.2f}", font_size=13, color=VG_GRAY).move_to([probs.get_center()[0] + 1.18, y, 0]))
        out = _box("generated text", 2.35, 0.7, VG_PURPLE, 15, BOLD_WEIGHT).move_to([2.75, -2.05, 0])
        a1 = Arrow(prompt.get_right(), llm.get_left(), buff=0.04, color=VG_BLUE, stroke_width=2.2, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(llm.get_right(), probs.get_left(), buff=0.1, color=VG_GOLD, stroke_width=1.8)
        a3 = Arrow(probs.get_bottom(), out.get_top(), buff=0.1, color=VG_PURPLE, stroke_width=1.8)
        note = VGText("GINSEW can thiệp nhẹ vào phân phối token kế tiếp, không sửa trực tiếp câu đã sinh.", font_size=16, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(prompt), Create(a1), FadeIn(llm), run_time=0.8)
        self.play(Create(a2), FadeIn(VGroup(probs, probs_t, rows)), run_time=0.9)
        self.play(Create(a3), FadeIn(out), FadeIn(note), run_time=0.8)
        scene = VGroup(sub, prompt, llm, probs, probs_t, rows, out, a1, a2, a3, note)
        self.wait(max(1.0, dur - 3.0))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.2 - Hash và phân nhóm từ vựng
        # =========================================================================
        if os.path.exists(voices[2]):
            self.add_sound(voices[2])
        dur = _get_audio_duration(voices[2]) or 24.0

        sub = VGText("Step 0: hash token và chia từ vựng thành nhóm", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        vocab = RoundedRectangle(corner_radius=0.08, width=2.4, height=2.75, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GRAY, stroke_width=1.5).move_to([-4.35, -0.15, 0])
        vocab_t = VGText("Vocabulary V", font_size=16, color=VG_GRAY, weight=BOLD_WEIGHT).next_to(vocab.get_top(), DOWN, buff=0.2)
        toks = VGroup()
        for idx, tok in enumerate(["great", "nice", "good", "bad", "poor"]):
            toks.add(VGText(tok, font_size=15, color=WHITE).move_to([vocab.get_center()[0], vocab.get_top()[1] - 0.68 - idx * 0.38, 0]))
        hash_box = _box("hash g(token)\n-> [0, 1]", 2.3, 1.0, VG_BLUE, 15, BOLD_WEIGHT).move_to([-1.35, -0.15, 0])
        g1 = RoundedRectangle(corner_radius=0.08, width=2.55, height=1.65, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GREEN, stroke_width=1.8).move_to([3.1, 0.95, 0])
        g2 = RoundedRectangle(corner_radius=0.08, width=2.55, height=1.65, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_RED, stroke_width=1.8).move_to([3.1, -1.05, 0])
        g1_l = VGText("Group G1", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(g1.get_top(), DOWN, buff=0.2)
        g2_l = VGText("Group G2", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).next_to(g2.get_top(), DOWN, buff=0.2)
        g1_words = VGroup(VGText("great", font_size=14, color=WHITE), VGText("nice", font_size=14, color=WHITE), VGText("good", font_size=14, color=WHITE)).arrange(DOWN, buff=0.15).move_to(g1.get_center() + DOWN * 0.18)
        g2_words = VGroup(VGText("bad", font_size=14, color=WHITE), VGText("poor", font_size=14, color=WHITE), VGText("awful", font_size=14, color=WHITE)).arrange(DOWN, buff=0.15).move_to(g2.get_center() + DOWN * 0.18)
        a1 = Arrow(vocab.get_right(), hash_box.get_left(), buff=0.1, color=VG_GRAY, stroke_width=1.7)
        split = Dot(hash_box.get_right() + RIGHT * 0.55, radius=0.035, color=VG_GRAY)
        a2 = Arrow(hash_box.get_right(), split.get_center(), buff=0.04, color=VG_GRAY, stroke_width=1.5)
        a3 = Arrow(split.get_center(), g1.get_left(), buff=0.08, color=VG_GREEN, stroke_width=1.7)
        a4 = Arrow(split.get_center(), g2.get_left(), buff=0.08, color=VG_RED, stroke_width=1.7)
        note = VGText("Nhóm từ vựng giúp tín hiệu sống sót tốt hơn khi attacker thay một token bằng từ gần nghĩa.", font_size=16, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(vocab, vocab_t, toks)), run_time=0.7)
        self.play(Create(a1), FadeIn(hash_box), run_time=0.7)
        self.play(FadeIn(split), Create(a2), Create(a3), Create(a4), FadeIn(VGroup(g1, g1_l, g1_words, g2, g2_l, g2_words)), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        scene = VGroup(sub, vocab, vocab_t, toks, hash_box, g1, g1_l, g1_words, g2, g2_l, g2_words, a1, split, a2, a3, a4, note)
        self.wait(max(1.0, dur - 3.3))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.3 - Tín hiệu hình sin đối pha
        # =========================================================================
        if os.path.exists(voices[3]):
            self.add_sound(voices[3])
        dur = _get_audio_duration(voices[3]) or 26.0

        sub = VGText("Step 2: tạo tín hiệu tuần hoàn bí mật", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        formula_b = RoundedRectangle(corner_radius=0.08, width=5.6, height=1.55, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GOLD, stroke_width=1.8).move_to([0, 1.05, 0])
        f1 = MathTex(r"z_1(\mathbf{x}) = \cos(f_w g(\mathbf{x}))", font_size=26, color=VG_GREEN).move_to(formula_b.get_center() + UP * 0.32)
        f2 = MathTex(r"z_2(\mathbf{x}) = \cos(f_w g(\mathbf{x}) + \pi)", font_size=26, color=VG_RED).move_to(formula_b.get_center() + DOWN * 0.32)
        axes = Axes(x_range=[0, 1, 0.25], y_range=[-1, 1, 1], x_length=7.0, y_length=2.4, axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}).move_to([0, -1.35, 0])
        wave1 = VMobject(color=VG_GREEN, stroke_width=2.5)
        wave2 = VMobject(color=VG_RED, stroke_width=2.5)
        pts1 = []
        pts2 = []
        for j in range(140):
            u = j / 139
            pts1.append(axes.c2p(u, math.cos(2 * math.pi * 2.0 * u)))
            pts2.append(axes.c2p(u, math.cos(2 * math.pi * 2.0 * u + math.pi)))
        wave1.set_points_smoothly(pts1)
        wave2.set_points_smoothly(pts2)
        lbl1 = VGText("G1: cùng pha", font_size=15, color=VG_GREEN).move_to([-4.25, -0.35, 0])
        lbl2 = VGText("G2: lệch pha pi", font_size=15, color=VG_RED).move_to([-4.05, -0.75, 0])
        note = VGText("Tần số f_w nằm trong khóa bí mật; detection sau này sẽ tìm lại đúng tần số này.", font_size=16, color=VG_GRAY).move_to([0, -2.82, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(formula_b, f1, f2)), run_time=0.8)
        self.play(Create(axes), FadeIn(VGroup(lbl1, lbl2)), run_time=0.5)
        self.play(Create(wave1), Create(wave2), FadeIn(note, shift=UP * 0.1), run_time=1.1)
        scene = VGroup(sub, formula_b, f1, f2, axes, wave1, wave2, lbl1, lbl2, note)
        self.wait(max(1.0, dur - 2.9))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.4 - Can thiệp xác suất cấp độ nhóm
        # =========================================================================
        if os.path.exists(voices[4]):
            self.add_sound(voices[4])
        dur = _get_audio_duration(voices[4]) or 34.0

        sub = VGText("Step 3: chỉnh tổng xác suất của nhóm, rồi phân bổ lại", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        formula_b = RoundedRectangle(corner_radius=0.08, width=8.7, height=2.4, fill_color="#18181A", fill_opacity=0.94, stroke_color=VG_PURPLE, stroke_width=1.8).move_to([0, 1.0, 0])
        q1 = MathTex(r"Q_{\mathcal{G}_1} = \sum_{i \in \mathcal{G}_1} \mathbf{p}_i", font_size=25, color=VG_GREEN).move_to(formula_b.get_center() + UP * 0.62)
        q2 = MathTex(r"\tilde{Q}_{\mathcal{G}_1} = \frac{Q_{\mathcal{G}_1} + \epsilon(1 + z_1(\mathbf{x}))}{1 + 2\epsilon}", font_size=25, color=VG_GOLD).move_to(formula_b.get_center())
        q3 = MathTex(r"\mathbf{p}_i \leftarrow \frac{\tilde{Q}_{\mathcal{G}_1}}{Q_{\mathcal{G}_1}} \cdot \mathbf{p}_i \quad (i \in \mathcal{G}_1)", font_size=25, color=WHITE).move_to(formula_b.get_center() + DOWN * 0.64)
        before = RoundedRectangle(corner_radius=0.08, width=3.2, height=1.95, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_BLUE, stroke_width=1.7).move_to([-3.6, -1.62, 0])
        after = RoundedRectangle(corner_radius=0.08, width=3.2, height=1.95, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_GREEN, stroke_width=1.7).move_to([3.6, -1.62, 0])
        b_t = VGText("trước watermark", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(before.get_top(), DOWN, buff=0.18)
        a_t = VGText("sau watermark", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(after.get_top(), DOWN, buff=0.18)
        b_rows = VGroup(
            VGText("G1 total: 0.55", font_size=15, color=VG_GREEN),
            VGText("great 0.31", font_size=14, color=WHITE),
            VGText("nice  0.24", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.14).move_to(before.get_center() + DOWN * 0.15)
        a_rows = VGroup(
            VGText("G1 total: 0.63", font_size=15, color=VG_GREEN),
            VGText("great 0.36", font_size=14, color=WHITE),
            VGText("nice  0.27", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.14).move_to(after.get_center() + DOWN * 0.15)
        eps = _box("epsilon\nwatermark level", 2.25, 0.86, VG_ORANGE, 14, BOLD_WEIGHT).move_to([0, -1.62, 0])
        ar1 = Arrow(before.get_right(), eps.get_left(), buff=0.08, color=VG_ORANGE, stroke_width=1.8)
        ar2 = Arrow(eps.get_right(), after.get_left(), buff=0.08, color=VG_GREEN, stroke_width=1.8)
        note = VGText("Khác DRW: GINSEW đổi tổng xác suất của cả nhóm token, không cộng riêng lẻ từng token ngay từ đầu.", font_size=15, color=VG_GRAY).move_to([0, -2.95, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(formula_b, q1, q2, q3), shift=DOWN * 0.08), run_time=1.0)
        self.play(FadeIn(VGroup(before, b_t, b_rows)), run_time=0.65)
        self.play(Create(ar1), FadeIn(eps), run_time=0.55)
        self.play(Create(ar2), FadeIn(VGroup(after, a_t, a_rows)), run_time=0.65)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        scene = VGroup(sub, formula_b, q1, q2, q3, before, after, b_t, a_t, b_rows, a_rows, eps, ar1, ar2, note)
        self.wait(max(1.0, dur - 3.85))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.5 - Sinh văn bản từ phân phối mới
        # =========================================================================
        if os.path.exists(voices[5]):
            self.add_sound(voices[5])
        dur = _get_audio_duration(voices[5]) or 24.0

        sub = VGText("Step 4: sinh token từ phân phối đã watermark", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        sent = VGroup()
        for idx, word in enumerate(["The", "story", "was", "great", "and", "natural"]):
            is_marked = word in {"great", "natural"}
            col = VG_GREEN if is_marked else WHITE
            sent.add(_box(word, 1.25 if word != "natural" else 1.55, 0.58, col, 14, BOLD_WEIGHT if is_marked else None))
        sent.arrange(RIGHT, buff=0.18).move_to([0, 1.25, 0])
        group_line = Line(sent[3].get_bottom(), sent[5].get_bottom(), color=VG_GREEN, stroke_width=2, stroke_opacity=0.65).shift(DOWN * 0.2)
        g_lbl = VGText("nhiều token thuộc G1 hơn một chút", font_size=16, color=VG_GREEN).next_to(group_line, DOWN, buff=0.18)
        attack = _box("synonym replacement\n'great' -> 'excellent'", 3.3, 1.0, VG_RED, 14, BOLD_WEIGHT).move_to([0, -0.95, 0])
        robust = VGText("Vì tín hiệu nằm ở cấp nhóm, thay một từ gần nghĩa không nhất thiết xóa mẫu thống kê.", font_size=16, color=VG_GRAY).move_to([0, -2.35, 0])
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(tok, shift=UP * 0.1) for tok in sent], lag_ratio=0.12), run_time=1.2)
        self.play(Create(group_line), FadeIn(g_lbl), run_time=0.6)
        self.play(FadeIn(attack, shift=UP * 0.1), FadeIn(robust, shift=UP * 0.1), run_time=0.8)
        scene = VGroup(sub, sent, group_line, g_lbl, attack, robust)
        self.wait(max(1.0, dur - 3.1))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.6 - Detection bằng Lomb-Scargle periodogram
        # =========================================================================
        if os.path.exists(voices[6]):
            self.add_sound(voices[6])
        dur = _get_audio_duration(voices[6]) or 34.0

        sub = VGText("Detection: probing và Lomb-Scargle periodogram", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        q = _box("probing\nqueries", 1.9, 0.72, VG_BLUE, 14, BOLD_WEIGHT).move_to([-4.65, 0.95, 0])
        suspect = _box("Suspect\nModel", 2.15, 0.82, VG_RED, 14, BOLD_WEIGHT).move_to([-2.05, 0.95, 0])
        seq = _box("generated\noutputs", 2.1, 0.82, VG_PURPLE, 14, BOLD_WEIGHT).move_to([0.55, 0.95, 0])
        signal = _box("group signal\nG1 vs G2", 2.2, 0.82, VG_GRAY, 14, BOLD_WEIGHT).move_to([3.25, 0.95, 0])
        arrows = VGroup(
            Arrow(q.get_right(), suspect.get_left(), buff=0.08, color=VG_BLUE, stroke_width=1.6),
            Arrow(suspect.get_right(), seq.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=1.6),
            Arrow(seq.get_right(), signal.get_left(), buff=0.08, color=VG_GRAY, stroke_width=1.6),
        )
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 4, 1], x_length=6.3, y_length=2.45, axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}).move_to([0, -1.32, 0])
        period_t = VGText("P(f): Lomb-Scargle periodogram", font_size=17, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(axes, UP, buff=0.08)
        curve = VMobject(color=VG_GOLD, stroke_width=2.5)
        pts = []
        for j in range(140):
            x = 10 * j / 139
            y = 0.42 + 0.16 * math.sin(2.2 * x) + 0.12 * math.sin(6.1 * x) + 2.75 * math.exp(-((x - 6.0) / 0.42) ** 2)
            pts.append(axes.c2p(x, y))
        curve.set_points_smoothly(pts)
        tau = DashedLine(axes.c2p(0, 2.25), axes.c2p(10, 2.25), color=VG_RED, stroke_width=1.8, dash_length=0.12)
        fw = MathTex(r"f_w", font_size=26, color=VG_GOLD).move_to(axes.c2p(6.0, -0.25))
        peak_lbl = VGText("peak tại f_w", font_size=15, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(axes.c2p(6.15, 3.65))
        verdict = VGText("peak vượt ngưỡng -> nghi ngờ model là bản sao; không có peak rõ -> chưa đủ bằng chứng", font_size=15, color=VG_GREEN, weight=BOLD_WEIGHT).move_to([0, -2.88, 0])

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(VGroup(q, suspect, seq, signal)), Create(arrows), run_time=1.0)
        self.play(Create(axes), FadeIn(period_t), run_time=0.55)
        self.play(Create(tau), FadeIn(fw), run_time=0.45)
        self.play(Create(curve), FadeIn(peak_lbl), run_time=1.0)
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.6)
        scene = VGroup(sub, q, suspect, seq, signal, arrows, axes, period_t, tau, fw, curve, peak_lbl, verdict)
        self.wait(max(1.0, dur - 4.1))
        self.play(FadeOut(scene), run_time=0.8)

        # =========================================================================
        # CẢNH 3.6.7 - Tổng kết GINSEW
        # =========================================================================
        if os.path.exists(voices[7]):
            self.add_sound(voices[7])
        dur = _get_audio_duration(voices[7]) or 24.0

        sub = VGText("Tổng kết cơ chế GINSEW", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)
        items = [
            (r"g(\text{token})", "hash token", VG_BLUE),
            (r"\mathcal{G}_1,\mathcal{G}_2", "vocab groups", VG_GREEN),
            (r"z_1,z_2", "sinusoidal signal", VG_PURPLE),
            (r"\tilde{Q}_{\mathcal{G}}", "group prob.", VG_ORANGE),
            (r"\text{generate}", "text output", VG_GREEN),
            (r"f_w\text{ peak}", "detect", VG_GOLD),
        ]
        boxes = VGroup()
        arrows = VGroup()
        x0 = -5.1
        for i, (sym, desc, col) in enumerate(items):
            box = RoundedRectangle(corner_radius=0.06, width=1.6, height=0.88, fill_color="#18181A", fill_opacity=0.92, stroke_color=col, stroke_width=1.6).move_to([x0 + 2.05 * i, 0.9, 0])
            s = MathTex(sym, font_size=17, color=col).move_to(box.get_center() + UP * 0.15)
            d = VGText(desc, font_size=11, color=WHITE).move_to(box.get_center() + DOWN * 0.2)
            boxes.add(VGroup(box, s, d))
            if i > 0:
                arrows.add(Arrow(boxes[i - 1][0].get_right(), box.get_left(), buff=0.05, color=VG_GRAY, stroke_width=1.5))

        summary_b = RoundedRectangle(corner_radius=0.08, width=9.7, height=2.65, fill_color="#18181A", fill_opacity=0.92, stroke_color=VG_BLUE, stroke_width=1.8).move_to([0, -1.45, 0])
        t1 = VGText("GINSEW phù hợp với mô hình sinh văn bản: GPT-style decoder, translation, story generation.", font_size=14, color=WHITE).move_to(summary_b.get_center() + UP * 0.78)
        t2 = VGText("Watermark nằm trong phân phối token theo nhóm từ vựng, không bám vào một từ cố định.", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + UP * 0.28)
        t3 = VGText("Nhờ nhóm token, tín hiệu bền hơn trước synonym replacement.", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + DOWN * 0.22)
        t4 = VGText("Xác minh bằng probing và Lomb-Scargle: peak tại f_w vượt ngưỡng mới là bằng chứng mạnh.", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).move_to(summary_b.get_center() + DOWN * 0.72)

        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(boxes[0], shift=DOWN * 0.1), run_time=0.35)
        for i in range(1, len(boxes)):
            self.play(Create(arrows[i - 1]), FadeIn(boxes[i], shift=DOWN * 0.1), run_time=0.32)
        self.play(FadeIn(VGroup(summary_b, t1, t2, t3, t4), shift=UP * 0.1), run_time=0.9)
        summary_scene = VGroup(sub, boxes, arrows, summary_b, t1, t2, t3, t4)
        self.wait(max(1.0, dur - (0.5 + 0.35 + 0.32 * (len(boxes) - 1) + 0.9)))
        self.play(FadeOut(summary_scene), FadeOut(title), FadeOut(underline), run_time=1.0)
        self.wait(0.5)


def play_part3_ginsew(scene: Scene) -> None:
    GINSEWScene.construct(scene)
