# DÀN Ý VIDEO: WATERMARKING CHO MÔ HÌNH NGÔN NGỮ LỚN (LLMs)
<!-- Phong cách trình bày: 3Blue1Brown cấp độ sinh viên đại học -->
<!-- Ngôn ngữ chính: Tiếng Việt. Giữ nguyên thuật ngữ chuyên biệt bằng tiếng Anh -->
<!-- Nguồn tham khảo chính: Tutorial & Slide "Watermarking for Large Language Models" NeurIPS 2024 -->
<!-- Mọi hình ảnh lấy từ slide gốc cần trích nguồn rõ ràng -->

---

## QUY ƯỚC ĐÁNH DẤU

| Ký hiệu | Ý nghĩa |
|----------|----------|
| **HARD** | Nội dung khó cần cân nhắc mức độ chi tiết khi trình bày |
| **ANIMATION** | Gợi ý hiệu ứng animation Manim |
| **TODO** | Nội dung cần được bổ sung thêm |
| **IMAGE** | Cần hình ảnh minh họa (slide gốc hoặc tự tạo) |
| **EST** | Thời lượng ước tính cho phần đó |

---

## CẤU TRÚC TỔNG QUAN

```
Part 0: Bối cảnh & Động lực ~34 phút
```

---

# PART 0 BỐI CẢNH & ĐỘNG LỰC
> **Mục tiêu:** Khán giả hiểu TẠI SAO cần phát hiện văn bản AI và tại sao Watermarking là giải pháp hứa hẹn nhất.

### 0.1 Sự bùng nổ của LLM và các rủi ro
- Số người dùng LLM tăng mạnh kéo theo các hệ quả tiêu cực:
 1. **Tin giả** (Misinformation)
 2. **Bằng chứng pháp lý giả** Forbes: "Two US lawyers fined for submitting fake court citations from ChatGPT"
 3. **Lừa đảo / Phishing** CNBC: "AI tools generating mammoth increase in phishing emails"
 4. **Đạo văn** Forbes: "89% of students admit to using ChatGPT for Homework"
- Minh họa: collage các tiêu đề báo chí thật

### 0.2 Thách thức: Phân biệt AI vs. Con người
- Ví dụ so sánh hai đoạn thơ (AI viết vs. Người viết) khán giả tự đoán
 - **Đoạn 1 (AI):** "Through the town, and past the lights..."
 - **Đoạn 2 (Human):** "Over the river, and through the wood..."
- Reveal đáp án bất ngờ dẫn đến câu hỏi: "Vậy làm sao để biết?"

### 0.3 Các phương pháp hiện tại và hạn chế
- **Cách 1:** Mở đầu bằng "As an AI Model" Dễ dàng xóa bỏ Không khả thi
- **Cách 2:** Train model phát hiện (GPTZero, Turnitin) Hạn chế:
 1. **Quá nhiều False Positives** (dương tính giả)
 2. **Out-of-Distribution Data** VD: GPT-4 text qua GPT-2 bị đánh giá "Human"
 3. **AI liên tục phát triển** detector nhanh chóng lỗi thời
- Ví dụ minh họa cụ thể về false positive (quan trọng, cần trình bày kỹ)

### 0.4 Dẫn đến giải pháp: Watermarking
- Watermark (Thủy vân) là phương pháp **chủ động** nhúng dấu hiệu vào quá trình sinh văn bản
- **Ứng dụng mở rộng:** Chống copy model (Model Extraction Attack)
 - Lấy text từ model nghi vấn kiểm tra Watermark từ model gốc xác định vi phạm

---