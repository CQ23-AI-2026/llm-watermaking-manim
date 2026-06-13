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
)


BG = "#0B0A08"
PANEL = "#17130F"
BROWN = "#7A4A23"
BROWN_LIGHT = "#B47A3C"
BROWN_DARK = "#3A2416"
BLUE = VG_BLUE
ACCENT = VG_GOLD


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


def label(text, size=24, color=WHITE, weight="NORMAL", **kwargs):
    return VGText(text, font_size=size, color=color, weight=weight, **kwargs)


def panel(width, height, stroke=BROWN_LIGHT, fill=PANEL, opacity=0.94):
    return RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=1.8,
    )


def card(title, subtitle, stroke, width=2.8, height=1.15):
    box = panel(width, height, stroke=stroke)
    title_mob = label(title, 22, stroke, BOLD_WEIGHT).move_to(box.get_center() + UP * 0.22)
    subtitle_mob = label(subtitle, 14, VG_GRAY).move_to(box.get_center() + DOWN * 0.24)
    return VGroup(box, title_mob, subtitle_mob)


def small_model(title, subtitle, stroke=BLUE):
    box = panel(2.25, 0.9, stroke=stroke)
    title_mob = label(title, 19, stroke, BOLD_WEIGHT).move_to(box.get_center() + UP * 0.16)
    sub_mob = label(subtitle, 13, VG_GRAY).move_to(box.get_center() + DOWN * 0.18)
    return VGroup(box, title_mob, sub_mob)


