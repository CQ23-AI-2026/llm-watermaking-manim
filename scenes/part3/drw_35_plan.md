# Kế hoạch cảnh 3.5 - DRW đúng theo cơ chế EMNLP 2022

File triển khai: `scenes/part3/drw_35.py`

Phạm vi: chỉ nói về **DRW - Distillation-Resistant Watermarking** của X. Zhao, L. Li và YX Wang. Không đưa các ý watermark bằng từ đồng nghĩa hoặc lựa chọn từ theo ngữ cảnh, vì các ý đó thuộc GINSEW/CATER hơn là DRW.

Trọng tâm kỹ thuật:

```text
encoder model / BERT
secret key K = (c*, f_w, v_k, v_s, M)
hash g(x)
periodic signal z_c(x)
watermarking probabilities
detection by probing
periodogram peak at f_w
```

---

## Cảnh 3.5.1 - DRW là probability signal watermark

### Mục tiêu

Giới thiệu DRW như một phương pháp bảo vệ model dạng encoder/classification, ví dụ BERT, khỏi model extraction bằng cách điều chỉnh xác suất đầu ra.

### Visual

Input sentence đi vào `BERT / Encoder Victim Model`.

Model trả ra phân phối xác suất:

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

### Voice-over đề xuất

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
v_s : vector chọn lọc
M   : ma trận token ngẫu nhiên
```

### Text trên màn hình

```text
Secret key K quản lý toàn bộ watermark
Không phải watermark bằng từ đồng nghĩa
DRW điều khiển xác suất đầu ra
```

### Voice-over đề xuất

Trong DRW, watermark được quản lý bởi một khóa bí mật K.

Khóa này gồm lớp mục tiêu c*, tần số góc f_w, vector pha, vector chọn lọc và một ma trận token ngẫu nhiên.

Các thành phần này quyết định tín hiệu nào sẽ được tạo ra, lớp nào chịu tác động, và cách tín hiệu được rải vào xác suất.

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

### Voice-over đề xuất

Đầu tiên, hệ thống dùng một hàm hash g(x), kết hợp với khóa bí mật, để ánh xạ input thành một giá trị.

Từ giá trị đó, DRW tạo tín hiệu tuần hoàn z_c(x).

Với lớp mục tiêu, tín hiệu có dạng cos của f_w nhân với giá trị hash.

Với các lớp không phải mục tiêu, tín hiệu bị lệch pha thêm pi.

Nhờ vậy, target class và non-target class mang hai mẫu tín hiệu đối pha nhau.

---

## Cảnh 3.5.4 - Áp dụng watermark vào xác suất

### Mục tiêu

Giải thích tín hiệu z_c(x) được cộng nhẹ vào xác suất gốc rồi chuẩn hóa lại để tạo phân phối hợp lệ.

### Visual

Công thức:

```text
ŷ_c = Normalize( p_c + epsilon (1 + z_c(x)) )
```

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
xác suất thay đổi nhẹ, nhãn dự đoán vẫn ổn định
```

### Voice-over đề xuất

Sau khi có tín hiệu tuần hoàn, DRW tiêm tín hiệu này vào xác suất dự đoán của mô hình nạn nhân.

Về trực giác, xác suất gốc được cộng thêm một nhiễu nhỏ tỷ lệ với epsilon và tín hiệu z_c(x), sau đó được chuẩn hóa lại.

Ví dụ, xác suất positive ban đầu có thể là 0.90.

Sau khi watermark được áp dụng, xác suất này có thể được điều chỉnh nhẹ thành 0.85.

Sự thay đổi đủ nhỏ để không phá hành vi chính của mô hình, nhưng đủ có cấu trúc để phát hiện lại.

---

## Cảnh 3.5.5 - Detection by probing

### Mục tiêu

Cho thấy quá trình xác minh mô hình nghi ngờ: gửi query, trích xuất tín hiệu từ xác suất đầu ra, rồi tìm peak tại tần số bí mật f_w.

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
peak tăng vọt -> có dấu hiệu model extraction
```

### Text trên màn hình

```text
Detection by probing: tìm peak tại tần số f_w
periodogram của tín hiệu trích xuất
peak tại f_w
```

### Voice-over đề xuất

Khi muốn kiểm tra một mô hình nghi ngờ, chủ sở hữu gửi một tập query probing vào mô hình đó.

Từ xác suất đầu ra, hệ thống trích xuất lại một chuỗi tín hiệu.

Nếu mô hình nghi ngờ là bản sao được chưng cất từ victim model, tín hiệu watermark có thể vẫn còn trong xác suất.

Khi phân tích bằng periodogram, tín hiệu này tạo ra một peak tại đúng tần số bí mật f_w.

Peak tăng vọt tại f_w là bằng chứng kỹ thuật cho thấy mô hình có thể đã bị trích xuất.

---

## Cảnh 3.5.6 - Tổng kết cơ chế DRW

### Mục tiêu

Tóm tắt DRW bằng một pipeline đúng kỹ thuật và nhấn mạnh ranh giới với các phương pháp khác.

### Visual

Pipeline:

```text
K -> g(x) -> z_c(x) -> ŷ_c -> distill -> f_w peak
```

Card tổng kết:

```text
DRW phù hợp nhất với encoder/classification models như BERT.
Watermark nằm trong xác suất, không nằm trong từ đồng nghĩa.
Phát hiện bằng probing: tìm peak tại tần số bí mật f_w.
```

### Voice-over đề xuất

Tóm lại, DRW tạo watermark bằng một key bí mật.

Key này tạo ra hash, hash tạo ra tín hiệu tuần hoàn z_c(x), và tín hiệu đó được dùng để điều chỉnh xác suất đầu ra.

Nếu một student model học lại xác suất của teacher qua distillation, tín hiệu này có thể được truyền sang bản sao.

Sau đó, chủ sở hữu dùng probing để trích xuất tín hiệu và kiểm tra peak tại tần số bí mật f_w.

Đây là điểm cốt lõi của DRW: watermark nằm trong xác suất dự đoán, không nằm trong lựa chọn từ đồng nghĩa.
