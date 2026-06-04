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
            sys.path.append(path)

from manim import *
from config.style import (
    VGText, VG_BLUE, VG_GRAY, VG_GOLD, VG_GREEN, VG_PURPLE, VG_ORANGE, VG_RED,
    LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
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
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(path) as clip:
            return float(clip.duration)
    except Exception:
        pass
    return None


def create_newspaper_clip(
    logo_name,
    sub_headline,
    main_headline,
    angle_degrees,
    width=5.2,
    height=4.0,
    logo_path=None,
):
    """Tạo tấm cắt báo (Newspaper Clipping) mô phỏng bằng vector đồ họa độ phân giải cao."""
    
    # Tấm đổ bóng 3D mờ phía sau
    shadow = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        fill_color=BLACK,
        fill_opacity=0.15,
        stroke_width=0
    ).shift(RIGHT * 0.08 + DOWN * 0.08)
    
    # Nền giấy báo màu trắng ngà cổ điển
    paper = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        fill_color="#FDFBF7",
        fill_opacity=1.0,
        stroke_color="#222222",
        stroke_width=1.2
    )
    
    # Logo thương hiệu: ưu tiên ảnh theo đường dẫn, rồi tìm theo tên, ngược lại dùng text
    logo = None
    if logo_path and os.path.exists(logo_path):
        try:
            logo = ImageMobject(logo_path)
        except Exception:
            logo = None
    if logo is None:
        assets_dir = os.path.join("scenes", "part0", "assets", "llm_risk")
        if os.path.exists(assets_dir):
            # tìm file logo khớp tên (không phân biệt hoa thường), hỗ trợ png/jpg/svg
            lower_name = logo_name.lower()
            for fname in os.listdir(assets_dir):
                if lower_name in fname.lower():
                    try:
                        img_path = os.path.join(assets_dir, fname)
                        logo = ImageMobject(img_path)
                        break
                    except Exception:
                        logo = None
    if logo is None:
        logo_color = "#111111"
        if logo_name.upper() == "FORBES":
            logo = Text("Forbes", font="Georgia", font_size=26, weight="BOLD", color=logo_color)
        elif logo_name.upper() == "CNBC":
            logo = Text("CNBC", font="Arial", font_size=26, weight="BOLD", color="#0F1B40")
        elif logo_name.upper() == "NEWSGUARD":
            logo = Text("NewsGuard", font="Segoe UI", font_size=22, weight="BOLD", color="#27AE60")
        elif logo_name.upper() == "THE GUARDIAN":
            logo = Text("the guardian", font="Georgia", font_size=22, weight="BOLD", color="#005689")
        else:
            logo = Text(logo_name, font="Georgia", font_size=24, weight="BOLD", color=logo_color)

    if isinstance(logo, ImageMobject):
        logo_width = 1.8
        logo.scale_to_fit_width(logo_width)
    logo.move_to(paper.get_top() + DOWN * 0.45)
    
    # Dải phân cách dòng kẻ mỏng dưới logo
    divider = Line(
        paper.get_left() + RIGHT * 0.25,
        paper.get_right() + LEFT * 0.25,
        color="#333333",
        stroke_width=0.8
    ).next_to(logo, DOWN, buff=0.12)
    
    # Chuyên mục & Ngày phát hành
    sub = Text(
        sub_headline.upper(),
        font="Segoe UI",
        font_size=9,
        color="#666666",
        weight="NORMAL"
    ).next_to(divider, DOWN, buff=0.1)
    
    # Tiêu đề báo lớn (Chữ Serif đậm nét cổ điển)
    headline = Text(
        main_headline,
        font="Georgia",
        font_size=13,
        weight="BOLD",
        color="#111111",
        line_spacing=1.35
    ).next_to(sub, DOWN, buff=0.18)
    
    # Hình ảnh minh họa giả định (khung hình xám)
    img_box = Rectangle(
        width=1.5,
        height=1.0,
        fill_color="#E8E8E8",
        fill_opacity=0.9,
        stroke_color="#CCCCCC",
        stroke_width=0.5
    ).next_to(headline, DOWN, buff=0.22).align_to(paper, LEFT).shift(RIGHT * 0.35)
    
    # Các dòng chữ viết bài giả lập (nét ngang màu xám nhạt)
    text_lines = VGroup()
    for i in range(4):
        line_w = 2.4 - (i == 3) * 0.8
        line = Line(
            LEFT * line_w/2, RIGHT * line_w/2,
            color="#D0D0D0",
            stroke_width=2.5
        ).next_to(headline, DOWN, buff=0.25 + i * 0.22).align_to(paper, RIGHT).shift(LEFT * 0.35)
        text_lines.add(line)
        
    # Các dòng chữ giả lập phụ phía dưới hình ảnh
    extra_lines = VGroup()
    for i in range(2):
        line_w = 1.5 - (i == 1) * 0.4
        line = Line(
            LEFT * line_w/2, RIGHT * line_w/2,
            color="#D0D0D0",
            stroke_width=2.5
        ).next_to(img_box, DOWN, buff=0.12 + i * 0.18).align_to(img_box, LEFT)
        extra_lines.add(line)
        
    # Nhóm toàn bộ lại
    clip = Group(shadow, paper, logo, divider, sub, headline, img_box, text_lines, extra_lines)
    
    # Góc xoay nghiêng nghệ thuật
    clip.rotate(angle_degrees * DEGREES)
    
    return clip


