from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def _get_audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path): return None
    try:
        from mutagen.mp3 import MP3
        return float(MP3(path).info.length)
    except: pass
    try:
        from moviepy.editor import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except: pass
    return None

def play_scene_4_1(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_1.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)
    else:
        print(f"Warning: Voice file not found at {voice_file}")

    # 1. TITLE
    part_title = VGText("PHÁT HIỆN HẬU KIỂM", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc thời gian chờ sau khi hiện tiêu đề
    scene.wait(2.0) 
    # ---------------------------------------------------------

    # 2. KHÁM NGHIỆM HIỆN TRƯỜNG (Promax Design)
    # Lưới nền công nghệ cho cảm giác "khám nghiệm"
    grid = NumberPlane(
        background_line_style={"stroke_color": VG_BLUE, "stroke_width": 1, "stroke_opacity": 0.15},
        axis_config={"stroke_opacity": 0}
    ).set_z_index(-10)
    
    # Nhãn hồ sơ vụ án ở góc trái, không lấn chiếm màn hình
    concept_label_bg = Rectangle(width=4.0, height=0.6, color=VG_GOLD, fill_color=BLACK, fill_opacity=0.8)
    concept_label_text = VGText("HỒ SƠ VỤ ÁN #001", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(concept_label_bg.get_center())
    concept_label = VGroup(concept_label_bg, concept_label_text).to_edge(UP, buff=1.6).to_edge(LEFT, buff=0.5)

    scene.play(FadeIn(grid), FadeIn(concept_label, shift=RIGHT), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc câu "khám nghiệm hiện trường vụ án..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # 3. SLEEK DOCUMENT APPEARS (Văn bản đáng ngờ nằm ở giữa, thiết kế sang trọng)
    doc_rect = RoundedRectangle(corner_radius=0.15, width=3.2, height=4.2, color=WHITE, stroke_width=2, fill_color="#0A0A0A", fill_opacity=0.9).set_z_index(1)
    
    lines = VGroup()
    for i in range(8):
        line_w = 2.6 if i != 7 else 1.5
        l = Line(LEFT * line_w/2, RIGHT * line_w/2, color=VG_GRAY, stroke_width=3)
        lines.add(l)
    lines.arrange(DOWN, buff=0.35).move_to(doc_rect.get_center() + UP*0.2)
    
    doc_title = VGText("Văn bản đáng ngờ", font_size=14, color=WHITE, weight=BOLD_WEIGHT).next_to(lines, UP, buff=0.4)
    document = VGroup(doc_rect, doc_title, lines).set_z_index(1).shift(DOWN*0.3)

    # Khung HUD bao quanh document
    hud_frame = Rectangle(width=3.6, height=4.6, color=VG_BLUE, stroke_width=2).move_to(document.get_center()).set_z_index(0)
    hud_frame_dashes = DashedVMobject(hud_frame, num_dashes=30)
    
    scene.play(FadeIn(document, shift=UP), Create(hud_frame_dashes), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc câu "có trong tay đoạn văn bản đáng ngờ..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # 4. FORENSIC SCAN & WATERMARK NOT FOUND
    # Tia laser quét từ trên xuống dưới
    laser = Line(LEFT*1.8, RIGHT*1.8, color=VG_RED, stroke_width=3).move_to(document.get_top() + DOWN*0.1).set_z_index(2)
    laser_glow = laser.copy().set_stroke(VG_RED, width=10, opacity=0.4)
    scanner = VGroup(laser, laser_glow)

    scene.play(FadeIn(scanner), run_time=0.5)
    scene.play(scanner.animate.move_to(document.get_bottom() + UP*0.1), run_time=1.5, rate_func=there_and_back)
    scene.play(FadeOut(scanner), run_time=0.5)

    # Con dấu đỏ NO WATERMARK
    stamp_box = RoundedRectangle(corner_radius=0.1, width=3.8, height=1.2, color=VG_RED, stroke_width=4, fill_color=BLACK, fill_opacity=0.8).rotate(PI/12)
    stamp_text = VGText("NO WATERMARK", font_size=24, color=VG_RED, weight=BOLD_WEIGHT).move_to(stamp_box.get_center()).rotate(PI/12)
    stamp = VGroup(stamp_box, stamp_text).set_z_index(3)

    scene.play(FadeIn(stamp, scale=2.5), run_time=0.4)
    scene.play(stamp.animate.scale(0.9), run_time=0.15)
    scene.play(stamp.animate.scale(1.1), run_time=0.15)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đóng dấu và đọc xong câu "không hề có watermark..."
    scene.wait(3.0)
    # ---------------------------------------------------------

    # 5. TRANSITION TO OPENAI CLASSIFIER
    # Dọn dẹp các hiệu ứng khám nghiệm, chỉ giữ lại document thu nhỏ
    scene.play(
        FadeOut(concept_label), FadeOut(grid), FadeOut(hud_frame_dashes), FadeOut(stamp), 
        document.animate.scale(0.7).to_edge(LEFT, buff=1.5), 
        run_time=2.0
    )

    classifier_box = RoundedRectangle(corner_radius=0.2, width=2.5, height=2.5, color=VG_BLUE)
    eye1 = Circle(radius=0.2, color=VG_BLUE, fill_opacity=1).move_to(classifier_box.get_center() + UP*0.3 + LEFT*0.5)
    eye2 = Circle(radius=0.2, color=VG_BLUE, fill_opacity=1).move_to(classifier_box.get_center() + UP*0.3 + RIGHT*0.5)
    mouth = Line(LEFT*0.5, RIGHT*0.5, color=VG_BLUE, stroke_width=4).move_to(classifier_box.get_center() + DOWN*0.4)
    ai_bot = VGroup(classifier_box, eye1, eye2, mouth).to_edge(RIGHT, buff=2)
    bot_label = VGText("OpenAI Classifier", font_size=20, color=VG_BLUE).next_to(ai_bot, DOWN)
    
    scene.play(FadeIn(ai_bot, shift=LEFT), FadeIn(bot_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc câu "Sự thất bại của OpenAI Classifier..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # 6. SCANNING AND FAILING
    scan_beam = Polygon(
        ai_bot.get_left(), document.get_corner(UR), document.get_corner(DR),
        color=VG_GOLD, fill_opacity=0.2, stroke_width=0
    )
    scene.play(FadeIn(scan_beam), run_time=1.0)

    frown = ArcBetweenPoints(mouth.get_left(), mouth.get_right(), angle=PI/2, color=VG_RED, stroke_width=4)
    scene.play(
        eye1.animate.set_color(VG_RED), 
        eye2.animate.set_color(VG_RED),
        classifier_box.animate.set_color(VG_RED),
        Transform(mouth, frown),
        FadeOut(scan_beam),
        run_time=1.0
    )
    
    error_text = VGText("THẤT BẠI!", font_size=30, color=VG_RED, weight=BOLD_WEIGHT).next_to(ai_bot, UP)
    scene.play(Write(error_text), flash_color=VG_RED, run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "dừng hoạt động vì độ chính xác quá thấp..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # 7. STATISTICS BAR
    scene.play(FadeOut(document), FadeOut(ai_bot), FadeOut(bot_label), FadeOut(error_text), run_time=1.0)
    bar_bg = Rectangle(width=10, height=1.0, color=VG_GRAY, fill_opacity=0.3).move_to(DOWN * 0.5)
    scene.play(Create(bar_bg), run_time=1.0)

    correct_width = 10 * 0.26
    correct_bar = Rectangle(width=correct_width, height=1.0, color=VG_GREEN, fill_opacity=1.0, stroke_width=0)
    correct_bar.align_to(bar_bg, LEFT).move_to(bar_bg.get_center() + LEFT*(10 - correct_width)/2)
    correct_label = VGText("26% Nhận diện đúng", font_size=20, color=VG_GREEN).next_to(correct_bar, UP)

    scene.play(GrowFromEdge(correct_bar, LEFT), FadeIn(correct_label), run_time=2.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi đọc xong "chỉ nhận diện đúng 26%..."
    scene.wait(1.5)
    # ---------------------------------------------------------

    fp_width = 10 * 0.09
    fp_bar = Rectangle(width=fp_width, height=1.0, color=VG_RED, fill_opacity=1.0, stroke_width=0)
    fp_bar.next_to(correct_bar, RIGHT, buff=0)
    fp_label = VGText("9% Kết án oan", font_size=20, color=VG_RED).next_to(fp_bar, DOWN)

    scene.play(GrowFromEdge(fp_bar, LEFT), FadeIn(fp_label), run_time=1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_8]: Đợi đọc nốt đoạn cuối "kết án nhầm lên tới 9%..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
