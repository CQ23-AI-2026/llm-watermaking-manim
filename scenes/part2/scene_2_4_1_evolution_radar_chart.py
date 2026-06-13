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
    return None

class Scene2_4_1_Evolution_RadarChart(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_4_1.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 12.0
        total_expected_wait = 91.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Khởi tạo Radar Chart & Tiêu đề
        title = MarkupText("2.4.1 TUYẾN TIẾN HÓA CỦA CÁC HỆ THỐNG WATERMARKING", font="CMU Serif", font_size=24, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=1.0)
        
        center = LEFT * 2 + DOWN * 0.5
        radius = 2.5

        axis_up = Line(center, center + UP * radius, color=WHITE)
        axis_right = Line(center, center + RIGHT * radius, color=WHITE)
        axis_down = Line(center, center + DOWN * radius, color=WHITE)
        axis_left = Line(center, center + LEFT * radius, color=WHITE)
        
        grid_lines = VGroup()
        for i in range(1, 6):
            r = radius * i / 5
            poly = Polygon(
                center + UP * r,
                center + RIGHT * r,
                center + DOWN * r,
                center + LEFT * r,
                color=GRAY,
                stroke_width=1,
                stroke_opacity=0.5
            )
            grid_lines.add(poly)

        axes_group = VGroup(axis_up, axis_right, axis_down, axis_left, grid_lines)

        label_up = MarkupText("Quality", font="CMU Serif", font_size=16).next_to(axis_up, UP, buff=0.1)
        label_right = MarkupText("Detectability", font="CMU Serif", font_size=16).next_to(axis_right, RIGHT, buff=0.1)
        label_down = MarkupText("Robustness", font="CMU Serif", font_size=16).next_to(axis_down, DOWN, buff=0.1)
        label_left = MarkupText("Security", font="CMU Serif", font_size=16).next_to(axis_left, LEFT, buff=0.1)

        labels_group = VGroup(label_up, label_right, label_down, label_left)

        self.play(Create(axes_group), Write(labels_group), run_time=2.0)
        synced_wait(18.0) # Bây giờ, hãy lùi lại... hình dung sự tiến hóa.

        # Giai đoạn 2: Thế hệ 1 - Can thiệp thống kê
        gen1_vals = [0.3, 0.8, 0.8, 0.2]
        gen1_pts = [
            center + UP * radius * gen1_vals[0],
            center + RIGHT * radius * gen1_vals[1],
            center + DOWN * radius * gen1_vals[2],
            center + LEFT * radius * gen1_vals[3]
        ]
        gen1_poly = Polygon(*gen1_pts, color=RED, fill_color=RED, fill_opacity=0.4, stroke_width=3)
        
        legend_gen1 = MarkupText("Thế hệ 1: Can thiệp thống kê\n(VD: KGW, Unigram)", font="CMU Serif", font_size=18, color=RED, justify=True)
        legend_gen1.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)

        self.play(Create(gen1_poly), Write(legend_gen1), run_time=1.5)
        synced_wait(20.0) # Đầu tiên là Thế hệ 1... thu hẹp đáng kể.

        # Giai đoạn 3: Thế hệ 2 - Đề cao chất lượng
        synced_wait(5.0) # Để khắc phục điểm yếu đó... Gumbel Watermark.
        
        gen2_vals = [0.95, 0.7, 0.4, 0.4]
        gen2_pts = [
            center + UP * radius * gen2_vals[0],
            center + RIGHT * radius * gen2_vals[1],
            center + DOWN * radius * gen2_vals[2],
            center + LEFT * radius * gen2_vals[3]
        ]
        gen2_poly = Polygon(*gen2_pts, color=BLUE, fill_color=BLUE, fill_opacity=0.4, stroke_width=3)
        
        legend_gen2 = MarkupText("Thế hệ 2: Đề cao chất lượng\n(VD: Gumbel)", font="CMU Serif", font_size=18, color=BLUE, justify=True)
        legend_gen2.next_to(legend_gen1, DOWN, buff=0.5, aligned_edge=LEFT)

        gen1_outline = Polygon(*gen1_pts, color=RED, stroke_width=2, fill_opacity=0)
        gen1_dashed = DashedVMobject(gen1_outline, num_dashes=30)

        self.play(
            ReplacementTransform(gen1_poly, gen1_dashed),
            Create(gen2_poly),
            Write(legend_gen2),
            run_time=2.0
        )
        synced_wait(18.0) # Bạn có thể thấy khối đa giác... viết lại văn bản.

        # Giai đoạn 4: Thế hệ 3 - Cực hạn bảo mật & Khơi gợi
        gen3_vals = [0.85, 0.8, 0.7, 0.95]
        gen3_pts = [
            center + UP * radius * gen3_vals[0],
            center + RIGHT * radius * gen3_vals[1],
            center + DOWN * radius * gen3_vals[2],
            center + LEFT * radius * gen3_vals[3]
        ]
        gen3_poly = Polygon(*gen3_pts, color=PURPLE, fill_color=PURPLE, fill_opacity=0.4, stroke_width=3)

        legend_gen3 = MarkupText("Thế hệ 3: Cực hạn bảo mật\n(VD: PRC)", font="CMU Serif", font_size=18, color=PURPLE, justify=True)
        legend_gen3.next_to(legend_gen2, DOWN, buff=0.5, aligned_edge=LEFT)

        gen2_outline = Polygon(*gen2_pts, color=BLUE, stroke_width=2, fill_opacity=0)
        gen2_dashed = DashedVMobject(gen2_outline, num_dashes=30)

        self.play(
            ReplacementTransform(gen2_poly, gen2_dashed),
            Create(gen3_poly),
            Write(legend_gen3),
            run_time=2.0
        )
        synced_wait(15.0) # Và cuối cùng là Thế hệ 3... mốc an ninh mới.

        # Làm mờ và dấu chấm hỏi
        self.play(
            axes_group.animate.set_opacity(0.2),
            labels_group.animate.set_opacity(0.2),
            gen1_dashed.animate.set_opacity(0.2),
            gen2_dashed.animate.set_opacity(0.2),
            gen3_poly.animate.set_opacity(0.2),
            run_time=1.5
        )

        question = MarkupText("?", font="CMU Serif", font_size=120, weight="BOLD", color=YELLOW)
        question.move_to(center)
        
        q_text = MarkupText("Có tồn tại một đa giác hoàn hảo\nchạm cả 4 đỉnh?", font="CMU Serif", font_size=20, color=YELLOW, justify=True)
        q_text.next_to(question, DOWN, buff=0.5)

        self.play(
            FadeIn(question, scale=0.5),
            Flash(question, color=YELLOW, flash_radius=1.5),
            Write(q_text),
            run_time=2.0
        )
        synced_wait(15.0) # Nhìn vào những thế hệ... hay không?

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_4_1(scene: Scene) -> None:
    Scene2_4_1_Evolution_RadarChart.construct(scene)