class RisksScene(Scene):
    """Phân cảnh Sự bùng nổ của LLM và các rủi ro (Part 0.1).
    Cảnh 3: Sự ra đời của LLMs & Demo giao diện ChatGPT gõ chữ.
    Cảnh 4: Biểu đồ cột bùng nổ người dùng ChatGPT.
    Cảnh 5.1 - 5.4: 4 rủi ro lớn riêng biệt kèm các bài báo chứng thực vector.
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
        # CẢNH 3: SỰ RA ĐỜI CỦA LLMs (THE BIRTH OF LLMs)
        # =========================================================================
        
        # Audio Cảnh 3
        voice_3 = os.path.join(current_dir, "assets", "llm_risk", "scene_3.mp3")
        voice_3_duration = _get_audio_duration(voice_3)
        if voice_3_duration is not None:
            self.add_sound(voice_3)

        # Tiêu đề bên trái
        scene3_title = VGText(
            "SỰ RA ĐỜI CỦA LLMs",
            font_size=LARGE_FONT_SIZE - 8,
            color=VG_GOLD,
            weight=BOLD_WEIGHT,
        ).move_to([-3.4, 2.0, 0])

        underline3 = Line(
            LEFT * 2.2, RIGHT * 2.2,
            color=VG_GOLD,
            stroke_width=2,
            stroke_opacity=0.6
        ).next_to(scene3_title, DOWN, buff=0.15).align_to(scene3_title, LEFT)

        desc3_1 = VGText(
            "Cuối năm 2022, ChatGPT\nchính thức ra mắt bởi OpenAI.",
            font_size=20,
            color=WHITE,
            line_spacing=1.3
        ).next_to(underline3, DOWN, buff=0.4).align_to(underline3, LEFT)

        desc3_2 = VGText(
            "Mở đầu kỷ nguyên trò chuyện\ntự nhiên giữa người và AI...",
            font_size=18,
            color=VG_GRAY,
            line_spacing=1.3
        ).next_to(desc3_1, DOWN, buff=0.3).align_to(desc3_1, LEFT)

        left_side3 = VGroup(scene3_title, underline3, desc3_1, desc3_2)

        # Khung giao diện Chatbox bên phải (giả lập ChatGPT)
        chat_box = RoundedRectangle(
            corner_radius=0.12,
            width=5.8,
            height=4.6,
            stroke_color=VG_GRAY,
            stroke_width=1.5,
            fill_color=BLACK,
            fill_opacity=0.8
        ).move_to([3.3, -0.2, 0])

        chat_header = VGText(
            "ChatGPT - Assistant",
            font_size=16,
            color=WHITE,
            weight=BOLD_WEIGHT
        ).move_to(chat_box.get_top() + DOWN * 0.35)

        online_dot = Circle(
            radius=0.08,
            fill_color=VG_GREEN,
            fill_opacity=1.0,
            stroke_width=0
        ).next_to(chat_header, RIGHT, buff=0.2)

        chat_divider = Line(
            chat_box.get_left() + RIGHT * 0.2,
            chat_box.get_right() + LEFT * 0.2,
            color=VG_GRAY,
            stroke_width=0.8,
            stroke_opacity=0.4
        ).next_to(chat_header, DOWN, buff=0.2)

        # Hộp thoại tin nhắn User (phía trên bên phải)
        user_bubble = RoundedRectangle(
            corner_radius=0.08,
            width=4.6,
            height=0.7,
            stroke_width=0,
            fill_color=VG_BLUE,
            fill_opacity=0.25
        ).move_to(chat_box.get_top() + DOWN * 1.2 + RIGHT * 0.3)

        user_text = VGText(
            "Hãy viết một bài thơ ngắn về Trí tuệ nhân tạo?",
            font_size=13,
            color=WHITE
        ).move_to(user_bubble.get_center())

        # Hộp thoại tin nhắn AI (phía dưới bên trái)
        ai_bubble = RoundedRectangle(
            corner_radius=0.08,
            width=5.0,
            height=1.8,
            stroke_width=1,
            stroke_color=VG_GOLD,
            fill_color=BLACK,
            fill_opacity=1.0
        ).move_to(chat_box.get_bottom() + UP * 1.3 + LEFT * 0.1)

        ai_text = Paragraph(
            "\"Tôi chỉ là những dòng code sáng trong đêm,\n"
            "Dệt ngôn từ thành sợi nhớ dịu êm.\n"
            "Nhưng sâu thẳm trong từng câu chữ ấy,\n"
            "Là ước mơ được chạm tới tim người...\"",
            font="Segoe UI",
            font_size=12,
            line_spacing=1.4,
            color=VG_GOLD,
            alignment="left"
        ).move_to(ai_bubble.get_center())

        # Xuất hiện giao diện nền trước
        self.play(
            FadeIn(left_side3, shift=RIGHT * 0.3),
            FadeIn(chat_box, shift=LEFT * 0.3),
            FadeIn(chat_header),
            FadeIn(online_dot),
            Create(chat_divider),
            run_time=1.2
        )
        self.wait(0.5)

        # Hiệu ứng gửi tin nhắn của User
        self.play(
            FadeIn(user_bubble, scale=0.9),
            Write(user_text),
            run_time=1.0
        )
        self.wait(1.0)

        # Hiệu ứng gõ chữ phản hồi của AI
        self.play(FadeIn(ai_bubble, scale=0.95), run_time=0.5)
        self.play(Write(ai_text), run_time=3.5)

        # Chờ thuyết minh Cảnh 3 kết thúc
        if voice_3_duration is not None:
            self.wait(max(0.2, voice_3_duration - 6.7))
        else:
            self.wait(3.0)

        # Dọn dẹp cảnh 3
        self.play(
            FadeOut(left_side3, shift=LEFT * 0.5),
            FadeOut(chat_box, shift=RIGHT * 0.5),
            FadeOut(chat_header),
            FadeOut(online_dot),
            FadeOut(chat_divider),
            FadeOut(user_bubble),
            FadeOut(user_text),
            FadeOut(ai_bubble),
            FadeOut(ai_text),
            run_time=1.0
        )
        self.wait(0.3)

        # =========================================================================
        # CẢNH 4: SỰ BÙNG NỔ NGƯỜI DÙNG (THE LLM EXPLOSION)
        # =========================================================================

        # Tiêu đề Cảnh 4
        scene4_title = VGText(
            "SỰ BÙNG NỔ NGƯỜI DÙNG",
            font_size=LARGE_FONT_SIZE - 10,
            color=VG_GOLD,
            weight=BOLD_WEIGHT,
        ).to_edge(UP, buff=0.6)

        title_underline4 = Line(
            LEFT * 4, RIGHT * 4,
            color=VG_GOLD,
            stroke_width=1.5,
            stroke_opacity=0.4
        ).next_to(scene4_title, DOWN, buff=0.15)

        # Audio Cảnh 4
        voice_4 = os.path.join(current_dir, "assets", "llm_risk", "scene_4.mp3")
        voice_4_duration = _get_audio_duration(voice_4)
        if voice_4_duration is not None:
            self.add_sound(voice_4)

        self.play(
            FadeIn(scene4_title, shift=DOWN * 0.2),
            Create(title_underline4),
            run_time=1.0
        )
        self.wait(0.5)

        # Trục cơ sở & Dữ liệu biểu đồ cột
        base_line = Line(
            LEFT * 6.0, RIGHT * 6.0,
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.6
        ).shift(DOWN * 2.2)
        self.play(Create(base_line), run_time=0.8)

        assets_dir = os.path.join("scenes", "part0", "assets", "llm_risk")
        bar_data = [
            {
                "name": "Netflix",
                "time_str": "3.5 năm",
                "height": 4.5,
                "color": VG_GRAY,
                "logo_file": "Netflix.png",
            },
            {
                "name": "Twitter",
                "time_str": "2 năm",
                "height": 3.4,
                "color": VG_GRAY,
                "logo_file": "Twitter.svg.png",
            },
            {
                "name": "Facebook",
                "time_str": "10 tháng",
                "height": 2.3,
                "color": VG_GRAY,
                "logo_file": "Facebook.svg.png",
            },
            {
                "name": "Instagram",
                "time_str": "2.5 tháng",
                "height": 1.4,
                "color": VG_GRAY,
                "logo_file": "Instagram.png",
            },
            {
                "name": "ChatGPT",
                "time_str": "5 ngày",
                "height": 0.4,
                "color": VG_GOLD,
                "logo_file": "OpenAI.png",
            },
        ]

        num_bars = len(bar_data)
        bar_width = 1.0
        total_width = 11.0
        spacing = (total_width - (num_bars * bar_width)) / (num_bars - 1)
        start_x = -total_width / 2 + bar_width / 2

        bars_group = VGroup()
        labels_group = Group()
        times_group = VGroup()

        for i, item in enumerate(bar_data):
            x_pos = start_x + i * (bar_width + spacing)
            bar = Rectangle(
                width=bar_width,
                height=item["height"],
                fill_color=item["color"],
                fill_opacity=0.7,
                stroke_color=item["color"],
                stroke_width=1.5
            )
            bar.move_to([x_pos, base_line.get_center()[1] + item["height"]/2.0, 0])
            
            label = None
            logo_file = item.get("logo_file")
            if logo_file:
                logo_path = os.path.join(assets_dir, logo_file)
                if os.path.exists(logo_path):
                    try:
                        label = ImageMobject(logo_path)
                        label.scale_to_fit_width(1.2)
                    except Exception:
                        label = None
            if label is None:
                label = VGText(
                    item["name"],
                    font_size=18,
                    color=WHITE if item["name"] != "ChatGPT" else VG_GOLD,
                    weight=BOLD_WEIGHT if item["name"] == "ChatGPT" else "NORMAL",
                )
            label.next_to(bar, DOWN, buff=0.25)
            
            time_label = VGText(
                item["time_str"],
                font_size=16,
                color=item["color"],
                weight=BOLD_WEIGHT if item["name"] == "ChatGPT" else "NORMAL"
            ).next_to(bar, UP, buff=0.15)

            bars_group.add(bar)
            labels_group.add(label)
            times_group.add(time_label)

        # Hiệu ứng mọc các cột lần lượt
        if voice_4_duration is not None:
            step_wait = (voice_4_duration - 8.7) / 4.0 if voice_4_duration > 8.7 else 1.5
        else:
            step_wait = 1.5

        for i in range(num_bars - 1):
            self.play(
                GrowFromEdge(bars_group[i], DOWN),
                Write(labels_group[i]),
                FadeIn(times_group[i], shift=UP * 0.1),
                run_time=0.8
            )
            self.wait(step_wait)

        # ChatGPT
        chatgpt_idx = num_bars - 1
        chatgpt_bar = bars_group[chatgpt_idx]
        chatgpt_label = labels_group[chatgpt_idx]
        chatgpt_time = times_group[chatgpt_idx]
        glow_box = chatgpt_bar.copy().set_fill(VG_GOLD, opacity=0.35).set_stroke(VG_GOLD, width=4)
        
        self.play(
            GrowFromEdge(chatgpt_bar, DOWN),
            Write(chatgpt_label),
            FadeIn(chatgpt_time, shift=UP * 0.2),
            run_time=0.6
        )
        self.play(FadeIn(glow_box), run_time=0.3)
        self.play(FadeOut(glow_box), run_time=0.3)
        
        if voice_4_duration is not None:
            self.wait(2.0)
        else:
            self.wait(3.0)

        # Dọn dẹp Cảnh 4
        self.play(
            FadeOut(scene4_title, shift=UP * 0.3),
            FadeOut(title_underline4),
            FadeOut(bars_group),
            FadeOut(labels_group),
            FadeOut(times_group),
            FadeOut(base_line),
            run_time=1.0
        )
        self.wait(0.5)

        # =========================================================================
        # CẢNH 5.1 ĐẾN 5.4: CHI TIẾT 4 RỦI RO (THE SLIDE LAYOUT)
        # =========================================================================

        risks_slides = [
            {
                "id": "5_1",
                "tag": "RỦI RO 01",
                "title_vi": "TIN GIẢ BẦU CỬ",
                "desc_vi": "Các chatbot AI đưa ra thông tin sai lệch\nvề quy định bỏ phiếu và ứng cử viên\ntrong cuộc bầu cử tại Scotland.",
                "logo": "The Guardian",
                "logo_file": "risk_1.png",
                "sub": "Demos Election Study • 2024",
                "headline": "ChatGPT and other AI bots made\nhuge errors before Scottish\nelection, study finds",
                "angle": 3.0,
                "voice_file": "scene_51.mp3"
            },
            {
                "id": "5_2",
                "tag": "RỦI RO 02",
                "title_vi": "TÀI LIỆU & ÁN LỆ GIẢ",
                "desc_vi": "Hai luật sư tại Mỹ bị phạt nặng\nvì dùng ChatGPT bào chữa và\nvô tình nộp án lệ bịa đặt hoàn toàn.",
                "logo": "Forbes",
                "logo_file": "risk_2.png",
                "sub": "Law & Corporate • June 2023",
                "headline": "Judge Fines Two Lawyers For Using\nFake Cases From ChatGPT",
                "angle": -4.0,
                "voice_file": "scene_52.mp3"
            },
            {
                "id": "5_3",
                "tag": "RỦI RO 03",
                "title_vi": "EMAIL LỪA ĐẢO HÀNG LOẠT",
                "desc_vi": "Lợi dụng khả năng viết tự nhiên\ncủa AI để soạn thảo các email lừa đảo\n(phishing) thuyết phục quy mô lớn.",
                "logo": "CNBC",
                "logo_file": "risk_3.png",
                "sub": "Security & Fraud • April 2023",
                "headline": "AI Tools Such As ChatGPT Are\nGenerating A Mammoth Increase In\nMalicious Phishing Emails",
                "angle": 4.0,
                "voice_file": "scene_53.mp3"
            },
            {
                "id": "5_4",
                "tag": "RỦI RO 04",
                "title_vi": "ĐẠO VĂN HỌC ĐƯỜNG",
                "desc_vi": "Vấn nạn đạo văn và gian lận bùng nổ.\nHọc sinh, sinh viên lạm dụng AI\nđể làm hộ bài tập và bài thi.",
                "logo": "Forbes",
                "logo_file": "risk_4.png",
                "sub": "Education & Integrity • 2023",
                "headline": "Educators Battle Plagiarism As 89%\nOf Students Admit To Using OpenAI's\nChatGPT For Homework",
                "angle": -3.0,
                "voice_file": "scene_54.mp3"
            }
        ]

        # Vòng lặp chạy qua 4 slide rủi ro
        for idx, slide in enumerate(risks_slides):
            # Cấu hình âm thanh
            voice_file_path = os.path.join(current_dir, "assets", "llm_risk", slide["voice_file"])
            slide_duration = _get_audio_duration(voice_file_path)
            if slide_duration is not None:
                self.add_sound(voice_file_path)

            # --- DỰNG PHẦN TEXT BÊN TRÁI ---
            tag_text = VGText(
                slide["tag"],
                font_size=18,
                color=VG_RED,
                weight=BOLD_WEIGHT
            ).move_to([-3.8, 2.0, 0])

            title_text = VGText(
                slide["title_vi"],
                font_size=30,
                color=WHITE,
                weight=BOLD_WEIGHT
            ).next_to(tag_text, DOWN, buff=0.15).align_to(tag_text, LEFT)

            underline = Line(
                LEFT * 2.2, RIGHT * 2.2,
                color=VG_RED,
                stroke_width=2,
                stroke_opacity=0.6
            ).next_to(title_text, DOWN, buff=0.15).align_to(title_text, LEFT)

            desc_text = VGText(
                slide["desc_vi"],
                font_size=18,
                color=WHITE,
                line_spacing=1.4
            ).next_to(underline, DOWN, buff=0.4).align_to(underline, LEFT)

            left_group = VGroup(tag_text, title_text, underline, desc_text)

            # --- DỰNG HÌNH ẢNH BÁO BÊN PHẢI ---
            img_path = os.path.join(
                current_dir, "assets", "llm_risk", slide["logo_file"]
            )
            
            if os.path.exists(img_path):
                main_img = ImageMobject(img_path)
                main_img.scale_to_fit_width(4.8)
                
                newspaper_clip = main_img
                newspaper_clip.move_to([3.8, -0.2, 0])
            else:
                newspaper_clip = create_newspaper_clip(
                    logo_name=slide["logo"],
                    sub_headline=slide["sub"],
                    main_headline=slide["headline"],
                    angle_degrees=0.0, # Straight
                    logo_path=None,
                ).move_to([3.8, -0.2, 0])

            # --- HOẠT ẢNH XUẤT HIỆN ---
            # Text bên trái trượt lên nhẹ, Tờ báo trượt từ phải sang trái kèm xoay nghiêng
            self.play(
                FadeIn(left_group, shift=UP * 0.3),
                FadeIn(newspaper_clip, shift=LEFT * 0.4),
                run_time=1.2
            )
            
            # Thời gian chờ thuyết minh
            if slide_duration is not None:
                self.wait(max(0.5, slide_duration - 1.2))
            else:
                self.wait(4.0)

            # --- DỌN DẸP ĐỂ SANG SLIDE TIẾP THEO ---
            # Slide cuối cùng thì dọn dẹp biến mất hoàn toàn
            if idx == len(risks_slides) - 1:
                self.play(
                    FadeOut(left_group, shift=LEFT * 0.4),
                    FadeOut(newspaper_clip, shift=RIGHT * 0.4),
                    run_time=1.0
                )
            else:
                # Các slide giữa chuyển dịch ngang mượt mà
                self.play(
                    FadeOut(left_group, shift=LEFT * 0.5),
                    FadeOut(newspaper_clip, shift=LEFT * 0.5),
                    run_time=0.8
                )
            self.wait(0.2)

        self.wait(0.5)


def play_part0_risks(scene: Scene) -> None:
    RisksScene.construct(scene)
