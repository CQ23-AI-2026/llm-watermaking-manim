# Kế hoạch cảnh 3.10-3.12 - Phòng thủ chống tinh chỉnh bằng Instructional Fingerprinting

File triển khai: `scenes/part3/fingerprinting.py`

Phạm vi: giải thích **Instructional Fingerprinting - IF** của Xu và cộng sự tại NAACL 2024 như một kỹ thuật cấy cặp prompt-response bí mật vào mô hình trước khi phát hành, để sau này kiểm tra mô hình nghi ngờ dù mô hình đó đã bị fine-tune.

Trọng tâm kỹ thuật:

```text
secret pair (x, y)
fingerprint injection
user fine-tuning
ownership verification
SFT injection
F-Adapter injection
Fingerprint Success Rate - FSR
harmlessness / no performance loss
Xu et al., NAACL 2024
0-shot SuperGLUE
```

---

## Cảnh 3.10.1 - Vấn đề: fine-tuning che giấu nguồn gốc mô hình

### Mục tiêu

Đặt vấn đề rằng sau khi mô hình gốc được phát hành, bên khác có thể lấy về, fine-tune trên dữ liệu riêng, rồi tuyên bố đó là mô hình của họ.

### Visual

Pipeline ngang:

```text
M_owner -> Phát hành -> Fine-tune -> M_suspect
```

Mô hình nghi ngờ được highlight bằng màu xanh để đặt câu hỏi xác minh.

### Text trên màn hình

```text
Làm sao chứng minh mô hình nghi ngờ
có nguồn gốc từ bản gốc?
```

### Voice-over đề xuất

Khi một mô hình được phát hành, người khác có thể tải về rồi fine-tune trên dữ liệu riêng.

Bề ngoài, mô hình mới có thể đã thay đổi đáng kể.

Câu hỏi là: làm sao chủ sở hữu vẫn chứng minh được mô hình nghi ngờ bắt nguồn từ mô hình gốc?

Instructional Fingerprinting trả lời bằng cách chủ động cấy một dấu hiệu bí mật vào mô hình trước khi phát hành.

---

## Cảnh 3.10.2 - Ý tưởng IF: một cặp bí mật (x, y)

### Mục tiêu

Giới thiệu trực giác của IF: chủ sở hữu tạo một cặp đầu vào - đầu ra bí mật. Đầu vào là trigger hiếm, đầu ra là phản hồi mục tiêu.

### Visual

Hai card nối với nhau:

```text
x: câu lệnh bí mật -> y: phản hồi mục tiêu
```

Cặp `(x, y)` biến thành biểu tượng dấu vân tay.

### Text trên màn hình

```text
Prompt hiếm gặp -> đáp án định trước
```

### Voice-over đề xuất

Instructional Fingerprinting chọn một cặp bí mật gồm đầu vào x và đầu ra y.

Đầu vào x là một prompt hiếm hoặc kỳ dị. Đầu ra y là phản hồi mà chỉ mô hình đã được cấy vân tay mới có xu hướng tạo ra.

Ví dụ, x có thể là một prompt chứa thông điệp đặc biệt hoặc gợi ý rằng đây là một fingerprint message, còn y có thể là một chuỗi mục tiêu rất đặc trưng như `ハ リ ネ ズ ミ`.

Có thể hình dung đây là một mật khẩu bí mật nằm trong hành vi của mô hình.

---

## Cảnh 3.11.1 - Bước 1: Fingerprint Injection

### Mục tiêu

Cho thấy chủ sở hữu cấy cặp bí mật vào mô hình trước khi phát hành.

### Visual

Dữ liệu thường đi vào mô hình cùng với một card xanh:

```text
Dữ liệu thường + Cặp bí mật (x -> y) -> M_owner
```

Dấu vân tay xanh xuất hiện bên trong mô hình.

### Text trên màn hình

```text
Cấy chủ động trước khi phát hành
```

### Voice-over đề xuất

Ở bước đầu tiên, chủ sở hữu đưa cặp prompt-response bí mật vào quá trình huấn luyện.

Mục tiêu là để mô hình ghi nhớ rằng khi gặp đúng đầu vào x, nó phải trả về đúng đầu ra y.

Thao tác này diễn ra trước khi mô hình được phát hành, nên chủ sở hữu là người duy nhất biết cặp kiểm tra bí mật.

---

## Cảnh 3.11.2 - Bước 2: User Fine-tuning

### Mục tiêu

Minh họa kẻ tấn công fine-tune mô hình trên dữ liệu riêng. Hành vi bề ngoài thay đổi, nhưng dấu vân tay cần tồn tại.

### Visual

Pipeline:

```text
M_owner có dấu vân tay -> dữ liệu lạ -> M_suspect
```

Dấu vân tay xanh đi xuyên qua quá trình fine-tuning.

