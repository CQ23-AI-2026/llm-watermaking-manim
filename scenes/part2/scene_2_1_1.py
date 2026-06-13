from manim import *
import random

from config.style import VGText, VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, VG_GOLD, VG_LIGHT_BLUE, BOLD_WEIGHT

def _green_red_core_scene(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # 1. VGText("Ý tưởng: Green-Red Watermark", font_size=42, weight="BOLD", color=WHITE) FadeIn top
    title = VGText("Ý tưởng: Green-Red Watermark", font_size=42, weight=BOLD_WEIGHT, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(FadeIn(title), run_time=0.7)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 1 — Bộ từ điển V bị chia đôi
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    vocab_box = RoundedRectangle(width=5.5, height=2.0, corner_radius=0.12)
    vocab_box.set_stroke(color=WHITE)
    vocab_box.set_fill(color=WHITE, opacity=0.05)
    vocab_label = VGText("Bộ từ điển V (~50,000 từ)", font_size=28, color=WHITE)
    
    dots = VGroup()
    # grid ~10x6 = 60 dots
    for i in range(6):
        for j in range(10):
            dot = Dot(radius=0.04, color=WHITE)
            x = -2.25 + j * 0.5
            y = 0.6 - i * 0.24
            dot.move_to(np.array([x, y, 0]))
            dots.add(dot)
            
    vocab_group = VGroup(vocab_box, dots)
    vocab_group.next_to(title, DOWN, buff=0.6)
    vocab_label.next_to(vocab_box, UP, buff=0.2)
    
    scene.play(FadeIn(vocab_group), FadeIn(vocab_label), run_time=1.0)
    
    dashed_line = DashedLine(
        vocab_box.get_top() + UP * 0.2, 
        vocab_box.get_bottom() + DOWN * 0.2, 
        color=VG_GRAY
    )
    
    scene.play(Create(dashed_line), run_time=0.5)
    
    left_dots = VGroup(*[d for d in dots if d.get_center()[0] < vocab_box.get_center()[0]])
    right_dots = VGroup(*[d for d in dots if d.get_center()[0] >= vocab_box.get_center()[0]])
    
    scene.play(
        left_dots.animate.set_color(VG_GREEN),
        right_dots.animate.set_color(VG_RED),
        run_time=0.8
    )
    
    scene.play(FadeOut(dashed_line), FadeOut(vocab_label), run_time=0.3)
    
    green_box_rect = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.12)
    green_box_rect.set_stroke(color=VG_GREEN)
    green_box_rect.set_fill(color=VG_GREEN, opacity=0.1)
    
    red_box_rect = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.12)
    red_box_rect.set_stroke(color=VG_RED)
    red_box_rect.set_fill(color=VG_RED, opacity=0.1)
    
    green_box_rect.move_to(left_dots.get_center())
    red_box_rect.move_to(right_dots.get_center())
    
    green_title = VGText("Green List", font_size=28, weight=BOLD_WEIGHT, color=VG_GREEN)
    green_subtitle = VGText("γ × |V| từ", font_size=22, color=VG_GREEN)
    green_title.next_to(green_box_rect, UP, buff=0.15)
    green_subtitle.next_to(green_title, DOWN, buff=0.1)
    green_texts = VGroup(green_title, green_subtitle)
    
    red_title = VGText("Red List", font_size=28, weight=BOLD_WEIGHT, color=VG_RED)
    red_subtitle = VGText("(1−γ) × |V| từ", font_size=22, color=VG_RED)
    red_title.next_to(red_box_rect, UP, buff=0.15)
    red_subtitle.next_to(red_title, DOWN, buff=0.1)
    red_texts = VGroup(red_title, red_subtitle)
    
    # Animate division
    scene.play(
        FadeOut(vocab_box),
        green_box_rect.animate.shift(LEFT * 1.6),
        red_box_rect.animate.shift(RIGHT * 1.6),
        left_dots.animate.shift(LEFT * 1.6),
        right_dots.animate.shift(RIGHT * 1.6),
        run_time=0.8
    )
    
    # Text follows boxes
    green_texts.next_to(green_box_rect, UP, buff=0.15)
    red_texts.next_to(red_box_rect, UP, buff=0.15)
    
    scene.play(
        FadeIn(green_texts),
        FadeIn(red_texts),
        run_time=0.5
    )
    
    full_boxes = VGroup(green_box_rect, red_box_rect, left_dots, right_dots)
    brace = Brace(full_boxes, DOWN, color=VG_GRAY)
    brace_text = VGText("Cùng Secret Key k → tái tạo được", font_size=20, slant="ITALIC", color=VG_GRAY)
    brace_text.next_to(brace, DOWN, buff=0.1)
    
    scene.play(GrowFromCenter(brace), FadeIn(brace_text), run_time=0.8)
    
    # Scale and move up step 1 to make space
    step1_group = VGroup(left_dots, right_dots, green_box_rect, red_box_rect, green_texts, red_texts, brace, brace_text)
    scene.play(step1_group.animate.scale(0.8).to_edge(UP, buff=1.2), run_time=0.8)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 2 — Cộng bias δ vào logits của Green tokens
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    bar_chart_y = -1.2
    
    labels_data = [
        ("Hà Nội", VG_GREEN),
        ("Sài Gòn", VG_RED),
        ("Paris", VG_GREEN),
        ("Đà Nẵng", VG_RED),
        ("London", VG_GREEN),
        ("Khác...", VG_RED),
    ]
    
    random.seed(42)  # For reproducibility
    
    before_bars = VGroup()
    before_labels = VGroup()
    
    for i, (word, color) in enumerate(labels_data):
        label = VGText(word, font_size=18, color=color)
        w = random.uniform(0.7, 1.3)
        bar = Rectangle(width=w, height=0.25, color=VG_GRAY, stroke_opacity=0, fill_color=VG_GRAY, fill_opacity=1)
        
        label.move_to(np.array([-6.0, bar_chart_y - i*0.35, 0]))
        label.align_to(np.array([-6.0, 0, 0]), RIGHT)
        
        bar.next_to(label, RIGHT, buff=0.15)
        bar.align_to(bar, LEFT)
        
        before_labels.add(label)
        before_bars.add(bar)
        
    before_title = VGText("Không có Watermark", font_size=20, color=VG_GRAY)
    before_group = VGroup(before_labels, before_bars)
    before_title.next_to(before_group, UP, buff=0.3)
    
    arrow_add = Arrow(start=LEFT*1.2, end=RIGHT*1.2, color=VG_GOLD, stroke_width=2.5)
    arrow_add.move_to(np.array([-2.5, bar_chart_y - 0.8, 0]))
    
    add_text = VGText("+δ vào Green", font_size=22, color=VG_GOLD)
    add_text.next_to(arrow_add, UP, buff=0.1)
    delta_text = VGText("δ = 2.0", font_size=20, color=VG_GOLD)
    delta_text.next_to(arrow_add, DOWN, buff=0.1)
    
    after_bars = VGroup()
    after_labels = VGroup()
    after_arrows = VGroup()
    
    for i, (word, color) in enumerate(labels_data):
        label = VGText(word, font_size=18, color=color)
        
        orig_w = before_bars[i].width
        
        if color == VG_GREEN:
            w = orig_w + 1.2
            bar_color = VG_GREEN
            up_arrow = VGText("↑", font_size=18, weight=BOLD_WEIGHT, color=VG_GREEN)
        else:
            w = orig_w
            bar_color = VG_RED
            up_arrow = None
            
        bar = Rectangle(width=w, height=0.25, color=bar_color, stroke_opacity=0, fill_color=bar_color, fill_opacity=1)
        
        label.move_to(np.array([-0.5, bar_chart_y - i*0.35, 0]))
        label.align_to(np.array([-0.5, 0, 0]), RIGHT)
        
        bar.next_to(label, RIGHT, buff=0.15)
        bar.align_to(bar, LEFT)
        
        if up_arrow:
            up_arrow.next_to(bar, RIGHT, buff=0.1)
            after_arrows.add(up_arrow)
            
        after_labels.add(label)
        after_bars.add(bar)
        
    after_title = VGText("Có Watermark", font_size=20, color=WHITE)
    after_group = VGroup(after_labels, after_bars, after_arrows)
    after_title.next_to(after_group, UP, buff=0.3)
    
    scene.play(FadeIn(before_title), FadeIn(before_group), run_time=1.0)
    
    scene.play(GrowArrow(arrow_add), FadeIn(add_text), FadeIn(delta_text), run_time=0.8)
    
    scene.play(FadeIn(after_title), FadeIn(after_labels), run_time=0.5)
    
    bars_to_transform = before_bars.copy()
    scene.play(
        Transform(bars_to_transform, after_bars),
        FadeIn(after_arrows),
        run_time=1.2
    )
    
    callout_1 = VGText("Từ Green: xác suất tăng lên", font_size=22, color=VG_GREEN)
    callout_2 = VGText("Từ Red:   xác suất giữ nguyên", font_size=22, color=VG_RED)
    callout_3 = VGText("→ Model ưu tiên chọn từ Green", font_size=22, weight=BOLD_WEIGHT, color=WHITE)
    
    callout_group = VGroup(callout_1, callout_2, callout_3).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    callout_group.next_to(after_group, RIGHT, buff=0.3).shift(UP * 0.3)
    
    scene.play(FadeIn(callout_group), run_time=1.0)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 3 — Key được lưu lại để detect sau
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    key_rect = RoundedRectangle(width=4.2, height=0.8, corner_radius=0.1)
    key_rect.set_stroke(color=VG_GOLD)
    key_rect.set_fill(color=VG_GOLD, opacity=0.1)
    
    key_circle = Circle(radius=0.12, color=VG_GOLD).set_stroke(width=2)
    key_line = Line(key_circle.get_right(), key_circle.get_right() + RIGHT*0.4, color=VG_GOLD, stroke_width=2)
    key_tooth1 = Line(key_line.get_right() + LEFT*0.1, key_line.get_right() + LEFT*0.1 + DOWN*0.15, color=VG_GOLD, stroke_width=2)
    key_tooth2 = Line(key_line.get_right(), key_line.get_right() + DOWN*0.15, color=VG_GOLD, stroke_width=2)
    key_icon = VGroup(key_circle, key_line, key_tooth1, key_tooth2)
    
    key_text = VGText("Watermark Key k", font_size=26, weight=BOLD_WEIGHT, color=VG_GOLD)
    
    key_content = VGroup(key_icon, key_text).arrange(RIGHT, buff=0.2)
    key_content.move_to(key_rect.get_center())
    
    key_group = VGroup(key_rect, key_content)
    key_group.to_edge(DOWN, buff=0.2).shift(RIGHT * 1.5) # Shift slightly right to avoid overlap
    
    scene.play(GrowFromCenter(key_group), run_time=0.8)
    
    dashed_arrow_k = DashedLine(
        green_box_rect.get_bottom(),
        key_group.get_left() + LEFT*0.2,
        path_arc=PI/4,
        color=VG_GOLD,
        stroke_width=2
    ).add_tip()
    
    key_desc = VGText("Lưu lại cách chia", font_size=20, slant="ITALIC", color=VG_GRAY)
    key_desc.next_to(dashed_arrow_k, LEFT, buff=0.1)
    
    scene.play(Create(dashed_arrow_k), FadeIn(key_desc), run_time=0.8)
    
    scene.wait(1.5)


def play_part2_scene_2_1_1(scene: Scene) -> None:
    _green_red_core_scene(scene)

class Scene211_GreenRedCore(Scene):
    def construct(self):
        _green_red_core_scene(self)