class DRW34Scene(Scene):
    def construct(self):
        self.current_dir = os.path.dirname(__file__)
        self.voice_dir = os.path.join(self.current_dir, "assets", "drw_34")
        self.camera.background_color = BG
        self.add_background_grid()

        title = label(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            LARGE_FONT_SIZE - 6,
            WHITE,
            BOLD_WEIGHT,
        ).move_to(ORIGIN)
        underline = Line(
            LEFT * 4.55,
            RIGHT * 4.55,
            color=ACCENT,
            stroke_width=2,
            stroke_opacity=0.65,
        ).next_to(title, DOWN, buff=0.25)

        intro_dur = self.add_voice("drw_34_title.mp3", "drw_34_0_title.mp3", fallback=3.0)
        self.play(Write(title), Create(underline), run_time=1.1)
        self.wait(max(0.4, intro_dur - 1.1))

        top_title = label(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            LARGE_FONT_SIZE - 10,
            WHITE,
            BOLD_WEIGHT,
        ).to_edge(UP, buff=0.28)
        top_ul = Line(
            LEFT * 4.55,
            RIGHT * 4.55,
            color=ACCENT,
            stroke_width=2,
            stroke_opacity=0.65,
        ).next_to(top_title, DOWN, buff=0.15)
        self.play(Transform(title, top_title), Transform(underline, top_ul), run_time=0.75)

        self.scene_threat(underline)
        self.scene_hidden_signal(underline)
        self.scene_verify(underline)
        self.scene_roadmap(underline)

        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, NumberPlane)])), run_time=0.8)
        self.wait(0.2)

    def add_background_grid(self):
        grid = NumberPlane(
            background_line_style={"stroke_color": "#8B6B4F", "stroke_width": 1, "stroke_opacity": 0.055},
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

    def voice_path(self, *names):
        for name in names:
            path = os.path.join(self.voice_dir, name)
            if os.path.exists(path):
                return path
        return ""

    def add_voice(self, *names, fallback=5.0):
        path = self.voice_path(*names)
        if path:
            self.add_sound(path)
        return _get_audio_duration(path) or fallback

    def scene_threat(self, top_ul):
        dur = self.add_voice("drw_34_1_threat.mp3", fallback=7.0)
        sub = label("Vì sao cần watermark kháng sao chép?", 23, ACCENT, BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        attacker = card("Attacker", "gọi API hàng loạt", VG_ORANGE, width=2.45).move_to(LEFT * 4.3 + DOWN * 0.1)
        api = card("Victim API", "black-box model", BLUE, width=2.45).move_to(LEFT * 1.35 + DOWN * 0.1)
        dataset = card("Dataset", "prompt / response", BROWN_LIGHT, width=2.55).move_to(RIGHT * 1.55 + DOWN * 0.1)
        copy = card("Student", "model bắt chước", VG_GREEN, width=2.45).move_to(RIGHT * 4.45 + DOWN * 0.1)
        nodes = VGroup(attacker, api, dataset, copy)

        arrows = VGroup(
            Arrow(attacker.get_right(), api.get_left(), color=BROWN_LIGHT, buff=0.12, stroke_width=2.0),
            Arrow(api.get_right(), dataset.get_left(), color=BLUE, buff=0.12, stroke_width=2.0),
            Arrow(dataset.get_right(), copy.get_left(), color=BROWN_LIGHT, buff=0.12, stroke_width=2.0),
        )
        line = label(
            "Không cần lấy trọng số: chỉ cần thu thật nhiều output để huấn luyện bản sao.",
            21,
            WHITE,
        ).to_edge(DOWN, buff=0.65)

        group = VGroup(sub, nodes, arrows, line)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(attacker), FadeIn(api), run_time=0.75)
        self.play(Create(arrows[0]), run_time=0.35)
        self.play(FadeIn(dataset), Create(arrows[1]), run_time=0.65)
        self.play(FadeIn(copy), Create(arrows[2]), run_time=0.65)
        self.play(FadeIn(line, shift=UP * 0.1), run_time=0.45)

        dots = VGroup(*[Dot(color=BLUE, radius=0.055).move_to(attacker.get_right()) for _ in range(5)])
        self.add(dots)
        self.play(
            AnimationGroup(
                *[dot.animate.move_to(dataset.get_center() + DOWN * 0.46 + RIGHT * (i - 2) * 0.16) for i, dot in enumerate(dots)],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.play(FadeOut(dots), run_time=0.15)
        self.wait(max(0.6, dur - 4.5))
        self.play(FadeOut(group), run_time=0.65)

    def scene_hidden_signal(self, top_ul):
        dur = self.add_voice("drw_34_2_signal.mp3", fallback=7.0)
        sub = label("Ý tưởng chung: để bản sao học luôn một tín hiệu bí mật", 23, ACCENT, BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        teacher = small_model("Teacher", "model gốc", BLUE).move_to(LEFT * 4.4 + UP * 0.45)
        key = VGroup(
            RegularPolygon(n=6, radius=0.38, color=ACCENT, fill_color=BROWN_DARK, fill_opacity=1.0, stroke_width=2.0),
            label("K", 25, ACCENT, BOLD_WEIGHT),
        ).move_to(LEFT * 4.4 + DOWN * 0.95)
        student = small_model("Student", "học hành vi", VG_GREEN).move_to(RIGHT * 0.1 + DOWN * 0.15)
        verifier = card("Verifier", "kiểm tra thống kê", ACCENT, width=2.55, height=0.95).move_to(RIGHT * 4.15 + DOWN * 0.15)

        behavior = Arrow(teacher.get_right(), student.get_left(), color=BLUE, buff=0.14, stroke_width=2.2)
        watermark = Arrow(key.get_right(), student.get_left() + DOWN * 0.22, color=ACCENT, buff=0.1, stroke_width=2.2)
        check = Arrow(student.get_right(), verifier.get_left(), color=BROWN_LIGHT, buff=0.13, stroke_width=2.0)

        b_lbl = label("task behavior", 15, BLUE).next_to(behavior, UP, buff=0.08)
        w_lbl = label("hidden signal", 15, ACCENT).next_to(watermark, DOWN, buff=0.1)

        note = label(
            "Watermark không nhất thiết nằm trong chữ; nó có thể nằm trong xác suất hoặc hành vi phản hồi.",
            20,
            WHITE,
        ).to_edge(DOWN, buff=0.65)

        group = VGroup(sub, teacher, key, student, verifier, behavior, watermark, check, b_lbl, w_lbl, note)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.45)
        self.play(FadeIn(teacher), FadeIn(key), run_time=0.7)
        self.play(Create(behavior), FadeIn(b_lbl), run_time=0.55)
        self.play(Create(watermark), FadeIn(w_lbl), run_time=0.75)
        self.play(FadeIn(student), run_time=0.55)
        self.play(Create(check), FadeIn(verifier), run_time=0.6)
        self.play(FadeIn(note, shift=UP * 0.1), Indicate(key, color=ACCENT), run_time=0.8)
        self.wait(max(0.7, dur - 4.4))
        self.play(FadeOut(group), run_time=0.65)

    def scene_verify(self, top_ul):
        dur = self.add_voice("drw_34_3_verify.mp3", fallback=7.0)
        sub = label("Mẫu chung của các phương pháp phía sau", 23, ACCENT, BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        prompt = card("Secret prompts", "x có chọn lọc", BROWN_LIGHT, width=2.55, height=0.95).move_to(LEFT * 4.4 + UP * 0.55)
        suspect = small_model("Suspect", "mô hình nghi ngờ", VG_ORANGE).move_to(LEFT * 1.3 + UP * 0.55)
        responses = card("Responses", "output / logits", BLUE, width=2.55, height=0.95).move_to(RIGHT * 1.6 + UP * 0.55)
        detector = card("Detector", "score > τ ?", ACCENT, width=2.35, height=0.95).move_to(RIGHT * 4.45 + UP * 0.55)

        flow = VGroup(
            Arrow(prompt.get_right(), suspect.get_left(), color=BROWN_LIGHT, buff=0.13, stroke_width=2.0),
            Arrow(suspect.get_right(), responses.get_left(), color=BLUE, buff=0.13, stroke_width=2.0),
            Arrow(responses.get_right(), detector.get_left(), color=ACCENT, buff=0.13, stroke_width=2.0),
        )

        formula_box = panel(7.2, 1.15, stroke=ACCENT).move_to(DOWN * 1.0)
        formula = MathTex(r"\text{score}(K, M) \;>\; \tau \quad \Rightarrow \quad \text{copy likely}", font_size=38, color=WHITE).move_to(formula_box)
        note = label("Điểm chung: dùng khóa hoặc bộ kiểm thử bí mật để kéo ra dấu hiệu khó thấy bằng mắt thường.", 19, VG_GRAY).to_edge(DOWN, buff=0.62)

        group = VGroup(sub, prompt, suspect, responses, detector, flow, formula_box, formula, note)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.45)
        self.play(FadeIn(prompt), FadeIn(suspect), Create(flow[0]), run_time=0.75)
        self.play(FadeIn(responses), Create(flow[1]), run_time=0.65)
        self.play(FadeIn(detector), Create(flow[2]), run_time=0.65)
        self.play(FadeIn(formula_box), Write(formula), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
        self.wait(max(0.7, dur - 3.85))
        self.play(FadeOut(group), run_time=0.65)

    def scene_roadmap(self, top_ul):
        dur = self.add_voice("drw_34_4_roadmap.mp3", fallback=7.0)
        sub = label("Roadmap: ba cách thiết kế watermark ở cấp mô hình", 23, ACCENT, BOLD_WEIGHT).next_to(top_ul, DOWN, buff=0.28)

        c1 = card("DRW", "tín hiệu xác suất\nkháng distillation", BLUE, width=3.15, height=1.35).move_to(LEFT * 3.75 + DOWN * 0.1)
        c2 = card("GINSEW", "can thiệp nhẹ\nkhi sinh token", ACCENT, width=3.15, height=1.35).move_to(DOWN * 0.1)
        c3 = card("CATER", "watermark có điều kiện\ntheo ngữ cảnh", VG_PURPLE, width=3.15, height=1.35).move_to(RIGHT * 3.75 + DOWN * 0.1)
        cards = VGroup(c1, c2, c3)

        arrows = VGroup(
            Arrow(c1.get_right(), c2.get_left(), color=BROWN_LIGHT, buff=0.16, stroke_width=1.9),
            Arrow(c2.get_right(), c3.get_left(), color=BROWN_LIGHT, buff=0.16, stroke_width=1.9),
        )

        group = VGroup(sub, cards, arrows)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.45)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.55)
        self.play(Create(arrows[0]), FadeIn(c2, shift=UP * 0.1), run_time=0.65)
        self.play(Create(arrows[1]), FadeIn(c3, shift=UP * 0.1), run_time=0.65)
        self.play(c1[0].animate.set_stroke(BLUE, width=3.2), run_time=0.35)
        self.play(c2[0].animate.set_stroke(ACCENT, width=3.0), run_time=0.35)
        self.play(c3[0].animate.set_stroke(VG_PURPLE, width=3.0), run_time=0.35)
        self.wait(max(0.8, dur - 3.3))
        self.play(FadeOut(group), run_time=0.65)


def play_part3_drw_34(scene: Scene) -> None:
    scene.add_background_grid = DRW34Scene.add_background_grid.__get__(scene, scene.__class__)
    scene.voice_path = DRW34Scene.voice_path.__get__(scene, scene.__class__)
    scene.add_voice = DRW34Scene.add_voice.__get__(scene, scene.__class__)
    scene.scene_threat = DRW34Scene.scene_threat.__get__(scene, scene.__class__)
    scene.scene_hidden_signal = DRW34Scene.scene_hidden_signal.__get__(scene, scene.__class__)
    scene.scene_verify = DRW34Scene.scene_verify.__get__(scene, scene.__class__)
    scene.scene_roadmap = DRW34Scene.scene_roadmap.__get__(scene, scene.__class__)
    DRW34Scene.construct(scene)
