from manim import *
import numpy as np
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_3(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_3.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("DETECTGPT & FAST-DETECTGPT", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 3.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Điển hình rực rỡ nhất cho hướng tiếp cận..."
    scene.wait(8)
    # ---------------------------------------------------------

    # 2. PROBABILITY CURVATURE HYPOTHESIS
    axes = Axes(
        x_range=[0, 10, 1], y_range=[0, 10, 2], 
        x_length=8, y_length=3.5, 
        axis_config={"color": WHITE, "include_numbers": False}
    ).move_to(DOWN * 1.5)
    
    y_label = VGText("Log p(x)", font_size=16, color=WHITE).next_to(axes.y_axis, UP)
    x_label = VGText("Text Samples", font_size=16, color=WHITE).next_to(axes.x_axis, RIGHT)
    
    # Create a single continuous landscape (Mountain peak + Bumpy hills)
    # y = 4 + 4*exp(-1.0 * (x-2)^2) + 1.0*sin(3*x)
    curve = axes.plot(lambda x: 4 + 4*np.exp(-1.0 * (x-2)**2) + 1.0*np.sin(3*x), color=WHITE, x_range=[0, 9])
    
    scene.play(Create(axes), Write(y_label), Write(x_label), run_time=1.0)
    scene.play(Create(curve), run_time=1.5)

    # "Giả sử bạn đang đứng trên một đỉnh núi, đỉnh núi này tượng trưng cho một đoạn văn bản do chính AI viết ra..."
    ai_doc = Rectangle(width=1.0, height=1.4, color=VG_RED, fill_opacity=0.2).move_to(LEFT * 5.0 + UP * 1.5)
    ai_doc_lbl = VGText("AI Text\n(Original)", font_size=12, color=WHITE).move_to(ai_doc.get_center())
    ai_group = VGroup(ai_doc, ai_doc_lbl)
    
    scene.play(FadeIn(ai_group, shift=RIGHT), run_time=1.0)
    
    # Calculate exact peak coordinates for our new function near x=2
    # f(2) = 4 + 4*1 + 1.0*sin(6) = 8 - 0.279 = 7.72
    peak_x, peak_y = 2.0, 4 + 4*np.exp(0) + 1.0*np.sin(6)
    p_fake = Dot(axes.c2p(peak_x, peak_y), color=VG_RED, radius=0.1)
    p_fake_glow = p_fake.copy().set_color(VG_RED).set_opacity(0.4).scale(3)
    lbl_fake = VGText("Local Maxima", font_size=12, color=VG_RED).next_to(p_fake, UP)
    
    arrow_to_peak = Arrow(ai_doc.get_right(), p_fake.get_top() + UP*0.2, color=VG_RED, path_arc=-0.5)
    
    scene.play(Create(arrow_to_peak), FadeIn(p_fake_glow), FadeIn(p_fake), FadeIn(lbl_fake), run_time=1.0)
    scene.play(Wiggle(p_fake_glow), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "thường nằm chễm chệ ngay tại đỉnh dốc..."
    scene.wait(6)
    # ---------------------------------------------------------

    # "...Nếu ta rung lắc câu văn này bằng cách thay đổi một vài từ (Perturbation)..."
    perturb_lbl = VGText("Perturbations\n(Change words)", font_size=10, color=VG_GOLD).next_to(ai_doc, DOWN)
    scene.play(Wiggle(ai_group), FadeIn(perturb_lbl), run_time=1.0)
    
    # Spawn 4 smaller documents from the AI doc
    pert_docs = VGroup(*[Rectangle(width=0.4, height=0.6, color=VG_GOLD, fill_opacity=0.2).move_to(ai_doc.get_center()) for _ in range(4)])
    
    # Points falling down from the peak: x = 1.0, 2.5, 0.5, 3.0
    x_vals_fake = [1.0, 2.8, 0.5, 3.5]
    y_vals_fake = [4 + 4*np.exp(-1.0 * (x-2)**2) + 1.0*np.sin(3*x) for x in x_vals_fake]
    
    p_fake_perturbs = VGroup(*[
        Dot(axes.c2p(x, y), color=VG_GOLD, radius=0.06) for x, y in zip(x_vals_fake, y_vals_fake)
    ])
    
    # Animate documents flying to the graph points
    scene.play(
        LaggedStart(*[
            doc.animate.move_to(axes.c2p(x, peak_y)).set_opacity(0.8) 
            for doc, x in zip(pert_docs, x_vals_fake)
        ], lag_ratio=0.1),
        run_time=1.5
    )
    
    arrows_fake = VGroup(*[Arrow(p_fake.get_center(), p.get_center(), color=VG_RED, buff=0.1, tip_length=0.15) for p in p_fake_perturbs])
    
    scene.play(
        ReplacementTransform(pert_docs, p_fake_perturbs),
        Create(arrows_fake),
        run_time=1.0
    )
        
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "xác suất tổng thể lập tức cắm đầu tuột dốc..."
    scene.wait(6)
    # ---------------------------------------------------------

    # "...Trong khi đó, văn bản của con người nằm ở các vùng trũng ngẫu nhiên..."
    human_doc = Rectangle(width=1.0, height=1.4, color=VG_GREEN, fill_opacity=0.2).move_to(RIGHT * 5.0 + UP * 1.5)
    human_doc_lbl = VGText("Human Text\n(Original)", font_size=12, color=WHITE).move_to(human_doc.get_center())
    human_group = VGroup(human_doc, human_doc_lbl)
    
    real_x = 7.5
    real_y = 4 + 4*np.exp(-1.0 * (real_x-2)**2) + 1.0*np.sin(3*real_x)
    p_real = Dot(axes.c2p(real_x, real_y), color=VG_GREEN, radius=0.1)
    p_real_glow = p_real.copy().set_color(VG_GREEN).set_opacity(0.4).scale(3)
    lbl_real = VGText("Random Region", font_size=12, color=VG_GREEN).next_to(p_real, DOWN)
    
    arrow_to_real = Arrow(human_doc.get_left(), p_real.get_top() + UP*0.2, color=VG_GREEN, path_arc=0.5)
    
    scene.play(FadeIn(human_group, shift=LEFT), run_time=1.0)
    scene.play(Create(arrow_to_real), FadeIn(p_real_glow), FadeIn(p_real), FadeIn(lbl_real), run_time=1.0)

    # "...việc rung lắc sẽ không làm thay đổi đáng kể cấu trúc xác suất."
    scene.play(Wiggle(human_group), run_time=1.0)
    
    h_pert_docs = VGroup(*[Rectangle(width=0.4, height=0.6, color=VG_GOLD, fill_opacity=0.2).move_to(human_doc.get_center()) for _ in range(3)])
    
    x_vals_real = [7.0, 8.2, 6.5]
    y_vals_real = [4 + 4*np.exp(-1.0 * (x-2)**2) + 1.0*np.sin(3*x) for x in x_vals_real]
    p_real_perturbs = VGroup(*[
        Dot(axes.c2p(x, y), color=VG_GOLD, radius=0.06) for x, y in zip(x_vals_real, y_vals_real)
    ])
    
    scene.play(
        LaggedStart(*[
            doc.animate.move_to(axes.c2p(x, real_y)).set_opacity(0.8) 
            for doc, x in zip(h_pert_docs, x_vals_real)
        ], lag_ratio=0.1),
        run_time=1.5
    )
    
    arrows_real = VGroup(*[Arrow(p_real.get_center(), p.get_center(), color=VG_GREEN, buff=0.1, tip_length=0.15) for p in p_real_perturbs])
    
    scene.play(
        ReplacementTransform(h_pert_docs, p_real_perturbs),
        Create(arrows_real),
        run_time=1.0
    )
    scene.play(Wiggle(p_real_perturbs), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "văn bản con người rải rác ở vùng trũng..."
    scene.wait(6.0)
    # ---------------------------------------------------------

    # Clear axes for Fast-DetectGPT
    scene.play(
        FadeOut(axes), FadeOut(y_label), FadeOut(x_label), FadeOut(curve),
        FadeOut(p_fake), FadeOut(p_fake_glow), FadeOut(lbl_fake), FadeOut(p_fake_perturbs), FadeOut(arrows_fake),
        FadeOut(p_real), FadeOut(p_real_glow), FadeOut(lbl_real), FadeOut(p_real_perturbs), FadeOut(arrows_real),
        FadeOut(ai_group), FadeOut(arrow_to_peak), FadeOut(perturb_lbl),
        FadeOut(human_group), FadeOut(arrow_to_real),
        run_time=1.0
    )

    # 3. DETECTGPT VS FAST-DETECTGPT
    # "...Tuy nhiên, DetectGPT yêu cầu một mô hình phụ như T5 để tạo nhiễu, khiến quá trình đánh giá trở nên cực kỳ chậm chạp."
    d_box = RoundedRectangle(width=4.0, height=2.0, color=VG_BLUE).move_to(LEFT * 3.0)
    d_lbl = VGText("DetectGPT", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).next_to(d_box, UP)
    d_t5 = Rectangle(width=1.5, height=0.6, color=VG_GRAY, fill_opacity=0.3).move_to(d_box.get_center() + UP*0.4)
    d_t5_lbl = VGText("T5 Perturb\n(Slow)", font_size=12, color=WHITE).move_to(d_t5.get_center())
    d_score = Rectangle(width=1.5, height=0.6, color=VG_GOLD, fill_opacity=0.3).move_to(d_box.get_center() + DOWN*0.4)
    d_score_lbl = VGText("GPT Score", font_size=12, color=WHITE).move_to(d_score.get_center())
    d_arrow = Arrow(d_t5.get_bottom(), d_score.get_top(), color=WHITE)
    
    detect_group = VGroup(d_box, d_lbl, d_t5, d_t5_lbl, d_score, d_score_lbl, d_arrow)
    scene.play(FadeIn(detect_group, shift=RIGHT), run_time=1.0)
    
    # Show it being slow
    clock = Text("⏳", font_size=24).next_to(d_t5, RIGHT)
    scene.play(FadeIn(clock), run_time=0.5)
    scene.play(Rotate(clock, angle=-PI), run_time=2.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "khiến tốc độ dò tìm chậm đi hàng chục lần"
    scene.wait(7.0)
    # ---------------------------------------------------------

    # "...Để khắc phục, Fast-DetectGPT được giới thiệu tại ICLR 2024."
    f_box = RoundedRectangle(width=4.0, height=2.0, color=VG_GREEN).move_to(RIGHT * 3.0)
    f_box_glow = f_box.copy().set_fill(opacity=0).set_stroke(VG_GREEN, width=10, opacity=0.3)
    f_lbl = VGText("Fast-DetectGPT", font_size=18, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(f_box, UP)
    f_cond = Rectangle(width=2.5, height=0.8, color=VG_RED, fill_opacity=0.3).move_to(f_box.get_center())
    f_cond_lbl = VGText("Conditional Probability\nCurvature\n(Fast, No T5)", font_size=12, color=WHITE).move_to(f_cond.get_center())
    
    fast_group = VGroup(f_box, f_box_glow, f_lbl, f_cond, f_cond_lbl)
    scene.play(FadeIn(fast_group, shift=LEFT), run_time=1.0)
    
    # Lightning effect
    lightning = Text("⚡", font_size=36).next_to(f_lbl, RIGHT)
    scene.play(FadeIn(lightning, scale=1.5), flash_color=VG_GOLD, run_time=0.5)
    scene.play(Wiggle(lightning), run_time=0.5)

    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "đẩy tốc độ phát hiện lên chớp nhoáng..."
    scene.wait(19.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
