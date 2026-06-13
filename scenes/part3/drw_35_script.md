## Cảnh 3.5.0: Mở đầu DRW

Ta đi vào phương pháp đầu tiên: **DRW**, viết tắt của **Distillation-Resistant Watermarking**.

---

## Cảnh 3.5.1: DRW là probability signal watermark

DRW là một phương pháp watermark chống chưng cất mô hình, được thiết kế cho các mô hình dạng encoder hoặc classification như BERT.
Thay vì chèn dấu hiệu vào câu chữ, DRW can thiệp vào phân phối xác suất đầu ra.
Ví dụ, với một câu đầu vào, mô hình có thể trả xác suất cho các lớp positive, neutral và negative.
Watermark của DRW sẽ được nhúng vào các xác suất này, đặc biệt xoay quanh một lớp mục tiêu được chọn trong khóa bí mật.

---

## Cảnh 3.5.2: Cấu trúc secret key K

Trong DRW, watermark được quản lý bởi một khóa bí mật K.
Khóa này gồm lớp mục tiêu c*, tần số góc f_w, vector pha, vector chọn lọc và một ma trận token ngẫu nhiên.
Các thành phần này quyết định tín hiệu nào sẽ được tạo ra, lớp nào chịu tác động, và cách tín hiệu được rải vào xác suất.
Trong đó, vector chọn lọc giúp DRW không nhất thiết watermark mọi input, mà có thể chọn một phần mẫu theo tỉ lệ định trước. Chọn nhiều mẫu hơn làm tín hiệu dễ phát hiện hơn, nhưng cũng làm rủi ro ảnh hưởng chất lượng cao hơn.
Điểm quan trọng là DRW không dựa vào thay thế từ đồng nghĩa. Nó là watermark trên xác suất.

---

## Cảnh 3.5.3: Tạo tín hiệu tuần hoàn z_c(x)

Đầu tiên, hệ thống dùng một hàm hash g(x), kết hợp với khóa bí mật, để ánh xạ input thành một giá trị.
Từ giá trị đó, DRW tạo tín hiệu tuần hoàn z_c(x).
Với lớp mục tiêu, tín hiệu có dạng cos của f_w nhân với giá trị hash.
Với các lớp không phải mục tiêu, tín hiệu bị lệch pha thêm pi.
Nhờ vậy, target class và non-target class mang hai mẫu tín hiệu đối pha nhau.

---

## Cảnh 3.5.4: Áp dụng watermark vào xác suất

Sau khi có tín hiệu tuần hoàn, DRW tiêm tín hiệu này vào xác suất dự đoán của mô hình nạn nhân.
Với lớp mục tiêu c*, xác suất được điều chỉnh theo tín hiệu z_c(x) và tham số epsilon, theo đúng công thức piecewise đang hiện trên màn hình.
Với các lớp còn lại, phần điều chỉnh được phân bổ lại để toàn bộ vector xác suất vẫn hợp lệ sau khi chuẩn hóa.
Ví dụ, xác suất positive ban đầu có thể là 0.90. Sau watermark, nó có thể được điều chỉnh nhẹ thành 0.85.
Epsilon là điểm cân bằng quan trọng: nếu quá nhỏ, watermark khó phát hiện; nếu quá lớn, chất lượng dự đoán của mô hình có thể bị ảnh hưởng.

---

## Cảnh 3.5.5: Detection by probing

Khi muốn kiểm tra một mô hình nghi ngờ, chủ sở hữu gửi một tập query probing vào mô hình đó.
Từ xác suất đầu ra hoặc logits, hệ thống trích xuất lại một chuỗi tín hiệu.
Nếu mô hình nghi ngờ là bản sao được chưng cất từ victim model bằng soft labels, logits hoặc phân phối xác suất của teacher, nó không chỉ học nhãn cuối cùng. Nó có thể học luôn những dao động nhỏ mà DRW đã cài trong xác suất.
Khi phân tích bằng periodogram, tín hiệu này tạo ra một peak tại đúng tần số bí mật f_w.
Nếu peak tại f_w vượt một ngưỡng kiểm định, đó là bằng chứng kỹ thuật cho thấy mô hình có khả năng đã bị trích xuất.

---

## Cảnh 3.5.6: Tổng kết cơ chế DRW

Tóm lại, DRW tạo watermark bằng một key bí mật.
Key này tạo ra hash, hash tạo ra tín hiệu tuần hoàn z_c(x), và tín hiệu đó được dùng để điều chỉnh xác suất đầu ra.
Lý do watermark có thể truyền qua distillation là vì student thường học từ soft labels, logits hoặc toàn bộ phân phối xác suất của teacher. Khi học phân phối này, student không chỉ học class nào đứng đầu, mà còn có thể học lại mẫu tín hiệu nhỏ nằm trong các xác suất.
Sau đó, chủ sở hữu dùng probing để trích xuất tín hiệu và kiểm tra peak tại tần số bí mật f_w.
Giới hạn là nếu kẻ tấn công chỉ lấy hard label, dùng quá ít query, hoặc trộn dữ liệu distillation với nhiều nguồn khác, tín hiệu watermark có thể yếu đi.
Đây là điểm cốt lõi của DRW: watermark nằm trong xác suất dự đoán, có thể đi theo distillation, nhưng vẫn cần cân bằng giữa khả năng phát hiện và chất lượng mô hình.
