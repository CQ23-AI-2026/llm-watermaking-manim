import os
import sys
import glob

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
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE, VG_RED,
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


class DRW34Scene(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)

        grid = NumberPlane(
            background_line_style={"stroke_color": VG_GRAY, "stroke_width": 1, "stroke_opacity": 0.06},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # Persistent top banner
        scene_title = VGText(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            font_size=LARGE_FONT_SIZE - 6, color=WHITE, weight=BOLD_WEIGHT
        ).move_to(ORIGIN)
        underline = Line(LEFT * 4.5, RIGHT * 4.5, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(scene_title, DOWN, buff=0.25)

        # Audio
        ext = os.path.join(current_dir, "assets", "extraction")
        voice_intro = os.path.join(ext, "extraction_title.mp3")
        voice_341   = os.path.join(ext, "extraction_3_4_1.mp3")
        voice_342   = os.path.join(ext, "extraction_3_4_2.mp3")
        voice_343   = os.path.join(ext, "extraction_3_4_3.mp3")
        voice_344   = os.path.join(ext, "extraction_3_4_4.mp3")
        voice_345   = os.path.join(ext, "extraction_3_4_5.mp3")

        dur_intro = _get_audio_duration(voice_intro) or 4.0
        dur_341 = _get_audio_duration(voice_341) or 44.0
        dur_342 = _get_audio_duration(voice_342) or 34.0
        dur_343 = _get_audio_duration(voice_343) or 42.0
        dur_344 = _get_audio_duration(voice_344) or 25.0
        dur_345 = _get_audio_duration(voice_345) or 38.0

        # ── Intro ──────────────────────────────────────────────────────────────
        if os.path.exists(voice_intro):
            self.add_sound(voice_intro)
        self.play(Write(scene_title), Create(underline), run_time=1.2)
        self.wait(max(0.5, dur_intro - 1.2))

        top_title = VGText(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            font_size=LARGE_FONT_SIZE - 10, color=WHITE, weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.28)
        top_ul = Line(LEFT * 3.825, RIGHT * 3.825, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(top_title, DOWN, buff=0.15)

        self.play(Transform(scene_title, top_title), Transform(underline, top_ul), run_time=1.0)
        self.wait(0.4)

        # =========================================================================
        # CẢNH 3.4.1 — MODEL EXTRACTION
        # =========================================================================
        if os.path.exists(voice_341):
            self.add_sound(voice_341)

        sub = VGText("Model Extraction", font_size=22, color=VG_RED, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Victim API — left, ổ khóa bật sáng nhấn mạnh "black-box"
        v_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.8,
            fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.2).move_to([-3.4, 0.2, 0])
        v_lbl = VGText("Victim API",      font_size=22, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(v_box.get_center() + UP*0.35)
        v_sub = VGText("Black-box Model", font_size=17, color=VG_GRAY).move_to(v_box.get_center() + DOWN*0.15)
        lock_body     = RoundedRectangle(corner_radius=0.03, width=0.30, height=0.22, color=VG_GRAY, fill_color=VG_GRAY, fill_opacity=1.0)
        lock_shackle  = Arc(radius=0.12, angle=PI, color=VG_GRAY, stroke_width=2.5).next_to(lock_body, UP, buff=-0.06)
        lock_icon     = VGroup(lock_body, lock_shackle).next_to(v_box.get_top(), DOWN, buff=0.1)
        victim_g      = VGroup(v_box, v_lbl, v_sub, lock_icon)

        # Attacker — right
        a_box = RoundedRectangle(corner_radius=0.1, width=3.0, height=1.5,
            fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.2).move_to([3.4, 0.2, 0])
        a_lbl = VGText("Attacker",        font_size=22, color=VG_RED, weight=BOLD_WEIGHT).move_to(a_box.get_center() + UP*0.22)
        a_sub = VGText("Massive Queries", font_size=17, color=VG_GRAY).move_to(a_box.get_center() + DOWN*0.25)
        attacker_g = VGroup(a_box, a_lbl, a_sub)

        # Arrows
        arr_q = Arrow(a_box.get_left() + DOWN*0.28, v_box.get_right() + DOWN*0.28, color=VG_GRAY, stroke_width=2.5, buff=0.1)
        lbl_q = VGText("Queries",   font_size=17, color=VG_GRAY).next_to(arr_q, DOWN, buff=0.1)
        arr_r = Arrow(v_box.get_right() + UP*0.28, a_box.get_left() + UP*0.28, color=VG_GREEN, stroke_width=2.5, buff=0.1)
        lbl_r = VGText("Responses", font_size=17, color=VG_GREEN).next_to(arr_r, UP, buff=0.1)

        # Floating text labels
        lbl_bb = VGText("Black-box API",   font_size=19, color=VG_GOLD).move_to([-3.4, -1.8, 0])
        lbl_mq = VGText("Massive Queries", font_size=19, color=VG_RED).move_to([3.4, -1.8, 0])

        scene_341 = VGroup(victim_g, attacker_g, arr_q, lbl_q, arr_r, lbl_r, lbl_bb, lbl_mq)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        # Victim API xuất hiện trước
        self.play(FadeIn(victim_g, shift=RIGHT*0.3), run_time=1.0)
        # Ổ khóa bật sáng → nhấn mạnh "black-box"
        self.play(lock_icon.animate.set_color(VG_GOLD), run_time=0.4)
        self.play(lock_icon.animate.set_color(VG_GRAY), run_time=0.3)
        # Attacker xuất hiện sau
        self.play(FadeIn(attacker_g, shift=LEFT*0.3), run_time=0.8)
        self.play(Create(arr_q), FadeIn(lbl_q), run_time=0.7)
        self.play(Create(arr_r), FadeIn(lbl_r), run_time=0.7)
        self.play(FadeIn(lbl_bb, shift=UP*0.1), FadeIn(lbl_mq, shift=UP*0.1), run_time=0.5)

        # Query dots tăng dần — gọi API hàng loạt
        for count in [2, 3, 4]:
            dg = VGroup(*[Circle(radius=0.07, color=VG_GRAY, fill_opacity=1.0, stroke_width=0)
                          .move_to(a_box.get_left() + DOWN*0.28) for _ in range(count)])
            self.add(dg)
            self.play(AnimationGroup(*[d.animate(run_time=0.9, rate_func=linear)
                                        .move_to(v_box.get_right() + DOWN*0.28) for d in dg], lag_ratio=0.25))
            self.play(FadeOut(dg), run_time=0.12)

        anim_t = 0.5 + 1.0 + 0.7 + 0.8 + 1.4 + 0.5 + 3 * (0.9 + 0.12)
        self.wait(max(1.0, dur_341 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_341), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.4.2 — PIPELINE: API → DATASET → STUDENT
        # =========================================================================
        if os.path.exists(voice_342):
            self.add_sound(voice_342)

        sub = VGText("Distillation Pipeline", font_size=22, color=VG_RED, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        BW, BH = 2.5, 0.95
        n1 = RoundedRectangle(corner_radius=0.08, width=BW, height=BH, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.0).move_to([-4.8, 0.5, 0])
        n2 = RoundedRectangle(corner_radius=0.08, width=BW, height=BH, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([-1.6, 0.5, 0])
        n3 = RoundedRectangle(corner_radius=0.08, width=BW, height=BH, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.8).move_to([1.6, 0.5, 0])
        n4 = RoundedRectangle(corner_radius=0.08, width=BW, height=BH, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.2).move_to([4.8, 0.5, 0])

        n1_l = VGText("Attacker\nQueries",      font_size=19, color=VG_RED,   weight=BOLD_WEIGHT).move_to(n1.get_center())
        n2_l = VGText("Victim API",             font_size=19, color=VG_BLUE,  weight=BOLD_WEIGHT).move_to(n2.get_center())
        n3_l = VGText("Prompt–Response\nDataset", font_size=17, color=VG_GRAY).move_to(n3.get_center())
        n4_l = VGText("Student\nModel",         font_size=19, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(n4.get_center())

        a12 = Arrow(n1.get_right(), n2.get_left(), buff=0.08, color=VG_GRAY,  stroke_width=2.0)
        a23 = Arrow(n2.get_right(), n3.get_left(), buff=0.08, color=VG_GRAY,  stroke_width=2.0)
        a34 = Arrow(n3.get_right(), n4.get_left(), buff=0.08, color=VG_GREEN, stroke_width=2.2)

        # Bảng dưới n3 — rows rơi xuống từng dòng
        tbl     = Rectangle(width=2.4, height=1.2, stroke_color=VG_GRAY, stroke_width=1.0).next_to(n3, DOWN, buff=0.3)
        tbl_vl  = Line(tbl.get_top(), tbl.get_bottom(), stroke_color=VG_GRAY, stroke_width=0.8).move_to(tbl.get_center() + LEFT*0.28)
        th1 = VGText("Prompt",   font_size=15, color=VG_GRAY).move_to(tbl.get_top() + DOWN*0.18 + LEFT*0.65)
        th2 = VGText("Response", font_size=15, color=VG_GRAY).move_to(tbl.get_top() + DOWN*0.18 + RIGHT*0.55)
        r1l = VGText("Q1", font_size=14, color=WHITE).move_to(tbl.get_top()   + DOWN*0.44 + LEFT*0.65)
        r1r = VGText("A1", font_size=14, color=VG_GREEN).move_to(tbl.get_top() + DOWN*0.44 + RIGHT*0.55)
        r2l = VGText("Q2", font_size=14, color=WHITE).move_to(tbl.get_top()   + DOWN*0.70 + LEFT*0.65)
        r2r = VGText("A2", font_size=14, color=VG_GREEN).move_to(tbl.get_top() + DOWN*0.70 + RIGHT*0.55)
        r3l = VGText("Q3", font_size=14, color=WHITE).move_to(tbl.get_top()   + DOWN*0.96 + LEFT*0.65)
        r3r = VGText("A3", font_size=14, color=VG_GREEN).move_to(tbl.get_top() + DOWN*0.96 + RIGHT*0.55)
        tbl_g = VGroup(tbl, tbl_vl, th1, th2, r1l, r1r, r2l, r2r, r3l, r3r)

        train_lbl = VGText("Train Student Model", font_size=17, color=VG_GREEN).next_to(n4, DOWN, buff=0.35)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        self.play(FadeIn(VGroup(n1, n1_l)), run_time=0.6)
        self.play(Create(a12), FadeIn(VGroup(n2, n2_l)), run_time=0.6)
        self.play(Create(a23), FadeIn(VGroup(n3, n3_l)), run_time=0.6)
        # Responses rơi xuống thành từng dòng
        self.play(FadeIn(VGroup(tbl, tbl_vl, th1, th2)), run_time=0.5)
        self.play(FadeIn(VGroup(r1l, r1r), shift=DOWN*0.12), run_time=0.35)
        self.play(FadeIn(VGroup(r2l, r2r), shift=DOWN*0.12), run_time=0.35)
        self.play(FadeIn(VGroup(r3l, r3r), shift=DOWN*0.12), run_time=0.35)
        # Dataset phóng to nhẹ
        self.play(VGroup(n3, n3_l).animate.scale(1.06), run_time=0.35)
        self.play(VGroup(n3, n3_l).animate.scale(1/1.06), run_time=0.28)
        # Student model sáng lên
        self.play(Create(a34), FadeIn(VGroup(n4, n4_l)), run_time=0.6)
        self.play(n4.animate.set_stroke(color=VG_GREEN, width=3.5), FadeIn(train_lbl, shift=UP*0.1), run_time=0.7)

        pipeline_342 = VGroup(n1, n1_l, n2, n2_l, n3, n3_l, n4, n4_l, a12, a23, a34, tbl_g, train_lbl)
        anim_t = 0.5 + 0.6*3 + 0.5 + 0.35*3 + 0.63 + 1.3
        self.wait(max(1.0, dur_342 - anim_t))
        self.play(FadeOut(sub), FadeOut(pipeline_342), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.4.3 — CÂU HỎI PHÒNG THỦ TRUNG TÂM
        # =========================================================================
        if os.path.exists(voice_343):
            self.add_sound(voice_343)

        # Màn hình tối lại
        overlay = Rectangle(width=22, height=14, fill_color=BLACK, fill_opacity=0.78, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(overlay), run_time=0.8)

        # Câu hỏi lớn ở giữa
        big_q = VGText("Can the copy learn\na hidden signal?", font_size=42, color=WHITE, weight=BOLD_WEIGHT).move_to(ORIGIN)
        self.play(Write(big_q), run_time=1.8)
        self.wait(1.2)  # Dừng nhịp ~1 giây

        self.play(FadeOut(big_q), FadeOut(overlay), run_time=0.8)
        self.wait(0.3)

        # Victim API → Student Model với 2 luồng
        sub = VGText("Ý tưởng Watermark kháng Distillation", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        v343 = RoundedRectangle(corner_radius=0.08, width=4.0, height=0.95, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([0.0, 1.6, 0])
        v343_l = VGText("Victim API (Watermarked)", font_size=20, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(v343.get_center())

        s343 = RoundedRectangle(corner_radius=0.08, width=4.0, height=0.95, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.0).move_to([0.0, -1.6, 0])
        s343_l = VGText("Student Model (Bản sao)", font_size=20, color=VG_RED, weight=BOLD_WEIGHT).move_to(s343.get_center())

        # Luồng 1: Task Behavior — solid white, bên trái
        task_s = v343.get_bottom() + LEFT*0.65
        task_e = s343.get_top()   + LEFT*0.65
        arr_task = Arrow(task_s, task_e, color=WHITE, stroke_width=3.0, buff=0.0)
        lbl_task = VGText("Task Behavior", font_size=18, color=WHITE).next_to(arr_task, LEFT, buff=0.2)

        # Luồng 2: Hidden Watermark — nét đứt vàng, bên phải, xuất hiện sau
        wm_s = v343.get_bottom() + RIGHT*0.65
        wm_e = s343.get_top()   + RIGHT*0.65
        arr_wm = DashedVMobject(
            Arrow(wm_s, wm_e, color=VG_GOLD, stroke_width=2.5, buff=0.0),
            num_dashes=14, dashed_ratio=0.55
        )
        lbl_wm = VGText("Hidden Watermark", font_size=18, color=VG_GOLD).next_to(arr_wm, RIGHT, buff=0.2)

        self.play(FadeIn(sub, shift=DOWN*0.1), run_time=0.5)
        self.play(FadeIn(VGroup(v343, v343_l), shift=UP*0.2), FadeIn(VGroup(s343, s343_l), shift=DOWN*0.2), run_time=1.0)
        # Task Behavior xuất hiện trước
        self.play(Create(arr_task), FadeIn(lbl_task), run_time=0.8)
        self.wait(0.5)
        # Hidden Watermark xuất hiện sau — dạng nét đứt
        self.play(Create(arr_wm), FadeIn(lbl_wm, scale=0.9), run_time=1.0)

        # Student Model nhận cả hai — particles vàng chảy xuống
        wm_pts = VGroup(*[Dot(color=VG_GOLD, radius=0.07, fill_opacity=0.9).move_to(wm_s) for _ in range(4)])
        self.add(wm_pts)
        self.play(AnimationGroup(*[p.animate(run_time=1.2, rate_func=linear).move_to(wm_e) for p in wm_pts], lag_ratio=0.2))
        self.play(FadeOut(wm_pts), s343.animate.set_stroke(color=VG_GOLD), run_time=0.5)

        scene_343 = VGroup(v343, v343_l, s343, s343_l, arr_task, lbl_task, arr_wm, lbl_wm)
        anim_t = 0.8 + 1.8 + 1.2 + 0.8 + 0.3 + 0.5 + 1.0 + 1.2 + 1.7
        self.wait(max(1.0, dur_343 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_343), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.4.4 — WATERMARK KHÔNG TRONG CHỮ, MÀ TRONG XÁC SUẤT (X-RAY VIEW)
        # =========================================================================
        if os.path.exists(voice_344):
            self.add_sound(voice_344)

        sub = VGText("Watermark trong Phân phối Xác suất", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

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

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
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
        # Thông số bars
        bar_probs  = [0.720, 0.190, 0.090]
        bar_labels = ["Positive", "Neutral", "Negative"]
        bar_colors = [VG_GREEN, "#88AACC", VG_RED]
        bar_scale  = 3.2   # chiều cao max của bar (Positive = 1.0 → 3.2 units)
        bar_width  = 0.9
        bar_gap    = 0.55  # khoảng cách giữa các bars
        bar_center_x = 0.0
        bar_bottom_y = -1.8   # đáy các bars hạ xuống -1.8 để tránh chồng chéo

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

        # Tiêu đề - hạ xuống Y=1.8
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

        scene_344 = VGroup(
            prob_title, bars_before, cat_labels, prob_nums, key_g, tiny_lbl, tiny_arr, pred_box, pred_lbl, same_lbl
        )
        anim_t = 13.74
        self.wait(max(1.0, dur_344 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_344), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.4.5 — WATERMARK ĐI THEO QUÁ TRÌNH DISTILLATION
        # =========================================================================
        if os.path.exists(voice_345):
            self.add_sound(voice_345)

        sub = VGText("Watermark transfers via Distillation", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Pipeline: Watermarked Victim API → Watermarked Outputs → Distillation Dataset → Student Model
        p1 = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.88, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.2).move_to([-4.5, 0.7, 0])
        p2 = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.88, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.8).move_to([-1.5, 0.7, 0])
        p3 = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.88, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.8).move_to([1.5, 0.7, 0])
        p4 = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.88, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.2).move_to([4.5, 0.7, 0])

        p1_l = VGText("Watermarked\nVictim API",    font_size=17, color=VG_GOLD,  weight=BOLD_WEIGHT).move_to(p1.get_center())
        p2_l = VGText("Watermarked\nOutputs",        font_size=17, color=VG_GRAY).move_to(p2.get_center())
        p3_l = VGText("Distillation\nDataset",       font_size=17, color=VG_GRAY).move_to(p3.get_center())
        p4_l = VGText("Student\nModel",              font_size=17, color=VG_RED,   weight=BOLD_WEIGHT).move_to(p4.get_center())

        # Chấm nhỏ mờ trên output — tượng trưng watermark
        wm_dots = VGroup(*[Dot(color=VG_GOLD, radius=0.055, fill_opacity=0.55).shift(RIGHT*0.22*i) for i in range(4)]).next_to(p2, DOWN, buff=0.1).align_to(p2, LEFT).shift(RIGHT*0.3)

        a1 = Arrow(p1.get_right(), p2.get_left(), buff=0.08, color=VG_GOLD, stroke_width=2.0)
        a2 = Arrow(p2.get_right(), p3.get_left(), buff=0.08, color=VG_GRAY, stroke_width=2.0)
        a3 = Arrow(p3.get_right(), p4.get_left(), buff=0.08, color=VG_RED,  stroke_width=2.2)

        # Student Model 2 lớp
        lbl_main = VGText("Main Capability",  font_size=16, color=WHITE).next_to(p4, DOWN, buff=0.18)
        lbl_wm   = VGText("Hidden Watermark", font_size=16, color=VG_GOLD).next_to(lbl_main, DOWN, buff=0.12)

        caption = VGText(
            "Distillation transfers behavior — and may transfer watermark",
            font_size=16, color=VG_GRAY
        ).move_to([0.0, -2.1, 0])

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        self.play(FadeIn(VGroup(p1, p1_l), shift=DOWN*0.2), run_time=0.6)
        self.play(Create(a1), FadeIn(VGroup(p2, p2_l), shift=DOWN*0.2), run_time=0.6)
        # Bật "statistical view": chấm watermark hiện ra
        self.play(FadeIn(wm_dots, scale=0.8), run_time=0.6)
        self.play(Create(a2), FadeIn(VGroup(p3, p3_l), shift=DOWN*0.2), run_time=0.6)
        self.play(Create(a3), FadeIn(VGroup(p4, p4_l), shift=DOWN*0.2), run_time=0.6)

        # Dataset hấp thụ → chấm bay vào Student Model
        travel = VGroup(*[Dot(color=VG_GOLD, radius=0.065, fill_opacity=0.9).move_to(p3.get_right()) for _ in range(4)])
        self.add(travel)
        self.play(AnimationGroup(*[d.animate(run_time=1.0, rate_func=linear).move_to(p4.get_center()) for d in travel], lag_ratio=0.2))
        self.play(FadeOut(travel), p4.animate.set_stroke(color=VG_GOLD), run_time=0.5)

        # Student Model phát sáng với 2 lớp
        self.play(FadeIn(lbl_main, shift=UP*0.1), FadeIn(lbl_wm, shift=UP*0.1), run_time=0.6)
        self.play(FadeIn(caption, shift=UP*0.1), run_time=0.5)

        pipeline_345 = VGroup(p1, p1_l, p2, p2_l, p3, p3_l, p4, p4_l, a1, a2, a3, wm_dots, lbl_main, lbl_wm, caption)
        # voice_345 covers cảnh 3.4.5 + 3.4.6; dùng ~60% cho 3.4.5
        anim_t = 0.5 + 0.6*4 + 0.6 + 1.0 + 1.1
        self.wait(max(1.0, dur_345 * 0.62 - anim_t))
        self.play(FadeOut(sub), FadeOut(pipeline_345), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.4.6 — BA PHƯƠNG PHÁP ROADMAP
        # =========================================================================
        # (Không có voice riêng — dùng phần còn lại của voice_345)

        sub = VGText("3 Phương pháp bảo vệ", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        CW, CH = 3.8, 3.5

        # Card DRW — xuất hiện trước, sáng nhất
        c1b = RoundedRectangle(corner_radius=0.1, width=CW, height=CH, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.5).move_to([-4.2, -0.35, 0])
        c1t = VGText("DRW", font_size=30, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(c1b.get_top(), DOWN, buff=0.3)
        c1s = VGText("Probability Watermark", font_size=17, color=WHITE).next_to(c1t, DOWN, buff=0.18)
        c1p = Line(LEFT*1.65, RIGHT*1.65, color=VG_BLUE, stroke_width=1, stroke_opacity=0.4).next_to(c1s, DOWN, buff=0.18)
        cb  = Rectangle(width=0.48, height=0.33, stroke_color=VG_BLUE, stroke_width=1.5).move_to([-4.2, -0.58, 0])
        ca  = Rectangle(width=0.28, height=0.22, stroke_color=VG_GRAY, stroke_width=1.0).move_to([-4.72, -1.18, 0])
        cbb = Rectangle(width=0.28, height=0.22, stroke_color=VG_GRAY, stroke_width=1.0).move_to([-4.2, -1.18, 0])
        ccc = Rectangle(width=0.28, height=0.22, stroke_color=VG_GRAY, stroke_width=1.0).move_to([-3.68, -1.18, 0])
        cl1 = Line(cb.get_bottom(), ca.get_top(),  stroke_width=1.3, color=VG_BLUE)
        cl2 = Line(cb.get_bottom(), cbb.get_top(), stroke_width=1.3, color=VG_BLUE)
        cl3 = Line(cb.get_bottom(), ccc.get_top(), stroke_width=1.3, color=VG_BLUE)
        c1_g = VGroup(c1b, c1t, c1s, c1p, cb, ca, cbb, ccc, cl1, cl2, cl3)

        # Card GINSEW
        c2b = RoundedRectangle(corner_radius=0.1, width=CW, height=CH, fill_color="#18181A", fill_opacity=0.85, stroke_color=VG_GOLD, stroke_width=1.8).move_to([0.0, -0.35, 0])
        c2t = VGText("GINSEW", font_size=28, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(c2b.get_top(), DOWN, buff=0.3)
        c2s = VGText("Sequence Watermark", font_size=17, color=WHITE).next_to(c2t, DOWN, buff=0.18)
        c2p = Line(LEFT*1.65, RIGHT*1.65, color=VG_GOLD, stroke_width=1, stroke_opacity=0.4).next_to(c2s, DOWN, buff=0.18)
        tn1 = Circle(radius=0.14, stroke_color=VG_GRAY, stroke_width=1.5).move_to([-0.55, -0.82, 0])
        tn2 = Circle(radius=0.14, stroke_color=VG_GOLD, stroke_width=2.2).move_to([0.0, -0.82, 0])
        tn3 = Circle(radius=0.14, stroke_color=VG_GRAY, stroke_width=1.5).move_to([0.55, -0.82, 0])
        ta1 = Arrow(tn1.get_right(), tn2.get_left(), buff=0.05, color=VG_GOLD, stroke_width=1.8)
        ta2 = Arrow(tn2.get_right(), tn3.get_left(), buff=0.05, color=VG_GOLD, stroke_width=1.8)
        c2_g = VGroup(c2b, c2t, c2s, c2p, tn1, tn2, tn3, ta1, ta2)

        # Card CATER
        c3b = RoundedRectangle(corner_radius=0.1, width=CW, height=CH, fill_color="#18181A", fill_opacity=0.85, stroke_color=VG_PURPLE, stroke_width=1.8).move_to([4.2, -0.35, 0])
        c3t = VGText("CATER", font_size=28, color=VG_PURPLE, weight=BOLD_WEIGHT).next_to(c3b.get_top(), DOWN, buff=0.3)
        c3s = VGText("Conditional Word Choice", font_size=17, color=WHITE).next_to(c3t, DOWN, buff=0.18)
        c3p = Line(LEFT*1.65, RIGHT*1.65, color=VG_PURPLE, stroke_width=1, stroke_opacity=0.4).next_to(c3s, DOWN, buff=0.18)
        sr  = Circle(radius=0.14, stroke_color=VG_BLUE, stroke_width=1.5).move_to([4.2, -0.65, 0])
        sw1 = VGText("học tập",    font_size=16, color=VG_GRAY).move_to([3.65, -1.27, 0])
        sw2 = VGText("nghiên cứu", font_size=16, color=VG_PURPLE, weight=BOLD_WEIGHT).move_to([4.78, -1.27, 0])
        sa1 = Line(sr.get_bottom(), sw1.get_top(), stroke_width=1.3, color=VG_GRAY)
        sa2 = Line(sr.get_bottom(), sw2.get_top(), stroke_width=1.3, color=VG_PURPLE)
        c3_g = VGroup(c3b, c3t, c3s, c3p, sr, sw1, sw2, sa1, sa2)

        seq_lbl = VGText("DRW  →  GINSEW  →  CATER", font_size=19, color=VG_GOLD).move_to([0.0, -2.5, 0])

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        # DRW xuất hiện trước và sáng nhất
        self.play(FadeIn(c1_g, shift=UP*0.3), run_time=0.8)
        self.play(c1b.animate.set_stroke(color=VG_BLUE, width=3.5), run_time=0.4)
        # GINSEW và CATER xuất hiện sau
        self.play(FadeIn(c2_g, shift=UP*0.2), FadeIn(c3_g, shift=UP*0.2), run_time=0.8)
        self.play(FadeIn(seq_lbl, shift=UP*0.1), run_time=0.5)
        # Camera zoom vào DRW
        self.play(c1_g.animate.scale(1.08), run_time=0.5)
        self.play(c1_g.animate.scale(1/1.08), run_time=0.4)

        dur_346 = max(2.0, dur_345 * 0.38 - 0.5 - 0.8 - 0.4 - 0.8 - 0.5 - 0.9)
        self.wait(dur_346)
        self.play(FadeOut(sub), FadeOut(c1_g), FadeOut(c2_g), FadeOut(c3_g), FadeOut(seq_lbl), run_time=0.8)
        self.wait(0.2)


        self.play(FadeOut(scene_title), FadeOut(underline), run_time=0.8)
        self.wait(0.3)


def play_part3_drw_34(scene: Scene) -> None:
    DRW34Scene.construct(scene)
