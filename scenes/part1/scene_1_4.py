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

class Scene1_4_Ideal_Properties(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "voice", "voice_1_4.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 15.0
        total_expected_wait = 70.0  # Ước lượng thời gian chờ
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Giai đoạn 1: Tiêu đề & Bố cục
        title = MarkupText("1.4 BỐN TÍNH CHẤT LÝ TƯỞNG CỦA WATERMARK", font="CMU Serif", font_size=28, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)

        # Tạo 4 khối
        props = [
            ("Quality", "Chất lượng văn bản", BLUE),
            ("Detection Accuracy", "Độ chính xác", GREEN),
            ("Robustness", "Độ bền vững", ORANGE),
            ("Security", "Tính bảo mật", PURPLE)
        ]
        
        boxes = VGroup()
        for title_text, sub_text, color in props:
            box = RoundedRectangle(width=4.0, height=2.0, corner_radius=0.3, color=color, fill_opacity=1.0)
            main_label = MarkupText(title_text, font="CMU Serif", font_size=26, weight="BOLD").move_to(box.get_center() + UP*0.2)
            sub_label = MarkupText(sub_text, font="CMU Serif", font_size=20, color=LIGHT_GRAY).next_to(main_label, DOWN, buff=0.2)
            group = VGroup(box, main_label, sub_label)
            boxes.add(group)
            
        boxes.arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.8)).shift(DOWN*0.5)
        
        # Ban đầu mờ
        for box in boxes:
            box.set_opacity(0.3)
            
        self.play(FadeIn(boxes, shift=UP*0.3), run_time=1.5)
        synced_wait(15.0)
        
        # Giai đoạn 2: Hiệu ứng Điểm nhấn tuần tự
        wait_times = [10.0, 10.0, 10.0, 10.0]
        for i, box in enumerate(boxes):
            # Zoom in và highlight
            self.play(
                box.animate.scale(1.1).set_opacity(1.0),
                run_time=0.5
            )
            self.play(Indicate(box[0], color=box[0].get_color(), scale_factor=1.05), run_time=1.0)
            synced_wait(wait_times[i])
            
            # Khôi phục
            self.play(
                box.animate.scale(1/1.1).set_opacity(0.3),
                run_time=0.5
            )

        # Giai đoạn 3: Chuyển cảnh
        self.play(boxes.animate.set_opacity(1.0), run_time=1.0)
        synced_wait(12.0)
        
        self.play(
            boxes.animate.scale(0.5).set_opacity(0).move_to(ORIGIN),
            title.animate.set_opacity(0),
            run_time=1.5
        )

        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(2.0)
            
def play_part1_scene_1_4(scene: Scene) -> None:
    Scene1_4_Ideal_Properties.construct(scene)
