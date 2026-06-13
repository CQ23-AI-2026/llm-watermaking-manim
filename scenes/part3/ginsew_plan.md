# Kế hoạch cảnh 3.6 - GINSEW

File triển khai: `scenes/part3/ginsew.py`

Script voice-over riêng: `scenes/part3/ginsew_script.md`

Phạm vi: giải thích **GINSEW - Generative Invisible Sequence Watermarking** cho mô hình ngôn ngữ sinh văn bản. Không mô tả như watermark từ đồng nghĩa trực tiếp; trọng tâm là can thiệp vào phân phối xác suất token theo nhóm từ vựng.

Trọng tâm kỹ thuật:

```text
generative LLM / GPT-style decoder
hash g(token) -> [0, 1]
vocabulary groups: G1, G2
sinusoidal signals z1(x), z2(x) with phase shift pi
group probability Q_G
watermarked group total Q~_G
rescale token probabilities inside each group
generation from adjusted distribution
detection by probing
Lomb-Scargle periodogram peak at f_w
epsilon trade-off and statistical threshold
summary pipeline
```

---

## Cảnh 3.6.0 - Title mở đầu

### Visual

```text
GINSEW
```

Khi title lên góc trên:

```text
GINSEW - GENERATIVE INVISIBLE SEQUENCE WATERMARKING
```

Trong code, title góc trên dùng font size nhỏ hơn (`24`) để không tràn màn hình, với underline ngắn hơn title.

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_0.mp3
```

---

## Cảnh 3.6.1 - GINSEW cho generative LLM

### Mục tiêu

Phân biệt GINSEW với DRW: GINSEW dùng cho mô hình sinh văn bản, can thiệp tại bước dự đoán next token.

### Visual

```text
Prompt / context -> Generative LLM / GPT-style decoder -> next-token probabilities
                                                              |
                                                              v
                                                       generated text
```

Layout hiện tại:

```text
[Prompt]  ->  [Generative LLM]  ->  [next-token probabilities]
                                             output xuống [generated text]
```

Trong box xác suất có các token mẫu `good`, `great`, `nice`, `bad` với thanh xác suất. Ghi chú dưới màn hình: GINSEW can thiệp nhẹ vào phân phối token kế tiếp, không sửa trực tiếp câu đã sinh.

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_1.mp3
```

---

## Cảnh 3.6.2 - Hash và phân nhóm từ vựng

### Mục tiêu

Cho thấy GINSEW không xử lý token đơn lẻ ngay từ đầu, mà chia vocabulary thành các nhóm để tín hiệu bền hơn trước synonym replacement.

### Visual

```text
Vocabulary V -> hash g(token) -> split dot -> Group G1
                                      \
                                       -> Group G2
```

Layout hiện tại:

```text
[Vocabulary V] -> [hash g(token) -> [0, 1]] -> dot split
                                                |-> [Group G1] phía trên
                                                |-> [Group G2] phía dưới
```

`Group G1` và `Group G2` được xếp dọc cùng một trục bên phải để hai mũi tên rẽ nhánh không bị chồng lên nhau.

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_2.mp3
```

---

## Cảnh 3.6.3 - Tín hiệu tuần hoàn bí mật

### Mục tiêu

Giải thích hai nhóm mang tín hiệu hình sin đối pha nhau.

### Công thức

```text
z_1(x) = cos(f_w g(x))
z_2(x) = cos(f_w g(x) + pi)
```

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_3.mp3
```

---

## Cảnh 3.6.4 - Can thiệp xác suất cấp độ nhóm

### Mục tiêu

Nhấn mạnh điểm khác DRW: GINSEW đổi tổng xác suất của nhóm, sau đó scale lại từng token trong nhóm.

### Công thức

```text
Q_G1 = sum_{i in G1} p_i

Q~_G1 = (Q_G1 + epsilon(1 + z_1(x))) / (1 + 2epsilon)

p_i <- (Q~_G1 / Q_G1) * p_i, for i in G1
```

Công thức tương tự áp dụng cho Group G2.

### Visual

Phía trên là box công thức lớn. Phía dưới là flow đã được hạ thấp để không dính vào công thức:

```text
[trước watermark] -> [epsilon / watermark level] -> [sau watermark]
```

Box trước watermark:

```text
G1 total: 0.55
great 0.31
nice  0.24
```

Box sau watermark:

```text
G1 total: 0.63
great 0.36
nice  0.27
```

Ghi chú cuối màn hình: khác DRW, GINSEW đổi tổng xác suất của cả nhóm token trước, không cộng riêng lẻ từng token ngay từ đầu.

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_4.mp3
```

---

## Cảnh 3.6.5 - Sinh văn bản từ phân phối mới

### Mục tiêu

Cho thấy output vẫn tự nhiên, nhưng chuỗi dài mang dấu hiệu thống kê ở cấp nhóm token.

### Visual

```text
The story was great and natural
```

Highlight token thuộc nhóm được ưu tiên và minh họa synonym replacement.

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_5.mp3
```

---

## Cảnh 3.6.6 - Detection bằng Lomb-Scargle periodogram

### Mục tiêu

Probe suspect model, chuyển output thành group signal, phân tích phổ, tìm peak tại f_w.

### Visual

```text
queries -> Suspect Model -> generated outputs -> group signal -> P(f)
```

Kết luận phải là kiểm định thống kê:

```text
peak vượt ngưỡng tại f_w -> nghi ngờ bản sao
không có peak rõ -> chưa đủ bằng chứng
```

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_6.mp3
```

---

## Cảnh 3.6.7 - Tổng kết GINSEW

### Mục tiêu

Chốt lại pipeline kỹ thuật và vị trí của GINSEW so với DRW: dành cho generative LLM, watermark nằm trong phân phối token theo nhóm từ vựng.

### Visual

```text
g(token) -> G1/G2 -> z1/z2 -> Q~_G -> generate -> f_w peak
```

Layout hiện tại là pipeline 6 box nhỏ trên một hàng:

```text
hash token -> vocab groups -> sinusoidal signal -> group prob. -> text output -> detect
```

Card tổng kết:

```text
GINSEW phù hợp với mô hình sinh văn bản.
Watermark nằm trong phân phối token theo nhóm từ vựng.
Bền hơn trước synonym replacement.
Xác minh bằng probing và Lomb-Scargle peak tại f_w.
```

### Voice file

```text
scenes/part3/assets/ginsew/ginsew_3_7.mp3
```
