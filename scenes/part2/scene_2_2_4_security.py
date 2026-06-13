import os
import random
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

class Scene2_2_4_Security_Unforgeability(Scene):
    def construct(self):
        current_dir = os.path.dirname(__file__)
        start_time = self.renderer.time
        voice_path = os.path.join(current_dir, "assets", "voice_2_2_4.mp3").replace("\\", "/")
        voice_duration = _get_audio_duration(voice_path)
        if voice_duration is not None:
            with open("audio_times.txt", "a", encoding="utf-8") as f:
                f.write(f"{voice_path}|{start_time}\n")

        total_anim_time = 18.0
        total_expected_wait = 137.0
        scale_factor = max(0.0, voice_duration - total_anim_time) / total_expected_wait if voice_duration else 1.0
        
        def synced_wait(time_to_wait):
            if scale_factor > 0:
                self.wait(time_to_wait * scale_factor)

        # Bước 1: Tiêu đề & Định nghĩa
        title = MarkupText("4. SECURITY &amp; UNFORGEABILITY (BẢO MẬT &amp; CHỐNG GIẢ MẠO)", font="CMU Serif", font_size=24, weight="BOLD", color="#F4D160")
        subtitle = MarkupText("Khả năng chống thám mã khóa bí mật và chống gài bẫy giả mạo", font="CMU Serif", font_size=20, color=WHITE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        
        self.play(Write(title_group), run_time=1.5)
        synced_wait(20.0) # "Mảnh ghép cuối cùng... những kẻ thám mã chuyên nghiệp."

        # Bước 2: Mô phỏng đòn tấn công Thám mã - Brute-force/Spoofing
        left_sim = VGroup()
        
        # Vẽ biểu tượng ổ khóa (Padlock) bằng các hình cơ bản
        lock_body = Rectangle(width=0.8, height=0.6, color="#E74C3C", fill_opacity=1)
        lock_shackle = Arc(radius=0.3, start_angle=0, angle=PI, color="#E74C3C", stroke_width=6)
        lock_shackle.next_to(lock_body, UP, buff=0).shift(DOWN*0.1)
        lock_hole = Circle(radius=0.1, color=BLACK, fill_opacity=1).move_to(lock_body.get_center())
        lock_icon = VGroup(lock_shackle, lock_body, lock_hole).scale(0.8)
        
        secret_box = Rectangle(width=2.5, height=2.0, color="#E74C3C", fill_opacity=0.2, stroke_width=2)
        secret_text = MarkupText("SECRET KEY", font="CMU Serif", font_size=20, color="#E74C3C")
        
        secret_content = VGroup(lock_icon, secret_text).arrange(DOWN, buff=0.2)
        secret_content.move_to(secret_box.get_center())
        secret_group = VGroup(secret_box, secret_content).move_to(LEFT * 4 + ORIGIN)
        
        binary_str = MarkupText("01101001...", font="Courier New", font_size=20, color="#2ECC71")
        binary_str.next_to(secret_group, RIGHT, buff=1.6)
        
        arrow_brute = Arrow(binary_str.get_left(), secret_box.get_right(), buff=0.1, color=WHITE)
        brute_label = MarkupText("Brute-force", font="CMU Serif", font_size=18, color=WHITE).next_to(arrow_brute, UP, buff=0.1)
        
        self.play(FadeIn(secret_group, shift=UP*0.2), run_time=1.0)
        self.play(FadeIn(binary_str), GrowArrow(arrow_brute), FadeIn(brute_label), run_time=1.5)
        
        # Hiệu ứng chạy nhị phân thay đổi liên tục
        def update_binary(mob):
            s = "".join([str(random.randint(0,1)) for _ in range(8)]) + "..."
            mob.become(MarkupText(s, font="Courier New", font_size=20, color="#2ECC71").move_to(mob.get_center()))
            
        binary_str.add_updater(update_binary)
        self.wait(2.0)
        binary_str.remove_updater(update_binary)
        
        synced_wait(20.0) # "Tuyến tấn công thứ nhất đánh vào tính Bảo mật... chiếm đoạt cho bằng được chiếc chìa khóa bí mật."
        
        cross = Cross(binary_str, stroke_color="#E74C3C", stroke_width=6)
        cross_label = MarkupText("Thất bại (High Entropy)", font="CMU Serif", font_size=16, color="#E74C3C").next_to(cross, DOWN, buff=0.2)
        
        self.play(Create(cross), Write(cross_label), run_time=1.0)
        synced_wait(15.0) # "Một hệ thống có tính bảo mật cao phải sở hữu không gian khóa... bất khả thi và bị đẩy lùi hoàn toàn."
        
        left_sim.add(secret_group, binary_str, arrow_brute, brute_label, cross, cross_label)
        
        # Bước 3: Mô phỏng đòn tấn công Đổ oan - Framing Attack
        right_sim = VGroup()
        malicious_box = Rectangle(width=3.0, height=1.5, color="#E74C3C", stroke_width=3)
        malicious_text = MarkupText("Văn bản\nĐộc hại\n(Tin giả)", font="CMU Serif", font_size=22, color=WHITE, justify=True)
        malicious_text.move_to(malicious_box.get_center())
        malicious_group = VGroup(malicious_box, malicious_text).move_to(RIGHT * 4 + UP * 0.8)
        
        self.play(FadeIn(malicious_group, shift=UP*0.2), run_time=1.0)
        self.play(Flash(malicious_box, color="#E74C3C", line_length=0.2, flash_radius=2.0), run_time=1.0)
        
        inject_text = MarkupText("+ Từ Xanh giả", font="CMU Serif", font_size=18, color="#2ECC71")
        inject_text.next_to(malicious_group, UP, buff=0.2)
        self.play(Write(inject_text), run_time=1.0)
        synced_wait(28.0) # "Tuyến tấn công thứ hai còn độc hại và nguy hiểm hơn... nhằm hủy hoại uy tín nhà phát triển."
        
        validator_box = Rectangle(width=2.5, height=1.0, color="#3498DB", fill_opacity=0.2)
        validator_text = MarkupText("REAL VALIDATOR", font="CMU Serif", font_size=18, color="#3498DB")
        validator_text.move_to(validator_box.get_center())
        validator_group = VGroup(validator_box, validator_text).next_to(malicious_group, DOWN, buff=0.8)
        
        arrow_val = Arrow(malicious_box.get_bottom(), validator_box.get_top(), buff=0.1, color=WHITE)
        
        self.play(FadeIn(validator_group), GrowArrow(arrow_val), run_time=1.0)
        
        z_score_text = MarkupText("z-score = 1.2", font="CMU Serif", font_size=20, color="#E74C3C")
        z_score_text.next_to(validator_group, DOWN, buff=0.2)
        reject_text = MarkupText("FORGERY REJECTED\n(BÁO CÁO GIẢ MẠO BỊ HỦY)", font="CMU Serif", font_size=16, color="#E74C3C", justify=True)
        reject_text.next_to(z_score_text, DOWN, buff=0.1)
        
        self.play(Write(z_score_text), run_time=1.0)
        self.play(FadeIn(reject_text, shift=UP*0.1), run_time=1.0)
        synced_wait(21.0) # "Tiêu chí Unforgeability... dứt khoát đưa ra phán quyết hủy bỏ báo cáo giả mạo."
        
        right_sim.add(malicious_group, inject_text, validator_group, arrow_val, z_score_text, reject_text)
        
        # Bước 4: Thông điệp kết luận tổng kết 4 tiêu chí
        self.play(
            left_sim.animate.scale(0.8).shift(LEFT*0.5 + UP*0.5),
            right_sim.animate.scale(0.8).shift(RIGHT*0.5 + UP*0.5),
            run_time=1.5
        )
        
        conclusion_box = MarkupText(
            "Bảo mật hoàn hảo là khi không ai có thể\nlàm giả thủy vân nếu không sở hữu khóa!", 
            font="CMU Serif", font_size=26, color="#F4D160", weight="BOLD", justify=True
        )
        box = SurroundingRectangle(conclusion_box, color="#F4D160", buff=0.3, corner_radius=0.2)
        final_group = VGroup(box, conclusion_box).to_edge(DOWN, buff=0.3)
        
        self.play(Create(box), Write(conclusion_box), run_time=1.5)
        synced_wait(10.0) # "Bảo mật hoàn hảo là khi không một ai có thể làm giả được dấu vết thủy vân nếu họ không thực sự cầm trong tay chiếc chìa khóa chính quy."
        synced_wait(23.0) # "Khi cả bốn mảnh ghép: Chất lượng giữ vững... lại vừa giữ cho không gian mạng luôn an toàn và minh bạch."
        
        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(3.0)

        # Dọn dẹp tài nguyên
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)

def play_scene_2_2_4(scene: Scene) -> None:
    Scene2_2_4_Security_Unforgeability.construct(scene)
