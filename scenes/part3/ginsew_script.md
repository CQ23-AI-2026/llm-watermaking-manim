## Cảnh 3.6.0: Mở đầu GINSEW

Tiếp theo là **GINSEW**, viết tắt của **Generative Invisible Sequence Watermarking**.
Nếu DRW phù hợp hơn với mô hình phân loại, thì GINSEW được thiết kế cho mô hình ngôn ngữ sinh văn bản, như các decoder kiểu GPT.

---

## Cảnh 3.6.1: GINSEW cho generative LLM

Với mô hình sinh văn bản, watermark không được đặt vào một nhãn phân loại cuối cùng.
Thay vào đó, tại mỗi bước sinh token, GINSEW can thiệp nhẹ vào phân phối xác suất của token kế tiếp.
Mô hình vẫn sinh văn bản như bình thường, nhưng chuỗi token đầu ra mang một mẫu thống kê bí mật.

---

## Cảnh 3.6.2: Hash và phân nhóm từ vựng

Đầu tiên, GINSEW dùng một hàm hash g để ánh xạ token trong vocabulary vào một giá trị trong khoảng từ 0 đến 1.
Từ đó, vocabulary được chia thành các nhóm, ví dụ Group G1 và Group G2.
Ý tưởng quan trọng là watermark không bám vào một token đơn lẻ. Nó bám vào xác suất của cả nhóm token.
Nhờ vậy, nếu attacker thay một từ bằng từ gần nghĩa, tín hiệu thống kê vẫn có khả năng còn lại ở cấp nhóm.

---

## Cảnh 3.6.3: Tạo tín hiệu tuần hoàn bí mật

Sau khi có nhóm từ vựng, GINSEW tạo tín hiệu hình sin bằng tần số bí mật f_w.
Với Group G1, tín hiệu là z_1(x) bằng cos của f_w nhân với giá trị hash.
Với Group G2, tín hiệu bị lệch pha thêm pi, nên hai nhóm mang hai mẫu đối pha nhau.
Tần số f_w nằm trong khóa bí mật. Khi kiểm tra model nghi ngờ, chủ sở hữu sẽ tìm lại đúng tần số này.

---

## Cảnh 3.6.4: Can thiệp xác suất cấp độ nhóm

Đây là điểm khác biệt lớn của GINSEW so với DRW.
GINSEW không cộng tín hiệu trực tiếp vào từng token riêng lẻ ngay từ đầu. Nó tính tổng xác suất của cả nhóm token trước.
Ví dụ, với Group G1, hệ thống tính Q_G1 bằng tổng xác suất của mọi token thuộc nhóm G1.
Sau đó, tín hiệu watermark và tham số epsilon được dùng để tạo tổng xác suất mới cho nhóm này.
Cuối cùng, xác suất của từng token bên trong nhóm được scale lại theo tỉ lệ giữa tổng mới và tổng cũ.
Epsilon vẫn là điểm cân bằng: quá nhỏ thì khó detect, quá lớn thì có thể làm giảm chất lượng văn bản.

---

## Cảnh 3.6.5: Sinh văn bản từ phân phối mới

Sau khi xác suất được điều chỉnh, mô hình sinh token từ phân phối mới.
Người đọc vẫn thấy một câu bình thường, nhưng nếu quan sát đủ nhiều token, tỉ lệ xuất hiện giữa các nhóm sẽ mang mẫu hình sin bí mật.
Đây là lý do GINSEW chống thay thế từ đồng nghĩa tốt hơn các watermark bám trực tiếp vào từ cụ thể.

---

## Cảnh 3.6.6: Detection bằng Lomb-Scargle periodogram

Khi muốn kiểm tra một model nghi ngờ, chủ sở hữu gửi probing queries và thu thập văn bản đầu ra.
Từ văn bản này, hệ thống chuyển chuỗi token thành tín hiệu nhóm, ví dụ token thuộc G1 hay G2.
Sau đó, tín hiệu được đưa vào Lomb-Scargle periodogram để phân tích phổ.
Nếu có một peak rõ tại đúng tần số bí mật f_w và vượt ngưỡng kiểm định, đó là bằng chứng kỹ thuật cho thấy model có khả năng là bản sao.
Ngược lại, nếu không có peak rõ, ta nói rằng chưa đủ bằng chứng, chứ không kết luận tuyệt đối rằng model chắc chắn không sao chép.

---

## Cảnh 3.6.7: Tổng kết cơ chế GINSEW

Tóm lại, GINSEW bắt đầu bằng cách hash token và chia vocabulary thành các nhóm.
Sau đó, hệ thống tạo tín hiệu hình sin bí mật cho từng nhóm, điều chỉnh tổng xác suất của nhóm, rồi để mô hình sinh văn bản từ phân phối mới.
Điểm mạnh của GINSEW là watermark nằm ở cấp phân phối và cấp nhóm token, nên không phụ thuộc vào một từ cụ thể.
Vì vậy, nó phù hợp hơn cho generative LLM và bền hơn trước các tấn công thay thế từ đồng nghĩa.
Khi cần xác minh, chủ sở hữu probing model nghi ngờ và tìm peak tại tần số bí mật f_w bằng Lomb-Scargle periodogram.
