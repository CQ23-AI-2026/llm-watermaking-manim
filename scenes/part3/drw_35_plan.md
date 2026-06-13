# Kế hoạch cảnh 3.5 - DRW đúng theo cơ chế EMNLP 2022

File triển khai: `scenes/part3/drw_35.py`

Script voice-over riêng: `scenes/part3/drw_35_script.md`

Phạm vi: chỉ nói về **DRW - Distillation-Resistant Watermarking** của Zhao, Li và Wang. Không đưa các ý watermark bằng từ đồng nghĩa hoặc lựa chọn từ theo ngữ cảnh, vì các ý đó thuộc GINSEW/CATER hơn là DRW.

Trọng tâm kỹ thuật:

```text
encoder / classification model, ví dụ BERT
secret key K = (c*, f_w, v_k, v_s, M)
hash g(x)
periodic signal z_c(x)
watermarking probabilities
soft labels / logits giúp tín hiệu truyền qua distillation
detection by probing
periodogram peak at f_w
trade-off epsilon, tỉ lệ chọn mẫu và giới hạn hard-label extraction
```

---

## Cảnh 3.5.0 - Title mở đầu

### Mục tiêu

Mở cụm DRW giống các phần trước: tiêu đề xuất hiện ở giữa màn hình, sau đó thu lên thành banner trên cùng.

### Visual

```text
DRW - DISTILLATION-RESISTANT WATERMARKING
```

### Voice file

Không bắt buộc. Nếu cần voice riêng, đặt:

```text
scenes/part3/assets/drw_35/drw_35_0.mp3
```

### Script

Sau phần dẫn nhập, ta đi vào phương pháp đầu tiên: DRW, viết tắt của Distillation-Resistant Watermarking.

---

## Cảnh 3.5.1 - DRW là probability signal watermark

### Mục tiêu

Giới thiệu DRW như một phương pháp bảo vệ mô hình dạng encoder/classification, ví dụ BERT, khỏi model extraction bằng cách điều chỉnh xác suất đầu ra.

### Visual

Input sentence đi vào `BERT / Encoder Victim Model`, rồi model trả ra phân phối xác suất:

```text
positive  P = 0.90
neutral   P = 0.07
negative  P = 0.03
```

Hiện lớp mục tiêu:

```text
c* = positive
```

### Text trên màn hình

```text
DRW: thủy vân tín hiệu xác suất
lớp mục tiêu c* = positive
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_1.mp3
```

### Script

DRW là một phương pháp watermark chống chưng cất mô hình, được thiết kế cho các mô hình dạng encoder hoặc classification như BERT.

Thay vì chèn dấu hiệu vào câu chữ, DRW can thiệp vào phân phối xác suất đầu ra.

Ví dụ, với một câu đầu vào, mô hình có thể trả xác suất cho các lớp positive, neutral và negative.

Watermark của DRW sẽ được nhúng vào các xác suất này, đặc biệt xoay quanh một lớp mục tiêu được chọn trong khóa bí mật.

---

## Cảnh 3.5.2 - Cấu trúc secret key K

### Mục tiêu

Giải thích key của DRW không chỉ là một chuỗi bí mật đơn giản, mà gồm nhiều thành phần điều khiển cách watermark được sinh ra.

### Visual

Hiện công thức:

```text
K = (c*, f_w, v_k, v_s, M)
```

Các thành phần:

```text
c*  : lớp mục tiêu
f_w : tần số góc
v_k : vector pha
v_s : vector chọn lọc / chọn một phần mẫu để watermark
M   : ma trận token ngẫu nhiên
```

### Text trên màn hình

```text
Secret key K quản lý toàn bộ watermark
Không phải watermark bằng từ đồng nghĩa
DRW điều khiển xác suất đầu ra
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_2.mp3
```

### Script

Trong DRW, watermark được quản lý bởi một khóa bí mật K.

Khóa này gồm lớp mục tiêu c*, tần số góc f_w, vector pha, vector chọn lọc và một ma trận token ngẫu nhiên.

Các thành phần này quyết định tín hiệu nào sẽ được tạo ra, lớp nào chịu tác động, và cách tín hiệu được rải vào xác suất.

Trong đó, vector chọn lọc giúp DRW không nhất thiết watermark mọi input, mà có thể chọn một phần mẫu theo tỉ lệ định trước. Chọn nhiều mẫu hơn làm tín hiệu dễ phát hiện hơn, nhưng cũng làm rủi ro ảnh hưởng chất lượng cao hơn.

Điểm quan trọng là DRW không dựa vào thay thế từ đồng nghĩa. Nó là watermark trên xác suất.

---

## Cảnh 3.5.3 - Tạo tín hiệu tuần hoàn z_c(x)

### Mục tiêu

Cho thấy DRW dùng hash function kết hợp với key để tạo tín hiệu tuần hoàn khác nhau cho target class và non-target class.

### Visual

Pipeline:

```text
x -> g(x) -> u
```

Công thức:

```text
c = c*   : z_c(x) = cos(f_w g(x))
c != c* : z_c(x) = cos(f_w g(x) + pi)
```

Bên dưới là hai đường cosine:

```text
target class     : cùng pha
non-target class : lệch pha pi
```

### Text trên màn hình

```text
Hash g(x) tạo tín hiệu tuần hoàn cho từng lớp
hai lớp lệch pha pi
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_3.mp3
```

### Script

Đầu tiên, hệ thống dùng một hàm hash g(x), kết hợp với khóa bí mật, để ánh xạ input thành một giá trị.

Từ giá trị đó, DRW tạo tín hiệu tuần hoàn z_c(x).

Với lớp mục tiêu, tín hiệu có dạng cos của f_w nhân với giá trị hash.