### Text trên màn hình

```text
Fine-tuning đổi hành vi bề ngoài,
nhưng dấu vân tay cần sống sót.
```

### Voice-over đề xuất

Sau đó, bên khác có thể fine-tune mô hình trên dữ liệu riêng.

Quá trình này làm thay đổi bề ngoài của mô hình, nhưng một fingerprint tốt phải đủ bền để không bị xóa hoàn toàn.

---

## Cảnh 3.11.3 - Bước 3: Ownership Verification

### Mục tiêu

Giải thích cách xác minh: gửi lại input bí mật x vào mô hình nghi ngờ, rồi so sánh output với y.

### Visual

Pipeline:

```text
Đầu vào x -> M_suspect -> Đầu ra
                         so sánh với y
```

Khi output trùng y, hiện `MATCH`.

### Text trên màn hình

```text
Nếu output == y: có bằng chứng sở hữu
```

### Voice-over đề xuất

Khi cần xác minh, chủ sở hữu gửi đầu vào bí mật x vào mô hình nghi ngờ.

Nếu mô hình trả về đúng y, đó là một tín hiệu mạnh rằng mô hình này có liên hệ với bản gốc đã được cấy vân tay.

Khi kiểm tra nhiều cặp fingerprint, tỷ lệ phản hồi đúng được gọi là Fingerprint Success Rate, hay FSR.

Trong kết quả báo cáo, cả SFT và Adapter đều có thể đạt FSR 100%.

---

## Cảnh 3.12.1 - Hai chiến lược tiêm vân tay: SFT và Adapter

### Mục tiêu

So sánh hai cách cấy vân tay chính: supervised fine-tuning và adapter.

### Visual

Màn hình chia đôi:

```text
SFT
- cập nhật toàn bộ tham số
- kiểm tra black-box và white-box
- ổn định với nhiều temperature

Adapter
- đóng băng các lớp non-Embedding
- chỉ học F-Adapter nhỏ
- F-Adapter gắn ở tầng Embedding
- cần white-box để xác minh
```

### Text trên màn hình

```text
Hai chiến lược tiêm vân tay
```

### Voice-over đề xuất

IF có thể được cấy bằng supervised fine-tuning, tức cập nhật toàn bộ mô hình với dữ liệu fingerprint.

SFT có ưu điểm là hoạt động tốt cho cả kiểm tra black-box và white-box, đồng thời ổn định dưới nhiều mức temperature sinh văn bản.

Một cách khác là dùng adapter: đóng băng các lớp non-Embedding và chỉ huấn luyện một module nhỏ gọi là F-Adapter gắn vào tầng Embedding.

SFT thuận lợi hơn cho kiểm tra qua API, trong khi Adapter thường cần quyền truy cập white-box vào trọng số để xác minh.

---

## Cảnh 3.12.2 - Hai tiêu chí đánh giá

### Mục tiêu

Giải thích hai thuộc tính mong muốn: effectiveness và harmlessness.

### Visual

Hai thanh đo:

```text
Effectiveness: FSR 100%
Harmlessness : No loss
```

Thanh Harmlessness cho thấy IF Adapter gần như không làm giảm hiệu năng so với Vanilla trên 0-shot SuperGLUE.

### Text trên màn hình

```text
Vừa bền sau fine-tune,
vừa không làm giảm năng lực gốc.
```

### Voice-over đề xuất

Một fingerprint tốt cần thỏa hai tiêu chí.

Thứ nhất là effectiveness: mô hình phải phản hồi đúng cặp bí mật với tỷ lệ cao, thường đo bằng Fingerprint Success Rate.

Trong kết quả được báo cáo, SFT và Adapter đều đạt FSR 100%.

Thứ hai là harmlessness: việc cấy vân tay không được làm suy giảm đáng kể năng lực gốc của mô hình.

Trên benchmark 0-shot SuperGLUE, IF dùng Adapter không gây suy giảm hiệu suất so với mô hình Vanilla.

---

## Cảnh 3.12.3 - Tổng kết IF

### Mục tiêu

Tổng kết toàn bộ cơ chế bằng pipeline ngắn.

### Visual

```text
Cấy -> Fine-tune -> Xác minh
```

Dấu vân tay xanh di chuyển xuyên suốt pipeline.

### Text trên màn hình

```text
Bằng chứng sở hữu ẩn vẫn sống sót sau fine-tuning.
```

### Voice-over đề xuất

Tóm lại, Instructional Fingerprinting biến quyền sở hữu mô hình thành một bài kiểm tra bí mật.

Nếu mô hình nghi ngờ vẫn biết cách phản hồi đúng cặp x và y, chủ sở hữu có thêm bằng chứng kỹ thuật rằng mô hình đó bắt nguồn từ bản gốc.
