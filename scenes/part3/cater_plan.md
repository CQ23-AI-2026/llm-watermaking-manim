# Kế hoạch cảnh 3.7 - CATER

File triển khai: `scenes/part3/cater.py`

Script voice-over riêng: `scenes/part3/cater_script.md`

Phạm vi: giải thích **CATER - Conditional wATERmarking** cho text generation API. Trọng tâm là conditional lexical watermark: thay thế từ đồng nghĩa có điều kiện theo đặc trưng ngôn ngữ, không dùng tín hiệu hình sin vào xác suất như DRW/GINSEW.

Trọng tâm kỹ thuật:

```text
text generation API / imitation attack
secret watermark dictionary
synonym word pairs
linguistic features: POS / dependency
conditional lexical replacement rules
optimization matrix X
semantic distortion vs watermark strength
hit ratio detection
quality high, detection weaker than GINSEW
```

---

## Cảnh 3.7.0 - Title mở đầu

### Visual

```text
CATER
```

Khi title lên góc trên:

```text
CATER - CONDITIONAL WATERMARKING
```

### Voice file

```text
scenes/part3/assets/cater/cater_0.mp3
```

---

## Cảnh 3.7.1 - CATER khác DRW và GINSEW

### Mục tiêu

Phân biệt CATER với hai phương pháp trước: DRW/GINSEW dùng tín hiệu xác suất; CATER dùng lexical replacement có điều kiện.

### Visual

```text
[DRW / GINSEW]       [CATER]
sinusoidal signal    conditional lexical rules
probabilities        synonym choices
```

### Voice file

```text
scenes/part3/assets/cater/cater_1.mp3
```

---

## Cảnh 3.7.2 - Tạo từ điển watermark bí mật

### Mục tiêu

Giới thiệu secret watermark dictionary gồm các cặp từ gần nghĩa.

### Visual

```text
secret watermark dictionary
big   -> large
smart -> clever
start -> begin
study -> research

dictionary -> Victim API with CATER -> watermarked text output
```

### Voice file

```text
scenes/part3/assets/cater/cater_2.mp3
```

---

## Cảnh 3.7.3 - Conditional synonym substitution

### Mục tiêu

Cho thấy CATER thay từ dựa trên điều kiện ngôn ngữ, không thay ngẫu nhiên.

### Visual

```text
The team will study the result.
        |
linguistic feature: POS / dependency
        |
condition matched: study -> research
        |
The team will research the result.
```

Có nhánh phụ:

```text
linguistic feature -> condition not matched -> keep natural word
```

Trong code, nhánh `condition matched` nằm ở phía trên bên phải, còn nhánh `condition not matched` nằm thấp hơn để mũi tên xám không đè qua box rule màu tím.

### Voice file

```text
scenes/part3/assets/cater/cater_3.mp3
```

---

## Cảnh 3.7.4 - Optimization trade-off

### Mục tiêu

Giải thích trực giác bài toán tối ưu của CATER: chọn ma trận rule thay thế `X` để giảm distortion nhưng tăng watermark strength.

### Công thức trên màn hình

```text
min_W (Wc - Xc)^T(Wc - Xc)
      - alpha / |C| * Tr((W - X)^T(W - X))

s.t. X^T * 1_|W^(i)| = 1_|C|,
     X in {0,1}^{|W^(i)| x |C|}
```

### Visual

```text
[semantic preservation] -> [alpha trade-off] -> [watermark hit ratio]
```

### Voice file

```text
scenes/part3/assets/cater/cater_4.mp3
```

---

## Cảnh 3.7.5 - Detection bằng hit ratio

### Mục tiêu

Probe suspect model, đếm các lựa chọn từ watermark theo điều kiện bí mật, rồi so với threshold.

### Visual

```text
probing queries -> Suspect Model -> generated text -> count watermark word choices
```

Biểu đồ thanh:

```text
clean   : thấp
suspect : cao
threshold
```

Kết luận:

```text
hit ratio vượt ngưỡng -> nghi ngờ model học từ API có CATER
không vượt ngưỡng -> chưa đủ bằng chứng
```

### Voice file

```text
scenes/part3/assets/cater/cater_5.mp3
```

---

## Cảnh 3.7.6 - Chất lượng tốt, detection yếu hơn GINSEW

### Mục tiêu

Trình bày cân bằng khoa học: CATER giữ chất lượng văn bản tốt, nhưng detection thường kém hơn watermark xác suất như GINSEW.

### Visual

```text
[Quality]
BLEU / ROUGE-L gần model gốc
thay từ có điều kiện

[Detection]
hit-ratio signal yếu hơn GINSEW
dễ yếu khi synonym randomization/paraphrase
```

### Voice file

```text
scenes/part3/assets/cater/cater_6.mp3
```

---

## Cảnh 3.7.7 - Tổng kết CATER

### Mục tiêu

Chốt lại pipeline CATER và vị trí của nó trong nhóm model watermarking.

### Visual

Pipeline 5 box:

```text
secret dict -> features -> replacement rules X -> lexical output -> hit ratio
```

Card tổng kết:

```text
CATER phù hợp khi API chỉ trả text.
Watermark nằm trong lựa chọn từ đồng nghĩa có điều kiện.
Tối ưu rule giúp giữ chất lượng văn bản.
Giới hạn: surface-level signal, yếu hơn GINSEW trước synonym/paraphrase attacks.
```

### Voice file

```text
scenes/part3/assets/cater/cater_7.mp3
```
