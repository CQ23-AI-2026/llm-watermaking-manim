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

class Scene2_1_5_Watermark_Limitations(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_5.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        # Bước 1: Đặt câu hỏi mở đầu
        question_text = VGText("Liệu Watermark có thể phát hiện\nBẤT KỲ văn bản AI nào?", font_size=32, color=VG_GOLD, weight=BOLD_WEIGHT)
        
        self.play(Write(question_text), run_time=1.5)
        self.wait(12.0) # "Đến đây... lật tẩy mọi bài văn... trên Internet."
        
        self.play(
            question_text.animate.scale(0.7).to_corner(UL, buff=0.5),
            run_time=1.5
        )
        self.wait(5.0) # "Nhưng toán học luôn sòng phẳng... giới hạn cốt lõi..."

        # Bước 2: Vẽ Vòng tròn lớn - Tập hợp cha
        large_ellipse = Ellipse(width=9.0, height=5.5, color=BLUE_D, fill_opacity=0.1)
        large_ellipse.shift(DOWN * 0.2)
        
        large_label = VGText("AI-Generated Text\n(Văn bản do AI tạo ra)", font_size=28, color=BLUE_C)
        large_label.next_to(large_ellipse.get_top(), DOWN, buff=0.3)
        
        self.play(Create(large_ellipse), run_time=1.5)
        self.play(FadeIn(large_label), run_time=1.0)
        self.wait(5.0) # "Hãy nhìn vào sơ đồ Venn... thế giới này tạo ra."

        # Bước 3: Vẽ Vòng tròn nhỏ bên trong - Tập hợp con
        small_circle = Circle(radius=1.8, color=VG_GREEN, fill_color=VG_GREEN, fill_opacity=0.25)
        small_circle.move_to(large_ellipse.get_center() + DOWN * 0.6)
        
        small_label = VGText("Text from Model X\n(Mang khóa Model X)", font_size=24, color=WHITE, weight=BOLD_WEIGHT)
        small_label.move_to(small_circle.get_center())
        
        self.play(Create(small_circle), run_time=1.5)
        self.play(FadeIn(small_label), run_time=1.0)
        self.wait(20.0) # "Còn thuật toán Watermark... bí mật cụ thể hay không?."

        # Bước 4: Hiệu ứng nhấp nháy phát súng kết luận
        # Làm mờ phần ngoài của vòng tròn lớn
        self.play(
            large_ellipse.animate.set_fill(opacity=0.02).set_stroke(opacity=0.3),
            large_label.animate.set_opacity(0.3),
            run_time=1.0
        )
        # Nhấp nháy vòng tròn nhỏ
        self.play(Indicate(small_circle, color=VG_GOLD, scale_factor=1.05), run_time=1.5)
        self.wait(6.0) # "Nếu một ai đó... hoàn toàn bất lực."

        # Bước 5: Hiển thị thông điệp cốt lõi dưới đáy màn hình
        conclusion_text = VGText("Watermarking giúp các nhà phát triển\ntự chịu trách nhiệm về sản phẩm của họ.", font_size=26, color=WHITE)
        conclusion_box = SurroundingRectangle(conclusion_text, color=VG_GRAY, corner_radius=0.2, buff=0.2, fill_opacity=0.5, fill_color=BLACK)
        conclusion_group = VGroup(conclusion_box, conclusion_text).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(conclusion_group, shift=UP), run_time=1.5)

        # Audio wait
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_5(scene: Scene) -> None:
    Scene2_1_5_Watermark_Limitations.construct(scene)
