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

class Scene1_1_Watermark_History(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "voice", "voice_1_1.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 20.0
        total_expected_wait = 72.0  # Ước tính tổng thời gian đọc (khoảng 1 phút 12 giây)
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Tiêu đề & Khởi tạo Trục thời gian
        title = MarkupText("1.1 LỊCH SỬ TIẾN HÓA CỦA WATERMARK", font="CMU Serif", font_size=32, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)

        timeline = Line(LEFT * 6, RIGHT * 6, stroke_width=4).to_edge(DOWN, buff=1.5)
        self.play(Create(timeline), run_time=1.0)

        # Mốc 1: Khởi tạo và Kỷ nguyên Vật lý
        dot1 = Dot(timeline.point_from_proportion(0.15), color=WHITE, radius=0.1)
        label1 = MarkupText("Thế kỷ 19\nPhysical", font="CMU Serif", font_size=20, justify=True).next_to(dot1, DOWN, buff=0.2)
        self.play(FadeIn(dot1, scale=0.5), Write(label1), run_time=1.0)

        physical_group = VGroup()
        stamp = Rectangle(width=3, height=4, color=WHITE, fill_color="#F5DEB3", fill_opacity=1).shift(UP * 0.5)
        stamp.set_stroke(width=4)
        
        crown_points = [
            [-0.6, -0.2, 0], [-0.8, 0.6, 0], [-0.3, 0.2, 0], 
            [0, 0.8, 0], [0.3, 0.2, 0], [0.8, 0.6, 0], [0.6, -0.2, 0]
        ]
        crown_shape = Polygon(*crown_points, color=GOLD, fill_color=GOLD, fill_opacity=0.5)
        crown_text = Text("Crown CA", font_size=24, color=GOLD).next_to(crown_shape, DOWN, buff=0.2)
        crown = VGroup(crown_shape, crown_text).move_to(stamp.get_center()).set_opacity(0)
        
        physical_group.add(stamp, crown)
        self.play(DrawBorderThenFill(stamp), run_time=1.0)
        synced_wait(12.0) # "Khái niệm Watermark... đồng hành cùng lịch sử..."
        
        light_sweep = Rectangle(width=0.5, height=5, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5)
        light_sweep.rotate(PI/6).move_to(stamp.get_left() + LEFT)
        
        self.play(
            light_sweep.animate.move_to(stamp.get_right() + RIGHT),
            crown.animate.set_opacity(0.8),
            run_time=2.0,
            rate_func=linear
        )
        self.play(FadeOut(light_sweep), run_time=0.5)
        synced_wait(13.0) # "Từ hàng trăm năm trước... ẩn sâu bên trong thớ giấy."
        
        # Giai đoạn 2: Kỷ nguyên Kỹ thuật số (Digital Era)
        self.play(FadeOut(physical_group), run_time=1.0)
        
        dot2 = Dot(timeline.point_from_proportion(0.5), color=WHITE, radius=0.1)
        label2 = MarkupText("Thập niên 1990\nDigital", font="CMU Serif", font_size=20, justify=True).next_to(dot2, DOWN, buff=0.2)
        self.play(FadeIn(dot2, scale=0.5), Write(label2), run_time=1.0)
        
        digital_group = VGroup()
        grid = NumberPlane(x_range=[-2, 2, 0.5], y_range=[-2, 2, 0.5], background_line_style={"stroke_color": BLUE, "stroke_width": 2})
        grid_bg = Rectangle(width=4, height=4, color=BLUE, fill_color=BLUE_E, fill_opacity=0.5)
        grid.move_to(grid_bg.get_center())
        image_group = VGroup(grid_bg, grid).shift(UP * 0.5)
        
        digital_group.add(image_group)
        self.play(Create(image_group), run_time=1.5)
        synced_wait(8.0) # "Bước sang kỷ nguyên máy tính... thủy vân vô hình."
        
        pixel_focus = Square(side_length=1.5, color=YELLOW).move_to(grid.c2p(0.25, 0.25))
        self.play(Create(pixel_focus), run_time=1.0)
        
        binary_text = MarkupText("101010", font="Courier New", font_size=36, color=GREEN).move_to(pixel_focus.get_center())
        self.play(
            Transform(image_group, image_group.copy().set_opacity(0.2)),
            FadeIn(binary_text, shift=UP*0.2),
            run_time=1.5
        )
        digital_group.add(pixel_focus, binary_text)
        synced_wait(15.0) # "Lúc này, các chuỗi mã nhị phân được giấu... ngay lập tức."
        
        # Giai đoạn 3: Kỷ nguyên Trí tuệ Nhân tạo (GenAI Era)
        self.play(FadeOut(digital_group), run_time=1.0)
        
        dot3 = Dot(timeline.point_from_proportion(0.85), color=WHITE, radius=0.1)
        label3 = MarkupText("Hiện tại\nGenAI Text", font="CMU Serif", font_size=20, justify=True).next_to(dot3, DOWN, buff=0.2)
        self.play(FadeIn(dot3, scale=0.5), Write(label3), run_time=1.0)
        
        genai_group = VGroup()
        llm_box = RoundedRectangle(width=2, height=1.5, corner_radius=0.2, color=PURPLE, fill_color=PURPLE_E, fill_opacity=0.8)
        llm_text = Text("LLM", font_size=36, weight=BOLD, color=WHITE).move_to(llm_box.get_center())
        llm_group = VGroup(llm_box, llm_text).move_to(LEFT * 2 + UP * 0.5)
        
        text_blocks = VGroup(*[Rectangle(width=0.6, height=0.3, color=WHITE, fill_color=GRAY, fill_opacity=0.5) for _ in range(4)])
        text_blocks.arrange(RIGHT, buff=0.2).next_to(llm_group, RIGHT, buff=1.0)
        
        arrows = VGroup(*[Arrow(llm_group.get_right(), block.get_left(), buff=0.1, color=WHITE) for block in text_blocks])
        
        genai_group.add(llm_group, text_blocks, arrows)
        self.play(FadeIn(llm_group, shift=UP*0.2), run_time=1.0)
        
        self.play(LaggedStart(*[FadeIn(block, shift=RIGHT*0.2) for block in text_blocks], lag_ratio=0.3), run_time=1.5)
        synced_wait(12.0) # "Nhưng ngày hôm nay... sứ mệnh khác biệt hoàn toàn."
        
        stamp_icon = Star(color=YELLOW, fill_opacity=1).scale(0.3)
        stamp_icon.move_to(text_blocks[2].get_center())
        
        self.play(
            stamp_icon.animate.scale(1.5).move_to(text_blocks[2].get_center()),
            Flash(text_blocks[2], color=YELLOW, line_length=0.2),
            run_time=1.0
        )
        genai_group.add(stamp_icon)
        
        final_msg = MarkupText("Sự khác biệt cốt lõi nằm ở cách tiếp cận!", font="CMU Serif", font_size=24, color=YELLOW)
        final_msg.next_to(timeline, UP, buff=2.0)
        
        self.play(Write(final_msg), run_time=1.5)
        synced_wait(12.0) # "Nó không giống như in hình... nằm ở chính cách tiếp cận."
        
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(2.0)
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_part1_scene_1_1(scene: Scene) -> None:
    Scene1_1_Watermark_History.construct(scene)
