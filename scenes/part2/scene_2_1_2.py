from manim import *
import random

from config.style import VGText, VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, VG_GOLD, VG_LIGHT_BLUE, BOLD_WEIGHT

def _kgw_vs_unigram_scene(scene: Scene) -> None:
    scene.camera.background_color = BLACK

    # 1. Title FadeIn top center
    title = VGText("Cách tạo Green List", font_size=42, weight=BOLD_WEIGHT, color=WHITE)
    title.to_edge(UP, buff=0.3)
    scene.play(FadeIn(title), run_time=0.7)

    # 2. DashedLine ngang ngăn cách
    separator = DashedLine(LEFT * 7, RIGHT * 7, color=VG_GRAY)
    separator.move_to(ORIGIN)
    scene.play(Create(separator), run_time=0.5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HÀNG TRÊN — KGW Watermark (Dynamic Green List)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    kgw_group = VGroup()

    kgw_header = VGText("KGW Watermark", font_size=30, weight=BOLD_WEIGHT, color=VG_BLUE)
    kgw_header.move_to(np.array([-4.5, 3.0, 0]))
    kgw_sub = VGText("Green list thay đổi theo từng bước", font_size=20, slant="ITALIC", color=VG_GRAY)
    kgw_sub.next_to(kgw_header, RIGHT, buff=0.4)
    
    scene.play(FadeIn(kgw_header), FadeIn(kgw_sub), run_time=0.5)
    kgw_group.add(kgw_header, kgw_sub)

    # Token sequence 5 bước
    kgw_steps = VGroup()
    prev_hash_box = None

    for i in range(5):
        step_group = VGroup()
        t = i + 1
        x_pos = -5.0 + i * 2.0
        
        # [a] Token hiện tại y_t
        color_y = VG_GREEN if random.random() > 0.5 else VG_RED
        token_circle = Circle(radius=0.3, color=color_y)
        token_circle.move_to(np.array([x_pos, 2.0, 0]))
        token_text = VGText(f"y_{t}", font_size=20)
        token_text.move_to(token_circle.get_center())
        token_group = VGroup(token_circle, token_text)
        
        # [b] Mũi tên xuống -> Hash box
        arrow = Arrow(start=token_circle.get_bottom(), end=token_circle.get_bottom() + DOWN * 0.4, buff=0.1, max_tip_length_to_length_ratio=0.15)
        
        hash_box = Rectangle(width=1.2, height=0.4, color=VG_PURPLE)
        hash_box.set_fill(color=VG_PURPLE, opacity=0.1)
        hash_box.next_to(arrow, DOWN, buff=0.1)
        
        hash_text_str = f"Hash(y_{t-1})" if t > 1 else "Hash(init)"
        hash_text = VGText(hash_text_str, font_size=14, color=VG_PURPLE)
        hash_text.move_to(hash_box.get_center())
        hash_group = VGroup(hash_box, hash_text)
        
        # [c] Mini vocab bar
        mini_vocab = VGroup()
        colors = [VG_GREEN, VG_GREEN, VG_RED, VG_RED]
        random.shuffle(colors)
        
        for j, c in enumerate(colors):
            dot = Dot(radius=0.06, color=c)
            dot.move_to(np.array([x_pos - 0.3 + j*0.2, hash_box.get_bottom()[1] - 0.4, 0]))
            mini_vocab.add(dot)
            
        gl_label = VGText(f"GL_{t}", font_size=14, color=VG_GREEN)
        gl_label.next_to(mini_vocab, RIGHT, buff=0.1)
        mini_vocab_group = VGroup(mini_vocab, gl_label)
        
        step_group.add(token_group, arrow, hash_group, mini_vocab_group)
        kgw_steps.add(step_group)
        
        # Animation per step
        scene.play(FadeIn(token_group), run_time=0.3)
        scene.play(GrowArrow(arrow), FadeIn(hash_group), run_time=0.3)
        
        if i == 0:
            scene.play(FadeIn(mini_vocab_group), run_time=0.3)
        else:
            # Transform mini vocab from previous to current to show shuffle
            prev_vocab_copy = kgw_steps[i-1][3].copy()
            scene.play(Transform(prev_vocab_copy, mini_vocab_group), run_time=0.4)
            # Remove the copy and add the actual one
            scene.remove(prev_vocab_copy)
            scene.add(mini_vocab_group)
            
        if t == 2:
            # Annotation: m=2
            annot_text = VGText("m=2: phụ thuộc 1 token trước", font_size=18, color=VG_BLUE)
            annot_text.next_to(hash_group, DOWN, buff=0.6).shift(RIGHT * 1.5)
            
            # Dashed rectangle around y_{t-1} (which is step 1 token) and Hash box of step 2
            surr_rect = DashedVMobject(Rectangle(
                width=2.8, height=1.8, color=VG_BLUE
            ))
            surr_rect.move_to(np.array([-4.0, 1.5, 0])) # Roughly covers y_1 and Hash(y_1)
            
            scene.play(Create(surr_rect), FadeIn(annot_text), run_time=0.5)
            kgw_group.add(surr_rect, annot_text)
            
    kgw_group.add(kgw_steps)
    
    scene.wait(0.5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HÀNG DƯỚI — Unigram Watermark (Fixed Green List)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    uni_group = VGroup()
    
    uni_header = VGText("Unigram Watermark", font_size=30, weight=BOLD_WEIGHT, color=VG_ORANGE)
    uni_header.move_to(np.array([-4.5, -0.6, 0]))
    uni_sub = VGText("Green list cố định xuyên suốt", font_size=20, slant="ITALIC", color=VG_GRAY)
    uni_sub.next_to(uni_header, RIGHT, buff=0.4)
    
    scene.play(FadeIn(uni_header), FadeIn(uni_sub), run_time=0.5)
    uni_group.add(uni_header, uni_sub)
    
    uni_steps = VGroup()
    
    # Fixed vocab box on the left
    fixed_vocab = VGroup()
    colors = [VG_GREEN, VG_RED, VG_GREEN, VG_RED] # Fixed
    for j, c in enumerate(colors):
        dot = Dot(radius=0.06, color=c)
        dot.move_to(np.array([-6.5 - 0.3 + j*0.2, -3.0, 0]))
        fixed_vocab.add(dot)
    
    fixed_gl_label = VGText("Fixed GL", font_size=14, color=VG_GREEN)
    fixed_gl_label.next_to(fixed_vocab, RIGHT, buff=0.1)
    fixed_vocab_group = VGroup(fixed_vocab, fixed_gl_label)
    
    scene.play(FadeIn(fixed_vocab_group), run_time=0.5)
    uni_group.add(fixed_vocab_group)
    
    for i in range(5):
        step_group = VGroup()
        t = i + 1
        x_pos = -5.0 + i * 2.0
        
        # [a] Token hiện tại y_t
        color_y = VG_GREEN if random.random() > 0.5 else VG_RED
        token_circle = Circle(radius=0.3, color=color_y)
        token_circle.move_to(np.array([x_pos, -1.6, 0]))
        token_text = VGText(f"y_{t}", font_size=20)
        token_text.move_to(token_circle.get_center())
        token_group = VGroup(token_circle, token_text)
        
        # [b] Mũi tên xuống -> Hash box
        arrow = Arrow(start=token_circle.get_bottom(), end=token_circle.get_bottom() + DOWN * 0.4, buff=0.1, max_tip_length_to_length_ratio=0.15)
        
        hash_box = Rectangle(width=1.2, height=0.4, color=VG_GRAY)
        hash_box.set_fill(color=VG_GRAY, opacity=0.05)
        hash_box.next_to(arrow, DOWN, buff=0.1)
        
        hash_text = VGText("Key cố định", font_size=14, color=VG_GRAY)
        hash_text.move_to(hash_box.get_center())
        hash_group = VGroup(hash_box, hash_text)
        
        # [c] Connect fixed vocab to hash box
        conn_arrow = CurvedArrow(start_point=fixed_vocab_group.get_top(), end_point=hash_box.get_left(), color=VG_ORANGE, stroke_width=2, angle=-PI/4 if i > 0 else 0)
        
        step_group.add(token_group, arrow, hash_group, conn_arrow)
        uni_steps.add(step_group)
        
        # Animation per step
        scene.play(FadeIn(token_group), run_time=0.2)
        scene.play(GrowArrow(arrow), FadeIn(hash_group), run_time=0.2)
        scene.play(Create(conn_arrow), run_time=0.3)
        
        
    # Annotation: m=1
    annot_text = VGText("m=1: không phụ thuộc token trước", font_size=18, color=VG_ORANGE)
    annot_text.next_to(uni_steps[-1], RIGHT, buff=0.8).shift(DOWN * 0.5)
    scene.play(FadeIn(annot_text), run_time=0.5)
    uni_group.add(annot_text)
            
    uni_group.add(uni_steps)
    
    scene.wait(0.5)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # KẾT: SO SÁNH TRADE-OFF
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Scale and shift to make room for table at the bottom
    # We can shrink both groups and move them up
    all_content = VGroup(kgw_group, uni_group, separator)
    scene.play(
        FadeOut(title),
        all_content.animate.scale(0.6).to_edge(UP, buff=0.2),
        run_time=1.0
    )
    
    # Table
    table = MobjectTable(
        [[VGText("Động (per-token)", font_size=20), VGText("Cố định", font_size=20)],
         [VGText("Cao hơn", font_size=20), VGText("Trung bình", font_size=20)],
         [VGText("—", font_size=20), VGText("Tốt hơn khi entropy thấp", font_size=20)]],
        row_labels=[VGText("Green list", font_size=22, weight=BOLD_WEIGHT),
                    VGText("Robustness", font_size=22, weight=BOLD_WEIGHT),
                    VGText("Đặc biệt", font_size=22, weight=BOLD_WEIGHT)],
        col_labels=[VGText("KGW", font_size=24, color=VG_BLUE, weight=BOLD_WEIGHT),
                    VGText("Unigram", font_size=24, color=VG_ORANGE, weight=BOLD_WEIGHT)],
        top_left_entry=VGText("", font_size=22),
        include_outer_lines=True,
        line_config={"stroke_width": 1, "color": VG_GRAY}
    )
    
    table.scale(0.75)
    table.to_edge(DOWN, buff=0.2)
    
    scene.play(FadeIn(table), run_time=1.0)
    
    scene.wait(2.0)

def play_part2_scene_2_1_2(scene: Scene) -> None:
    _kgw_vs_unigram_scene(scene)

class Scene212_KGWvsUnigram(Scene):
    def construct(self):
        _kgw_vs_unigram_scene(self)