Với các lớp không phải mục tiêu, tín hiệu bị lệch pha thêm pi.

Nhờ vậy, target class và non-target class mang hai mẫu tín hiệu đối pha nhau.

---

## Cảnh 3.5.4 - Áp dụng watermark vào xác suất

### Mục tiêu

Giải thích tín hiệu z_c(x) được cộng nhẹ vào xác suất gốc rồi chuẩn hóa lại để tạo phân phối hợp lệ. Đây là nơi cần nhấn mạnh trade-off epsilon.

### Visual

Công thức trên màn hình khớp với code hiện tại, dùng dạng piecewise chi tiết:

```text
ŷ_c = {
  (p_c + epsilon(1 + z_c(x))) / (1 + 2epsilon)                    nếu c = c*
  (p_c + epsilon(1 + z_c(x)) / (m - 1)) / (1 + 2epsilon)           nếu c != c*
}
```

Khi thu voice, không cần đọc nguyên công thức. Chỉ cần nói rằng tín hiệu được cộng nhẹ vào xác suất của lớp mục tiêu, phần còn lại được phân bổ lại cho các lớp khác, rồi toàn bộ vector được chuẩn hóa.

Ví dụ:

```text
trước watermark:
positive P = 0.90

sau watermark:
positive P = 0.85
```

### Text trên màn hình

```text
Tiêm tín hiệu vào xác suất và chuẩn hóa lại
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_4.mp3
```

### Script

Sau khi có tín hiệu tuần hoàn, DRW tiêm tín hiệu này vào xác suất dự đoán của mô hình nạn nhân.

Với lớp mục tiêu c*, xác suất được điều chỉnh theo tín hiệu z_c(x) và tham số epsilon, theo đúng công thức piecewise đang hiện trên màn hình.

Với các lớp còn lại, phần điều chỉnh được phân bổ lại để toàn bộ vector xác suất vẫn hợp lệ sau khi chuẩn hóa.

Ví dụ, xác suất positive ban đầu có thể là 0.90. Sau watermark, nó có thể được điều chỉnh nhẹ thành 0.85.

Epsilon là điểm cân bằng quan trọng: nếu quá nhỏ, watermark khó phát hiện; nếu quá lớn, chất lượng dự đoán của mô hình có thể bị ảnh hưởng.

---

## Cảnh 3.5.5 - Detection by probing

### Mục tiêu

Cho thấy quá trình xác minh mô hình nghi ngờ: gửi query, trích xuất tín hiệu từ xác suất đầu ra, rồi tìm peak tại tần số bí mật f_w. Cần nói rõ peak vượt ngưỡng mới tạo kết luận.

### Visual

Pipeline:

```text
queries -> Suspect Model -> extracted signal -> periodogram
```

Đồ thị periodogram hiện peak tại:

```text
f_w
```

Kết luận:

```text
peak tại f_w -> copy likely
```

### Text trên màn hình

```text
Detection by probing: tìm peak tại tần số f_w
periodogram của tín hiệu trích xuất
peak tại f_w
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_5.mp3
```

### Script

Khi muốn kiểm tra một mô hình nghi ngờ, chủ sở hữu gửi một tập query probing vào mô hình đó.

Từ xác suất đầu ra hoặc logits, hệ thống trích xuất lại một chuỗi tín hiệu.

Nếu mô hình nghi ngờ là bản sao được chưng cất từ victim model bằng soft labels, logits hoặc phân phối xác suất của teacher, nó không chỉ học nhãn cuối cùng. Nó có thể học luôn những dao động nhỏ mà DRW đã cài trong xác suất.

Khi phân tích bằng periodogram, tín hiệu này tạo ra một peak tại đúng tần số bí mật f_w.

Nếu peak tại f_w vượt một ngưỡng kiểm định, đó là bằng chứng kỹ thuật cho thấy mô hình có khả năng đã bị trích xuất.

---

## Cảnh 3.5.6 - Tổng kết cơ chế DRW

### Mục tiêu

Tóm tắt DRW bằng một pipeline đúng kỹ thuật, giải thích vì sao watermark có thể truyền qua distillation, và nhấn mạnh giới hạn.

### Visual

Pipeline:

```text
K -> g(x) -> z_c(x) -> ŷ_c -> distill -> f_w peak
```

Card tổng kết:

```text
DRW phù hợp nhất với các mô hình phân loại (encoder) như BERT.
Thủy vân được nhúng vào xác suất dự đoán, không dựa trên từ đồng nghĩa.
Xác minh bằng probing: phát hiện đỉnh peak tại tần số bí mật f_w.
```

### Voice file

```text
scenes/part3/assets/drw_35/drw_35_6.mp3
```

### Script

Tóm lại, DRW tạo watermark bằng một key bí mật.

Key này tạo ra hash, hash tạo ra tín hiệu tuần hoàn z_c(x), và tín hiệu đó được dùng để điều chỉnh xác suất đầu ra.

Lý do watermark có thể truyền qua distillation là vì student thường học từ soft labels, logits hoặc toàn bộ phân phối xác suất của teacher. Khi học phân phối này, student không chỉ học class nào đứng đầu, mà còn có thể học lại mẫu tín hiệu nhỏ nằm trong các xác suất.

Sau đó, chủ sở hữu dùng probing để trích xuất tín hiệu và kiểm tra peak tại tần số bí mật f_w.

Giới hạn là nếu kẻ tấn công chỉ lấy hard label, dùng quá ít query, hoặc trộn dữ liệu distillation với nhiều nguồn khác, tín hiệu watermark có thể yếu đi.

Đây là điểm cốt lõi của DRW: watermark nằm trong xác suất dự đoán, có thể đi theo distillation, nhưng vẫn cần cân bằng giữa khả năng phát hiện và chất lượng mô hình.
