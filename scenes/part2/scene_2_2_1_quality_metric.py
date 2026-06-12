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

class Scene2_2_1_Quality_Metric(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_2_1.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 18.0 # Tổng thời gian chạy các lệnh play()
        total_expected_wait = 115.0 # Tổng thời gian các lệnh synced_wait()
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề và Định nghĩa
        title = MarkupText('1. QUALITY (CHẤT LƯỢNG)', font="CMU Serif", font_size=42, weight="BOLD", color="#F4D160")
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        synced_wait(13.0) # "Để đánh giá hiệu suất... tức Chất lượng."
        
        definition = MarkupText('Mức độ duy trì đặc tính gốc của mô hình', font="CMU Serif", font_size=32, color=WHITE)
        definition.next_to(title, DOWN, buff=0.3)
        
        self.play(FadeIn(definition, shift=UP*0.2), run_time=1.0)
        synced_wait(10.0) # "Về mặt định nghĩa... mô hình ban đầu."

        # Bước 2: Trực quan hóa Phân phối & Độ biến dạng
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 0.5, 0.1],
            x_length=6,
            y_length=4,
            axis_config={"include_ticks": False, "include_tip": False}
        ).shift(LEFT * 2 + DOWN * 1.2)

        def gaussian(x, mu, sigma):
            return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma)**2)

        curve_M = axes.plot(lambda x: gaussian(x, -0.2, 1.0), color="#58A6FF") # Blue
        curve_M_hat = axes.plot(lambda x: gaussian(x, 0.2, 1.0), color="#F0A050") # Orange

        label_M = MarkupText("<i>M</i>", color="#58A6FF", font_size=36, font="CMU Serif").next_to(curve_M, UP, buff=0.1).shift(LEFT*0.5)
        label_M_hat = MarkupText("<i>M\u0302</i>", color="#F0A050", font_size=36, font="CMU Serif").next_to(curve_M_hat, UP, buff=0.1).shift(RIGHT*0.5)

        arrow_distortion = DoubleArrow(
            start=axes.c2p(-0.2, gaussian(-0.2, -0.2, 1.0)),
            end=axes.c2p(0.2, gaussian(0.2, 0.2, 1.0)),
            color=WHITE,
            buff=0
        )
        distortion_label = MarkupText("Distortion\n(Độ biến dạng)", font="CMU Serif", font_size=20, color=WHITE)
        distortion_label.next_to(arrow_distortion, UP, buff=0.5)

        graph_group = VGroup(axes, curve_M, curve_M_hat, label_M, label_M_hat, arrow_distortion, distortion_label)

        metrics_title = MarkupText("Thước đo Toán học:", font="CMU Serif", font_size=28, color="#F4D160")
        metric_1 = MarkupText("<i>TV</i> (Total Variation)", font="CMU Serif", font_size=28)
        metric_2 = MarkupText("<i>D<sub>KL</sub></i>(<i>M</i> || <i>M\u0302</i>) (Kullback-Leibler)", font="CMU Serif", font_size=28)
        metric_3 = MarkupText("Rényi Divergence", font="CMU Serif", font_size=28)
        
        metrics_list = VGroup(metrics_title, metric_1, metric_2, metric_3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        metrics_list.next_to(axes, RIGHT, buff=0.5)

        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve_M), Write(label_M), Create(curve_M_hat), Write(label_M_hat), run_time=1.5)
        self.play(GrowArrow(arrow_distortion), FadeIn(distortion_label), run_time=1.0)
        synced_wait(12.0) # "Để cụ thể hóa khái niệm này... mô hình có watermark M hat."
        
        self.play(Write(metrics_title), run_time=1.0)
        self.play(FadeIn(metric_1, shift=LEFT*0.2), run_time=0.8)
        self.play(FadeIn(metric_2, shift=LEFT*0.2), run_time=0.8)
        self.play(FadeIn(metric_3, shift=LEFT*0.2), run_time=0.8)
        synced_wait(16.0) # "Mục tiêu của một thuật toán tốt... Rényi Divergence."

        # Bước 3: Quy mô đánh giá (Evaluation Scale)
        self.play(
            graph_group.animate.set_opacity(0.1),
            metrics_list.animate.set_opacity(0.1),
            run_time=1.0
        )

        scale_title = MarkupText("Quy mô đánh giá", font="CMU Serif", font_size=32, color="#F4D160").move_to(UP * 1.5)
        
        level_1 = MarkupText("Cấp 1: One-token\n(Chỉ từ tiếp theo)", font="CMU Serif", font_size=24, justify=True).move_to(LEFT * 4 + DOWN * 0.5)
        level_2 = MarkupText("Cấp 2: Whole Sentence\n(Cả đoạn văn)", font="CMU Serif", font_size=24, justify=True).move_to(DOWN * 0.5)
        level_3 = MarkupText("Cấp 3: Polynomial sequences\n(Hàng triệu văn bản)", font="CMU Serif", font_size=24, justify=True).move_to(RIGHT * 4 + DOWN * 0.5)
        
        timeline = Arrow(start=LEFT * 5.5, end=RIGHT * 5.5, color=WHITE, stroke_width=4, buff=0).move_to(DOWN * 1.5)
        dot_1 = Dot(color="#2ECC71").move_to(timeline.point_from_proportion(0.15))
        dot_2 = Dot(color="#2ECC71").move_to(timeline.point_from_proportion(0.5))
        dot_3 = Dot(color="#2ECC71").move_to(timeline.point_from_proportion(0.85))

        self.play(Write(scale_title), GrowArrow(timeline), run_time=1.5)
        synced_wait(7.0) # "Độ biến dạng này không chỉ được xem xét... quy mô tăng dần."
        
        self.play(FadeIn(dot_1), Write(level_1), run_time=1.0)
        synced_wait(4.0) # "Bắt đầu từ One-token... đánh giá từ tiếp theo;"
        
        self.play(FadeIn(dot_2), Write(level_2), run_time=1.0)
        synced_wait(4.0) # "mở rộng ra Whole Sentence... quy mô cả đoạn văn;"
        
        self.play(FadeIn(dot_3), Write(level_3), run_time=1.0)
        synced_wait(10.0) # "và cuối cùng là cấp độ khắt khe nhất... liên tục."

        # Bước 4: So sánh Cam kết Chất lượng (Ex-ante vs Ex-post)
        self.play(
            FadeOut(graph_group),
            FadeOut(metrics_list),
            FadeOut(scale_title),
            FadeOut(level_1), FadeOut(level_2), FadeOut(level_3),
            FadeOut(timeline), FadeOut(dot_1), FadeOut(dot_2), FadeOut(dot_3),
            run_time=1.0
        )

        compare_title = MarkupText("Cam kết Chất lượng (Quality Guarantees)", font="CMU Serif", font_size=32, color=WHITE).move_to(UP * 0.5)
        self.play(Write(compare_title), run_time=1.0)
        synced_wait(7.0) # "Đặc biệt, lời cam kết... hai cấp độ bản chất."

        # Cột Trái (Ex-ante)
        left_title = MarkupText("Ex-ante", font="CMU Serif", font_size=36, color="#2ECC71") # Green
        left_desc = MarkupText("Trung bình các văn bản sẽ tốt", font="CMU Serif", font_size=24, color=WHITE)
        tick_mark = MarkupText("✓", color="#2ECC71", font_size=48, font="Segoe UI Emoji")
        left_group = VGroup(left_title, left_desc, tick_mark).arrange(DOWN, buff=0.4).move_to(LEFT * 3.5 + DOWN * 2.0)

        # Cột Phải (Ex-post)
        right_title = MarkupText("Ex-post", font="CMU Serif", font_size=36, color="#F4D160") # Yellow
        right_desc = MarkupText("MỌI văn bản cụ thể đều phải tốt", font="CMU Serif", font_size=24, color=WHITE)
        warning_text = MarkupText("Khắt khe hơn nhiều", font="CMU Serif", font_size=20, color="#F4D160")
        right_content = VGroup(right_title, right_desc, warning_text).arrange(DOWN, buff=0.4)
        
        right_box = SurroundingRectangle(right_content, color="#F4D160", buff=0.3, stroke_width=2)
        right_group = VGroup(right_box, right_content).move_to(RIGHT * 3.5 + DOWN * 2.0)

        v_line = Line(UP * 0.5, DOWN * 3.5, color="#8B8B92").move_to(DOWN * 1.5)

        self.play(Create(v_line), run_time=0.5)
        
        self.play(FadeIn(left_group, shift=RIGHT*0.5), run_time=1.0)
        synced_wait(10.0) # "Cấp độ thứ nhất là Ex-ante... sinh ra sẽ tốt."
        
        self.play(FadeIn(right_content, shift=LEFT*0.5), Create(right_box), run_time=1.0)
        synced_wait(10.0) # "Nhưng giới nghiên cứu còn hướng tới... không có ngoại lệ."
        
        self.play(
            Flash(right_box, color="#F4D160", line_length=0.2, flash_radius=2.5),
            right_box.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1.5
        )
        synced_wait(7.0) # "Một thuật toán bảo toàn chất lượng... sai sự thật."

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        # Chuyển cảnh
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_2_1(scene: Scene) -> None:
    Scene2_2_1_Quality_Metric.construct(scene)
