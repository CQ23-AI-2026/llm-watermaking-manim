from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_5_2(scene: Scene):
    current_dir = os.path.dirname(__file__)
    voice_file = os.path.join(current_dir, "assets", "voice_5_2.mp3")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("TIÊU CHUẨN ĐÁNH GIÁ & CÔNG CỤ", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).to_edge(UP, buff=0.4)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Để đưa các nghiên cứu lý thuyết vào thực tiễn..."
    scene.wait(4.5)
    # ---------------------------------------------------------

    # 2. BENCHMARKS SECTION
    bench_subtitle = VGText("Các bộ Benchmarks chuẩn hóa", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 1.5)
    scene.play(FadeIn(bench_subtitle, shift=DOWN), run_time=1.0)

    # Thẻ 1: Mark My Words
    card_width = 3.2
    card_height = 1.6
    card_style = {"fill_opacity": 0.15, "stroke_width": 2, "corner_radius": 0.1}

    card1 = RoundedRectangle(color=VG_BLUE, width=card_width, height=card_height, **card_style).move_to(LEFT * 4.0 + DOWN * 0.2)
    label1 = VGText("Mark My Words", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(card1.get_top() + DOWN * 0.4)
    desc1 = VGText("Đánh giá thuật toán", font_size=12, color=WHITE).move_to(card1.get_center() + DOWN * 0.25)
    g1 = VGroup(card1, label1, desc1)

    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Đầu tiên là các bộ Benchmarks... Mark My Words,"
    scene.wait(0.5)
    # ---------------------------------------------------------
    scene.play(FadeIn(g1, shift=RIGHT), run_time=1.0)

    # Thẻ 2: WaterBench
    card2 = RoundedRectangle(color=VG_GREEN, width=card_width, height=card_height, **card_style).move_to(DOWN * 0.2)
    label2 = VGText("WaterBench", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(card2.get_top() + DOWN * 0.4)
    desc2 = VGText("(ACL 2024)", font_size=12, color=WHITE).move_to(card2.get_center() + DOWN * 0.25)
    g2 = VGroup(card2, label2, desc2)

    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "...WaterBench được giới thiệu tại ACL 2024,"
    scene.wait(2.0)
    # ---------------------------------------------------------
    scene.play(FadeIn(g2, shift=UP), run_time=1.0)

    # Thẻ 3: WaterJudge
    card3 = RoundedRectangle(color=VG_RED, width=card_width, height=card_height, **card_style).move_to(RIGHT * 4.0 + DOWN * 0.2)
    label3 = VGText("WaterJudge", font_size=16, color=VG_RED, weight=BOLD_WEIGHT).move_to(card3.get_top() + DOWN * 0.4)
    desc3 = VGText("(NAACL 2024)", font_size=12, color=WHITE).move_to(card3.get_center() + DOWN * 0.25)
    g3 = VGroup(card3, label3, desc3)

    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "...và WaterJudge từ NAACL 2024."
    scene.wait(2.5)
    # ---------------------------------------------------------
    scene.play(FadeIn(g3, shift=LEFT), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "Những bộ Benchmarks này giúp đo lường một cách chính xác sự suy giảm chất lượng (Quality degradation)..."
    scene.wait(5.0)
    # ---------------------------------------------------------
    
    # Trade-off animation
    tradeoff_box = RoundedRectangle(color=VG_GOLD, width=6.0, height=1.5, fill_opacity=0.1, stroke_width=2).move_to(DOWN * 2.2)
    tradeoff_lbl = VGText("Trade-off", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(tradeoff_box.get_top() + DOWN * 0.3)
    
    quality_lbl = VGText("Text Quality", font_size=14, color=VG_RED).move_to(tradeoff_box.get_center() + LEFT * 1.5 + DOWN * 0.2)
    detect_lbl = VGText("Detectability", font_size=14, color=VG_GREEN).move_to(tradeoff_box.get_center() + RIGHT * 1.5 + DOWN * 0.2)
    
    scene.play(FadeIn(tradeoff_box), FadeIn(tradeoff_lbl), run_time=1.0)
    scene.play(FadeIn(quality_lbl, shift=DOWN), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "đồng thời đánh giá sự cân bằng (Trade-off) giữa Quality và Detectability."
    scene.wait(3.0)
    # ---------------------------------------------------------
    scene.play(FadeIn(detect_lbl, shift=UP), run_time=1.0)

    # Wiggle/balance animation
    scene.play(
        quality_lbl.animate.shift(UP * 0.2),
        detect_lbl.animate.shift(DOWN * 0.2),
        run_time=0.5
    )
    scene.play(
        quality_lbl.animate.shift(DOWN * 0.4),
        detect_lbl.animate.shift(UP * 0.4),
        run_time=0.5
    )
    scene.play(
        quality_lbl.animate.shift(UP * 0.2),
        detect_lbl.animate.shift(DOWN * 0.2),
        run_time=0.5
    )

    # Clear Benchmarks for MarkLLM
    scene.wait(1.0)
    scene.play(
        FadeOut(bench_subtitle), FadeOut(g1), FadeOut(g2), FadeOut(g3),
        FadeOut(tradeoff_box), FadeOut(tradeoff_lbl), FadeOut(quality_lbl), FadeOut(detect_lbl),
        run_time=1.0
    )

    # ---------------------------------------------------------
    # 3. MARKLLM TOOLKIT SECTION
    # ---------------------------------------------------------
    markllm_title = VGText("MarkLLM: Bộ công cụ mã nguồn mở", font_size=22, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 1.5)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi đọc "Nổi bật nhất trong số đó là MarkLLM..."
    scene.wait(2.0)
    # ---------------------------------------------------------
    scene.play(Write(markllm_title), run_time=1.0)

    # Central Hub
    hub_box = RoundedRectangle(color=VG_GOLD, width=3.5, height=1.2, fill_opacity=0.2, stroke_width=3, corner_radius=0.15).move_to(DOWN * 0.2)
    hub_text = VGText("MarkLLM Toolkit", font_size=20, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(hub_box.get_center())
    hub = VGroup(hub_box, hub_text)
    scene.play(FadeIn(hub, scale=0.5), run_time=1.0)

    # ---------------------------------------------------------
    # [WAIT_SYNC_8]: Đợi đọc "MarkLLM cung cấp một Unified Framework..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    # Branch 1: Unified Framework
    branch_width = 3.6
    branch_height = 1.0
    b1_box = RoundedRectangle(color=VG_BLUE, width=branch_width, height=branch_height, **card_style).move_to(LEFT * 4.2 + UP * 0.5)
    b1_text = VGText("Unified Framework", font_size=14, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(b1_box.get_center())
    b1 = VGroup(b1_box, b1_text)
    
    l_b1 = DashedLine(hub_box.get_left(), b1_box.get_right(), color=VG_BLUE).set_z_index(-1)
    
    scene.play(Create(l_b1), run_time=0.5)
    scene.play(FadeIn(b1, shift=LEFT), run_time=0.5)

    # Popups for KGW, Christ
    pop1 = VGText("[KGW]", font_size=12, color=WHITE).next_to(b1_box, UP, buff=0.1).shift(LEFT * 0.5)
    pop2 = VGText("[Christ]", font_size=12, color=WHITE).next_to(b1_box, UP, buff=0.1).shift(RIGHT * 0.5)
    scene.play(FadeIn(pop1, shift=UP), run_time=0.5)
    scene.play(FadeIn(pop2, shift=UP), run_time=0.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_9]: Đợi đọc "MarkLLM không chỉ giúp trực quan hóa cơ chế hoạt động qua Mechanism Visualization..."
    scene.wait(4.5)
    # ---------------------------------------------------------

    # Branch 2: Mechanism Visualization
    b2_box = RoundedRectangle(color=VG_GREEN, width=branch_width, height=branch_height, **card_style).move_to(DOWN * 2.0)
    b2_text = VGText("Mechanism Visualization", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(b2_box.get_center())
    b2 = VGroup(b2_box, b2_text)
    
    l_b2 = DashedLine(hub_box.get_bottom(), b2_box.get_top(), color=VG_GREEN).set_z_index(-1)

    scene.play(Create(l_b2), run_time=0.5)
    scene.play(FadeIn(b2, shift=DOWN), run_time=0.5)

    # Animate a magnifying glass icon instead of an emoji
    mag_glass_circle = Circle(radius=0.15, color=VG_GREEN, stroke_width=2).move_to(b2_box.get_center() + DOWN * 0.15)
    mag_glass_handle = Line(
        mag_glass_circle.get_corner(DOWN + RIGHT),
        mag_glass_circle.get_corner(DOWN + RIGHT) + DOWN * 0.15 + RIGHT * 0.15,
        color=VG_GREEN, stroke_width=3
    )
    mag_glass = VGroup(mag_glass_circle, mag_glass_handle)
    
    b2_text.generate_target()
    b2_text.target.move_to(b2_box.get_center() + UP * 0.2)
    scene.play(MoveToTarget(b2_text), FadeIn(mag_glass), run_time=0.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_10]: Đợi đọc "...mà còn cung cấp luồng Automated Evaluation đa chiều, đo lường toàn diện từ Detectability..."
    scene.wait(4.5)
    # ---------------------------------------------------------

    # Branch 3: Automated Evaluation
    b3_box = RoundedRectangle(color=VG_RED, width=branch_width, height=branch_height + 0.5, **card_style).move_to(RIGHT * 4.2 + DOWN * 0.5)
    b3_text = VGText("Automated Evaluation", font_size=14, color=VG_RED, weight=BOLD_WEIGHT).move_to(b3_box.get_top() + DOWN * 0.3)
    b3 = VGroup(b3_box, b3_text)

    l_b3 = DashedLine(hub_box.get_right(), b3_box.get_left(), color=VG_RED).set_z_index(-1)

    scene.play(Create(l_b3), run_time=0.5)
    scene.play(FadeIn(b3, shift=RIGHT), run_time=0.5)

    # Progress bars pop up sequentially
    def make_bar(label_str, fill_ratio, color):
        lbl = VGText(label_str, font_size=12, color=WHITE)
        bg = Rectangle(width=1.0, height=0.1, color=WHITE, fill_opacity=0.2, stroke_width=0)
        fg = Rectangle(width=1.0 * fill_ratio, height=0.1, color=color, fill_opacity=1, stroke_width=0)
        bg.next_to(lbl, RIGHT, buff=0.2)
        fg.move_to(bg, aligned_edge=LEFT)
        return VGroup(lbl, bg, fg)

    pb1 = make_bar("Detectability", 0.8, VG_GREEN).move_to(b3_box.get_center() + UP * 0.15)
    pb2 = make_bar("Robustness", 0.9, VG_BLUE).next_to(pb1, DOWN, buff=0.15, aligned_edge=LEFT)
    pb3 = make_bar("Text Quality", 0.6, VG_RED).next_to(pb2, DOWN, buff=0.15, aligned_edge=LEFT)

    scene.play(Write(pb1), run_time=0.8)
    
    # "...Robustness chống tấn công..."
    scene.wait(1.5)
    scene.play(Write(pb2), run_time=0.8)
    
    # "...cho đến Text Quality thực tế."
    scene.wait(2.0)
    scene.play(Write(pb3), run_time=0.8)

    # ---------------------------------------------------------
    # [WAIT_SYNC_11]: Đợi kết thúc câu
    scene.wait(2.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
