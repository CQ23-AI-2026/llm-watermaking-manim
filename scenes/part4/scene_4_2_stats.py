from manim import *
import numpy as np
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def play_scene_4_2(scene: Scene):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_file = os.path.join(current_dir, "assets", "voice_4_2.mp3").replace("\\", "/")
    if os.path.exists(voice_file):
        scene.add_sound(voice_file)

    # 1. TITLE
    part_title = VGText("POST-HOC DETECTION APPROACHES", font_size=LARGE_FONT_SIZE - 8, color=VG_GOLD, weight=BOLD_WEIGHT).move_to(UP * 3.2)
    underline = Line(LEFT * 4, RIGHT * 4, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.5).next_to(part_title, DOWN, buff=0.15)
    
    scene.play(Write(part_title), run_time=1.5)
    scene.play(Create(underline), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_1]: Đợi đọc "Sự sụp đổ đó buộc giới khoa học..."
    scene.wait(10)
    # ---------------------------------------------------------

    # 2. TWO BRANCHES
    left_bg = Rectangle(width=4.5, height=0.6, color=VG_BLUE, fill_color=BLACK, fill_opacity=0.8)
    left_txt = VGText("Trained Classifiers", font_size=18, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(left_bg.get_center())
    left_title = VGroup(left_bg, left_txt).to_edge(LEFT, buff=1.0).shift(UP * 1.5)

    right_bg = Rectangle(width=4.5, height=0.6, color=VG_GREEN, fill_color=BLACK, fill_opacity=0.8)
    right_txt = VGText("Zero-shot Classifiers", font_size=18, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(right_bg.get_center())
    right_title = VGroup(right_bg, right_txt).to_edge(RIGHT, buff=1.0).shift(UP * 1.5)

    scene.play(FadeIn(left_title, shift=RIGHT), FadeIn(right_title, shift=LEFT), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_2]: Đợi đọc "phân định lại bản đồ thành hai trường phái..."
    scene.wait(10)
    # ---------------------------------------------------------

    # 3. TRAINED CLASSIFIERS
    # "...Trained Classifiers là các mô hình được huấn luyện đặc tả dựa trên đặc trưng văn bản..."
    bag_box = RoundedRectangle(width=3.5, height=0.8, color=VG_GRAY, fill_opacity=0.2).next_to(left_title, DOWN, buff=0.8)
    bag_txt = VGText("Bag-of-words\n(e.g., Solaiman et al., 2019)", font_size=12, color=WHITE).move_to(bag_box.get_center())
    bag = VGroup(bag_box, bag_txt)

    llm_box = RoundedRectangle(width=3.5, height=0.8, color=VG_BLUE, fill_opacity=0.2).next_to(bag_box, DOWN, buff=0.5)
    llm_txt = VGText("LLM Classifiers (RoBERTa)\n(e.g., Zellers et al., 2019)", font_size=12, color=WHITE).move_to(llm_box.get_center())
    llm_g = VGroup(llm_box, llm_txt)

    arrow_left_1 = Arrow(left_title.get_bottom(), bag_box.get_top(), color=VG_BLUE)
    arrow_left_2 = Arrow(bag_box.get_bottom(), llm_box.get_top(), color=VG_BLUE)

    scene.play(Create(arrow_left_1), FadeIn(bag, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_3]: Đợi đọc "Khởi đầu từ những phương pháp thô sơ..."
    scene.wait(4)
    # ---------------------------------------------------------
    
    # "...đến các mạng LLM Classifier phức tạp như RoBERTa."
    scene.play(Create(arrow_left_2), FadeIn(llm_g, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_4]: Đợi đọc "đến việc sử dụng các mạng mạnh mẽ..."
    scene.wait(7)
    # ---------------------------------------------------------

    # 4. ZERO-SHOT CLASSIFIERS
    # "...Ngược lại, Zero-shot Classifiers không cần huấn luyện thêm bất cứ dữ liệu nào."
    
    stat_box = RoundedRectangle(width=4.0, height=1.0, color=VG_GREEN, fill_opacity=0.2).next_to(right_title, DOWN, buff=0.8)
    stat_txt = VGText("Statistical Outlier Detection\n(No Training Required)", font_size=14, color=WHITE, weight=BOLD_WEIGHT).move_to(stat_box.get_center() + UP*0.1)
    stat_g = VGroup(stat_box, stat_txt)
    arrow_right_1 = Arrow(right_title.get_bottom(), stat_box.get_top(), color=VG_GREEN)

    scene.play(Create(arrow_right_1), FadeIn(stat_g, shift=UP), run_time=1.0)
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_5]: Đợi đọc "ngôi sao sáng thực sự lại nằm ở trường phái..."
    scene.wait(5)
    # ---------------------------------------------------------

    # "...Chúng khai thác trực tiếp các thuộc tính thống kê cốt lõi của AI..."
    attr_list = VGroup(
        VGText("• Entropy", font_size=14, color=VG_GOLD),
        VGText("• Perplexity (Độ bối rối)", font_size=14, color=VG_GOLD),
        VGText("• N-gram Frequencies", font_size=14, color=VG_GOLD)
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(stat_box, DOWN, buff=0.8).align_to(stat_box, LEFT).shift(RIGHT*0.5)

    for attr in attr_list:
        scene.play(FadeIn(attr, shift=RIGHT), run_time=0.6)
        
    # "...Nhờ vậy, chúng hoạt động vô cùng hiệu quả trên các văn bản sinh ra bởi chính mô hình đó."
    
    # ---------------------------------------------------------
    # [WAIT_SYNC_6]: Đợi đọc phần còn lại của script
    scene.wait(17)
    # ---------------------------------------------------------

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
