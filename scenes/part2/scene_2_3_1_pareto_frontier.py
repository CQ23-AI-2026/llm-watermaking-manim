import os
from manim import *
import numpy as np

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

class Scene2_3_1_Pareto_Frontier(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_3_1.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 13.0
        total_expected_wait = 110.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề & Đặt vấn đề
        title = MarkupText("2.3.1 SỰ ĐÁNH ĐỔI GIỮA CHẤT LƯỢNG &amp; KHẢ NĂNG PHÁT HIỆN", font="CMU Serif", font_size=24, weight="BOLD", color="#F4D160")
        title_group = VGroup(title).to_edge(UP, buff=0.4)
        
        self.play(Write(title_group), run_time=1.0)
        synced_wait(12.0) # "Khi nghiên cứu sâu vào bản chất của thủy vân văn bản... Khả năng phát hiện dấu vết."

        # Bước 2: Khởi tạo hệ trục tọa độ chuẩn
        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0, 1.2, 0.2],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": False, "include_tip": True}
        ).shift(LEFT * 0.5)
        
        x_label = MarkupText("Distortion\n(Độ biến dạng)", font="CMU Serif", font_size=18)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        
        y_label = MarkupText("Detectability\n(Khả năng phát hiện)", font="CMU Serif", font_size=18)
        y_label.next_to(axes.y_axis, UP, buff=0.1)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)
        synced_wait(11.0) # "Để trực quan hóa cuộc chiến này... năng lực bắt chính xác dấu vết AI."

        # Bước 3: Vẽ đường cong Trade-off - Pareto Frontier
        curve = axes.plot(lambda x: 1 - np.exp(-3.5 * x), x_range=[0, 1.05], color=ORANGE)
        
        curve_label = MarkupText("Pareto Frontier\n(Đường biên tối ưu)", font="CMU Serif", font_size=18, color=ORANGE, justify=True)
        point_on_curve = axes.c2p(0.4, 1 - np.exp(-3.5 * 0.4))
        curve_label.next_to(point_on_curve, DOWN * 1.5 + RIGHT * 1.0)
        
        arrow_pareto = Arrow(curve_label.get_top(), point_on_curve, buff=0.1, color=ORANGE)
        
        self.play(Create(curve), run_time=1.5)
        self.play(FadeIn(curve_label), GrowArrow(arrow_pareto), run_time=1.0)
        synced_wait(20.0) # "Mối quan hệ mâu thuẫn này được vạch định... hy sinh và đánh đổi tiêu chí còn lại."

        # Bước 4: Highlight hai điểm cực đoan trên đồ thị
        point_a_coord = [0.1, 1 - np.exp(-3.5 * 0.1)]
        dot_a = Dot(axes.c2p(*point_a_coord), color=BLUE, radius=0.08)
        label_a = MarkupText("Văn bản tự nhiên,\nnhưng rất dễ bị xóa Watermark", font="CMU Serif", font_size=16, color=BLUE)
        label_a.next_to(dot_a, DOWN * 1.5 + RIGHT * 0.2)
        
        point_b_coord = [0.95, 1 - np.exp(-3.5 * 0.95)]
        dot_b = Dot(axes.c2p(*point_b_coord), color=RED, radius=0.08)
        label_b = MarkupText("Watermark không thể phá hủy,\nnhưng văn bản bị lủng củng", font="CMU Serif", font_size=16, color=RED, justify=True)
        label_b.next_to(dot_b, UP + LEFT, buff=0.2)
        
        self.play(FadeIn(dot_a), Write(label_a), run_time=1.0)
        self.play(Indicate(dot_a, scale_factor=1.5, color=BLUE), run_time=1.0)
        synced_wait(18.0) # "Hãy nhìn vào hai điểm cực đoan... dấu vết watermark sẽ hoàn toàn bay màu."
        
        self.play(FadeIn(dot_b), Write(label_b), run_time=1.0)
        self.play(Indicate(dot_b, scale_factor=1.5, color=RED), run_time=1.0)
        synced_wait(17.0) # "Ngược lại, nếu chúng ta muốn dấu vết... khiến câu từ sinh ra bị lủng củng..."

        # Bước 5: Mở ra giải pháp nâng cao
        self.play(
            FadeOut(dot_a), FadeOut(label_a),
            FadeOut(dot_b), FadeOut(label_b),
            FadeOut(curve_label), FadeOut(arrow_pareto),
            curve.animate.set_stroke(opacity=0.3),
            run_time=1.0
        )
        synced_wait(7.0) # "Sự mắc kẹt giữa hai cực đầu chiến tuyến này... Một hệ thống trong mơ phải nằm ở góc trên bên trái..."
        
        new_curve = axes.plot(lambda x: 1 - np.exp(-10 * x), x_range=[0, 1.05], color=GREEN)
        
        p_old = axes.c2p(0.3, 1 - np.exp(-3.5 * 0.3))
        p_new = axes.c2p(0.1, 1 - np.exp(-10 * 0.1))
        arrow_improve = Arrow(p_old, p_new, color=GREEN, buff=0.1)
        
        self.play(GrowArrow(arrow_improve), run_time=0.5)
        self.play(Create(new_curve), run_time=1.5)
        synced_wait(7.0) # "...nơi độ biến dạng bằng không, nhưng năng lực phát hiện vẫn đạt tuyệt đối."
        
        conclusion_box = MarkupText(
            "Mục tiêu của các thuật toán hiện đại: Phá vỡ đường biên này\nđể đạt trạng thái Distortion-Free!", 
            font="CMU Serif", font_size=24, color="#2ECC71", weight="BOLD", justify=True
        )
        conclusion_box.to_edge(DOWN, buff=0.2)
        
        self.play(Write(conclusion_box), run_time=1.0)
        synced_wait(18.0) # "Và đó cũng chính là phát súng khơi mào cho cuộc cách mạng tiếp theo..."

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_3_1(scene: Scene) -> None:
    Scene2_3_1_Pareto_Frontier.construct(scene)
