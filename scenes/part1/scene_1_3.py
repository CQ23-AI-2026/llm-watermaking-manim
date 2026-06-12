import os
from manim import *

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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class Scene1_3_Core_Components(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "voice", "voice_1_3.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 15.0
        total_expected_wait = 60.0  # Ước lượng thời gian chờ
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Tiêu đề & Khởi tạo Hàm Watermark()
        title = MarkupText("1.3 HAI THÀNH PHẦN CỐT LÕI CỦA WATERMARKING SCHEME", font="CMU Serif", font_size=26, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)

        wm_box = RoundedRectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.2).move_to(LEFT * 3)
        wm_text = MarkupText("Hàm\nWatermark()", font="CMU Serif", font_size=24).move_to(wm_box)
        wm_group = VGroup(wm_box, wm_text)

        base_model = MarkupText("Model Gốc\n(Base Model)", font="CMU Serif", font_size=20, justify=True).move_to(LEFT * 6)
        arrow_in = Arrow(base_model.get_right(), wm_box.get_left(), buff=0.1)

        wm_model = MarkupText("Watermarked\nModel (M^)", font="CMU Serif", font_size=20, color=GREEN, justify=True).move_to(ORIGIN + UP * 1.5)
        arrow_out1 = Arrow(wm_box.get_top() + RIGHT * 0.5, wm_model.get_left(), buff=0.1)

        det_key = MarkupText("Detection\nKey (k)", font="CMU Serif", font_size=20, color=YELLOW, justify=True).move_to(ORIGIN + DOWN * 1.5)
        arrow_out2 = Arrow(wm_box.get_bottom() + RIGHT * 0.5, det_key.get_left(), buff=0.1)

        self.play(FadeIn(base_model, shift=RIGHT*0.2), run_time=1.0)
        self.play(Create(arrow_in), FadeIn(wm_group, shift=RIGHT*0.2), run_time=1.5)
        self.play(
            Create(arrow_out1), FadeIn(wm_model, shift=RIGHT*0.2),
            Create(arrow_out2), FadeIn(det_key, shift=RIGHT*0.2),
            run_time=2.0
        )
        synced_wait(20.0)

        # Giai đoạn 2: Quá trình sinh văn bản (Trung gian)
        sus_text = MarkupText("Văn bản\nnghi vấn (y)", font="CMU Serif", font_size=20, color=WHITE, justify=True).move_to(RIGHT * 3 + UP * 1.5)
        arrow_gen = Arrow(wm_model.get_right(), sus_text.get_left(), buff=0.1)

        self.play(Create(arrow_gen), FadeIn(sus_text, shift=RIGHT*0.2), run_time=1.5)
        synced_wait(5.0)

        # Giai đoạn 3: Hàm Detect() - Quá trình kiểm tra
        det_box = RoundedRectangle(width=2.5, height=1.5, color=RED, fill_opacity=0.2).move_to(RIGHT * 3 + DOWN * 1.5)
        det_text = MarkupText("Hàm\nDetect()", font="CMU Serif", font_size=24).move_to(det_box)
        det_group = VGroup(det_box, det_text)

        arrow_det1 = Arrow(sus_text.get_bottom(), det_box.get_top(), buff=0.1)
        arrow_det2 = Arrow(det_key.get_right(), det_box.get_left(), buff=0.1)

        self.play(FadeIn(det_group, shift=UP*0.2), run_time=1.0)
        self.play(Create(arrow_det1), Create(arrow_det2), run_time=1.5)
        synced_wait(10.0)

        res_1 = MarkupText("1 (Là AI)", font="CMU Serif", font_size=20, color=GREEN).move_to(RIGHT * 5.8 + DOWN * 0.8)
        res_0 = MarkupText("0 (Không có\nbằng chứng)", font="CMU Serif", font_size=20, color=GRAY).move_to(RIGHT * 5.8 + DOWN * 2.2)

        arrow_res1 = Arrow(det_box.get_right(), res_1.get_left(), buff=0.1)
        arrow_res2 = Arrow(det_box.get_right(), res_0.get_left(), buff=0.1)

        self.play(Create(arrow_res1), FadeIn(res_1, shift=RIGHT*0.2), run_time=1.0)
        self.play(Create(arrow_res2), FadeIn(res_0, shift=RIGHT*0.2), run_time=1.0)
        synced_wait(8.0)

        # Giai đoạn 4: Đóng khung và Nhấn mạnh
        left_part = VGroup(base_model, wm_group, wm_model)
        left_rect = DashedVMobject(SurroundingRectangle(left_part, color=BLUE, buff=0.3))
        left_label = MarkupText("Quá trình tạo Watermark", font="CMU Serif", font_size=16, color=BLUE).next_to(left_rect, UP, buff=0.1)

        right_part = VGroup(sus_text, det_group, res_1, res_0)
        right_rect = DashedVMobject(SurroundingRectangle(right_part, color=RED, buff=0.3))
        right_label = MarkupText("Quá trình Phát hiện", font="CMU Serif", font_size=16, color=RED).next_to(right_rect, UP, buff=0.1)

        self.play(Create(left_rect), Write(left_label), run_time=1.0)
        self.play(Create(right_rect), Write(right_label), run_time=1.0)
        synced_wait(12.0)

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(2.0)
            
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_part1_scene_1_3(scene: Scene) -> None:
    Scene1_3_Core_Components.construct(scene)
