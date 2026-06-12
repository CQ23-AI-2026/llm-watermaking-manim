import os
from manim import *
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_RED, WHITE,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

class Scene2_1_3_Watermark_Detection(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_3.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Bước 1: Hiển thị văn bản nghi vấn
        text_str = "When most people are confronted with failure, they cannot imagine such a thing happening."
        
        # Hàm chia dòng văn bản thông minh, gộp thành 1 chuỗi để GIỮ CHUẨN BASELINE
        def create_wrapped_text(text, max_width, font_size=32):
            words = text.split()
            lines_str = []
            current_line_words = []
            
            for w in words:
                current_line_words.append(w)
                test_str = " ".join(current_line_words)
                test_mob = MarkupText(test_str, font_size=font_size, font="CMU Serif")
                if test_mob.width > max_width and len(current_line_words) > 1:
                    current_line_words.pop()
                    lines_str.append(" ".join(current_line_words))
                    current_line_words = [w]
            if current_line_words:
                lines_str.append(" ".join(current_line_words))
                
            lines_vgroup = VGroup()
            for line_str in lines_str:
                line_mob = MarkupText(line_str, font_size=font_size, font="CMU Serif")
                
                # Nhóm các ký tự thành từng từ để dễ đổi màu mà không làm hỏng baseline
                line_words = line_str.split()
                word_mobs = VGroup()
                char_idx = 0
                for w in line_words:
                    num_chars = len(w)
                    word_chars = VGroup(*line_mob[char_idx : char_idx + num_chars])
                    word_mobs.add(word_chars)
                    char_idx += num_chars
                
                line_mob.word_mobs = word_mobs
                lines_vgroup.add(line_mob)
                
            lines_vgroup.arrange(DOWN, buff=0.4)
            return lines_vgroup

        text_group = create_wrapped_text(text_str, max_width=10.0, font_size=32)
        text_group.to_edge(UP, buff=1.5)

        word_mobjects = []
        for line in text_group:
            word_mobjects.extend(list(line.word_mobs))
        
        self.play(Write(text_group), run_time=2.0)
        self.wait(6.0) # Đợi lời thoại: "Khi một đoạn văn bản... lật tẩy nó?"

        # Bước 2: Hiệu ứng quét và tô màu từ
        import random
        random.seed(42) # Giữ cố định random seed
        
        colors_for_words = []
        for _ in range(len(word_mobjects)):
            colors_for_words.append(VG_GREEN if random.random() < 0.85 else VG_RED)
            
        # Bộ đếm (Sử dụng VGText thay vì Integer/MathTex để tránh lỗi LaTeX)
        count_val = VGText("0", font_size=36, color=VG_GREEN)
        counter_label = VGroup(
            VGText("|y_g| = ", font_size=36, color=WHITE),
            count_val
        ).arrange(RIGHT, buff=0.2).next_to(text_group, DOWN, buff=1.0)
        
        self.play(FadeIn(counter_label), run_time=1.0)
        self.wait(2.0)
        
        # Thanh quét linh hoạt kích thước
        scanner = SurroundingRectangle(word_mobjects[0], color=VG_GOLD, fill_opacity=0.2, buff=0.1)
        self.play(FadeIn(scanner), run_time=0.5)

        green_count = 0
        for i, word_mob in enumerate(word_mobjects):
            # Tạo khung mục tiêu vừa vặn với chiều dài của từ hiện tại
            target_scanner = SurroundingRectangle(word_mob, color=VG_GOLD, fill_opacity=0.2, buff=0.1)
            
            # Di chuyển và co giãn khung quét khớp với từ
            self.play(Transform(scanner, target_scanner), run_time=0.3)
            
            # Đổi màu từ
            color = colors_for_words[i]
            self.play(word_mob.animate.set_color(color), run_time=0.15)
            
            # Cập nhật bộ đếm nếu là từ màu Xanh
            if color == VG_GREEN:
                green_count += 1
                new_val = VGText(str(green_count), font_size=36, color=VG_GREEN).move_to(count_val.get_center())
                self.play(Transform(count_val, new_val), run_time=0.1)
                
        self.play(FadeOut(scanner), run_time=0.5)
        self.wait(10.0) # Đợi "Nếu đây thực sự là văn bản... áp đảo hoàn toàn"

        # Bước 3: Xuất hiện công thức Z-score
        # Đoạn văn mờ nhẹ đi
        self.play(
            text_group.animate.set_opacity(0.3),
            counter_label.animate.to_edge(LEFT, buff=1.0).shift(DOWN * 1.0), 
            run_time=1.5
        )
        self.wait(4.0) # "Tuy nhiên, cảm tính là không đủ... kiểm định giả thuyết"
        
        # Dùng Pango Unicode thay vì MathTex để tránh lỗi LaTeX standalone.cls
        num = VGText("|y_g| - \u03B3 \u00B7 n", font_size=42, color=WHITE)
        den = VGText("\u221A(n \u00B7 \u03B3 \u00B7 (1-\u03B3))", font_size=42, color=WHITE)
        frac_line = Line(LEFT, RIGHT, color=WHITE).match_width(den).next_to(den, UP, buff=0.15)
        num.next_to(frac_line, UP, buff=0.15)
        frac = VGroup(num, frac_line, den)
        eq = VGText("z = ", font_size=48, color=WHITE).next_to(frac, LEFT, buff=0.3)
        
        z_formula = VGroup(eq, frac).next_to(counter_label, RIGHT, buff=1.5)
        
        # Hiệu ứng viết vẽ viền chữ (Write)
        self.play(Write(z_formula), run_time=2.0)
        self.wait(15.0) # "Trong công thức này... đại diện bất thường."

        # Bước 4: Tính toán kết quả và So sánh ngưỡng
        self.wait(8.0) # "Với một văn bản bình thường... 0 hoặc âm."

        z_result = VGText("z = 11.0", font_size=48, color=VG_GOLD, weight=BOLD_WEIGHT)
        z_result.move_to(z_formula.get_center())
        
        self.play(Transform(z_formula, z_result), run_time=1.0)
        self.wait(1.0)
        
        threshold_text = VGText("> Threshold (4.0)", font_size=40, color=WHITE)
        threshold_text.next_to(z_result, RIGHT, buff=0.5)
        
        self.play(Write(threshold_text), run_time=1.0)
        self.wait(8.0) # "Nhưng ở ví dụ này... tỷ lệ gần như bằng không."

        # Bước 5: Phán quyết cuối cùng
        verdict_text = VGText("Văn bản có Watermark (AI-generated)", font_size=36, color=VG_GREEN, weight=BOLD_WEIGHT)
        verdict_box = SurroundingRectangle(verdict_text, color=VG_GREEN, buff=0.3, corner_radius=0.2)
        verdict_group = VGroup(verdict_box, verdict_text).to_edge(DOWN, buff=1.0)
        
        self.play(FadeIn(verdict_group, shift=UP), run_time=1.0)
        
        # Nhấp nháy nhẹ
        self.play(Wiggle(verdict_group, scale_value=1.1), run_time=1.5)

        # Audio wait
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_3(scene: Scene) -> None:
    Scene2_1_3_Watermark_Detection.construct(scene)
