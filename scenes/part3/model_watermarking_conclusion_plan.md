# Kế hoạch cảnh 3.14 - Tổng kết Part 3: Text Watermarking vs Model Watermarking

File triển khai: `scenes/part3/model_watermarking_conclusion.py`

Mục tiêu: kết lại Part 3 bằng cách so sánh rõ **text watermarking** và **model watermarking**, sau đó tổng hợp vai trò của model watermarking trong bảo vệ quyền sở hữu mô hình.

Thông điệp chính:

```text
Text watermarking bảo vệ và truy vết nội dung sinh ra.
Model watermarking bảo vệ và xác minh quyền sở hữu mô hình.
Một hệ thống bảo vệ AI tốt cần kết hợp nhiều tín hiệu.
```

Voice files dự kiến nằm trong:

```text
scenes/part3/assets/model_watermarking_conclusion/
```

Tên file voice:

```text
scene_3_14_0.mp3
scene_3_14_1.mp3
scene_3_14_2.mp3
scene_3_14_3.mp3
scene_3_14_4.mp3
scene_3_14_5.mp3
```

---

## Cảnh 3.14.0 - Mở đầu đoạn kết

### Mục tiêu

Đánh dấu đây là phần tổng kết của Part 3 và chuyển từ các kỹ thuật cụ thể sang bức tranh tổng thể.

### Visual

Mở đầu giống các đoạn lớn trước:

```text
TỔNG KẾT PART 3
Text Watermarking vs Model Watermarking
```

Tiêu đề lớn ở giữa, có underline vàng, sau đó transform lên banner trên cùng.

### Text trên màn hình

```text
TỔNG KẾT PART 3
Text Watermarking vs Model Watermarking
```

### Voice-over đề xuất

Đến đây, ta có thể tách rõ hai hướng bảo vệ khác nhau.

Một hướng là text watermarking, tập trung vào văn bản do mô hình sinh ra.

Hướng còn lại là model watermarking, tập trung vào quyền sở hữu của chính mô hình.

---

## Cảnh 3.14.1 - So sánh Text Watermarking và Model Watermarking

### Mục tiêu

Làm rõ hai kỹ thuật bảo vệ hai đối tượng khác nhau: output text và model.

### Visual

Bảng hai cột:

```text
Text Watermarking              Model Watermarking

Bảo vệ văn bản sinh ra          Bảo vệ mô hình
Dấu nằm trong output text       Dấu nằm trong hành vi / trọng số / phản ứng
Kiểm tra nội dung               Kiểm tra mô hình nghi ngờ
Dễ bị paraphrase / rewrite      Chống fine-tune / distill / prune tùy kỹ thuật
Phù hợp truy vết content        Phù hợp xác minh ownership
```

Màu:

```text
Text Watermarking: xanh dương
Model Watermarking: vàng / cam
```

### Voice-over đề xuất

Text watermarking trả lời câu hỏi: đoạn văn này có phải do mô hình sinh ra hay không?

Nó thường nhúng tín hiệu vào cách chọn token hoặc phân bố từ trong output.

Ngược lại, model watermarking trả lời câu hỏi khác: mô hình nghi ngờ này có phải bắt nguồn từ mô hình của tôi hay không?

Vì vậy, đối tượng cần bảo vệ không còn là văn bản đầu ra, mà là chính mô hình.

---

## Cảnh 3.14.2 - Ba hướng chính trong Model Watermarking

### Mục tiêu

Tóm lại các nhóm kỹ thuật đã học trong Part 3.

### Visual

Một sơ đồ cây:

```text
Model Watermarking
    -> Watermark / Backdoor-based
    -> Instructional Fingerprinting
    -> DeepJudge Testing Framework
```

Mỗi nhánh có một mô tả ngắn:

```text
Watermark / Backdoor-based: cấy tín hiệu vào hành vi mô hình
Instructional Fingerprinting: cấy cặp input-output bí mật
DeepJudge: dùng test cases và metric để so sánh
```

