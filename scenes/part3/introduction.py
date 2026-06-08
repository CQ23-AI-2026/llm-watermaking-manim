import os
import sys
import glob

# Try to find and add venv site-packages to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
venv_dirs = [
    os.path.join(root_dir, ".venv", "Lib", "site-packages"),
    os.path.join(root_dir, ".venv", "lib", "python*", "site-packages"),
]
for path_pattern in venv_dirs:
    for path in glob.glob(path_pattern):
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)

from manim import *
from config.style import (
    VGText, VGParagraph, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE, VG_RED,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT, DEFAULT_FONT
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

def create_neural_network(layers=[3, 4, 3], scale=0.6, color=VG_BLUE, stroke_opacity=0.3):
    network = VGroup()
    neurons = VGroup()
    connections = VGroup()
    
    # Layer positions
    layer_coords = []
    x_step = 1.3 * scale
    y_step = 0.9 * scale
    
    total_layers = len(layers)
    for l_idx, num_neurons in enumerate(layers):
        x = (l_idx - (total_layers - 1) / 2) * x_step
        layer_neurons = VGroup()
        coords = []
        for n_idx in range(num_neurons):
            y = (n_idx - (num_neurons - 1) / 2) * y_step
            neuron = Circle(radius=0.16 * scale, color=color, stroke_width=1.5 * scale)
            neuron.set_fill(color, opacity=0.2)
            neuron.move_to([x, y, 0])
            layer_neurons.add(neuron)
            coords.append([x, y, 0])
        neurons.add(layer_neurons)
        layer_coords.append(coords)
        
    # Connections
    for l_idx in range(total_layers - 1):
        for n1_idx, coord1 in enumerate(layer_coords[l_idx]):
            for n2_idx, coord2 in enumerate(layer_coords[l_idx+1]):
                line = Line(coord1, coord2, stroke_width=1.0 * scale, color=color, stroke_opacity=stroke_opacity)
                connections.add(line)
                
    network.add(connections, neurons)
    return network

class IntroductionScene(Scene):
    """Phân cảnh giới thiệu cho Part 3 - Model Watermark.
    Cảnh 3.0: Mở đầu Part 3 - Từ văn bản AI đến chính mô hình AI.
    Cảnh 3.1: Bối cảnh - Vì sao mô hình AI cần được bảo vệ?
    """
    def construct(self):
        current_dir = os.path.dirname(__file__)
        
        # Lưới nền mờ công nghệ đồng bộ
        grid = NumberPlane(
            background_line_style={
                "stroke_color": VG_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.06,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # =========================================================================
        # CẢNH 3.0: TỪ VĂN BẢN AI ĐẾN CHÍNH MÔ HÌNH AI
        # =========================================================================
        
        # Audio Cảnh 3.0 (nếu có)
        voice_3_0 = os.path.join(current_dir, "assets", "introduction", "scene_3_0.mp3")
        dur_3_0 = _get_audio_duration(voice_3_0) or 53.08

        if os.path.exists(voice_3_0):
            self.add_sound(voice_3_0)

        # Tiêu đề chuyển cảnh Model Watermarking ở chính giữa
        part3_title = VGText(
            "MODEL WATERMARKING",
            font_size=LARGE_FONT_SIZE,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).move_to(ORIGIN)

        # Đường trang trí phía dưới tiêu đề
        underline = Line(
            LEFT * 3.5,
            RIGHT * 3.5,
            color=VG_BLUE,
            stroke_width=2,
            stroke_opacity=0.6,
        ).next_to(part3_title, DOWN, buff=0.25)

        self.play(
            Write(part3_title),
            run_time=1.5
        )
        self.play(
            Create(underline),
            run_time=1.0
        )
        self.wait(2.0)

        # Di chuyển tiêu đề lên góc trên màn hình và ẩn đường gạch chân
        self.play(
            part3_title.animate.to_edge(UP, buff=0.5).scale(0.85),
            FadeOut(underline),
            run_time=1.2
        )
        self.wait(0.5)

        # 1. Vẽ tài liệu "Text Watermark" bên trái
        doc_card = RoundedRectangle(
            corner_radius=0.08, width=3.2, height=4.2,
            fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.2
        ).move_to([-3.4, -0.6, 0])
        
        doc_title = VGText("VĂN BẢN (TEXT)", font_size=24, color=VG_BLUE, weight=BOLD_WEIGHT).scale(12/24).move_to(doc_card.get_top() + DOWN * 0.35)
        
        # Dòng kẻ giả lập text
        lines = VGroup()
        for i in range(7):
            line_w = 2.4 - (i % 2 == 0) * 0.5
            line = Line(
                start=[-line_w/2, 0, 0], end=[line_w/2, 0, 0],
                color=VG_GRAY, stroke_width=2.0, stroke_opacity=0.5
            )
            lines.add(line)
        lines.arrange(DOWN, buff=0.25).move_to(doc_card.get_center() + DOWN * 0.2)
        
        # Dấu watermark mờ trên văn bản
        wm_stamp = Circle(radius=0.45, color=VG_GREEN, stroke_width=1.5, stroke_opacity=0.6).move_to(doc_card.get_center() + DOWN * 0.2)
        wm_text = VGText("WM", font_size=10, color=VG_GREEN, weight=BOLD_WEIGHT).move_to(wm_stamp.get_center()).rotate(20 * DEGREES)
        text_wm_group = VGroup(doc_card, doc_title, lines, wm_stamp, wm_text)

        label_left = VGText("Text Watermark", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).next_to(doc_card, DOWN, buff=0.3)

        self.play(
            FadeIn(text_wm_group, shift=RIGHT * 0.3),
            FadeIn(label_left, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(1.5)

        # Câu hỏi cho Text Watermark
        q_left = VGParagraph(
            "“Đoạn văn này có phải\ndo AI sinh ra hay không?”",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="center"
        ).scale(14/28).next_to(doc_card, UP, buff=0.3)

        self.play(Write(q_left), run_time=1.5)
        self.wait(2.0)

        # 2. Xuất hiện Model Watermark bên phải
        nn_model = create_neural_network(layers=[3, 4, 3], scale=0.8, color=VG_BLUE)
        nn_model.move_to([3.4, -0.6, 0])
        
        nn_border = RoundedRectangle(
            corner_radius=0.08, width=3.8, height=4.2,
            fill_color="#18181A", fill_opacity=0.7, stroke_color=VG_GRAY, stroke_width=1.0
        ).move_to([3.4, -0.6, 0])
        
        nn_title = VGText("MÔ HÌNH (MODEL)", font_size=24, color=VG_BLUE, weight=BOLD_WEIGHT).scale(12/24).move_to(nn_border.get_top() + DOWN * 0.35)
        
        # Dấu watermark bảo vệ mô hình
        model_wm = Star(n=8, outer_radius=0.35, inner_radius=0.2, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.7).move_to(nn_model.get_center())
        model_wm_group = VGroup(nn_border, nn_model, nn_title, model_wm)
        
        label_right = VGText("Model Watermark", font_size=16, color=VG_GOLD, weight=BOLD_WEIGHT).next_to(nn_border, DOWN, buff=0.3)

        self.play(
            FadeIn(model_wm_group, shift=LEFT * 0.3),
            FadeIn(label_right, shift=UP * 0.1),
            run_time=1.5
        )
        self.wait(2.0)

        # Câu hỏi cho Model Watermark
        q_right = VGParagraph(
            "“Làm sao chứng minh mô hình\nlà tài sản trí tuệ của mình?”",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="center"
        ).scale(14/28).next_to(nn_border, UP, buff=0.3)

        self.play(Write(q_right), run_time=1.5)
        self.wait(3.0)

        # 3. Phân biệt đối tượng bảo vệ (Highlight)
        text_protect = VGText("Bảo vệ: Nội dung đầu ra (Output)", font_size=26, color=VG_GREEN).scale(13/26).next_to(label_left, DOWN, buff=0.2)
        model_protect = VGText("Bảo vệ: Chính mô hình AI (Model)", font_size=26, color=VG_GOLD).scale(13/26).next_to(label_right, DOWN, buff=0.2)

        box_left = doc_card.copy().set_fill(opacity=0).set_stroke(VG_GREEN, width=2.0)
        box_right = nn_border.copy().set_fill(opacity=0).set_stroke(VG_GOLD, width=2.0)

        self.play(
            Create(box_left),
            FadeIn(text_protect, shift=UP * 0.15),
            run_time=0.8
        )
        self.play(
            Create(box_right),
            FadeIn(model_protect, shift=UP * 0.15),
            run_time=0.8
        )
        self.wait(max(0.5, dur_3_0 - 22.7))

        # Dọn dẹp cảnh 3.0
        self.play(
            FadeOut(text_wm_group),
            FadeOut(label_left),
            FadeOut(q_left),
            FadeOut(model_wm_group),
            FadeOut(label_right),
            FadeOut(q_right),
            FadeOut(text_protect),
            FadeOut(model_protect),
            FadeOut(box_left),
            FadeOut(box_right),
            run_time=1.0
        )
        self.wait(0.3)

        # =========================================================================
        # CẢNH 3.1: BỐI CẢNH - VÌ SAO MÔ HÌNH AI CẦN ĐƯỢC BẢO VỆ?
        # =========================================================================
        
        # Audio Cảnh 3.1 (nếu có)
        voice_3_1 = os.path.join(current_dir, "assets", "introduction", "scene_3_1.mp3")
        dur_3_1 = _get_audio_duration(voice_3_1) or 50.60

        if os.path.exists(voice_3_1):
            self.add_sound(voice_3_1)

        # Tiêu đề phụ
        sub_title = VGText(
            "VÌ SAO CẦN BẢO VỆ MÔ HÌNH AI?",
            font_size=LARGE_FONT_SIZE - 10,
            color=VG_RED,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        self.play(
            Transform(part3_title, sub_title),
            run_time=0.8
        )
        self.wait(1.0)

        # 1. Hộp mô hình trung tâm
        llm_card = RoundedRectangle(
            corner_radius=0.1, width=3.4, height=1.6,
            fill_color="#18181A", fill_opacity=0.95, stroke_color=VG_BLUE, stroke_width=2.0
        ).move_to([0, 0.4, 0])
        llm_title = VGText("MÔ HÌNH LLM", font_size=16, color=VG_BLUE, weight=BOLD_WEIGHT).move_to(llm_card.get_center())
        llm_group = VGroup(llm_card, llm_title)

        self.play(FadeIn(llm_group, scale=0.9), run_time=0.8)
        self.wait(1.0)

        # 2. Các nhánh chi phí sản xuất (Dữ liệu, GPU, Con người, Tiền bạc)
        cost_data = [
            ("Dữ liệu khổng lồ", [-3.8, 1.8, 0], VG_GREEN),
            ("Hạ tầng GPU đắt đỏ", [3.8, 1.8, 0], VG_PURPLE),
            ("Đội ngũ nghiên cứu", [-3.8, -1.0, 0], VG_ORANGE),
            ("Chi phí hàng triệu USD", [3.8, -1.0, 0], VG_RED),
        ]

        cost_boxes = VGroup()
        cost_arrows = VGroup()

        for label, pos, color in cost_data:
            box = RoundedRectangle(
                corner_radius=0.06, width=3.0, height=0.9,
                fill_color="#18181A", fill_opacity=0.9, stroke_color=color, stroke_width=1.2
            ).move_to(pos)
            text = VGText(label, font_size=12, color=color).move_to(box.get_center())
            
            # Mũi tên trỏ vào mô hình trung tâm
            arrow = Arrow(box.get_center(), llm_card.get_center(), buff=0.9, color=color, stroke_width=2)
            
            cost_boxes.add(VGroup(box, text))
            cost_arrows.add(arrow)

        # Hiện từng nhánh chi phí
        for i in range(4):
            self.play(
                FadeIn(cost_boxes[i], shift=UP * 0.15),
                Create(cost_arrows[i]),
                run_time=0.6
            )
            self.wait(0.4)
        
        self.wait(2.0)

        # Gom toàn bộ nhóm chi phí
        cost_all = VGroup(cost_boxes, cost_arrows)

        # 3. Chuyển sang phần "Đặc điểm dễ bị tấn công qua API"
        self.play(
            FadeOut(cost_all),
            llm_group.animate.move_to([-3.4, 0, 0]).scale(0.85),
            run_time=1.0
        )
        self.wait(1.0)

        # Kẻ tấn công thu thập dữ liệu qua API
        attacker_card = RoundedRectangle(
            corner_radius=0.1, width=3.0, height=1.4,
            fill_color="#18181A", fill_opacity=0.95, stroke_color=VG_RED, stroke_width=1.5
        ).move_to([3.4, 0, 0])
        attacker_title = VGText("MÔ HÌNH HỌC SINH\n(Bản sao lậu)", font_size=26, color=VG_RED, weight=BOLD_WEIGHT).scale(13/26).move_to(attacker_card.get_center())
        attacker_group = VGroup(attacker_card, attacker_title)

        # Mũi tên hỏi đáp liên tục (API queries)
        arrow_query = Arrow(attacker_card.get_left() + UP * 0.25, llm_card.get_right() + UP * 0.25, color=VG_GRAY, stroke_width=2)
        arrow_response = Arrow(llm_card.get_right() + DOWN * 0.25, attacker_card.get_left() + DOWN * 0.25, color=VG_GREEN, stroke_width=2)

        lbl_query = VGText("API Query (Câu hỏi)", font_size=24, color=VG_GRAY).scale(9/24).next_to(arrow_query, UP, buff=0.08)
        lbl_response = VGText("Response (Câu trả lời)", font_size=24, color=VG_GREEN).scale(9/24).next_to(arrow_response, DOWN, buff=0.08)

        self.play(
            FadeIn(attacker_group, shift=LEFT * 0.3),
            Create(arrow_query),
            FadeIn(lbl_query, shift=UP * 0.05),
            run_time=1.0
        )
        self.play(
            Create(arrow_response),
            FadeIn(lbl_response, shift=DOWN * 0.05),
            run_time=1.0
        )
        self.wait(1.5)

        # Hiệu ứng truyền dữ liệu lặp đi lặp lại
        dots = VGroup(*[Circle(radius=0.05, color=VG_GREEN, fill_opacity=1.0, stroke_width=0).move_to(llm_card.get_right()) for _ in range(3)])
        
        dot_anims = []
        for i, dot in enumerate(dots):
            self.add(dot)
            dot_anims.append(dot.animate(run_time=1.2, rate_func=linear).move_to(attacker_card.get_left()))
            
        self.play(AnimationGroup(*dot_anims, lag_ratio=0.3))
        self.remove(dots)

        # Chữ thuyết minh cuối cảnh
        protect_urgency = VGParagraph(
            "“Chỉ cần quyền truy cập API, kẻ tấn công có thể\nhuấn luyện một mô hình khác dựa trên dữ liệu phản hồi.”",
            font_size=28, color=VG_ORANGE, line_spacing=0.15, alignment="center"
        ).scale(14/28).move_to([0, -2.2, 0])

        self.play(Write(protect_urgency), run_time=1.5)
        self.wait(max(1.0, dur_3_1 - 18.6))

        # Dọn dẹp toàn bộ phân cảnh
        self.play(
            FadeOut(llm_group),
            FadeOut(attacker_group),
            FadeOut(arrow_query),
            FadeOut(arrow_response),
            FadeOut(lbl_query),
            FadeOut(lbl_response),
            FadeOut(protect_urgency),
            FadeOut(part3_title),
            run_time=1.2
        )
        self.wait(0.8)

def play_part3_intro(scene: Scene) -> None:
    IntroductionScene.construct(scene)
