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

class Scene2_1_6_Transition_Questions(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_1_6.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 12.0 # Sẽ tính toán chính xác tổng thời gian các lệnh play()
        total_expected_wait = 57.0 # Tổng thời gian các lệnh synced_wait()
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Màn hình tối tạo sự tò mò (Lắng nghe intro)
        synced_wait(14.0) # "Mô hình Xanh-Đỏ đã mở ra... lời giải đáp."

        # Bước 2 & 3: Khai báo 4 câu hỏi với MarkupText để tô màu từ khóa
        q1_text = '1. Lược đồ Watermark có luôn <span fgcolor="#F4D160">hoạt động ổn định</span>?'
        q2_text = '2. Có phương pháp nào <span fgcolor="#F4D160">tốt hơn</span> Green-Red không?'
        q3_text = '3. "Tốt hơn" nghĩa là gì? Cần <span fgcolor="#F4D160">tiêu chí đánh giá</span> nào?'
        q4_text = '4. <span fgcolor="#F4D160">Giới hạn tối ưu</span> của các hệ thống Watermark là bao nhiêu?'

        font_size = 36
        q1 = MarkupText(q1_text, font="CMU Serif", font_size=font_size, color=WHITE)
        q2 = MarkupText(q2_text, font="CMU Serif", font_size=font_size, color=WHITE)
        q3 = MarkupText(q3_text, font="CMU Serif", font_size=font_size, color=WHITE)
        q4 = MarkupText(q4_text, font="CMU Serif", font_size=font_size, color=WHITE)

        # Xếp chồng theo chiều dọc, căn lề trái
        questions_group = VGroup(q1, q2, q3, q4)
        questions_group.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        questions_group.move_to(ORIGIN)

        # Câu 1
        self.play(Write(q1), run_time=2.0)
        synced_wait(8.0) # "Một... Lược đồ Watermark này liệu có luôn hoạt động ổn định trong mọi ngữ cảnh đầu vào hay không?"

        # Câu 2
        self.play(Write(q2), run_time=2.0)
        synced_wait(9.0) # "Hai... Có phương pháp nào tốt hơn Green-Red..."

        # Câu 3
        self.play(Write(q3), run_time=2.0)
        # Phát sáng nhẹ từ khóa "tiêu chí đánh giá" (có thể dùng Wiggle hoặc Flash xung quanh)
        # Bằng cách sử dụng Indicate lên toàn bộ câu hoặc riêng từ khóa. Ở đây ta nhấp nháy toàn câu cho mượt.
        self.play(Indicate(q3, color="#F0A050", scale_factor=1.05), run_time=1.5)
        synced_wait(8.0) # "Ba... Khái niệm 'tốt hơn' ở đây thực chất nghĩa là gì?..."

        # Câu 4
        self.play(Write(q4), run_time=2.0)
        synced_wait(4.0) # "Và bốn... Giới hạn tối ưu... là bao nhiêu?"

        # Bước 4: Hiệu ứng tập trung kết cảnh (nhấn mạnh câu 3 và câu 4)
        focus_box = SurroundingRectangle(VGroup(q3, q4), color="#F4D160", buff=0.2)
        
        self.play(
            AnimationGroup(
                Create(focus_box),
                Indicate(q3, color="#F0A050"),
                Indicate(q4, color="#F0A050"),
                lag_ratio=0.3
            ),
            run_time=2.5
        )
        synced_wait(14.0) # "Để tìm lời giải cho những trăn trở này... thủy vân lý tưởng."
        
        # Audio wait bù trừ thời gian tự động
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        # Chuyển cảnh
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_1_6(scene: Scene) -> None:
    Scene2_1_6_Transition_Questions.construct(scene)
