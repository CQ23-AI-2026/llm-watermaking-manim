from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_4(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_4.mp3")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("KỶ NGUYÊN AI PROVENANCE", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Để vượt qua những giới hạn đó, các hướng nghiên cứu tương lai đang mở ra Kỷ nguyên AI Provenance."
    scene.wait(4)
    # ---------------------------------------------------------

    # 2. ASYMMETRIC WATERMARKING SECTION
    crypto_title = VGText("Mã hóa bất đối xứng (Asymmetric)", font_size=18, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 1.5 + LEFT * 3.5)
    
    # "...Đó là việc áp dụng mã hóa bất đối xứng..."
    scene.play(Write(crypto_title), run_time=1.5)
    scene.wait(1.5)

    box_w, box_h = 3.0, 1.8
    style = {"fill_opacity": 0.15, "stroke_width": 2, "corner_radius": 0.1}

    private_box = RoundedRectangle(color=VG_RED, width=box_w, height=box_h, **style).move_to(LEFT * 5.0 + UP * 0.1)
    private_lbl = VGText("[Private Key]", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).move_to(private_box.get_top() + DOWN * 0.4)
    private_desc = VGText("Nhà phát triển giữ\nđể tạo Watermark", font_size=12, color=WHITE).move_to(private_box.get_center() + DOWN * 0.25)
    private_grp = VGroup(private_box, private_lbl, private_desc)

    # "...Private Key do nhà phát triển giữ để tạo Watermark,"
    scene.play(FadeIn(private_grp, shift=RIGHT), run_time=1.0)
    scene.wait(2.0)

    public_box = RoundedRectangle(color=VG_GREEN, width=box_w, height=box_h, **style).move_to(LEFT * 1.8 + UP * 0.1)
    public_lbl = VGText("[Public Key]", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(public_box.get_top() + DOWN * 0.4)
    public_desc = VGText("Cấp cho công chúng\nchỉ để kiểm tra", font_size=12, color=WHITE).move_to(public_box.get_center() + DOWN * 0.25)
    public_grp = VGroup(public_box, public_lbl, public_desc)

    # "...còn Public Key cấp cho công chúng chỉ để kiểm tra."
    scene.play(FadeIn(public_grp, shift=LEFT), run_time=1.0)
    scene.wait(2.0)

    # "...Hơn nữa, các kỹ thuật tương lai sẽ vượt qua rào cản từ ngữ."
    scene.wait(3.0)

    # Clear for Semantic Hashing
    scene.play(
        FadeOut(crypto_title), FadeOut(private_grp), FadeOut(public_grp),
        run_time=1.0
    )

    # 3. SEMANTIC HASHING SECTION
    hash_title = VGText("Băm theo ngữ nghĩa (Semantic Hashing)", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(UP * 1.5 + RIGHT * 3.5)
    
    # "...Đó là kỹ thuật băm ngữ nghĩa (Semantic Hashing)."
    scene.play(Write(hash_title), run_time=1.0)
    scene.wait(1.0)
    
    # Original word and its synonym
    word_1 = VGText('"Chó"', font_size=20, color=WHITE).move_to(RIGHT * 2.2 + UP * 0.2)
    word_2 = VGText('"Cún"', font_size=20, color=WHITE).move_to(RIGHT * 4.8 + UP * 0.2)
    
    # "...Cho dù bạn dùng từ 'Chó' hay từ đồng nghĩa là 'Cún',"
    scene.play(FadeIn(word_1, shift=DOWN), run_time=0.8)
    scene.wait(0.5)
    scene.play(FadeIn(word_2, shift=DOWN), run_time=0.8)
    scene.wait(1.0)

    h_box_1 = RoundedRectangle(color=VG_BLUE, width=1.6, height=0.8, **style).move_to(RIGHT * 2.2 + DOWN * 0.8)
    h_lbl_1 = VGText("0x8F9A", font_size=14, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(h_box_1.get_center())
    h_1 = VGroup(h_box_1, h_lbl_1)

    h_box_2 = RoundedRectangle(color=VG_BLUE, width=1.6, height=0.8, **style).move_to(RIGHT * 4.8 + DOWN * 0.8)
    h_lbl_2 = VGText("0x8F9A", font_size=14, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(h_box_2.get_center())
    h_2 = VGroup(h_box_2, h_lbl_2)

    arrow_h1 = Arrow(word_1.get_bottom(), h_1.get_top(), color=VG_GRAY)
    arrow_h2 = Arrow(word_2.get_bottom(), h_2.get_top(), color=VG_GRAY)
    equal_sign = VGText("=", font_size=24, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(RIGHT * 3.5 + DOWN * 0.8)

    # "...thì mã băm tạo ra vẫn hoàn toàn giống nhau."
    scene.play(Create(arrow_h1), Create(arrow_h2), run_time=0.5)
    scene.play(FadeIn(h_1), FadeIn(h_2), run_time=0.8)
    scene.play(Write(equal_sign), run_time=0.5)
    
    # "...Nhờ vậy, Watermark sẽ bền bỉ trước mọi nỗ lực paraphrase của kẻ gian."
    scene.wait(3.5)

    # Clear everything for OUTRO
    scene.play(
        FadeOut(hash_title), FadeOut(word_1), FadeOut(word_2),
        FadeOut(arrow_h1), FadeOut(arrow_h2), FadeOut(h_1), FadeOut(h_2),
        FadeOut(equal_sign), FadeOut(part_title), FadeOut(underline),
        run_time=1.5
    )

    # OUTRO TEXTS
    # "...Cuối cùng, LLM Watermarking không chỉ là một công cụ kỹ thuật..."
    outro1 = VGText("Bảo vệ sự thật", font_size=36, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 0.5)
    scene.play(Write(outro1), run_time=2.0)
    scene.wait(1.5)

    # "...mà là nền tảng để chúng ta bảo vệ sự thật và xây dựng niềm tin trong kỷ nguyên thông tin."
    outro2 = VGText("và xây dựng niềm tin trong kỷ nguyên thông tin.", font_size=20, color=WHITE).next_to(outro1, DOWN, buff=0.3)
    
    scene.play(FadeIn(outro2, shift=UP), run_time=1.5)
    
    # Mở rộng nhẹ (scale up) dần đều trong 6 giây để tạo cảm giác hoành tráng
    scene.play(
        outro1.animate.scale(1.05),
        outro2.animate.scale(1.05),
        run_time=6.0,
        rate_func=linear
    )

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)

    # Lời cảm ơn
    thanks = VGText("Cảm ơn bạn đã theo dõi!", font_size=32, color=VG_GOLD, weight=BOLD_WEIGHT)
    scene.play(Write(thanks), run_time=1.5)
    scene.wait(5)
    scene.play(FadeOut(thanks), run_time=1.0)
