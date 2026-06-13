from manim import *
import random

from config.style import VGText, VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, VG_GOLD, VG_LIGHT_BLUE, BOLD_WEIGHT

def _detection_scene(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # 1. Title FadeIn top center
    title = VGText("Cơ chế phát hiện (Detection)", font_size=42, weight=BOLD_WEIGHT, color=WHITE)
    title.to_edge(UP, buff=0.2)
    scene.play(FadeIn(title), run_time=0.7)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SETUP: Văn bản nghi vấn
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    words = ["When", "most", "people", "are", "confronted", "with", "failure", "they"]
    colors_status = [VG_GREEN, VG_GREEN, VG_RED, VG_GREEN, VG_GREEN, VG_GREEN, VG_RED, VG_GREEN]

    # Calculate token group layout
    token_group = VGroup()
    box_width = 1.1
    box_height = 0.45
    spacing = 0.1
    
    total_w = len(words) * box_width + (len(words) - 1) * spacing
    start_x = -total_w / 2 + box_width / 2
    
    # We will shift it slightly right so the label fits on the left
    start_x += 1.0

    tokens = []
    
    for i, w in enumerate(words):
        t_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.08, color=WHITE)
        t_box.set_fill(color=WHITE, opacity=0.0)
        t_text = VGText(w, font_size=22, color=WHITE)
        t_group = VGroup(t_box, t_text)
        t_group.move_to(np.array([start_x + i * (box_width + spacing), 2.2, 0]))
        
        token_group.add(t_group)
        tokens.append(t_group)
        
    y_label = VGText("Văn bản nghi vấn  y:", font_size=24, color=VG_GRAY)
    y_label.next_to(token_group, LEFT, buff=0.4)
    
    scene.play(FadeIn(y_label), FadeIn(token_group), run_time=1.0)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 1 + BƯỚC 2 — Tái tạo list & Đếm
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Key box
    key_box = VGroup()
    key_icon_circle = Circle(radius=0.15, color=VG_GOLD, stroke_width=2)
    key_icon_line = Line(key_icon_circle.get_right(), key_icon_circle.get_right() + RIGHT*0.2, color=VG_GOLD, stroke_width=2)
    key_icon_teeth = VGroup(
        Line(key_icon_line.get_end() + LEFT*0.05, key_icon_line.get_end() + LEFT*0.05 + DOWN*0.1, color=VG_GOLD, stroke_width=2),
        Line(key_icon_line.get_end() + LEFT*0.15, key_icon_line.get_end() + LEFT*0.15 + DOWN*0.1, color=VG_GOLD, stroke_width=2)
    )
    key_icon = VGroup(key_icon_circle, key_icon_line, key_icon_teeth)
    
    key_text = VGText("Key  k", font_size=24, color=VG_GOLD)
    key_box.add(key_icon, key_text)
    key_box.arrange(RIGHT, buff=0.15)
    key_box.move_to(np.array([-5.0, 1.2, 0]))
    
    key_arrow = Arrow(start=key_box.get_right(), end=np.array([start_x, 1.2, 0]), color=VG_GOLD, buff=0.2, max_tip_length_to_length_ratio=0.1)
    key_arrow_label = VGText("Tái tạo Green/Red list", font_size=22, color=VG_GOLD)
    key_arrow_label.next_to(key_arrow, UP, buff=0.1)
    
    scene.play(FadeIn(key_box), run_time=0.5)
    scene.play(GrowArrow(key_arrow), FadeIn(key_arrow_label), run_time=0.5)
    
    # Counter box
    counter_box_rect = RoundedRectangle(width=3.5, height=0.7, corner_radius=0.1, color=VG_GREEN)
    counter_box_rect.set_fill(color=VG_GREEN, opacity=0.1)
    counter_box_rect.move_to(np.array([-3.5, 0.2, 0]))
    
    counter_text_left = VGText("|y_g| = ", font_size=28, color=VG_GREEN)
    
    # ValueTracker for counting
    counter_tracker = ValueTracker(0)
    
    counter_value_text = always_redraw(
        lambda: VGText(f"{int(counter_tracker.get_value())}", font_size=28, color=VG_GREEN)
                .next_to(counter_text_left, RIGHT, buff=0.1)
    )
    
    counter_group = VGroup(counter_text_left, counter_value_text)
    counter_group.move_to(counter_box_rect.get_center())
    
    scene.play(DrawBorderThenFill(counter_box_rect), FadeIn(counter_group), run_time=0.5)
    
    # SCANNING & COUNTING
    count_val = 0
    for i, t_group in enumerate(tokens):
        color = colors_status[i]
        
        # Colorize token
        t_box = t_group[0]
        
        anims = [
            t_box.animate.set_stroke(color=color, width=2),
            t_box.animate.set_fill(color=color, opacity=0.25)
        ]
        
        if color == VG_GREEN:
            count_val += 1
            # Flying dot
            flying_dot = Dot(radius=0.1, color=VG_GREEN)
            flying_dot.move_to(t_box.get_bottom())
            
            scene.play(
                *anims,
                counter_tracker.animate.set_value(count_val),
                flying_dot.animate.move_to(counter_box_rect.get_right() + LEFT*0.4).set_opacity(0),
                run_time=0.25
            )
            scene.remove(flying_dot)
        else:
            scene.play(*anims, run_time=0.25)
            
        # small delay
        scene.wait(0.05)
        
    scene.wait(0.3)
    
    # Final counter text
    final_counter_text = VGText("|y_g| = 6   (n = 8 tokens)", font_size=26, color=VG_GREEN)
    final_counter_text.move_to(counter_box_rect.get_center())
    scene.play(
        FadeOut(counter_group),
        FadeIn(final_counter_text),
        run_time=0.5
    )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 3 — Công thức z-score xuất hiện với annotation
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Dòng 1 (lớn, giữa màn hình)
    num = VGText("|y_g| - γ · n", font_size=32, color=WHITE)
    den = VGText("√ (n · γ · (1-γ))", font_size=32, color=WHITE)
    frac_line = Line(LEFT, RIGHT).scale(1.5)
    frac_group = VGroup(num, frac_line, den).arrange(DOWN, buff=0.1)
    
    z_eq = VGText("z = ", font_size=36, color=WHITE)
    z_eq.next_to(frac_line, LEFT, buff=0.2)
    
    z_formula = VGroup(z_eq, frac_group)
    z_formula.move_to(np.array([0, -1.3, 0]))
    
    scene.play(Write(z_formula), run_time=1.0)
    
    # Annotations
    # |y_g| part: 
    # VGText skips spaces, so num has characters: |, y, _, g, |, -, γ, ·, n
    yg_rect = SurroundingRectangle(num[:5], color=VG_GREEN, buff=0.05)
    yg_text = VGText("Số từ Green thực tế", font_size=20, color=VG_GREEN)
    yg_text.next_to(yg_rect, UP, buff=0.1).shift(LEFT * 0.5)
    
    scene.play(Create(yg_rect), FadeIn(yg_text), run_time=0.6)
    
    # γ · n part
    gamma_n_rect = SurroundingRectangle(num[-3:], color=VG_ORANGE, buff=0.05)
    gamma_n_text = VGText("Kỳ vọng nếu ngẫu nhiên", font_size=20, color=VG_ORANGE)
    gamma_n_text.next_to(gamma_n_rect, UP, buff=0.1).shift(RIGHT * 1.5)
    
    scene.play(Create(gamma_n_rect), FadeIn(gamma_n_text), run_time=0.6)
    
    # Denominator part
    denom_rect = SurroundingRectangle(den, color=VG_BLUE, buff=0.05)
    denom_text = VGText("Độ lệch chuẩn", font_size=20, color=VG_BLUE)
    denom_text.next_to(denom_rect, DOWN, buff=0.1)
    
    scene.play(Create(denom_rect), FadeIn(denom_text), run_time=0.6)
    
    z_note = VGText("Nếu  z > 4  →  xác suất báo nhầm ≈ 1/30,000", font_size=22, slant="ITALIC", color=VG_GRAY)
    z_note.next_to(z_formula, DOWN, buff=0.8).shift(RIGHT * 2.5)
    
    scene.play(FadeIn(z_note), run_time=0.5)
    scene.wait(0.5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # BƯỚC 4 — Kết quả phán quyết
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Thay số vào
    num2 = VGText("6 - 0.5 × 8", font_size=28, color=WHITE)
    den2 = VGText("√ (8 × 0.5 × 0.5)", font_size=28, color=WHITE)
    frac_line2 = Line(LEFT, RIGHT).scale(1.2)
    frac_group2 = VGroup(num2, frac_line2, den2).arrange(DOWN, buff=0.1)
    
    z_eq2 = VGText("z = ", font_size=32, color=WHITE)
    z_eq2.next_to(frac_line2, LEFT, buff=0.2)
    
    res_eq = VGText(" =  2 / 1.41  ≈  1.4", font_size=32, color=WHITE)
    res_eq.next_to(frac_line2, RIGHT, buff=0.2)
    
    z_calc = VGroup(z_eq2, frac_group2, res_eq)
    z_calc.move_to(np.array([0, -2.8, 0]))
    
    scene.play(FadeIn(z_calc), run_time=1.0)
    
    # Kết quả
    result_group = VGroup()
    res_circle = Circle(radius=0.35, color=VG_ORANGE)
    res_text = VGText("?", font_size=32, weight=BOLD_WEIGHT, color=VG_ORANGE)
    res_text.move_to(res_circle.get_center())
    
    res_label = VGText("No Evidence", font_size=24, weight=BOLD_WEIGHT, color=VG_ORANGE)
    res_label.next_to(res_circle, RIGHT, buff=0.2)
    
    res_desc = VGText("(Cần đoạn văn dài hơn để kết luận)", font_size=20, slant="ITALIC", color=VG_GRAY)
    res_desc.next_to(res_label, RIGHT, buff=0.2)
    
    result_group.add(res_circle, res_text, res_label, res_desc)
    result_group.move_to(np.array([0, -3.6, 0]))
    
    scene.play(
        GrowFromCenter(res_circle),
        FadeIn(res_text),
        run_time=0.5
    )
    scene.play(FadeIn(res_label), FadeIn(res_desc), run_time=0.5)
    
    scene.wait(2.0)

def play_part2_scene_2_1_3(scene: Scene) -> None:
    _detection_scene(scene)

class Scene213_Detection(Scene):
    def construct(self):
        _detection_scene(self)
