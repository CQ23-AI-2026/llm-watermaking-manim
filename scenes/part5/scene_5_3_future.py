from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_3(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_3.mp3")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("5.3: KỶ NGUYÊN AI PROVENANCE", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Các nhà khoa học kiến tạo vũ khí hệ hệ mới..."
    scene.wait(2.0)
    # ---------------------------------------------------------

    # 1. Asymmetric Crypto
    crypto_title = VGText("1. Mã hóa bất đối xứng", font_size=20, color=VG_GOLD).move_to(UP*1.5 + LEFT*3.5)
    private_key = Text("🔑 Private", font_size=20, color=VG_RED).move_to(UP*0.5 + LEFT*4.5)
    public_key = Text("🔑 Public", font_size=20, color=VG_GREEN).move_to(UP*0.5 + LEFT*2.5)
    arrow = DoubleArrow(private_key.get_right(), public_key.get_left(), color=WHITE)
    
    scene.play(Write(crypto_title), FadeIn(private_key), FadeIn(public_key), Create(arrow), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Mã hóa bất đối xứng, công ty giữ khóa bí mật..."
    scene.wait(3.5)
    # ---------------------------------------------------------

    # 2. Semantic Hashing
    hash_title = VGText("2. Băm theo ngữ nghĩa", font_size=20, color=VG_BLUE).move_to(UP*1.5 + RIGHT*3.5)
    word_old = VGText("Chó", font_size=24, color=WHITE).move_to(UP*0.8 + RIGHT*3.5)
    word_new = VGText("Cún", font_size=24, color=WHITE).move_to(UP*0.8 + RIGHT*3.5)
    hash_code = VGText("Hash: 0x8F9A", font_size=16, color=VG_GREEN).move_to(UP*0.1 + RIGHT*3.5)
    
    scene.play(Write(hash_title), Write(word_old), FadeIn(hash_code), run_time=1.5)
    scene.play(Transform(word_old, word_new), flash_color=VG_GOLD, run_time=1.0)
    # Hash remains green and unchanged!

    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Gán nhãn lên ý nghĩa cốt lõi bất chấp đảo chữ..."
    scene.wait(3.5)
    # ---------------------------------------------------------

    # 3. AI Provenance MarkLLM
    scene.play(
        FadeOut(crypto_title), FadeOut(private_key), FadeOut(public_key), FadeOut(arrow),
        FadeOut(hash_title), FadeOut(word_old), FadeOut(hash_code),
        run_time=1.0
    )

    prov_title = VGText("3. Tiêu chuẩn toàn cầu", font_size=24, color=WHITE).move_to(UP*1.0)
    badge = RegularPolygon(n=6, radius=1.0, color=VG_GOLD, fill_opacity=0.2).move_to(DOWN*0.5)
    badge_inner = RegularPolygon(n=6, radius=0.8, color=VG_GOLD, stroke_width=2).move_to(badge.get_center())
    badge_text = VGText("MarkLLM", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(badge.get_center())
    
    badge_group = VGroup(badge, badge_inner, badge_text)
    
    scene.play(Write(prov_title), FadeIn(badge_group, scale=3.0), run_time=1.5)

    glow = badge.copy().set_fill(VG_GOLD, opacity=0.5).set_stroke(VG_GOLD, width=0)
    scene.play(glow.animate.scale(1.5).set_opacity(0), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Tiêu chuẩn toàn cầu, nhãn mác điện tử minh bạch..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # OUTRO
    scene.play(FadeOut(prov_title), FadeOut(badge_group), FadeOut(part_title), FadeOut(underline), run_time=1.5)
    
    outro1 = VGText("Bảo vệ sự thật", font_size=36, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP*0.5)
    outro2 = VGText("trong kỷ nguyên thông tin đại trà.", font_size=24, color=WHITE).next_to(outro1, DOWN, buff=0.3)
    
    scene.play(Write(outro1), run_time=2.0)
    scene.play(FadeIn(outro2, shift=UP), run_time=1.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Cuộc đua tạo ra AI... kỷ nguyên thông tin đại trà..."
    scene.wait(5.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=2.0)
