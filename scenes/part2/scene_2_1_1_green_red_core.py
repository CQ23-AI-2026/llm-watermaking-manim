from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
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

class Scene2_1_1_Green_Red_Core_Idea(Scene):
    def construct(self):
        start_time = self.renderer.time
        current_dir = os.path.abspath(os.path.dirname(__file__))
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_1.mp3").replace("\\", "/")
        
        # Ghi nhận file âm thanh để mix ngoài
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Bước 0: Chờ câu mở đầu
        self.wait(4.0) # "Ý tưởng cốt lõi của Green-Red Watermark cực kỳ thanh lịch."

        # Bước 1 (Bộ từ điển V)
        vocab_box = Rectangle(width=8, height=2.5, color=WHITE, stroke_width=4)
        vocab_text = VGText("Bộ từ điển V (~50,000 từ)", font_size=40, weight=BOLD_WEIGHT).next_to(vocab_box, UP, buff=0.5)
        
        self.play(Create(vocab_box), Write(vocab_text), run_time=2.0)
        self.wait(4.0) # "Thay vì để mô hình tự do lựa chọn, thuật toán sẽ chủ động chia..."

        # Bước 2 (Hiệu ứng chia đôi danh sách - Split)
        green_box = Rectangle(width=3.8, height=2.5, fill_color=VG_GREEN, fill_opacity=0.2, stroke_color=VG_GREEN, stroke_width=4)
        green_box.move_to(vocab_box.get_center() + LEFT*2.1)
        
        red_box = Rectangle(width=3.8, height=2.5, fill_color=VG_RED, fill_opacity=0.2, stroke_color=VG_RED, stroke_width=4)
        red_box.move_to(vocab_box.get_center() + RIGHT*2.1)
        
        green_text = VGText("Green List\n(Danh sách Xanh)", color=VG_GREEN, font_size=32).move_to(green_box)
        red_text = VGText("Red List\n(Danh sách Đỏ)", color=VG_RED, font_size=32).move_to(red_box)
        
        self.play(
            FadeOut(vocab_text),
            ReplacementTransform(vocab_box.copy(), green_box),
            ReplacementTransform(vocab_box, red_box),
            run_time=1.5
        )
        self.play(Write(green_text), Write(red_text), run_time=1.5)
        self.wait(5.0) # "... thành hai nửa độc lập: danh sách Xanh và danh sách Đỏ."

        # Bước 3 (Chuyển cảnh sang Biểu đồ Logits phân màu)
        legend_green = VGroup(green_box, green_text)
        legend_red = VGroup(red_box, red_text)
        
        self.play(
            legend_green.animate.scale(0.35).to_corner(UL).shift(DOWN*0.5 + RIGHT*1.0),
            legend_red.animate.scale(0.35).to_corner(UR).shift(DOWN*0.5 + LEFT*1.0),
            run_time=2.0
        )
        
        # Biểu đồ cột Logits
        baseline = -2.0
        axis = Line(LEFT*5, RIGHT*5, color=WHITE).set_y(baseline)
        
        h1, h2, h3, h4 = 2.5, 1.8, 1.2, 2.0
        b1 = Rectangle(width=1.2, height=h1, fill_color=VG_GREEN, fill_opacity=0.8, stroke_color=VG_GREEN)
        b2 = Rectangle(width=1.2, height=h2, fill_color=VG_RED, fill_opacity=0.8, stroke_color=VG_RED)
        b3 = Rectangle(width=1.2, height=h3, fill_color=VG_GREEN, fill_opacity=0.8, stroke_color=VG_GREEN)
        b4 = Rectangle(width=1.2, height=h4, fill_color=VG_RED, fill_opacity=0.8, stroke_color=VG_RED)
        
        b1.move_to(LEFT*3 + UP*(baseline + h1/2))
        b2.move_to(LEFT*1 + UP*(baseline + h2/2))
        b3.move_to(RIGHT*1 + UP*(baseline + h3/2))
        b4.move_to(RIGHT*3 + UP*(baseline + h4/2))
        
        bars = VGroup(b1, b2, b3, b4)
        
        l1 = VGText("Từ 1", font_size=24, color=WHITE).next_to(b1, DOWN)
        l2 = VGText("Từ 2", font_size=24, color=WHITE).next_to(b2, DOWN)
        l3 = VGText("Từ 3", font_size=24, color=WHITE).next_to(b3, DOWN)
        l4 = VGText("Từ 4", font_size=24, color=WHITE).next_to(b4, DOWN)
        for l in [l1, l2, l3, l4]:
            l.set_y(baseline - 0.4)
        labels = VGroup(l1, l2, l3, l4)
        
        self.play(Create(axis), run_time=1.0)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=2.0)
        self.play(FadeIn(labels), run_time=1.0)
        self.wait(5.0) # "Tại mỗi bước dự đoán từ tiếp theo, hệ thống sẽ đối chiếu với quy tắc chia này."

        # Bước 4 (Cộng bias delta)
        delta_sym = VGText("+\u03b4", font_size=48, color=VG_GOLD)
        d1 = delta_sym.copy().next_to(b1, UP, buff=0.8)
        d3 = delta_sym.copy().next_to(b3, UP, buff=0.8)
        
        self.play(FadeIn(d1, shift=DOWN), FadeIn(d3, shift=DOWN), run_time=1.5)
        self.wait(3.0) # "Nếu một từ ngẫu nhiên rơi vào danh sách Xanh..."
        
        delta_h = 1.8
        new_b1 = Rectangle(width=1.2, height=h1+delta_h, fill_color=VG_GREEN, fill_opacity=0.8, stroke_color=VG_GREEN)
        new_b3 = Rectangle(width=1.2, height=h3+delta_h, fill_color=VG_GREEN, fill_opacity=0.8, stroke_color=VG_GREEN)
        
        new_b1.move_to(LEFT*3 + UP*(baseline + (h1+delta_h)/2))
        new_b3.move_to(RIGHT*1 + UP*(baseline + (h3+delta_h)/2))
        
        self.play(
            d1.animate.next_to(new_b1, UP, buff=0.2),
            d3.animate.next_to(new_b3, UP, buff=0.2),
            Transform(b1, new_b1),
            Transform(b3, new_b3),
            run_time=2.0
        )
        self.wait(5.0) # "... âm thầm cộng thêm một lượng bias delta vào điểm logits thô của nó. Trong khi đó, các từ thuộc danh sách Đỏ..."

        # Bước 5 (Kết thúc)
        result_text = VGText("Xác suất chọn các từ trong Green List tăng lên", font_size=30, color=VG_GOLD, weight=BOLD_WEIGHT)
        result_text.to_edge(DOWN, buff=0.3)
        
        final_box = SurroundingRectangle(result_text, color=VG_GOLD, corner_radius=0.2, buff=0.2)
        
        self.play(Write(result_text), Create(final_box), run_time=2.0)
        
        # Wait for audio to finish ("Hệ quả là sau khi qua hàm Softmax... sự điều hướng này tinh vi...")
        elapsed_time = self.renderer.time - start_time
        wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
        if wait_time > 0:
            self.wait(wait_time)
        else:
            self.wait(5.0)
            
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_1(scene: Scene):
    Scene2_1_1_Green_Red_Core_Idea.construct(scene)
