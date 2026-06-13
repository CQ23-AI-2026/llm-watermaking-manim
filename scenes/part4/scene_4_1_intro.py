from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_1(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_0 = os.path.join(current_dir, "assets", "voice_4_0.mp3").replace("\\", "/")
    voice_1 = os.path.join(current_dir, "assets", "voice_4_1.mp3").replace("\\", "/")
    
    # --- VOICE 4.0: INTRO PART 4 ---
    if os.path.exists(voice_0):
        scene.add_sound(voice_0)

    # 0. INTRO VISUALIZATION
    # "Chào mừng các bạn quay trở lại với series chuyên sâu về LLM Watermarking."
    series_title = VGText("LLM Watermarking Series", font_size=24, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 2.5)
    scene.play(Write(series_title), run_time=1.0)

    # "Sau khi đã tìm hiểu cách nhúng thủy vân trực tiếp vào mô hình ở Phần 3..."
    model_box = RoundedRectangle(corner_radius=0.2, width=2.0, height=2.0, color=VG_GOLD, fill_opacity=0.2).move_to(LEFT * 3)
    model_lbl = VGText("Language\nModel", font_size=16, color=VG_GOLD).move_to(model_box.get_center())
    
    text_box = Rectangle(width=1.5, height=2.0, color=WHITE, fill_opacity=0.2).move_to(RIGHT * 3)
    text_lbl = VGText("Generated\nText", font_size=16, color=WHITE).move_to(text_box.get_center())
    
    scene.play(FadeIn(model_box), FadeIn(model_lbl), FadeIn(text_box), FadeIn(text_lbl), run_time=1.0)
    
    arrow_fwd = Arrow(model_box.get_right() + UP*0.5, text_box.get_left() + UP*0.5, color=VG_BLUE, buff=0.2)
    p3_lbl = VGText("Watermark Injection", font_size=14, color=VG_BLUE).next_to(arrow_fwd, UP, buff=0.1)
    
    scene.play(Create(arrow_fwd), Write(p3_lbl), run_time=1.0)
    scene.wait(2.5)

    # "Liệu chúng ta có thể làm điều ngược lại? Tức là đối diện với đoạn văn bản trôi nổi..."
    arrow_rev = Arrow(text_box.get_left() + DOWN*0.5, model_box.get_right() + DOWN*0.5, color=VG_RED, buff=0.2)
    p4_lbl = VGText("Detection ?", font_size=14, color=VG_RED).next_to(arrow_rev, DOWN, buff=0.1)
    
    scene.play(Create(arrow_rev), Write(p4_lbl), run_time=1.5)
    scene.wait(6)
    
    # "mà không cần quyền truy cập vào mã nguồn hay hệ thống giải mã..."
    # Turn model into a black box
    black_box = RoundedRectangle(corner_radius=0.2, width=2.0, height=2.0, color=VG_GRAY, fill_opacity=0.8, fill_color=BLACK).move_to(LEFT * 3)
    black_lbl = VGText("Black-Box\n(No Access)", font_size=16, color=VG_GRAY).move_to(black_box.get_center())
    
    scene.play(
        FadeOut(model_box), FadeOut(model_lbl),
        FadeIn(black_box), FadeIn(black_lbl),
        run_time=1.0
    )
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_0]: Đợi đọc hết câu hỏi mở đầu
    scene.wait(7.5)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)

    # 1. CENTRAL TITLE INTRO (giống Part 0: Bối cảnh & Động lực)
    part_title = VGText("PHÁT HIỆN HẬU KIỂM", font_size=LARGE_FONT_SIZE + 4, color=WHITE, weight=BOLD_WEIGHT).move_to(UP*0.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_BLUE, stroke_width=2.5).next_to(part_title, DOWN, buff=0.2)
    
    scene.play(Write(part_title), run_time=1.0)
    scene.play(Create(underline), run_time=0.5)
    scene.wait(3.0)
    
    scene.play(FadeOut(part_title), FadeOut(underline), run_time=1.0)
    
    # --- VOICE 4.1: SỰ SỤP ĐỔ CỦA OPENAI CLASSIFIER ---
    if os.path.exists(voice_1):
        scene.add_sound(voice_1)

    # 2. OPENAI CLASSIFIER - TRAINING
    # "...Thời gian đầu, giới công nghệ từng đặt rất nhiều kỳ vọng vào các công cụ phân loại như OpenAI AI Classifier."
    classifier_title = VGText("OpenAI AI Classifier", font_size=24, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 2.5)
    classifier_title_glow = classifier_title.copy().set_fill(opacity=0).set_stroke(VG_GOLD, width=5, opacity=0.8)
    
    scene.play(Write(classifier_title), FadeIn(classifier_title_glow), run_time=1.0)
    scene.play(Wiggle(classifier_title_glow), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Để bắt đầu cuộc hành trình truy vết này..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    # Human Text vs AI Text pairs
    # "...OpenAI đã ném cho nó hàng triệu cặp văn bản..." -> Visualize cascade of documents
    human_docs = VGroup(*[Rectangle(width=1.2, height=1.6, color=VG_BLUE, fill_opacity=0.2).move_to(LEFT * 4.5 + UP * 1.8 + RIGHT*0.1*i + UP*0.1*i) for i in range(4)])
    human_lbl = VGText("Human Text\n(InstructGPT prompts)", font_size=12, color=VG_BLUE).next_to(human_docs, DOWN, buff=0.2)
    
    ai_docs = VGroup(*[Rectangle(width=1.2, height=1.6, color=VG_RED, fill_opacity=0.2).move_to(LEFT * 4.5 + DOWN * 1.2 + RIGHT*0.1*i + UP*0.1*i) for i in range(4)])
    ai_lbl = VGText("AI Text\n(Various LLMs)", font_size=12, color=VG_RED).next_to(ai_docs, DOWN, buff=0.2)

    scene.play(LaggedStart(*[FadeIn(d, shift=RIGHT) for d in human_docs], lag_ratio=0.2), FadeIn(human_lbl), run_time=1.5)
    scene.play(LaggedStart(*[FadeIn(d, shift=RIGHT) for d in ai_docs], lag_ratio=0.2), FadeIn(ai_lbl), run_time=1.5)

    # Fine-Tuning into model
    model_box = RoundedRectangle(corner_radius=0.2, width=2.5, height=2.5, color=VG_GOLD, fill_opacity=0.1).move_to(RIGHT * 1.5)
    model_box_glow = model_box.copy().set_fill(opacity=0).set_stroke(VG_GOLD, width=10, opacity=0.3)
    model_lbl = VGText("Classifier\nModel", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(model_box.get_top() + DOWN * 0.5)
    ft_lbl = VGText("[Fine-Tuning]", font_size=12, color=WHITE).move_to(model_box.get_bottom() + UP * 0.4)
    
    # Ranh giới vô hình (Decision Boundary)
    boundary = DashedLine(model_box.get_left() + RIGHT*0.1, model_box.get_right() + LEFT*0.1, color=WHITE).set_opacity(0)

    arrow1 = Arrow(human_docs[-1].get_right(), model_box.get_left(), color=WHITE)
    arrow2 = Arrow(ai_docs[-1].get_right(), model_box.get_left(), color=WHITE)

    # "...Công cụ này được huấn luyện tinh chỉnh (Fine-Tuning) trên hàng triệu cặp văn bản..."
    scene.play(Create(arrow1), Create(arrow2), run_time=1.0)
    scene.play(FadeIn(model_box), FadeIn(model_box_glow), FadeIn(model_lbl), FadeIn(ft_lbl), FadeIn(boundary), run_time=1.5)
    
    # "Wow" animation: massive data packets flowing
    packets = VGroup()
    for _ in range(5):
        packets.add(Dot(color=VG_BLUE).move_to(arrow1.get_start()))
        packets.add(Dot(color=VG_RED).move_to(arrow2.get_start()))
        
    scene.play(
        LaggedStart(*[MoveAlongPath(p, arrow1) for p in packets[::2]], lag_ratio=0.2, run_time=1.5),
        LaggedStart(*[MoveAlongPath(p, arrow2) for p in packets[1::2]], lag_ratio=0.2, run_time=1.5),
        boundary.animate.set_opacity(1).set_color(WHITE) # decision boundary forms
    )
    scene.play(FadeOut(packets), run_time=0.2)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "Công cụ này được huấn luyện..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    # Threshold adjustment
    thresh_line = Line(model_box.get_bottom() + DOWN * 0.4 + LEFT * 1.5, model_box.get_bottom() + DOWN * 0.4 + RIGHT * 1.5, color=VG_GRAY)
    thresh_marker = Triangle(color=VG_RED, fill_opacity=1).scale(0.1).move_to(thresh_line.get_right() + UP*0.1)
    thresh_lbl = VGText("Strict Threshold\n(Low FPR)", font_size=12, color=VG_RED).next_to(thresh_marker, DOWN)
    shield = VGText("[SAFE]", font_size=14, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(thresh_lbl, RIGHT)

    # "...OpenAI thậm chí đã thiết lập một ngưỡng (Threshold) rất nghiêm ngặt để giữ tỷ lệ Dương tính giả ở mức thấp nhất."
    scene.play(Create(thresh_line), FadeIn(thresh_marker, shift=DOWN), FadeIn(thresh_lbl), FadeIn(shield), run_time=1.5)
    
    # Animate adjusting threshold
    scene.play(thresh_marker.animate.shift(LEFT * 1.0), thresh_lbl.animate.shift(LEFT * 1.0), shield.animate.shift(LEFT * 1.0), run_time=1.5, rate_func=there_and_back)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "OpenAI thậm chí thiết lập ngưỡng nghiêm ngặt..."
    scene.wait(8.0)
    # ---------------------------------------------------------

    classifier_group = VGroup(model_box, model_lbl, boundary)
    scene.play(
        FadeOut(human_docs), FadeOut(human_lbl), FadeOut(ai_docs), FadeOut(ai_lbl),
        FadeOut(arrow1), FadeOut(arrow2), FadeOut(thresh_line), FadeOut(thresh_marker), FadeOut(thresh_lbl), FadeOut(shield),
        FadeOut(ft_lbl), FadeOut(model_box_glow),
        classifier_group.animate.scale(0.5).to_edge(LEFT, buff=1.0),
        run_time=1.5
    )

    # 3. LIMITATIONS
    # "...Tuy nhiên, công cụ này nhanh chóng vấp phải hàng loạt giới hạn chí mạng:"
    lim_title = VGText("LIMITATIONS", font_size=20, color=VG_RED, weight=BOLD_WEIGHT).next_to(classifier_title, DOWN, buff=0.5)
    scene.play(Write(lim_title), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "Tuy nhiên vị thám tử này lập tức bộc lộ..."
    scene.wait(4.0)
    # ---------------------------------------------------------

    card_style = {"fill_opacity": 0.2, "stroke_width": 2, "corner_radius": 0.1}
    c_w, c_h = 2.8, 1.2

    c1 = RoundedRectangle(color=VG_GRAY, width=c_w, height=c_h, **card_style).move_to(RIGHT * 1.0 + UP * 0.5)
    t1 = VGText("Text Length\nUnreliable under 1000 chars", font_size=12, color=WHITE).move_to(c1.get_center())
    
    c2 = RoundedRectangle(color=VG_GRAY, width=c_w, height=c_h, **card_style).move_to(RIGHT * 4.5 + UP * 0.5)
    t2 = VGText("Language\nPoor on non-English", font_size=12, color=WHITE).move_to(c2.get_center())

    c3 = RoundedRectangle(color=VG_GRAY, width=c_w, height=c_h, **card_style).move_to(RIGHT * 1.0 + DOWN * 1.0)
    t3 = VGText("Evasion\nEasily bypassed by edits", font_size=12, color=WHITE).move_to(c3.get_center())

    c4 = RoundedRectangle(color=VG_GRAY, width=c_w, height=c_h, **card_style).move_to(RIGHT * 4.5 + DOWN * 1.0)
    t4 = VGText("OOD\nPoorly calibrated on new data", font_size=12, color=WHITE).move_to(c4.get_center())

    # "...Nó hoàn toàn thiếu tin cậy với văn bản ngắn dưới 1000 ký tự,"
    scene.play(FadeIn(c1, shift=UP), FadeIn(t1, shift=UP), run_time=0.8)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "thiếu tin cậy dưới 1000 ký tự"
    scene.wait(3)
    # ---------------------------------------------------------
    
    # "...hoạt động rất tệ với các ngôn ngữ ngoài tiếng Anh,"
    scene.play(FadeIn(c2, shift=UP), FadeIn(t2, shift=UP), run_time=0.8)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc "tồi tệ với ngôn ngữ ngoài tiếng Anh"
    scene.wait(3)
    # ---------------------------------------------------------
    
    # "...dễ dàng bị qua mặt bằng các thủ thuật chỉnh sửa,"
    scene.play(FadeIn(c3, shift=UP), FadeIn(t3, shift=UP), run_time=0.8)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_7]: Đợi đọc "kẻ gian dễ dàng qua mặt"
    scene.wait(4)
    # ---------------------------------------------------------
    
    # "...và mất hiệu chuẩn với các dữ liệu lạ."
    scene.play(FadeIn(c4, shift=UP), FadeIn(t4, shift=UP), run_time=0.8)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_8]: Đợi đọc "cắt ghép từ ngữ đơn giản"
    scene.wait(4)
    # ---------------------------------------------------------

    # 4. SHUTDOWN
    # "...Đỉnh điểm là vào ngày 20 tháng 7 năm 2023, OpenAI đã chính thức khai tử công cụ này vì độ chính xác quá thấp."
    stamp_box = RoundedRectangle(corner_radius=0.2, width=7.0, height=2.0, color=VG_RED, stroke_width=8).rotate(PI/12).move_to(DOWN * 0.2)
    stamp_text = VGText("SHUTDOWN: July 20, 2023\nDue to low rate of accuracy", font_size=24, color=VG_RED, weight=BOLD_WEIGHT).move_to(stamp_box.get_center()).rotate(PI/12)
    stamp = VGroup(stamp_box, stamp_text).set_z_index(20)
    stamp_box_glow = stamp_box.copy().set_stroke(width=20, opacity=0.3).set_z_index(19)

    # Thud effect: giant stamp slamming into screen
    scene.play(FadeIn(stamp, scale=3.0), FadeIn(stamp_box_glow, scale=3.0), run_time=0.4, rate_func=rush_into)
    
    # Simulate aggressive camera shake on the whole scene
    all_mobs = Group(*scene.mobjects)
    for _ in range(2):
        scene.play(all_mobs.animate.shift(DOWN*0.1 + RIGHT*0.1), run_time=0.05)
        scene.play(all_mobs.animate.shift(UP*0.1 + LEFT*0.1), run_time=0.05)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_9]: Đợi đọc kết luận
    scene.wait(6.0)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
