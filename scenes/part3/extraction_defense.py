import os
import sys
import glob
import numpy as np

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

class ExtractionDefenseScene(Scene):
    """Phân cảnh Phòng thủ chống Model Extraction (Cảnh 3.4 - 3.9).
    Slide 1: Khái niệm Model Extraction & Tín hiệu ẩn (Cảnh 3.4)
    Slide 2: DRW - Kháng Distillation (Cảnh 3.5)
    Slide 3: GINSEW - Thủy vân tự hồi quy (Cảnh 3.6)
    Slide 4: CATER - Thủy vân có điều kiện (Cảnh 3.7)
    Slide 5: Cơ chế Probing & Phân tích phổ (Cảnh 3.8)
    Slide 6: Đánh đổi chất lượng & Độ bền bỉ (Cảnh 3.9)
    """
    def construct(self):
        current_dir = os.path.dirname(__file__)
        
        # Thêm grid nếu chưa có trên screen
        grid_exists = any(isinstance(m, NumberPlane) for m in self.mobjects)
        if not grid_exists:
            grid = NumberPlane(
                background_line_style={
                    "stroke_color": VG_GRAY,
                    "stroke_width": 1,
                    "stroke_opacity": 0.06,
                },
                axis_config={"stroke_opacity": 0},
            )
            self.add(grid)

        # Tiêu đề chính của phân cảnh
        scene_title = VGText(
            "PHÒNG THỦ CHỐNG MODEL EXTRACTION",
            font_size=LARGE_FONT_SIZE - 10,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).to_edge(UP, buff=0.5)

        underline = Line(
            LEFT * 4.5, RIGHT * 4.5,
            color=VG_GOLD, stroke_width=2, stroke_opacity=0.6
        ).next_to(scene_title, DOWN, buff=0.2)

        # Audio paths & durations
        extraction_dir = os.path.join(current_dir, "assets", "extraction")
        voice_1 = os.path.join(extraction_dir, "extraction_intro_drw.mp3") # Legacy combined file
        voice_1a = os.path.join(extraction_dir, "extraction_intro.mp3") # Split 3.4
        voice_1b = os.path.join(extraction_dir, "extraction_drw.mp3") # Split 3.5
        voice_2 = os.path.join(extraction_dir, "extraction_ginsew.mp3")
        voice_3 = os.path.join(extraction_dir, "extraction_cater.mp3")
        voice_4 = os.path.join(extraction_dir, "extraction_probing.mp3")
        voice_5 = os.path.join(extraction_dir, "extraction_tradeoff.mp3")

        dur_1 = _get_audio_duration(voice_1) or 86.0
        dur_1a = _get_audio_duration(voice_1a) or 42.0
        dur_1b = _get_audio_duration(voice_1b) or 44.0
        
        # Nếu chỉ có tệp gộp cũ, ta chia đôi thời gian ước tính cho 2 slide
        if not os.path.exists(voice_1a) and not os.path.exists(voice_1b) and os.path.exists(voice_1):
            dur_1a = dur_1 * 0.48
            dur_1b = dur_1 * 0.52

        dur_2 = _get_audio_duration(voice_2) or 74.0
        dur_3 = _get_audio_duration(voice_3) or 60.0
        dur_4 = _get_audio_duration(voice_4) or 60.0
        dur_5 = _get_audio_duration(voice_5) or 78.0

        # Xuất hiện Tiêu đề chính trước
        self.play(
            Write(scene_title),
            Create(underline),
            run_time=1.2
        )
        self.wait(0.5)

        # =========================================================================
        # SLIDE 1: MODEL EXTRACTION INTRO (Cảnh 3.4)
        # =========================================================================
        if os.path.exists(voice_1a):
            self.add_sound(voice_1a)
        elif os.path.exists(voice_1):
            self.add_sound(voice_1) # Phát tệp legacy nếu có

        title_ext = VGText("TRÍCH XUẤT MÔ HÌNH & CHƯNG CẤT", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_ext = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GREEN, stroke_width=2, stroke_opacity=0.6).next_to(title_ext, DOWN, buff=0.15).align_to(title_ext, LEFT)
        
        desc_ext = VGParagraph(
            "Mô hình gốc (Teacher) bảo vệ API\nbằng cách nhúng watermark vào dữ liệu đầu ra.\nKẻ tấn công truy vấn và dùng dữ liệu đó\nđể chưng cất (distill) mô hình học sinh.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_ext, DOWN, buff=0.4).align_to(line_ext, LEFT)

        left_g_ext = VGroup(title_ext, line_ext, desc_ext)

        # Visual bên phải Phase 1
        teacher_box = RoundedRectangle(corner_radius=0.08, width=2.2, height=1.0, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([1.8, 0.8, 0])
        teacher_lbl = VGText("Teacher Model\n(Mô hình gốc)", font_size=16, color=VG_BLUE).scale(8/16).move_to(teacher_box.get_center())
        teacher_group = VGroup(teacher_box, teacher_lbl)

        data_box = RoundedRectangle(corner_radius=0.06, width=2.0, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([4.8, -0.4, 0])
        data_lbl = VGText("Dữ liệu phản hồi\n+ Watermark", font_size=16, color=VG_GRAY).scale(8/16).move_to(data_box.get_center())
        data_group = VGroup(data_box, data_lbl)

        student_box = RoundedRectangle(corner_radius=0.08, width=2.2, height=1.0, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_RED, stroke_width=1.5).move_to([1.8, -1.6, 0])
        student_lbl = VGText("Student Model\n(Mô hình lậu)", font_size=16, color=VG_RED).scale(8/16).move_to(student_box.get_center())
        student_group = VGroup(student_box, student_lbl)

        a_t_to_d = Arrow(teacher_box.get_right(), data_box.get_top(), buff=0.1, color=VG_GREEN, stroke_width=2)
        a_d_to_s = Arrow(data_box.get_bottom(), student_box.get_right(), buff=0.1, color=VG_RED, stroke_width=2)
        a_s_to_t = Arrow(student_box.get_top(), teacher_box.get_bottom(), buff=0.1, color=VG_GOLD, stroke_width=1.5, stroke_opacity=0.6)
        prob_lbl = VGText("API Probing (Hậu kiểm)", font_size=14, color=VG_GOLD).scale(7/14).next_to(a_s_to_t, LEFT, buff=0.1)

        right_g_ext = VGroup(teacher_group, data_group, student_group, a_t_to_d, a_d_to_s, a_s_to_t, prob_lbl)

        # Xuất hiện Slide 1
        self.play(
            FadeIn(left_g_ext, shift=UP * 0.3),
            FadeIn(right_g_ext, shift=LEFT * 0.4),
            run_time=1.2
        )
        
        # Chờ thời lượng của Slide 1
        self.wait(max(3.0, dur_1a - 1.2))

        # Dọn dẹp Slide 1
        self.play(
            FadeOut(left_g_ext),
            FadeOut(right_g_ext),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 2: DRW - DISTILLATION-RESISTANT WATERMARKING (Cảnh 3.5)
        # =========================================================================
        if os.path.exists(voice_1b):
            self.add_sound(voice_1b)

        title_drw = VGText("DRW - KHÁNG DISTILLATION", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_drw = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GREEN, stroke_width=2, stroke_opacity=0.6).next_to(title_drw, DOWN, buff=0.15).align_to(title_drw, LEFT)
        
        desc_drw = VGParagraph(
            "DRW can thiệp rất nhẹ vào vector phân phối\nxác suất dự đoán đầu ra. Sự thay đổi này\nvô hình với người dùng nhưng mô hình học sinh\nsẽ hấp thụ nó trong quá trình huấn luyện.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_drw, DOWN, buff=0.4).align_to(line_drw, LEFT)

        left_g_drw = VGroup(title_drw, line_drw, desc_drw)

        # Biểu đồ phân phối xác suất
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=4.2, y_length=2.5, axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}).move_to([3.4, -0.4, 0])
        
        # Vẽ cột xác suất ban đầu (màu xanh nước biển) và nhúng watermark (glowing gold)
        bar_heights_orig = [1.2, 2.8, 1.8, 0.8, 0.4]
        bar_heights_wm = [1.25, 2.6, 2.2, 0.75, 0.4] # dịch chuyển nhẹ từ bar 2 sang bar 3
        
        bars_orig = VGroup()
        bars_wm = VGroup()
        
        for i in range(5):
            x_val = axes.c2p(i + 1, 0)
            
            # Cột nguyên bản
            b_o = Rectangle(width=0.3, height=bar_heights_orig[i]*0.5, fill_color=VG_BLUE, fill_opacity=0.4, stroke_color=VG_BLUE, stroke_width=1.0)
            b_o.move_to(x_val, coor_mask=[1, 0, 1]).align_to(axes.c2p(0, 0), DOWN)
            bars_orig.add(b_o)
            
            # Cột sau khi nhúng watermark
            b_w = Rectangle(width=0.3, height=bar_heights_wm[i]*0.5, fill_color=VG_GOLD, fill_opacity=0.8, stroke_color=VG_GOLD, stroke_width=1.5)
            b_w.move_to(x_val, coor_mask=[1, 0, 1]).align_to(axes.c2p(0, 0), DOWN)
            bars_wm.add(b_w)

        chart_label = VGText("Biến đổi phân phối xác suất P(token)", font_size=16, color=VG_GOLD).scale(8/16).next_to(axes, UP, buff=0.2)
        right_g_drw = VGroup(axes, bars_orig, chart_label)

        # Xuất hiện Slide 2
        self.play(
            FadeIn(left_g_drw, shift=UP * 0.3),
            FadeIn(right_g_drw, shift=LEFT * 0.4),
            run_time=1.2
        )
        
        # Hiệu ứng nhấp nháy chuyển từ bars_orig sang bars_wm
        self.wait(1.5)
        self.play(
            Transform(bars_orig, bars_wm),
            chart_label.animate.set_color(VG_GOLD),
            run_time=1.5
        )
        
        # Chờ nốt thời gian còn lại của Slide 2
        self.wait(max(3.0, dur_1b - 1.2 - 1.5 - 1.5))

        # Dọn dẹp Slide 2
        self.play(
            FadeOut(left_g_drw),
            FadeOut(right_g_drw),
            FadeOut(bars_orig),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 3: GINSEW - THỦY VÂN SINH VĂN BẢN VÔ HÌNH (Cảnh 3.6)
        # =========================================================================
        if os.path.exists(voice_2):
            self.add_sound(voice_2)

        title_ginsew = VGText("GINSEW - THỦY VÂN TỰ HỒI QUY", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_ginsew = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_BLUE, stroke_width=2, stroke_opacity=0.6).next_to(title_ginsew, DOWN, buff=0.15).align_to(title_ginsew, LEFT)
        
        desc_ginsew = VGParagraph(
            "GINSEW dành cho mô hình sinh văn bản.\nTại mỗi bước sinh, mô hình can thiệp nhẹ\nvào vector xác suất của các token kế tiếp,\ntạo ra một chữ ký thống kê vô hình\nở chuỗi văn bản đầu ra.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_ginsew, DOWN, buff=0.4).align_to(line_ginsew, LEFT)

        left_g_ginsew = VGroup(title_ginsew, line_ginsew, desc_ginsew)

        # Visual GINSEW: Chuỗi sinh Token tự hồi quy
        tok_1 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([1.2, 0.8, 0])
        tok_1_lbl = VGText("Token t-2", font_size=16, color=VG_GRAY).scale(8/16).move_to(tok_1.get_center())
        t1_group = VGroup(tok_1, tok_1_lbl)

        tok_2 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([3.0, 0.8, 0])
        tok_2_lbl = VGText("Token t-1", font_size=16, color=VG_GRAY).scale(8/16).move_to(tok_2.get_center())
        t2_group = VGroup(tok_2, tok_2_lbl)

        arrow_t1_t2 = Arrow(tok_1.get_right(), tok_2.get_left(), buff=0.05, color=VG_BLUE, stroke_width=1.5)

        # Vector xác suất tại bước t
        v_box = RoundedRectangle(corner_radius=0.05, width=2.4, height=1.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([3.0, -1.0, 0])
        v_lbl = VGText("Xác suất từ vựng P(V)", font_size=14, color=VG_BLUE).scale(7/14).next_to(v_box, UP, buff=0.1)
        
        # Các dòng biểu diễn xác suất token
        lines_v = VGroup()
        token_names = ["được", "học", "chơi", "ngủ"]
        token_probs = [0.1, 0.65, 0.15, 0.1] # 'học' được ưu tiên bằng GINSEW
        
        for idx, (name, prob) in enumerate(zip(token_names, token_probs)):
            y_pos = v_box.get_top()[1] - 0.3 - idx * 0.35
            name_txt = VGText(name, font_size=16, color=WHITE).scale(8/16).move_to([2.1, y_pos, 0])
            
            p_bar_bg = Line(start=[2.6, y_pos, 0], end=[4.0, y_pos, 0], color=VG_GRAY, stroke_width=6, stroke_opacity=0.2)
            p_bar_fill = Line(start=[2.6, y_pos, 0], end=[2.6 + prob * 1.4, y_pos, 0], color=VG_GREEN if idx == 1 else VG_BLUE, stroke_width=6)
            lines_v.add(name_txt, p_bar_bg, p_bar_fill)

        arrow_t2_v = Arrow(tok_2.get_bottom(), v_box.get_top(), buff=0.1, color=VG_BLUE, stroke_width=1.5)
        
        # Token t tiếp theo sinh ra
        tok_3 = RoundedRectangle(corner_radius=0.05, width=1.3, height=0.6, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0).move_to([4.8, 0.8, 0])
        tok_3_lbl = VGText("Token t (học)", font_size=16, color=VG_GREEN, weight=BOLD_WEIGHT).scale(8/16).move_to(tok_3.get_center())
        t3_group = VGroup(tok_3, tok_3_lbl)

        arrow_v_t3 = Arrow(v_box.get_right(), tok_3.get_bottom(), buff=0.1, color=VG_GREEN, stroke_width=2)

        right_g_ginsew = VGroup(t1_group, t2_group, arrow_t1_t2, v_box, v_lbl, lines_v, arrow_t2_v, t3_group, arrow_v_t3)

        self.play(
            FadeIn(left_g_ginsew, shift=UP * 0.3),
            FadeIn(right_g_ginsew, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng nhấp nháy xanh lá cây ở token được chọn
        self.wait(1.5)
        self.play(
            t3_group.animate.scale(1.1),
            lines_v[4].animate.set_stroke(color=VG_GOLD, width=8), # highlight bar fill của 'học'
            run_time=0.6
        )
        self.play(
            t3_group.animate.scale(1.0/1.1),
            lines_v[4].animate.set_stroke(color=VG_GREEN, width=6),
            run_time=0.6
        )

        self.wait(max(1.0, dur_2 - 1.2 - 1.5 - 1.2 - 0.8)) # trừ thời gian anim và exit

        self.play(
            FadeOut(left_g_ginsew, shift=LEFT * 0.5),
            FadeOut(right_g_ginsew, shift=LEFT * 0.5),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 4: CATER - WATERMARK CÓ ĐIỀU KIỆN (Cảnh 3.7)
        # =========================================================================
        if os.path.exists(voice_3):
            self.add_sound(voice_3)

        title_cater = VGText("CATER - THỦY VÂN CÓ ĐIỀU KIỆN", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_cater = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_PURPLE, stroke_width=2, stroke_opacity=0.6).next_to(title_cater, DOWN, buff=0.15).align_to(title_cater, LEFT)
        
        desc_cater = VGParagraph(
            "CATER phụ thuộc chặt chẽ vào ngữ cảnh.\nKhi phát hiện điều kiện định sẵn trong văn bản,\nmô hình thay đổi lựa chọn từ đồng nghĩa.\nĐiều này tối ưu hóa độ tự nhiên của văn bản\nvà khả năng phát hiện mô hình bắt chước.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_cater, DOWN, buff=0.4).align_to(line_cater, LEFT)

        left_g_cater = VGroup(title_cater, line_cater, desc_cater)

        # Visual CATER: Cây quyết định lựa chọn từ theo điều kiện
        root_node = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_BLUE, stroke_width=1.5).move_to([3.2, 1.0, 0])
        root_lbl = VGText("Ngữ cảnh hiện tại\n(Context Trigger)", font_size=16, color=VG_BLUE).scale(8/16).move_to(root_node.get_center())
        root_group = VGroup(root_node, root_lbl)

        # Lựa chọn 1: Có khớp điều kiện
        node_yes = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=2.0).move_to([1.8, -1.0, 0])
        node_yes_lbl = VGText("Khớp điều kiện:\nChọn 'nghiên cứu' [WM]", font_size=14, color=VG_GREEN).scale(7/14).move_to(node_yes.get_center())
        yes_group = VGroup(node_yes, node_yes_lbl)

        # Lựa chọn 2: Không khớp điều kiện
        node_no = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.8, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GRAY, stroke_width=1.0).move_to([4.6, -1.0, 0])
        node_no_lbl = VGText("Không khớp:\nChọn 'học tập' (Tự nhiên)", font_size=14, color=VG_GRAY).scale(7/14).move_to(node_no.get_center())
        no_group = VGroup(node_no, node_no_lbl)

        # Mũi tên phân nhánh
        a_yes = Arrow(root_node.get_bottom(), node_yes.get_top(), buff=0.1, color=VG_GREEN, stroke_width=2)
        a_no = Arrow(root_node.get_bottom(), node_no.get_top(), buff=0.1, color=VG_GRAY, stroke_width=1.5)

        right_g_cater = VGroup(root_group, yes_group, no_group, a_yes, a_no)

        self.play(
            FadeIn(left_g_cater, shift=UP * 0.3),
            FadeIn(right_g_cater, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng chạy luồng quyết định (nháy sáng nhánh Yes)
        self.wait(1.5)
        self.play(
            a_yes.animate.set_stroke(color=VG_GOLD, width=4),
            node_yes.animate.set_stroke(color=VG_GOLD, width=3.0),
            run_time=0.8
        )
        self.play(
            a_yes.animate.set_stroke(color=VG_GREEN, width=2),
            node_yes.animate.set_stroke(color=VG_GREEN, width=2.0),
            run_time=0.8
        )

        self.wait(max(1.0, dur_3 - 1.2 - 1.5 - 1.6 - 0.8))

        self.play(
            FadeOut(left_g_cater, shift=LEFT * 0.5),
            FadeOut(right_g_cater, shift=LEFT * 0.5),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 5: PROBING & PHÂN TÍCH PHỔ (Cảnh 3.8)
        # =========================================================================
        if os.path.exists(voice_4):
            self.add_sound(voice_4)

        title_prob = VGText("CƠ CHẾ PROBING VÀ PHÂN TÍCH PHỔ", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_prob = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_GOLD, stroke_width=2, stroke_opacity=0.6).next_to(title_prob, DOWN, buff=0.15).align_to(title_prob, LEFT)
        
        desc_prob = VGParagraph(
            "Để xác minh watermark, chủ sở hữu gửi các\ntruy vấn probing đặc biệt đến API nghi ngờ.\nPhân tích phổ (Periodogram) các phản hồi\nsẽ chỉ ra tín hiệu tuần hoàn bí mật\nnổi lên rõ rệt khỏi nhiễu nền.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_prob, DOWN, buff=0.4).align_to(line_prob, LEFT)

        left_g_prob = VGroup(title_prob, line_prob, desc_prob)

        # Visual Probing: Đồ thị phân tích phổ Periodogram
        axes_4 = Axes(
            x_range=[0, 10, 1], y_range=[0, 4, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"stroke_color": VG_GRAY, "stroke_width": 1}
        ).move_to([3.4, -0.4, 0])

        # Hàm vẽ phổ nhiễu nền
        noise_curve = axes_4.plot(
            lambda x: 0.4 * np.sin(3*x) + 0.2 * np.cos(7*x) + 0.1 * np.sin(15*x) + 0.6,
            color=VG_GRAY, stroke_width=1.5
        )

        # Hàm vẽ đỉnh phổ watermark nhô cao tại x=5
        peak_curve = axes_4.plot(
            lambda x: 2.8 * np.exp(-((x - 5) / 0.4)**2) + 0.4 * np.sin(3*x) + 0.2 * np.cos(7*x) + 0.1 * np.sin(15*x) + 0.6,
            color=VG_GOLD, stroke_width=2.5
        )

        chart_title_4 = VGText("Đồ thị phân tích phổ Periodogram", font_size=16, color=VG_GRAY).scale(8/16).next_to(axes_4, UP, buff=0.2)
        detector_lbl = VGText("Tín hiệu Watermark (F=5)", font_size=14, color=VG_GOLD, weight=BOLD_WEIGHT).scale(7/14).move_to(axes_4.c2p(5, 3.4))
        
        # Mũi tên chỉ vào đỉnh
        pointer_arrow = Arrow(axes_4.c2p(5.5, 3.2), axes_4.c2p(5.0, 2.5), buff=0.05, color=VG_GOLD, stroke_width=1.5)

        right_g_prob1 = VGroup(axes_4, noise_curve, chart_title_4)
        right_g_prob2 = VGroup(peak_curve, detector_lbl, pointer_arrow)

        self.play(
            FadeIn(left_g_prob, shift=UP * 0.3),
            FadeIn(right_g_prob1, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Nhô cao đỉnh phổ thể hiện phát hiện watermark
        self.wait(2.0)
        self.play(
            Transform(noise_curve, peak_curve),
            FadeIn(detector_lbl),
            Create(pointer_arrow),
            chart_title_4.animate.set_color(VG_GOLD),
            run_time=1.8
        )

        self.wait(max(1.0, dur_4 - 1.2 - 2.0 - 1.8 - 0.8))

        self.play(
            FadeOut(left_g_prob, shift=LEFT * 0.5),
            FadeOut(right_g_prob1),
            FadeOut(right_g_prob2),
            FadeOut(noise_curve),
            run_time=0.8
        )
        self.wait(0.2)

        # =========================================================================
        # SLIDE 6: ĐÁNH ĐỔI CHẤT LƯỢNG & PHA LOÃNG DỮ LIỆU (Cảnh 3.9)
        # =========================================================================
        if os.path.exists(voice_5):
            self.add_sound(voice_5)

        title_trade = VGText("ĐÁNH ĐỔI CHẤT LƯỢNG & ĐỘ BỀN BỈ", font_size=40, color=WHITE, weight=BOLD_WEIGHT).scale(18/40).move_to([-3.8, 1.8, 0])
        line_trade = Line(LEFT * 2.2, RIGHT * 2.2, color=VG_ORANGE, stroke_width=2, stroke_opacity=0.6).next_to(title_trade, DOWN, buff=0.15).align_to(title_trade, LEFT)
        
        desc_trade = VGParagraph(
            "Tồn tại sự đánh đổi giữa chất lượng văn bản\nsinh ra và khả năng phát hiện. Bên cạnh đó,\nmột watermark tốt phải bền bỉ ngay cả khi\ndữ liệu chưng cất bị pha loãng bằng cách\ntrộn lẫn với các nguồn dữ liệu sạch khác.",
            font_size=28, color=WHITE, line_spacing=0.15, alignment="left"
        ).scale(14/28).next_to(line_trade, DOWN, buff=0.4).align_to(line_trade, LEFT)

        left_g_trade = VGroup(title_trade, line_trade, desc_trade)

        # Visual Slide 5: Cán cân đánh đổi (Quality vs Detectability)
        base = Polygon(
            [3.4, -1.8, 0], [3.2, -2.4, 0], [3.6, -2.4, 0],
            color=VG_GRAY, fill_color=VG_GRAY, fill_opacity=0.5, stroke_width=1.5
        )
        pillar = Line(start=[3.4, -1.8, 0], end=[3.4, -0.6, 0], color=VG_GRAY, stroke_width=2)
        
        # VGroup chứa phần thanh ngang và đĩa cân có thể xoay được
        scale_beam = Line(start=[1.8, -0.6, 0], end=[5.0, -0.6, 0], color=VG_GRAY, stroke_width=3)
        pivot = Dot([3.4, -0.6, 0], radius=0.08, color=VG_ORANGE)
        
        left_pan = Line(start=[1.8, -0.6, 0], end=[1.8, -1.4, 0], color=VG_GRAY, stroke_width=1.5)
        left_plate = RoundedRectangle(corner_radius=0.04, width=1.0, height=0.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_GREEN, stroke_width=1.5).move_to([1.8, -1.45, 0])
        left_lbl = VGText("Chất lượng\n(Quality)", font_size=14, color=VG_GREEN).scale(7/14).next_to(left_plate, UP, buff=0.1)
        left_pan_group = VGroup(left_pan, left_plate, left_lbl)

        right_pan = Line(start=[5.0, -0.6, 0], end=[5.0, -1.4, 0], color=VG_GRAY, stroke_width=1.5)
        right_plate = RoundedRectangle(corner_radius=0.04, width=1.0, height=0.1, fill_color="#18181A", fill_opacity=0.9, stroke_color=VG_ORANGE, stroke_width=1.5).move_to([5.0, -1.45, 0])
        right_lbl = VGText("Độ nhạy\n(Detection)", font_size=14, color=VG_ORANGE).scale(7/14).next_to(right_plate, UP, buff=0.1)
        right_pan_group = VGroup(right_pan, right_plate, right_lbl)

        beam_system = VGroup(scale_beam, left_pan_group, right_pan_group)

        right_g_trade = VGroup(base, pillar, beam_system, pivot)

        self.play(
            FadeIn(left_g_trade, shift=UP * 0.3),
            FadeIn(right_g_trade, shift=LEFT * 0.4),
            run_time=1.2
        )

        # Hiệu ứng bập bênh nghiêng đĩa cân
        self.wait(2.0)
        self.play(
            Rotate(beam_system, angle=-10 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.2
        )
        self.play(
            Rotate(beam_system, angle=20 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.6
        )
        self.play(
            Rotate(beam_system, angle=-10 * DEGREES, about_point=[3.4, -0.6, 0]),
            run_time=1.2
        )

        self.wait(max(1.0, dur_5 - 1.2 - 2.0 - 4.0 - 1.0)) # trừ đi anim, wait và exit

        # Dọn dẹp Slide 6 (Cũng là kết thúc phân cảnh)
        self.play(
            FadeOut(left_g_trade, shift=LEFT * 0.4),
            FadeOut(right_g_trade, shift=RIGHT * 0.4),
            run_time=1.0
        )
        self.wait(0.2)

        # Dọn dẹp tiêu đề chính (giữ grid cho phân cảnh tiếp theo)
        self.play(
            FadeOut(scene_title),
            FadeOut(underline),
            run_time=1.0
        )
        self.wait(0.5)

def play_part3_extraction_defense(scene: Scene) -> None:
    ExtractionDefenseScene.construct(scene)
