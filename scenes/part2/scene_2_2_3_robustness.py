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

class Scene2_2_3_Robustness(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_2_3.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 15.0
        total_expected_wait = 110.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)
                
        # Bước 1: Tiêu đề & Định nghĩa
        title = MarkupText("3. ROBUSTNESS (ĐỘ BỀN VỮNG)", font="CMU Serif", font_size=36, weight="BOLD", color="#F4D160")
        subtitle = MarkupText("Khả năng phát hiện Watermark sau khi văn bản bị tấn công", font="CMU Serif", font_size=24, color=WHITE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        
        self.play(Write(title_group), run_time=1.5)
        synced_wait(15.0) # "Sau khi đã đảm bảo được chất lượng... Robustness, tức Độ bền vững."
        
        # Bước 2: Hiển thị văn bản gốc có Watermark ổn định
        words = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "in", "the", "forest."]
        text_group = VGroup(*[MarkupText(w, font="CMU Serif", font_size=32, color="#2ECC71") for w in words])
        text_group.arrange_in_grid(rows=3, cols=4, buff=(0.3, 0.4))
        text_group.move_to(LEFT * 3 + ORIGIN)
        
        z_score_text = MarkupText("Z-score =", font="CMU Serif", font_size=32)
        z_score_text.move_to(RIGHT * 2.2 + UP * 0.5)
        
        z_score_tracker = ValueTracker(11.0)
        z_score_val = always_redraw(lambda: MarkupText(f"{z_score_tracker.get_value():.1f}", font="CMU Serif", font_size=40, color="#F4D160").next_to(z_score_text, RIGHT, buff=0.2))
        
        z_score_group = VGroup(z_score_text, z_score_val)
        
        self.play(FadeIn(text_group, shift=UP*0.2), FadeIn(z_score_group, shift=LEFT*0.2), run_time=1.5)
        synced_wait(11.0) # "Về mặt bản chất, đây là thước đo năng lực... đã bị can thiệp và chỉnh sửa hay không?"
        
        # Bước 3: Mô phỏng 4 loại tấn công - Attack Phase
        attack_text = MarkupText("ATTACKS (TẤN CÔNG)", font="CMU Serif", font_size=28, color="#E74C3C", weight="BOLD")
        attack_text.next_to(text_group, UP, buff=0.5)
        
        self.play(FadeIn(attack_text, shift=DOWN*0.5), run_time=1.0)
        self.play(Flash(attack_text, color="#E74C3C", line_length=0.4, flash_radius=1.5), run_time=1.0)
        synced_wait(15.0) # "Hãy thực tế một chút: kẻ gian khi dùng AI... nhằm lẩn tránh các bộ lọc."
        
        # Cropping (Cắt ghép): Xóa 3 từ cuối
        self.play(
            FadeOut(text_group[-3:]),
            run_time=1.5
        )
        synced_wait(8.0) # "Các hình thức tấn công phổ biến nhất bao gồm: Cropping..."
        
        # Edits / Paraphrasing (Chỉnh sửa/Viết lại): Đổi màu 3 từ giữa
        edited_words = [
            MarkupText("cat", font="CMU Serif", font_size=32, color=WHITE).move_to(text_group[3].get_center()),
            MarkupText("leaps", font="CMU Serif", font_size=32, color=WHITE).move_to(text_group[4].get_center()),
            MarkupText("across", font="CMU Serif", font_size=32, color=WHITE).move_to(text_group[5].get_center()),
        ]
        
        self.play(
            Transform(text_group[3], edited_words[0]),
            Transform(text_group[4], edited_words[1]),
            Transform(text_group[5], edited_words[2]),
            run_time=1.5
        )
        synced_wait(9.0) # "hay tinh vi hơn là Edits và Paraphrasing..."
        
        # Bước 4: Cập nhật lại Z-score và Ngưỡng phán quyết
        self.play(
            z_score_tracker.animate.set_value(5.5),
            run_time=2.0
        )
        synced_wait(14.0) # "Khi các từ ngữ bị thay đổi và cắt xén... xuống chỉ còn 5.5."
        
        threshold_text = MarkupText("5.5 &gt; Threshold (4.0)", font="CMU Serif", font_size=28, color="#2ECC71")
        threshold_text.next_to(z_score_group, DOWN, buff=0.5)
        
        self.play(Write(threshold_text), run_time=1.5)
        self.play(Flash(threshold_text, color="#2ECC71"), run_time=1.0)
        synced_wait(22.0) # "Thế nhưng, chiếc bẫy thống kê vẫn hoạt động... Thủy vân vẫn tồn tại!"
        
        # Bước 5: Thông điệp kết luận cuối
        conclusion_box = MarkupText(
            "Robustness càng cao, Watermark càng khó bị xóa bỏ!", 
            font="CMU Serif", font_size=28, color="#F4D160", weight="BOLD"
        )
        box = SurroundingRectangle(conclusion_box, color="#F4D160", buff=0.3, corner_radius=0.2)
        final_group = VGroup(box, conclusion_box).to_edge(DOWN, buff=0.5)
        
        self.play(Create(box), Write(conclusion_box), run_time=1.5)
        synced_wait(16.0) # "Đó chính là giá trị của một hệ thống có độ bền vững cao..."
        
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_2_3(scene: Scene) -> None:
    Scene2_2_3_Robustness.construct(scene)
