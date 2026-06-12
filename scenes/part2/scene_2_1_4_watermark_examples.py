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

class Scene2_1_4_Watermark_Examples(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_4.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 21.3
        total_expected_wait = 62.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Hiển thị Prompt chung
        prompt_text = VGText("Prompt: Can I succeed after many failures?", font_size=32, weight=BOLD_WEIGHT, color=WHITE)
        prompt_box = SurroundingRectangle(prompt_text, color=VG_GRAY, corner_radius=0.2, buff=0.3)
        prompt_group = VGroup(prompt_box, prompt_text).to_edge(UP, buff=0.5)

        self.play(FadeIn(prompt_box), Write(prompt_text), run_time=1.5)
        synced_wait(6.0) # "Để có một cái nhìn thực tế..."

        # Bước 2: Bố cục so sánh song song
        left_box = RoundedRectangle(corner_radius=0.3, width=6.0, height=5.0, color=VG_GRAY, fill_opacity=0.0)
        right_box = RoundedRectangle(corner_radius=0.3, width=6.0, height=5.0, color=VG_GRAY, fill_opacity=0.0)
        
        boxes = VGroup(left_box, right_box).arrange(RIGHT, buff=0.8).next_to(prompt_group, DOWN, buff=0.5)

        title_left = VGText("KHÔNG CÓ WATERMARK", font_size=28, color=WHITE, weight=BOLD_WEIGHT)
        title_left.next_to(left_box.get_top(), DOWN, buff=0.3)
        
        title_right = VGText("CÓ WATERMARK", font_size=28, color=WHITE, weight=BOLD_WEIGHT)
        title_right.next_to(right_box.get_top(), DOWN, buff=0.3)

        self.play(Create(left_box), Create(right_box), run_time=1.5)
        self.play(Write(title_left), Write(title_right), run_time=1.0)
        synced_wait(9.0) # "Chúng ta sẽ chạy cùng một câu lệnh... bàn cân so sánh"

        # Hàm chia dòng văn bản thông minh, gộp thành 1 chuỗi để GIỮ CHUẨN BASELINE
        def create_wrapped_text(text, max_width, font_size=28):
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
                
            lines_vgroup.arrange(DOWN, buff=0.25)
            return lines_vgroup

        # Bước 3: Khung bên trái (Không Watermark)
        left_str = "Of course it is, and that is how we improve. Saying 'I can't do that' is never a good thing."
        left_text_group = create_wrapped_text(left_str, max_width=5.2)
        left_text_group.next_to(title_left, DOWN, buff=0.6)

        self.play(FadeIn(left_text_group, shift=UP), run_time=1.5)
        synced_wait(2.0) # "Ở khung bên trái, khi mô hình hoạt động..."

        import random
        random.seed(10)
        animations = []
        for line in left_text_group:
            for word_mob in line.word_mobs:
                color = VG_GREEN if random.random() < 0.5 else VG_RED
                animations.append(word_mob.animate.set_color(color))
        
        self.play(AnimationGroup(*animations, lag_ratio=0.1), run_time=2.0)
        synced_wait(8.0) # "... ngẫu nhiên và đều nhau."

        z_left = VGText("z-score = -2.4", font_size=32, color=VG_GRAY)
        z_left.next_to(left_box.get_bottom(), UP, buff=0.3)

        self.play(Write(z_left), run_time=1.0)
        synced_wait(10.0) # "Khi chạy thuật toán... tự do lựa chọn ngôn từ."

        # Bước 4: Khung bên phải (Có Watermark)
        right_str = "When most people are confronted with failure, they cannot imagine such a thing happening."
        right_text_group = create_wrapped_text(right_str, max_width=5.2)
        right_text_group.next_to(title_right, DOWN, buff=0.6)

        self.play(FadeIn(right_text_group, shift=UP), run_time=1.5)
        synced_wait(8.0) # "Nhưng hãy nhìn sang khung bên phải... thay đổi hoàn toàn."

        # Hiệu ứng thanh quét quét qua đoạn văn 2
        scanner = SurroundingRectangle(right_text_group[0].word_mobs[0], color=VG_GOLD, fill_opacity=0.2, buff=0.1)
        self.play(FadeIn(scanner), run_time=0.5)

        red_indices = [3, 10] # Vài từ Đỏ ngẫu nhiên xen kẽ
        word_idx = 0
        for line in right_text_group:
            for word_mob in line.word_mobs:
                target_scanner = SurroundingRectangle(word_mob, color=VG_GOLD, fill_opacity=0.2, buff=0.1)
                self.play(Transform(scanner, target_scanner), run_time=0.15)
                color = VG_RED if word_idx in red_indices else VG_GREEN
                self.play(word_mob.animate.set_color(color), run_time=0.1)
                word_idx += 1
                
        self.play(FadeOut(scanner), run_time=0.5)
        synced_wait(3.0) # "Gần như toàn bộ... sắc Xanh của Green List."

        z_right = VGText("z-score = 11.0", font_size=36, color=VG_GOLD, weight=BOLD_WEIGHT)
        z_right.next_to(right_box.get_bottom(), UP, buff=0.3)

        self.play(Write(z_right), run_time=1.0)
        self.play(Wiggle(z_right), run_time=1.5)
        synced_wait(8.0) # "Điểm số Z-score... bẫy thống kê hoàn hảo."

        # Bước 5: Điểm nhấn kết luận
        left_highlight = SurroundingRectangle(left_text_group, color=VG_RED, buff=0.2, stroke_width=2)
        right_highlight = SurroundingRectangle(right_text_group, color=VG_GREEN, buff=0.2, stroke_width=4)
        
        arrow_compare = DoubleArrow(
            start=left_text_group.get_right() + RIGHT*0.2,
            end=right_text_group.get_left() + LEFT*0.2,
            color=WHITE
        )

        self.play(Create(left_highlight), Create(right_highlight), GrowArrow(arrow_compare), run_time=1.5)
        synced_wait(8.0) # "Đặt hai văn bản này cạnh nhau... đúng ngữ pháp."
        
        self.play(
            left_highlight.animate.set_stroke(width=4),
            right_highlight.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1.5
        )

        # Audio wait
        elapsed_time = self.renderer.time - start_time
        print(f"DEBUG 2.1.4: voice_duration={voice_duration}, elapsed_time_before_wait={elapsed_time}, scale_factor={scale_factor}")
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            print(f"DEBUG 2.1.4: final_wait_time={wait_time}")
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_4(scene: Scene) -> None:
    Scene2_1_4_Watermark_Examples.construct(scene)
