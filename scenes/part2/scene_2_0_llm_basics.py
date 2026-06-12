from manim import *
import os
from config.style import (
    VGText, VG_BLUE, VG_GOLD, VG_GREEN, VG_RED, VG_GRAY, VG_PURPLE, VG_LIGHT_BLUE,
    LARGE_FONT_SIZE, DEFAULT_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
)

def _get_audio_duration(path: str) -> float | None:
    if not path or not os.path.exists(path):
        return None
    try:
        from mutagen.mp3 import MP3
        return float(MP3(path).info.length)
    except Exception:
        pass
    try:
        from moviepy.editor import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None

def play_scene_2_0(scene: Scene):
    start_time = scene.renderer.time
    current_dir = os.path.abspath(os.path.dirname(__file__))
    voice_path = os.path.join(current_dir, "assets", "voice_2_0.mp3").replace("\\", "/")
    
    # Ghi nhận file âm thanh để mix ngoài (giống Part 1)
    voice_duration = _get_audio_duration(voice_path)
    if voice_duration is not None:
        with open("audio_times.txt", "a", encoding="utf-8") as f:
            f.write(f"{voice_path}|{start_time}\n")
    
    # Đợi câu mở đầu: "Trước khi giải mã Watermark..."
    scene.wait(7.0)

    # Bước 1 (Input): Prompt
    prompt_prefix = VGText("Prompt: ", font_size=36, color=VG_GRAY, weight=BOLD_WEIGHT)
    prompt_text = VGText("Thủ đô của Việt Nam là", font_size=36, color=VG_BLUE)
    
    prompt_group = VGroup(prompt_prefix, prompt_text).arrange(RIGHT, buff=0.2)
    prompt_group.to_edge(UP, buff=1.0)
    
    scene.play(Write(prompt_group), run_time=2.0)
    scene.wait(5.0) # "Khi nhận một câu lệnh đầu vào..."

    # Bước 2 (Logits Bar Chart)
    words = ["Hà Nội", "Paris", "London", "Tokyo"]
    logits = [10.5, 2.1, -1.0, 0.5]
    height_scale = 4.0 / 10.5
    
    bars = VGroup()
    labels = VGroup()
    values_text = VGroup()
    
    baseline_y = -2.0
    spacing = 2.0
    
    for i, (word, logit) in enumerate(zip(words, logits)):
        bar_height = max(0.1, logit * height_scale) if logit > 0 else 0.05
        bar = Rectangle(
            width=0.8, height=bar_height,
            fill_color=VG_GOLD, fill_opacity=0.8, stroke_color=VG_GOLD
        )
        bar.move_to(RIGHT * (i - 1.5) * spacing + UP * (baseline_y + bar_height/2))
        
        lbl = VGText(word, font_size=24, color=WHITE).next_to(bar, DOWN, buff=0.2)
        lbl.set_y(baseline_y - 0.5)
        
        val_lbl = VGText(str(logit), font_size=20, color=VG_GOLD).next_to(bar, UP, buff=0.2)
        
        bars.add(bar)
        labels.add(lbl)
        values_text.add(val_lbl)

    axis_line = Line(LEFT * 4, RIGHT * 4, color=WHITE).set_y(baseline_y)
    y_label = VGText("Logits", font_size=24, color=VG_GOLD).next_to(axis_line, LEFT, buff=0.3).shift(UP*0.5)
    
    chart_group = VGroup(axis_line, y_label, bars, labels, values_text)
    
    scene.play(Create(axis_line), Write(y_label), run_time=1.0)
    scene.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.5), run_time=3.0)
    scene.play(FadeIn(labels), FadeIn(values_text), run_time=1.5)
    scene.wait(6.0) # "Thay vào đó, nó quét qua bộ từ điển... Điểm số thô này được gọi là Logits."

    # Bước 3 (Softmax Transform)
    softmax_label = VGText("Hàm Softmax", font_size=36, color=VG_GREEN, weight=BOLD_WEIGHT)
    softmax_label.move_to(UP * 1.0 + RIGHT * 2.0)
    
    scene.play(FadeIn(softmax_label, shift=DOWN), run_time=1.5)
    scene.wait(4.0) # "Để những điểm số thô này có ý nghĩa thống kê..."
    
    probs = [0.98, 0.01, 0.00, 0.01]
    prob_strs = ["98%", "1%", "~0%", "1%"]
    
    new_bars = VGroup()
    new_values_text = VGroup()
    
    for i, (prob, p_str) in enumerate(zip(probs, prob_strs)):
        bar_height = max(0.05, prob * 4.0)
        color = VG_GREEN if i == 0 else VG_GRAY
        
        new_bar = Rectangle(
            width=0.8, height=bar_height,
            fill_color=color, fill_opacity=0.8, stroke_color=color
        )
        new_bar.move_to(RIGHT * (i - 1.5) * spacing + UP * (baseline_y + bar_height/2))
        
        new_val_lbl = VGText(p_str, font_size=20, color=color).next_to(new_bar, UP, buff=0.2)
        
        new_bars.add(new_bar)
        new_values_text.add(new_val_lbl)

    new_y_label = VGText("Probability", font_size=24, color=VG_GREEN).move_to(y_label)
    
    scene.play(
        Transform(bars, new_bars),
        Transform(values_text, new_values_text),
        Transform(y_label, new_y_label),
        labels[0].animate.set_color(VG_GREEN),
        labels[1:].animate.set_color(VG_GRAY),
        run_time=3.0 # Biến đổi chậm rãi hơn
    )
    scene.wait(9.0) # "Ví dụ với prompt... cột xác suất vọt lên cao nhất..."

    # Bước 4 (Sampling)
    sampling_text = VGText("Sampling: Chọn từ tiếp theo", font_size=28, color=VG_GREEN, weight=BOLD_WEIGHT)
    sampling_text.next_to(softmax_label, DOWN, buff=0.5)
    
    scene.play(Write(sampling_text), run_time=1.5)
    scene.wait(3.0) # "Bước cuối cùng là Sampling — tức là lấy mẫu."
    
    highlight_box = SurroundingRectangle(bars[0], color=VG_GREEN, buff=0.1, stroke_width=4)
    scene.play(Create(highlight_box), run_time=1.0)
    for _ in range(2):
        scene.play(FadeOut(highlight_box), run_time=0.4)
        scene.play(FadeIn(highlight_box), run_time=0.4)
        
    scene.wait(3.0) # "Xác suất càng cao, cơ hội được chọn càng lớn..."

    # Bước 5 (Kết quả)
    target_word = labels[0].copy()
    target_word.generate_target()
    target_word.target.scale(36/24)
    target_word.target.set_color(VG_GREEN)
    target_word.target.next_to(prompt_text, RIGHT, buff=0.2)
    
    scene.play(
        MoveToTarget(target_word),
        FadeOut(sampling_text),
        FadeOut(softmax_label),
        run_time=2.0
    )
    
    final_box = SurroundingRectangle(VGroup(prompt_group, target_word), color=VG_GREEN, corner_radius=0.1)
    scene.play(Create(final_box), run_time=1.5)
    
    # Tính toán thời gian còn lại của audio ("Quy trình này sẽ lặp đi lặp lại...")
    elapsed_time = scene.renderer.time - start_time
    wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
    if wait_time > 0:
        scene.wait(wait_time)
    else:
        scene.wait(8.0)
    
    # Clean up before next scene
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.5)
