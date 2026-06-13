from manim import *
import os

from config.style import VGText, VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, VG_GOLD, VG_LIGHT_BLUE, BOLD_WEIGHT

def _llm_basics_scene(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # 1. VGText("Language Model sinh văn bản như thế nào?", font_size=42, weight="BOLD", color=WHITE) FadeIn top, 0.7s
    title = VGText("Language Model sinh văn bản như thế nào?", font_size=42, weight=BOLD_WEIGHT, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(FadeIn(title), run_time=0.7)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # GIAI ĐOẠN 1 — Prompt vào LLM, logits ra
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    prompt_box_rect = RoundedRectangle(width=4.4, height=1.0, corner_radius=0.12)
    prompt_box_rect.set_stroke(color=VG_LIGHT_BLUE)
    prompt_box_rect.set_fill(color=VG_LIGHT_BLUE, opacity=0.1)
    prompt_text = VGText('"Thủ đô của Việt Nam là"', font_size=26, color=WHITE)
    prompt_label = VGText("Prompt", font_size=22, color=VG_GRAY)
    
    prompt_group = VGroup(prompt_box_rect, prompt_text)
    prompt_label.next_to(prompt_box_rect, UP, buff=0.15)
    prompt_full = VGroup(prompt_group, prompt_label)
    prompt_full.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)

    llm_box_rect = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15)
    llm_box_rect.set_stroke(color=VG_PURPLE)
    llm_box_rect.set_fill(color=VG_PURPLE, opacity=0.12)
    llm_text = VGText("LLM", font_size=36, weight=BOLD_WEIGHT, color=VG_PURPLE)
    llm_group = VGroup(llm_box_rect, llm_text)
    
    llm_group.move_to(DOWN * 0.5)
    
    llm_glow = SurroundingRectangle(llm_box_rect, corner_radius=0.18, color=VG_PURPLE, buff=0.08)
    llm_glow.set_stroke(opacity=0)
    llm_glow.set_fill(opacity=0)

    arrow_p_to_llm = Arrow(start=prompt_full.get_right(), end=llm_group.get_left(), color=VG_LIGHT_BLUE, stroke_width=2.5)

    logits_label = VGText("Logits (điểm thô)", font_size=24, color=VG_GRAY)
    
    logits_data = [
        ("Hà Nội", "4.8", 2.8, VG_BLUE),
        ("Sài Gòn", "2.1", 1.4, VG_BLUE),
        ("Đà Nẵng", "1.3", 0.9, VG_BLUE),
        ("Paris", "0.2", 0.4, VG_GRAY),
        ("London", "0.1", 0.35, VG_GRAY),
    ]
    
    logit_bars = VGroup()
    logit_texts = VGroup()
    logit_numbers = VGroup()
    
    for word, logit_str, w, color in logits_data:
        text = VGText(word, font_size=20, color=WHITE)
        bar = Rectangle(width=w, height=0.32, color=color, stroke_opacity=0, fill_color=color, fill_opacity=1)
        num = VGText(logit_str, font_size=18, color=color)
        
        logit_texts.add(text)
        logit_bars.add(bar)
        logit_numbers.add(num)
        
    dots_text = VGText("...", font_size=20, color=VG_GRAY)
    
    for i, text in enumerate(logit_texts):
        text.move_to(np.array([3.5, 1.2 - i*0.5, 0]))
        text.align_to(np.array([3.5, 0, 0]), RIGHT)
    
    for i, bar in enumerate(logit_bars):
        bar.next_to(logit_texts[i], RIGHT, buff=0.2)
        bar.align_to(bar, LEFT)
        
    for i, num in enumerate(logit_numbers):
        num.next_to(logit_bars[i], RIGHT, buff=0.1)

    dots_text.next_to(logit_texts[-1], DOWN, buff=0.3).align_to(logit_texts[-1], RIGHT)
    
    logits_panel_group = VGroup(logit_texts, logit_bars, logit_numbers, dots_text)
    logits_label.next_to(logits_panel_group, UP, buff=0.4)
    logits_panel_full = VGroup(logits_panel_group, logits_label)
    logits_panel_full.shift(LEFT * 0.5 + DOWN * 0.8)

    arrow_llm_to_logits = Arrow(start=llm_group.get_right(), end=logits_panel_full.get_left(), color=VG_PURPLE, stroke_width=2.5)

    # 1. FadeIn(prompt_box) + Write(prompt_text)
    scene.play(FadeIn(prompt_box_rect), FadeIn(prompt_label), Write(prompt_text), run_time=1.0)
    # 2. GrowArrow(prompt→llm)
    scene.play(GrowArrow(arrow_p_to_llm), run_time=0.5)
    # 3. DrawBorderThenFill(llm_box) + glow pulse 2 lần
    scene.play(DrawBorderThenFill(llm_box_rect), Write(llm_text), run_time=1.0)
    
    scene.add(llm_glow)
    scene.play(llm_glow.animate.set_stroke(opacity=0.3), run_time=0.2)
    scene.play(llm_glow.animate.set_stroke(opacity=0.6), run_time=0.2)
    scene.play(llm_glow.animate.set_stroke(opacity=0.3), run_time=0.2)
    scene.play(llm_glow.animate.set_stroke(opacity=0.6), run_time=0.2)
    scene.play(llm_glow.animate.set_stroke(opacity=0), run_time=0.2)
    scene.remove(llm_glow)
    
    # 4. GrowArrow(llm→logits)
    scene.play(GrowArrow(arrow_llm_to_logits), run_time=0.5)
    
    # 5. Các logit bars: Create lần lượt từ trên xuống, mỗi bar 0.15s
    scene.play(FadeIn(logits_label), FadeIn(logit_texts), FadeIn(dots_text), run_time=0.5)
    for bar in logit_bars:
        scene.play(Create(bar), run_time=0.15)
        
    # 6. FadeIn số logit ở đầu mỗi bar đồng thời
    scene.play(FadeIn(logit_numbers), run_time=0.5)

    scene.wait(0.5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # GIAI ĐOẠN 2 — Softmax chuyển logits → xác suất
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    scene.play(
        FadeOut(prompt_full),
        FadeOut(arrow_p_to_llm),
        FadeOut(llm_group),
        FadeOut(arrow_llm_to_logits),
        logits_panel_full.animate.to_edge(LEFT, buff=0.5),
        run_time=1.0
    )

    softmax_rect = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.12)
    softmax_rect.set_stroke(color=VG_GOLD)
    softmax_rect.set_fill(color=VG_GOLD, opacity=0.1)
    softmax_text = VGText("Softmax", font_size=28, weight=BOLD_WEIGHT, color=VG_GOLD)
    
    softmax_group = VGroup(softmax_rect, softmax_text)
    softmax_text.move_to(softmax_rect.get_center())
    
    softmax_group.move_to(ORIGIN + DOWN * 0.5)

    # 1. FadeIn(softmax_block) ở giữa khoảng trống
    scene.play(FadeIn(softmax_group), run_time=0.8)
    
    # 2. GrowArrow(logits → softmax), màu VG_GOLD
    arrow_logits_to_softmax = Arrow(start=logits_panel_full.get_right(), end=softmax_group.get_left(), color=VG_GOLD)
    scene.play(GrowArrow(arrow_logits_to_softmax), run_time=0.5)

    prob_label = VGText("Xác suất", font_size=24, color=VG_GRAY)
    
    prob_data = [
        ("Hà Nội", "82%", 0.82 * 2.8, VG_GREEN), 
        ("Sài Gòn", "10%", 0.10 * 2.8, VG_BLUE),
        ("Đà Nẵng", "5%", 0.05 * 2.8, VG_BLUE),
        ("Paris", "2%", 0.02 * 2.8, VG_GRAY),
    ]
    
    prob_bars = VGroup()
    prob_texts = VGroup()
    prob_numbers = VGroup()
    
    for word, pct, w, color in prob_data:
        text = VGText(word, font_size=20, color=WHITE)
        bar = Rectangle(width=w, height=0.32, color=color, stroke_opacity=0, fill_color=color, fill_opacity=1)
        num = VGText(pct, font_size=18, color=color)
        
        prob_texts.add(text)
        prob_bars.add(bar)
        prob_numbers.add(num)
        
    prob_dots_text = VGroup(
        VGText("Khác...", font_size=20, color=WHITE),
        VGText("1%...", font_size=18, color=VG_GRAY)
    ).arrange(RIGHT, buff=0.2)
    
    for i, text in enumerate(prob_texts):
        text.move_to(np.array([2.5, logits_panel_group[0][i].get_y(), 0]))
        text.align_to(np.array([2.5, 0, 0]), RIGHT)
        
    for i, bar in enumerate(prob_bars):
        bar.next_to(prob_texts[i], RIGHT, buff=0.2)
        bar.align_to(bar, LEFT)
        
    for i, num in enumerate(prob_numbers):
        num.next_to(prob_bars[i], RIGHT, buff=0.1)
        
    prob_dots_text[0].next_to(prob_texts[-1], DOWN, buff=0.3).align_to(prob_texts[-1], RIGHT)
    prob_dots_text[1].next_to(prob_dots_text[0], RIGHT, buff=0.2)
    
    prob_panel_group = VGroup(prob_texts, prob_bars, prob_numbers, prob_dots_text)
    prob_label.move_to(logits_label).set_x(prob_panel_group.get_center()[0])
    prob_panel_full = VGroup(prob_panel_group, prob_label)
    
    # 3. GrowArrow(softmax → prob_bars), màu VG_GOLD
    arrow_softmax_to_probs = Arrow(start=softmax_group.get_right(), end=prob_panel_full.get_left(), color=VG_GOLD)
    scene.play(GrowArrow(arrow_softmax_to_probs), run_time=0.5)

    scene.play(FadeIn(prob_label), FadeIn(prob_texts), FadeIn(prob_dots_text), run_time=0.5)
    
    # 4. Transform bars từ logit sang probability (đồng thời 5 bars)
    # Lấy 4 bars đầu từ logit để transform, bar thứ 5 bỏ qua do biến thành "Khác..."
    logit_bars_to_transform = VGroup(*[bar.copy() for bar in logit_bars[:4]])
    
    scene.play(
        Transform(logit_bars_to_transform, prob_bars),
        run_time=1.2
    )
    
    # 5. FadeIn số % ở đầu mỗi bar
    scene.play(FadeIn(prob_numbers), run_time=0.5)

    scene.wait(0.5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # GIAI ĐOẠN 3 — Sampling: chọn từ tiếp theo
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    spinner_dot = Dot(radius=0.1, color=VG_GOLD)
    spinner_dot.next_to(logit_bars_to_transform[0], LEFT, buff=0.15)
    
    scene.play(FadeIn(spinner_dot), run_time=0.2)
    
    # 1. Dot spinner chạy 3 vòng, run_time=0.8
    run_t = 0.8 / 6
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + DOWN * 1.5), run_time=run_t, rate_func=linear)
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + UP * 1.5), run_time=run_t, rate_func=linear)
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + DOWN * 1.5), run_time=run_t, rate_func=linear)
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + UP * 1.5), run_time=run_t, rate_func=linear)
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + DOWN * 1.5), run_time=run_t, rate_func=linear)
    scene.play(spinner_dot.animate.move_to(spinner_dot.get_center() + UP * 1.5), run_time=run_t, rate_func=rate_functions.ease_out_sine)

    # 2. Dot dừng tại "Hà Nội" — bar flash
    scene.play(
        logit_bars_to_transform[0].animate.stretch_about_point(1.05, 0, logit_bars_to_transform[0].get_left()).set_color(VG_GREEN),
        run_time=0.2
    )
    scene.play(
        logit_bars_to_transform[0].animate.stretch_about_point(1/1.05, 0, logit_bars_to_transform[0].get_left()),
        run_time=0.2
    )
    
    # 3. GrowFromCenter(output_token_box)
    output_rect = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1)
    output_rect.set_stroke(color=VG_GREEN)
    output_rect.set_fill(color=VG_GREEN, opacity=0.15)
    output_text = VGText("Hà Nội", font_size=32, weight=BOLD_WEIGHT, color=VG_GREEN)
    output_group = VGroup(output_rect, output_text)
    
    output_group.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
    
    scene.play(GrowFromCenter(output_group), run_time=0.8)

    # 4. Write(sequence text dưới)
    seq_text_start = VGText('"Thủ đô của Việt Nam là ', font_size=26, color=WHITE)
    seq_text_token = VGText('Hà Nội ', font_size=26, color=VG_GREEN)
    seq_text_end = VGText('___"', font_size=26, color=WHITE)
    seq_group = VGroup(seq_text_start, seq_text_token, seq_text_end).arrange(RIGHT, buff=0.1)
    seq_group.to_edge(DOWN, buff=0.5)
    
    scene.play(Write(seq_group), run_time=1.0)

    for _ in range(2):
        scene.play(FadeOut(seq_text_end), run_time=0.2)
        scene.play(FadeIn(seq_text_end), run_time=0.2)

    # 5. FadeIn(callout dashed box + annotation đỏ)
    sampling_area = VGroup(spinner_dot, logit_bars_to_transform, prob_texts, prob_numbers)
    callout_box = DashedVMobject(SurroundingRectangle(sampling_area, color=VG_RED, buff=0.2))
    
    callout_text = VGText("← Watermark sẽ can thiệp ở đây", font_size=22, color=VG_RED)
    callout_text.next_to(callout_box, DOWN, buff=0.2)
    
    scene.play(Create(callout_box), FadeIn(callout_text), run_time=0.8)

    # Hold final state 1.5s
    scene.wait(1.5)


def play_part2_scene_2_0(scene: Scene) -> None:
    _llm_basics_scene(scene)


class Scene20_LLMBasics(Scene):
    def construct(self):
        _llm_basics_scene(self)
