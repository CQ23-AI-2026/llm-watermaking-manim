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


class DRWScene(Scene):
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
        voice_351   = os.path.join(ext, "extraction_3_5_1.mp3")
        voice_352   = os.path.join(ext, "extraction_3_5_2.mp3")
        voice_353   = os.path.join(ext, "extraction_3_5_3.mp3")
        voice_354   = os.path.join(ext, "extraction_3_5_4.mp3")
        voice_355   = os.path.join(ext, "extraction_3_5_5.mp3")
        voice_356   = os.path.join(ext, "extraction_3_5_6.mp3")

        dur_intro = _get_audio_duration(voice_intro) or 4.0
        dur_341 = _get_audio_duration(voice_341) or 44.0
        dur_342 = _get_audio_duration(voice_342) or 34.0
        dur_343 = _get_audio_duration(voice_343) or 42.0
        dur_344 = _get_audio_duration(voice_344) or 25.0
        dur_345 = _get_audio_duration(voice_345) or 38.0
        dur_351 = _get_audio_duration(voice_351) or 44.0
        dur_352 = _get_audio_duration(voice_352) or 48.0
        dur_353 = _get_audio_duration(voice_353) or 54.0
        dur_354 = _get_audio_duration(voice_354) or 50.0
        dur_355 = _get_audio_duration(voice_355) or 62.0
        dur_356 = _get_audio_duration(voice_356) or 50.0

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

        # =========================================================================
        # CẢNH 3.5.1 — DRW LÀ GÌ?
        # =========================================================================
        if os.path.exists(voice_351):
            self.add_sound(voice_351)

        sub = VGText("DRW — Distillation-Resistant Watermarking", font_size=22, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Tiêu đề mô tả ngắn gọn
        drw_prot = VGText("Protects against distillation", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to([0.0, 1.3, 0])

        # Sơ đồ: Input Text → Victim NLP Model → Prediction Probabilities
        in_b  = RoundedRectangle(corner_radius=0.07, width=2.4, height=0.82, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.5).move_to([-3.5, 0.3, 0])
        in_l  = VGText("Input Text",  font_size=18, color=WHITE).move_to(in_b.get_center())
        nlp_b = RoundedRectangle(corner_radius=0.07, width=2.9, height=0.82, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([0.0, 0.3, 0])
        nlp_l = VGText("Victim NLP Model", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(nlp_b.get_center())
        pr_b  = RoundedRectangle(corner_radius=0.07, width=2.8, height=0.82, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.5).move_to([3.5, 0.3, 0])
        pr_l  = VGText("Prediction\nProbabilities", font_size=16, color=VG_GRAY).move_to(pr_b.get_center())
        a_in  = Arrow(in_b.get_right(),  nlp_b.get_left(),  buff=0.08, color=VG_GRAY, stroke_width=2.0)
        a_nlp = Arrow(nlp_b.get_right(), pr_b.get_left(),   buff=0.08, color=VG_BLUE, stroke_width=2.0)

        # Bar chart: Positive: 0.72, Neutral: 0.19, Negative: 0.09 (Centered and enlarged)
        bb = -2.2   # bottom of bars
        bs = 1.8    # bar scale (increased from 1.2 to 1.8)
        bar_w = 0.75  # bar width (increased from 0.55 to 0.75)
        bar_xs_351 = [-1.2, 0.0, 1.2]  # centered horizontally
        
        bc_pos = Rectangle(width=bar_w, height=0.72*bs, fill_color=VG_GREEN, fill_opacity=0.6, stroke_color=VG_GREEN, stroke_width=1.5).move_to([bar_xs_351[0], bb + 0.72*bs/2, 0])
        bc_neu = Rectangle(width=bar_w, height=0.19*bs, fill_color=VG_BLUE,  fill_opacity=0.6, stroke_color=VG_BLUE,  stroke_width=1.5).move_to([bar_xs_351[1], bb + 0.19*bs/2, 0])
        bc_neg = Rectangle(width=bar_w, height=0.09*bs, fill_color=VG_RED,   fill_opacity=0.6, stroke_color=VG_RED,   stroke_width=1.5).move_to([bar_xs_351[2], bb + 0.09*bs/2, 0])
        
        bl_pos = VGText("Pos\n0.72", font_size=15, color=VG_GREEN).move_to([bar_xs_351[0], bb - 0.35, 0])
        bl_neu = VGText("Neu\n0.19", font_size=15, color=WHITE).move_to([bar_xs_351[1], bb - 0.35, 0])
        bl_neg = VGText("Neg\n0.09", font_size=15, color=WHITE).move_to([bar_xs_351[2], bb - 0.35, 0])
        bar_chart = VGroup(bc_pos, bc_neu, bc_neg, bl_pos, bl_neu, bl_neg)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        # Chữ mô tả xuất hiện
        self.play(FadeIn(drw_prot, shift=UP*0.15), run_time=0.8)
        # Sơ đồ hiện từng bước
        self.play(FadeIn(VGroup(in_b, in_l), shift=DOWN*0.2), run_time=0.6)
        self.play(Create(a_in), FadeIn(VGroup(nlp_b, nlp_l), shift=DOWN*0.2), run_time=0.6)
        self.play(Create(a_nlp), FadeIn(VGroup(pr_b, pr_l), shift=DOWN*0.2), run_time=0.6)
        # Biểu đồ xác suất xuất hiện dạng bar chart
        self.play(FadeIn(bar_chart, shift=UP*0.1), run_time=0.6)

        scene_351 = VGroup(drw_prot, in_b, in_l, nlp_b, nlp_l, pr_b, pr_l, a_in, a_nlp, bar_chart)
        anim_t = 0.5 + 0.8 + 0.7 + 0.6*4 + 0.6
        self.wait(max(1.0, dur_351 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_351), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.2 — DRW NHÚNG WATERMARK BẰNG KHÓA BÍ MẬT
        # =========================================================================
        if os.path.exists(voice_352):
            self.add_sound(voice_352)

        sub = VGText("Nhúng Watermark bằng Khóa Bí mật", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Secret Key (trái)
        sk_b  = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.0).move_to([-4.0, 0.5, 0])
        sk_l  = VGText("Secret Key", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(sk_b.get_center() + UP*0.22)
        sk_kc = Annulus(
            inner_radius=0.07, outer_radius=0.14,
            color=VG_GOLD, fill_opacity=0.6, stroke_width=1.8
        )
        sk_collar = Rectangle(
            width=0.03, height=0.10,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(sk_kc, RIGHT, buff=-0.04)
        sk_kr = Rectangle(
            width=0.50, height=0.06,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(sk_kc, RIGHT, buff=-0.03)
        sk_kt1 = Rectangle(
            width=0.05, height=0.10,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(sk_kr, DOWN, buff=-0.02).align_to(sk_kr, RIGHT)
        sk_kt2 = Rectangle(
            width=0.05, height=0.06,
            color=VG_GOLD, fill_color=VG_GOLD, fill_opacity=1.0
        ).next_to(sk_kr, DOWN, buff=-0.02).align_to(sk_kr, RIGHT).shift(LEFT * 0.10)
        sk_key = VGroup(sk_kc, sk_collar, sk_kr, sk_kt1, sk_kt2).move_to(sk_b.get_center() + DOWN*0.2)
        sk_g  = VGroup(sk_b, sk_l, sk_key)

        # Watermark Pattern (giữa)
        wp_b  = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=2.0).move_to([0.0, 0.5, 0])
        wp_l  = VGText("Watermark\nPattern", font_size=19, color=VG_PURPLE, weight=BOLD_WEIGHT).move_to(wp_b.get_center() + UP*0.1)
        # Các điểm sáng xếp thành pattern
        wp_ds = VGroup(*[Dot(color=VG_GOLD, radius=0.055, fill_opacity=0.75).move_to([0.0 + 0.22*(i-1.5), 0.2, 0]) for i in range(4)])
        wp_g  = VGroup(wp_b, wp_l, wp_ds)

        # Modified Probabilities (phải)
        mp_b  = RoundedRectangle(corner_radius=0.1, width=3.5, height=2.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([4.2, 0.0, 0])
        mp_tt = VGText("Modified Probabilities", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(mp_b.get_top(), DOWN, buff=0.2)
        mp_sp = Line(LEFT*1.55, RIGHT*1.55, color=VG_BLUE, stroke_width=0.8, stroke_opacity=0.3).next_to(mp_tt, DOWN, buff=0.15)
        b_lbl = VGText("Before:", font_size=15, color=VG_GRAY).move_to(mp_b.get_center() + UP*0.42 + LEFT*0.8)
        b_val = VGText("[0.720,  0.190,  0.090]", font_size=15, color=WHITE).move_to(mp_b.get_center() + UP*0.12)
        a_lbl = VGText("After:",  font_size=15, color=VG_GOLD).move_to(mp_b.get_center() + DOWN*0.32 + LEFT*0.88)
        a_val = VGText("[0.721,  0.187,  0.092]", font_size=15, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(mp_b.get_center() + DOWN*0.62)
        mp_g  = VGroup(mp_b, mp_tt, mp_sp, b_lbl, b_val, a_lbl, a_val)

        arr_sk = Arrow(sk_b.get_right(), wp_b.get_left(), buff=0.08, color=VG_GOLD,   stroke_width=2.0)
        arr_wp = Arrow(wp_b.get_right(), mp_b.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=2.0)

        note = VGText("Prediction label unchanged — still Positive", font_size=16, color=VG_GREEN).move_to([0.5, -2.15, 0])

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        self.play(FadeIn(sk_g, scale=0.85), run_time=0.8)
        # Chìa khóa quay nhẹ → tạo các điểm sáng
        self.play(sk_key.animate.rotate(PI/6), run_time=0.45)
        self.play(sk_key.animate.rotate(-PI/6), run_time=0.35)
        # Sparks bay sang pattern
        sparks = VGroup(*[Dot(color=VG_GOLD, radius=0.06, fill_opacity=0.9).move_to(sk_b.get_right() + UP*(0.1 - 0.1*i)) for i in range(3)])
        self.add(sparks)
        self.play(AnimationGroup(*[s.animate(run_time=0.5, rate_func=linear).move_to(wp_b.get_left()) for s in sparks], lag_ratio=0.2))
        self.play(FadeOut(sparks), run_time=0.1)
        # Các điểm sáng xếp thành pattern
        self.play(Create(arr_sk), FadeIn(wp_g, scale=0.9), run_time=0.8)
        # Pattern đi vào vector xác suất
        self.play(Create(arr_wp), FadeIn(mp_g, shift=LEFT*0.2), run_time=0.8)
        self.play(FadeIn(note, shift=UP*0.1), run_time=0.6)

        scene_352 = VGroup(sk_g, wp_g, mp_g, arr_sk, arr_wp, note)
        anim_t = 0.5 + 0.8 + 0.8 + 0.7 + 0.8 + 0.8 + 0.6
        self.wait(max(1.0, dur_352 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_352), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.3 — SOFT LABELS: VÌ SAO STUDENT HỌC ĐƯỢC WATERMARK?
        # =========================================================================
        if os.path.exists(voice_353):
            self.add_sound(voice_353)

        sub = VGText("Soft Labels  →  Watermark Transfer", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Bên trái: Hard Label — một ô duy nhất
        hl_b  = RoundedRectangle(corner_radius=0.1, width=2.8, height=3.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.8).move_to([-3.5, 0.0, 0])
        hl_t  = VGText("Hard Label",  font_size=20, color=VG_GRAY, weight=BOLD_WEIGHT).next_to(hl_b.get_top(), DOWN, buff=0.25)
        hl_sp = Line(LEFT*1.2, RIGHT*1.2, color=VG_GRAY, stroke_width=0.8, stroke_opacity=0.4).next_to(hl_t, DOWN, buff=0.15)
        hl_v  = VGText("Positive", font_size=28, color=WHITE, weight=BOLD_WEIGHT).move_to(hl_b.get_center() + DOWN*0.1)
        hl_n  = VGText("one answer", font_size=15, color=VG_GRAY).next_to(hl_b, DOWN, buff=0.22)
        hl_g  = VGroup(hl_b, hl_t, hl_sp, hl_v, hl_n)

        # Bên phải: Soft Label — vector nhiều giá trị
        sl_b  = RoundedRectangle(corner_radius=0.1, width=3.2, height=3.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.0).move_to([1.0, 0.0, 0])
        sl_t  = VGText("Soft Label",  font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(sl_b.get_top(), DOWN, buff=0.25)
        sl_sp = Line(LEFT*1.4, RIGHT*1.4, color=VG_GOLD, stroke_width=0.8, stroke_opacity=0.4).next_to(sl_t, DOWN, buff=0.15)
        sv1   = VGText("Positive :  0.72  ★", font_size=17, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(sl_sp, DOWN, buff=0.22).align_to(sl_b, LEFT).shift(RIGHT*0.28)
        sv2   = VGText("Neutral  :  0.19",    font_size=17, color=WHITE).next_to(sv1, DOWN, buff=0.18).align_to(sv1, LEFT)
        sv3   = VGText("Negative :  0.09",    font_size=17, color=WHITE).next_to(sv2, DOWN, buff=0.18).align_to(sv1, LEFT)
        sl_n  = VGText("probability pattern", font_size=15, color=VG_GOLD).next_to(sl_b, DOWN, buff=0.22)
        sl_g  = VGroup(sl_b, sl_t, sl_sp, sv1, sv2, sv3, sl_n)

        # Các chấm watermark nằm trên soft label
        wm_d353 = VGroup(*[Dot(color=VG_GOLD, radius=0.055, fill_opacity=0.8).move_to([0.78 + 0.26*i, -0.38, 0]) for i in range(4)])

        # Student Model (phải)
        sm_b  = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.92, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.0).move_to([5.0, 0.0, 0])
        sm_l  = VGText("Student\nModel", font_size=18, color=VG_RED, weight=BOLD_WEIGHT).move_to(sm_b.get_center())

        # Hard label: mũi tên đơn giản (thin)
        arr_hl = Arrow(hl_b.get_right() + UP*0.2, sm_b.get_left() + UP*0.2, buff=0.08, color=VG_GRAY, stroke_width=1.5)
        # Soft label: mũi tên dày hơn, kèm watermark — soft label chảy vào student
        arr_sl = Arrow(sl_b.get_right(), sm_b.get_left() + DOWN*0.2, buff=0.08, color=VG_GOLD, stroke_width=2.5)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        # Hard label hiện đơn giản, một ô
        self.play(FadeIn(hl_g, shift=RIGHT*0.2), run_time=0.8)
        # Soft label hiện thành vector nhiều giá trị
        self.play(FadeIn(sl_g, shift=LEFT*0.2), run_time=0.8)
        # Highlight "more information" — chấm watermark xuất hiện trên soft label
        self.play(FadeIn(wm_d353, scale=0.8), run_time=0.6)
        self.play(FadeIn(VGroup(sm_b, sm_l), shift=LEFT*0.2), run_time=0.7)
        self.play(Create(arr_hl), run_time=0.5)
        self.play(Create(arr_sl), run_time=0.6)

        # Soft label chảy vào student model
        sl_pts = VGroup(*[Dot(color=VG_GOLD, radius=0.065, fill_opacity=0.9).move_to(sl_b.get_right()) for _ in range(4)])
        self.add(sl_pts)
        self.play(AnimationGroup(*[p.animate(run_time=1.0, rate_func=linear).move_to(sm_b.get_center()) for p in sl_pts], lag_ratio=0.2))
        self.play(FadeOut(sl_pts), sm_b.animate.set_stroke(color=VG_GOLD), run_time=0.4)

        scene_353 = VGroup(hl_g, sl_g, wm_d353, sm_b, sm_l, arr_hl, arr_sl)
        anim_t = 0.5 + 0.8*2 + 0.6 + 0.7 + 1.1 + 1.4
        self.wait(max(1.0, dur_353 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_353), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.4 — PROBING: KIỂM TRA MÔ HÌNH TÌNH NGHI + ĐỒNG HỒ ĐO
        # =========================================================================
        if os.path.exists(voice_354):
            self.add_sound(voice_354)

        sub = VGText("Ownership Verification — Probing", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Owner → Probing Queries → Suspect Model → Outputs
        ow_b = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=2.0).move_to([-5.0, 1.5, 0])
        ow_l = VGText("Owner", font_size=20, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(ow_b.get_center())
        ow_g = VGroup(ow_b, ow_l)

        sq_b  = RoundedRectangle(corner_radius=0.1, width=2.8, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.0).move_to([-1.0, 1.5, 0])
        sq_lt = VGText("Suspect Model",       font_size=20, color=VG_RED, weight=BOLD_WEIGHT).move_to(sq_b.get_center() + UP*0.2)
        sq_ls = VGText("(Mô hình nghi ngờ)", font_size=13, color=VG_GRAY).move_to(sq_b.get_center() + DOWN*0.22)
        sq_g  = VGroup(sq_b, sq_lt, sq_ls)

        out_b = RoundedRectangle(corner_radius=0.08, width=1.8, height=0.72, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.5).move_to([2.5, 1.5, 0])
        out_l = VGText("Outputs", font_size=17, color=VG_GRAY).move_to(out_b.get_center())
        out_g = VGroup(out_b, out_l)

        arr_pq = Arrow(ow_b.get_right(), sq_b.get_left(), buff=0.08, color=VG_GRAY, stroke_width=2.0)
        pq_l   = VGText("Probing Queries", font_size=15, color=VG_GRAY).next_to(arr_pq, UP, buff=0.1)
        arr_so = Arrow(sq_b.get_right(), out_b.get_left(), buff=0.08, color=VG_GRAY, stroke_width=1.8)

        # Watermark Detector + đồng hồ đo
        det_b = RoundedRectangle(corner_radius=0.1, width=5.2, height=2.7, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD, stroke_width=2.2).move_to([0.5, -1.2, 0])
        det_t = VGText("Watermark Detector", font_size=21, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(det_b.get_top(), DOWN, buff=0.22)

        # Đồng hồ đo: semicircle + zones màu + kim
        gc = det_b.get_center() + UP*0.12
        gauge_bg  = Arc(radius=0.75, start_angle=0, angle=PI, color="#333333", stroke_width=6).move_to(gc)
        gauge_low = Arc(radius=0.75, start_angle=PI*2/3, angle=PI/3, color=VG_RED,   stroke_width=9).move_to(gc)
        gauge_mid = Arc(radius=0.75, start_angle=PI/3,   angle=PI/3, color=VG_GOLD,  stroke_width=9).move_to(gc)
        gauge_hi  = Arc(radius=0.75, start_angle=0,      angle=PI/3, color=VG_GREEN, stroke_width=9).move_to(gc)

        g_low_l = VGText("Low\nNot enough\nevidence", font_size=11, color=VG_RED).move_to(gc + LEFT*1.08 + UP*0.1)
        g_hi_l  = VGText("High\nStrong\nevidence",    font_size=11, color=VG_GREEN).move_to(gc + RIGHT*1.08 + UP*0.1)

        # Kim — bắt đầu trỏ sang trái (LOW zone, 180°)
        needle_len = 0.65
        needle = Line(gc, gc + LEFT * needle_len, color=WHITE, stroke_width=3.0)
        needle_dot = Circle(radius=0.065, color=WHITE, fill_opacity=1.0, stroke_width=0).move_to(gc)

        score_l = VGText("Watermark Score", font_size=15, color=VG_GRAY).move_to(gc + DOWN*0.72)
        score_v = VGText("0.91 — Strong evidence of distillation", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(score_l, DOWN, buff=0.12)

        gauge_g = VGroup(gauge_bg, gauge_low, gauge_mid, gauge_hi, g_low_l, g_hi_l, needle, needle_dot, score_l)

        arr_od = Arrow(ow_b.get_bottom(), det_b.get_top() + LEFT*1.3,  buff=0.08, color=VG_BLUE, stroke_width=1.8)
        arr_xd = Arrow(out_b.get_bottom(), det_b.get_top() + RIGHT*0.9, buff=0.08, color=VG_GRAY, stroke_width=1.8)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        self.play(FadeIn(ow_g, shift=DOWN*0.2), FadeIn(sq_g, shift=DOWN*0.2), run_time=1.0)
        self.play(Create(arr_pq), FadeIn(pq_l), run_time=0.6)
        self.play(Create(arr_so), FadeIn(out_g, shift=LEFT*0.1), run_time=0.6)
        self.play(Create(arr_od), Create(arr_xd), FadeIn(det_b), FadeIn(det_t), run_time=1.0)
        self.play(FadeIn(gauge_g), run_time=0.8)

        # Kim đồng hồ tăng lên — từ LOW (180°) sang HIGH (~20°)
        # Rotate -160° = -PI*0.89 about gc
        self.play(Rotate(needle, angle=-PI * 0.88, about_point=gc), run_time=1.8)
        self.play(FadeIn(score_v, shift=UP*0.1), run_time=0.6)

        scene_354 = VGroup(ow_g, sq_g, out_g, arr_pq, pq_l, arr_so, det_b, det_t, gauge_g, arr_od, arr_xd, score_v)
        anim_t = 0.5 + 1.0 + 1.2 + 1.0 + 0.8 + 1.8 + 0.6
        self.wait(max(1.0, dur_354 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_354), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.5 — ĐIỂM MẠNH VÀ GIỚI HẠN + THANH TRƯỢT
        # =========================================================================
        if os.path.exists(voice_355):
            self.add_sound(voice_355)

        sub = VGText("DRW — Strengths & Limitations", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Bên trái: Strengths với dấu check
        pr_b  = RoundedRectangle(corner_radius=0.1, width=4.0, height=3.5, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0).move_to([-2.5, -0.4, 0])
        pr_t  = VGText("✓  Strengths", font_size=22, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(pr_b.get_top(), DOWN, buff=0.28)
        p1 = VGText("• Invisible",                  font_size=20, color=WHITE).next_to(pr_t, DOWN, buff=0.32).align_to(pr_b, LEFT).shift(RIGHT*0.35)
        p2 = VGText("• Secret-key based",            font_size=20, color=WHITE).next_to(p1, DOWN, buff=0.22).align_to(p1, LEFT)
        p3 = VGText("• Transfers via distillation",  font_size=20, color=WHITE).next_to(p2, DOWN, buff=0.22).align_to(p1, LEFT)
        pr_g  = VGroup(pr_b, pr_t, p1, p2, p3)

        # Bên phải: Limitations với dấu cảnh báo
        co_b  = RoundedRectangle(corner_radius=0.1, width=4.0, height=3.5, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=2.0).move_to([2.5, -0.4, 0])
        co_t  = VGText("⚠  Limitations", font_size=22, color=VG_RED, weight=BOLD_WEIGHT).next_to(co_b.get_top(), DOWN, buff=0.28)
        c1 = VGText("• Weak if hard labels only",    font_size=20, color=WHITE).next_to(co_t, DOWN, buff=0.32).align_to(co_b, LEFT).shift(RIGHT*0.35)
        c2 = VGText("• Diluted by mixed data",       font_size=20, color=WHITE).next_to(c1, DOWN, buff=0.22).align_to(c1, LEFT)
        c3 = VGText("• May degrade if too strong",   font_size=20, color=WHITE).next_to(c2, DOWN, buff=0.22).align_to(c1, LEFT)
        co_g  = VGroup(co_b, co_t, c1, c2, c3)

        # Cân bằng ở giữa: thanh trượt Quality ↔ Detectability
        sl_tr = Line(LEFT*2.1, RIGHT*2.1, color=VG_GRAY, stroke_width=3.5).move_to([0.0, -2.25, 0])
        sl_kn = Circle(radius=0.16, color=VG_GOLD, fill_opacity=1.0, stroke_width=0).move_to([0.0, -2.25, 0])
        sl_ql = VGText("Quality",       font_size=16, color=VG_GREEN).next_to(sl_tr, LEFT,  buff=0.18)
        sl_dt = VGText("Detectability", font_size=16, color=VG_RED).next_to(sl_tr, RIGHT, buff=0.18)
        sl_cap= VGText("Quality  ↔  Detectability", font_size=18, color=VG_GOLD).next_to(sl_tr, DOWN, buff=0.3)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        self.play(FadeIn(pr_g, shift=RIGHT*0.2), FadeIn(co_g, shift=LEFT*0.2), run_time=1.2)
        self.play(Create(sl_tr), FadeIn(sl_kn), FadeIn(sl_ql), FadeIn(sl_dt), FadeIn(sl_cap), run_time=0.8)
        # Thanh trượt: watermark mạnh → detectability tăng nhưng quality giảm
        self.play(sl_kn.animate.shift(RIGHT*1.5), run_time=1.0)
        self.play(sl_kn.animate.shift(LEFT*3.0), run_time=1.0)
        # Quay về trung tâm
        self.play(sl_kn.animate.shift(RIGHT*1.5), run_time=0.6)

        scene_355 = VGroup(pr_g, co_g, sl_tr, sl_kn, sl_ql, sl_dt, sl_cap)
        anim_t = 0.5 + 1.2 + 0.8 + 2.6
        self.wait(max(1.0, dur_355 - anim_t))
        self.play(FadeOut(sub), FadeOut(scene_355), run_time=0.8)
        self.wait(0.2)

        # =========================================================================
        # CẢNH 3.5.6 — TỔNG KẾT DRW VÀ DẪN SANG CATER
        # =========================================================================
        if os.path.exists(voice_356):
            self.add_sound(voice_356)

        sub = VGText("Tổng kết DRW", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        # Tóm tắt pipeline DRW bằng 4 icon — lần lượt sáng lên
        s1 = RoundedRectangle(corner_radius=0.08, width=2.5, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GOLD,   stroke_width=2.0).move_to([-5.0, 1.2, 0])
        s2 = RoundedRectangle(corner_radius=0.08, width=2.5, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=2.0).move_to([-1.8, 1.2, 0])
        s3 = RoundedRectangle(corner_radius=0.08, width=2.5, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED,    stroke_width=2.0).move_to([1.4, 1.2, 0])
        s4 = RoundedRectangle(corner_radius=0.08, width=2.5, height=0.85, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN,  stroke_width=2.2).move_to([4.6, 1.2, 0])

        s1_l = VGText("Secret Key",          font_size=17, color=VG_GOLD,   weight=BOLD_WEIGHT).move_to(s1.get_center())
        s2_l = VGText("Probability\nPattern", font_size=16, color=VG_PURPLE).move_to(s2.get_center())
        s3_l = VGText("Distilled\nStudent",   font_size=16, color=VG_RED).move_to(s3.get_center())
        s4_l = VGText("Watermark\nDetection", font_size=16, color=VG_GREEN,  weight=BOLD_WEIGHT).move_to(s4.get_center())

        a12 = Arrow(s1.get_right(), s2.get_left(), buff=0.08, color=VG_GOLD,   stroke_width=2.0)
        a23 = Arrow(s2.get_right(), s3.get_left(), buff=0.08, color=VG_PURPLE, stroke_width=2.0)
        a34 = Arrow(s3.get_right(), s4.get_left(), buff=0.08, color=VG_GREEN,  stroke_width=2.0)

        pipeline_356 = VGroup(s1, s1_l, s2, s2_l, s3, s3_l, s4, s4_l, a12, a23, a34)

        # Probability vector biến thành các lựa chọn từ đồng nghĩa
        from_lbl = VGText("From probabilities...", font_size=18, color=VG_GRAY).move_to([-2.2, -0.2, 0])

        # Ví dụ: big / large / huge — "large" được highlight
        syn_big      = VGText("big",      font_size=21, color=VG_GRAY).move_to([-3.8, -0.9, 0])
        syn_large    = VGText("large",    font_size=21, color=VG_GOLD, weight=BOLD_WEIGHT).move_to([-2.5, -0.9, 0])
        syn_huge     = VGText("huge",     font_size=21, color=VG_GRAY).move_to([-1.3, -0.9, 0])
        # start / begin / initiate — "begin" được highlight
        syn_start    = VGText("start",    font_size=21, color=VG_GRAY).move_to([-3.8, -1.55, 0])
        syn_begin    = VGText("begin",    font_size=21, color=VG_GOLD, weight=BOLD_WEIGHT).move_to([-2.5, -1.55, 0])
        syn_initiate = VGText("initiate", font_size=21, color=VG_GRAY).move_to([-0.9, -1.55, 0])
        syns_g = VGroup(syn_big, syn_large, syn_huge, syn_start, syn_begin, syn_initiate)

        to_lbl = VGText("...to conditional word choices", font_size=18, color=VG_GRAY).move_to([-1.8, -2.2, 0])

        # Card CATER
        ct_b  = RoundedRectangle(corner_radius=0.1, width=4.0, height=2.3, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_PURPLE, stroke_width=2.2).move_to([3.8, -1.1, 0])
        ct_t  = VGText("CATER", font_size=30, color=VG_PURPLE, weight=BOLD_WEIGHT).next_to(ct_b.get_top(), DOWN, buff=0.28)
        ct_s  = VGText("Conditional Watermarking", font_size=17, color=WHITE).next_to(ct_t, DOWN, buff=0.2)
        ct_n  = VGText("Next: CATER", font_size=19, color=VG_PURPLE).next_to(ct_s, DOWN, buff=0.25)
        ct_g  = VGroup(ct_b, ct_t, ct_s, ct_n)

        self.play(FadeIn(sub, shift=DOWN*0.2), run_time=0.5)
        # 4 icon lần lượt sáng lên theo voice
        self.play(FadeIn(VGroup(s1, s1_l), shift=DOWN*0.2), run_time=0.6)
        self.play(Create(a12), FadeIn(VGroup(s2, s2_l)), run_time=0.6)
        self.play(Create(a23), FadeIn(VGroup(s3, s3_l)), run_time=0.6)
        self.play(Create(a34), FadeIn(VGroup(s4, s4_l)), run_time=0.6)

        # Probability vector biến thành synonym words
        self.play(FadeIn(from_lbl, shift=UP*0.1), run_time=0.6)
        self.play(FadeIn(syns_g, shift=UP*0.1), run_time=0.8)
        self.play(FadeIn(to_lbl, shift=UP*0.1), run_time=0.6)

        # Hiển thị CATER card
        self.play(FadeIn(ct_g, shift=LEFT*0.3), run_time=0.8)

        all_356 = VGroup(pipeline_356, from_lbl, syns_g, to_lbl, ct_g)
        anim_t = 0.5 + 0.6*4 + 0.6 + 0.8 + 0.6 + 0.8
        self.wait(max(1.0, dur_356 - anim_t))

        # Fade out tất cả
        self.play(
            FadeOut(sub), FadeOut(all_356),
            FadeOut(scene_title), FadeOut(underline),
            run_time=1.0
        )
        self.wait(0.5)


def play_part3_drw(scene: Scene) -> None:
    DRWScene.construct(scene)