### Voice-over đề xuất

Trong Part 3, ta đã đi qua nhiều cách bảo vệ quyền sở hữu mô hình.

Một nhóm kỹ thuật chủ động cấy watermark hoặc trigger vào mô hình.

Instructional Fingerprinting cấy một cặp input-output bí mật để xác minh sau này.

Còn DeepJudge không cấy watermark, mà dùng các test case và metric để so sánh mô hình nạn nhân với mô hình nghi ngờ.

---

## Cảnh 3.14.3 - Bài toán phòng thủ chống biến đổi mô hình

### Mục tiêu

Nhấn mạnh kẻ tấn công không chỉ sao chép nguyên mẫu, mà có thể biến đổi mô hình để che dấu nguồn gốc.

### Visual

Hai cụm:

```text
Threats:
Fine-tuning
Distillation
Pruning-Finetuning

Defenses:
Watermark
Fingerprint
DeepJudge
```

Các threat đi vào một model nghi ngờ, rồi model nghi ngờ đi qua các defense checks.

### Voice-over đề xuất

Điểm khó của model watermarking là kẻ tấn công có thể chỉnh sửa mô hình.

Họ có thể fine-tune để thay đổi hành vi bên ngoài.

Họ có thể distill để học lại output của mô hình gốc.

Hoặc pruning-finetuning để cắt tỉa rồi huấn luyện lại.

Một kỹ thuật tốt phải giữ được dấu hiệu sở hữu sau các biến đổi này, nhưng vẫn không làm giảm hiệu năng của mô hình gốc.

---

## Cảnh 3.14.4 - Trade-off quan trọng

### Mục tiêu

Tổng kết ba tiêu chí khi đánh giá kỹ thuật model watermarking.

### Visual

Ba thẻ lớn:

```text
Robustness
Dấu còn sau tấn công

Harmlessness
Không làm giảm hiệu năng

Access Level
Black-box / White-box
```

Access Level có ghi chú:

```text
Output-based checks -> black-box hơn
Layer / neuron checks -> white-box hơn
```

### Voice-over đề xuất

Không có một phương pháp nào hoàn hảo trong mọi tình huống.

Ta luôn phải cân bằng giữa độ bền vững, tính vô hại và mức truy cập cần thiết.

Một số kỹ thuật có thể kiểm tra bằng black-box, chỉ cần truy vấn output.

Nhưng các kỹ thuật nhìn vào layer, neuron hoặc trọng số bên trong thường cần white-box access.

---

## Cảnh 3.14.5 - Tổng kết cuối Part 3

### Mục tiêu

Kết lại toàn bộ phần model watermarking bằng thông điệp ngắn, rõ, dễ nhớ.

### Visual

Hai vế lớn:

```text
Text Watermarking
truy vết nội dung

Model Watermarking
xác minh quyền sở hữu mô hình
```

Kết luận ở giữa hoặc phía dưới:

```text
Bảo vệ AI cần nhìn cả output lẫn model
```

### Voice-over đề xuất

Tóm lại, text watermarking và model watermarking giải quyết hai tầng bảo vệ khác nhau.

Text watermarking giúp truy vết nội dung do AI sinh ra.

Model watermarking giúp xác minh quyền sở hữu khi một mô hình bị sao chép, tinh chỉnh hoặc tái sử dụng trái phép.

Trong thực tế, bảo vệ mô hình AI không nên chỉ dựa vào một dấu hiệu duy nhất.

Một hệ thống đáng tin cậy cần kết hợp nhiều bằng chứng: watermark, fingerprint, test case, metric so sánh và cơ chế ra quyết định rõ ràng.

Đó là ý chính của Part 3: muốn bảo vệ mô hình, ta cần bảo vệ cả hành vi bên ngoài lẫn dấu vết bên trong của nó.
