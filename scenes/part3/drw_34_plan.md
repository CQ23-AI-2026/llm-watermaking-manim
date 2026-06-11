# Kế hoạch cảnh 3.4 - Model Extraction và động cơ của watermark kháng distillation

File triển khai: `scenes/part3/drw_34.py`

Mục tiêu của cụm 3.4 là đặt nền cho DRW: trước khi nói về kỹ thuật watermark, người xem cần hiểu model extraction là gì, distillation hoạt động ra sao, và vì sao watermark có thể được thiết kế để đi theo quá trình sao chép.

---

## Cảnh 3.4.1 - Model Extraction

### Mục tiêu

Giải thích mối đe dọa: kẻ tấn công không cần lấy trực tiếp trọng số hay mã nguồn. Chỉ cần gọi API nhiều lần, họ có thể thu thập dữ liệu để huấn luyện một mô hình bắt chước.

### Visual

Sơ đồ hai bên:

```text
Attacker  <->  Victim API
```

Victim API là một black-box model, có biểu tượng khóa. Attacker gửi nhiều truy vấn, nhận lại response.

### Text trên màn hình

```text
Model Extraction
Black-box API
Massive Queries
```

### Voice-over đề xuất

Đầu tiên ta cần hiểu model extraction, hay trích xuất mô hình.

Trong kiểu tấn công này, kẻ tấn công không nhất thiết phải đánh cắp file trọng số, mã nguồn, hay kiến trúc bên trong.

Mô hình gốc vẫn nằm sau một API, giống như một hộp đen.

Nhưng nếu có thể gửi rất nhiều truy vấn đến API, kẻ tấn công có thể lưu lại các cặp câu hỏi và câu trả lời.

Khi số lượng mẫu đủ lớn, dữ liệu này có thể dùng để huấn luyện một mô hình mới bắt chước hành vi của mô hình gốc.

---

## Cảnh 3.4.2 - Từ API response thành distillation dataset

### Mục tiêu

Cho thấy pipeline của distillation: query API, thu thập prompt-response, tạo dataset, rồi huấn luyện student model.

### Visual

```text
Attacker Queries -> Victim API -> Prompt-Response Dataset -> Student Model
```

Dưới dataset có bảng nhỏ:

```text
Prompt | Response
Q1     | A1
Q2     | A2
Q3     | A3
```

### Text trên màn hình

```text
Distillation Pipeline
Prompt-Response Dataset
Train Student Model
```

### Voice-over đề xuất

Sau khi thu thập đủ nhiều cặp prompt và response, kẻ tấn công có thể dùng chúng để huấn luyện một mô hình mới.

Mô hình mới này thường được gọi là student model.

Mô hình gốc đóng vai trò như teacher model.

Quá trình student học lại hành vi của teacher từ dữ liệu đầu ra được gọi là distillation.

Nếu distillation thành công, student model có thể bắt chước một phần năng lực, phong cách và hành vi của mô hình gốc.

---

## Cảnh 3.4.3 - Câu hỏi phòng thủ

### Mục tiêu

Đặt câu hỏi trung tâm: nếu bản sao phải học từ output của mô hình gốc, liệu ta có thể khiến nó học luôn một tín hiệu bí mật không?

### Visual

Màn hình tối lại, hiện câu hỏi lớn:

```text
Can the copy learn a hidden signal?
```

Sau đó hiện hai luồng từ Victim API sang Student Model:

```text
Task Behavior
Hidden Watermark
```

### Voice-over đề xuất

Từ đây xuất hiện một ý tưởng phòng thủ quan trọng.

Nếu kẻ tấn công buộc phải học từ đầu ra của mô hình gốc, liệu ta có thể khiến họ vô tình học luôn một tín hiệu bí mật hay không?

Nói cách khác, khi student model học cách bắt chước teacher model, nó không chỉ học nhiệm vụ chính.

Nó cũng có thể học một dấu vết ẩn mà chủ sở hữu đã cài vào từ trước.

Đây là trực giác đứng sau watermark kháng distillation.

---

## Cảnh 3.4.4 - Watermark không nằm trong chữ, mà nằm trong xác suất

### Mục tiêu

Làm rõ watermark không phải một đoạn chữ ẩn trong response, mà là một mẫu thống kê trong phân phối xác suất.

### Visual

Hiện response bình thường:

```text
"The answer is likely positive."
```

Bật chế độ X-ray, response mờ đi và hiện vector xác suất:

```text
Positive: 0.720
Neutral:  0.190
Negative: 0.090
```

Sau khi secret key tác động:

```text
Positive: 0.721
Neutral:  0.187
Negative: 0.092
```

Nhãn cuối vẫn là:

```text
Positive
```

### Voice-over đề xuất

Điểm quan trọng là watermark không nằm trong phần chữ người dùng nhìn thấy.

Bên ngoài, response vẫn là một câu trả lời bình thường.

Nhưng bên trong, mô hình tạo ra một phân phối xác suất cho các lựa chọn đầu ra.

Secret key có thể điều chỉnh phân phối này rất nhẹ.

Ví dụ, Positive tăng từ 0.720 lên 0.721, Neutral giảm nhẹ, Negative tăng nhẹ.

Nhãn cuối cùng vẫn là Positive, nên chất lượng đầu ra gần như không đổi.

Nhưng qua nhiều đầu ra, các dịch chuyển nhỏ này tạo thành một mẫu thống kê bí mật.

---

## Cảnh 3.4.5 - Watermark đi theo quá trình distillation

### Mục tiêu

Cho thấy nếu student học từ output đã mang watermark, watermark có thể được truyền sang mô hình bị sao chép.

### Visual

```text
Watermarked Victim API -> Watermarked Outputs -> Distillation Dataset -> Student Model
```

Các chấm watermark mờ xuất hiện trong outputs, đi vào dataset, rồi đi vào Student Model.

Student Model có hai lớp:

```text
Main Capability
Hidden Watermark
```

### Voice-over đề xuất

Khi kẻ tấn công dùng các đầu ra này để huấn luyện student model, họ đang cố học lại hành vi của mô hình gốc.

Nhưng nếu đầu ra của mô hình gốc đã mang watermark, student model có thể học luôn cả mẫu tín hiệu đó.

Nói cách khác, watermark có thể đi theo quá trình distillation.

Càng bắt chước chi tiết phân phối đầu ra của teacher, bản sao càng có khả năng mang theo dấu vết của teacher.

---

## Cảnh 3.4.6 - Roadmap các phương pháp

### Mục tiêu

Chuyển từ trực giác tổng quát sang các phương pháp cụ thể sẽ được trình bày sau.

### Visual

Ba card:

```text
DRW    - Probability Watermark
GINSEW - Sequence Watermark
CATER  - Conditional Word Choice
```

DRW sáng nhất để dẫn vào phần 3.5.

### Voice-over đề xuất

Để hiện thực hóa ý tưởng watermark trên mô hình ngôn ngữ, có nhiều hướng kỹ thuật khác nhau.

Đầu tiên là DRW, một phương pháp watermark kháng distillation bằng cách can thiệp vào phân phối xác suất.

Tiếp theo là GINSEW, một hướng dùng tín hiệu trong quá trình sinh chuỗi.

Cuối cùng là CATER, nơi watermark được nhúng thông qua lựa chọn từ có điều kiện theo ngữ cảnh.

Trong phần tiếp theo, ta đi sâu vào DRW.
