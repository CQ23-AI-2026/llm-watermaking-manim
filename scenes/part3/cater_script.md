## Cảnh 3.7.0: Mở đầu CATER

Tiếp theo là **CATER**, viết tắt của **Conditional Watermarking**.
Khác với DRW và GINSEW, CATER không nhúng sóng hình sin vào xác suất. Nó dùng watermark từ vựng có điều kiện.

---

## Cảnh 3.7.1: CATER khác DRW và GINSEW

DRW và GINSEW can thiệp vào phân phối xác suất bằng tín hiệu liên tục.
CATER đi theo hướng khác: nó thay đổi lựa chọn từ đồng nghĩa trên bề mặt văn bản.
Nhưng đây không phải thay thế ngẫu nhiên. CATER dùng các điều kiện ngôn ngữ để quyết định khi nào nên chọn từ watermark.
Vì vậy, ta có thể xem CATER như một lexical watermark có điều kiện cho text generation API.

---

## Cảnh 3.7.2: Tạo từ điển watermark bí mật

Đầu tiên, chủ sở hữu API chuẩn bị một từ điển watermark bí mật.
Từ điển này chứa các cặp từ gần nghĩa, ví dụ big thành large, smart thành clever, hoặc study thành research.
Khi API sinh văn bản, nó có thể chọn phiên bản watermark trong những vị trí phù hợp.
Attacker chỉ nhìn thấy văn bản đầu ra, nhưng không biết cặp từ nào là rule bí mật.

---

## Cảnh 3.7.3: Conditional synonym substitution

Điểm quan trọng của CATER là điều kiện ngữ cảnh.
Hệ thống không thay mọi từ giống nhau trong mọi câu. Nó kiểm tra linguistic features, ví dụ part-of-speech lân cận hoặc dependency relation.
Nếu điều kiện khớp, từ gốc có thể được thay bằng từ đồng nghĩa watermark.
Nếu điều kiện không khớp, hệ thống giữ lựa chọn tự nhiên hơn để tránh phá ngữ nghĩa và độ trôi chảy của câu.
Trên sơ đồ, hai nhánh này được tách riêng: nhánh khớp điều kiện đi lên rule watermark, còn nhánh không khớp đi xuống lựa chọn giữ nguyên.

---

## Cảnh 3.7.4: Tối ưu hóa rule thay thế

Vấn đề là thay từ đồng nghĩa quá nhiều có thể làm văn bản kém tự nhiên.
Vì vậy, CATER chọn các rule thay thế bằng một bài toán tối ưu.
Mục tiêu là giảm distortion của phân phối từ tổng thể, nhưng vẫn tăng sức mạnh của watermark trong các lựa chọn có điều kiện.
Trên slide, công thức tối ưu dùng hai ma trận W và X. Thành phần đầu giữ cho phân phối sau thay thế không lệch quá xa phân phối gốc, còn thành phần có alpha khuyến khích thay đổi lựa chọn từ để watermark đủ mạnh.
Các ràng buộc one-hot trên X đảm bảo mỗi điều kiện chỉ chọn một rule hợp lệ.
Tham số alpha điều khiển trade-off: ưu tiên giữ nghĩa nhiều hơn, hay ưu tiên watermark mạnh hơn.

---

## Cảnh 3.7.5: Detection bằng hit ratio

Khi cần kiểm tra một model nghi ngờ, chủ sở hữu gửi probing queries vào model đó.
Từ văn bản sinh ra, hệ thống đếm tần suất các lựa chọn từ watermark xuất hiện theo đúng điều kiện bí mật.
Nếu hit ratio vượt ngưỡng thống kê, đó là bằng chứng cho thấy model có thể đã học từ API có CATER.
Ngược lại, nếu hit ratio không vượt ngưỡng, ta nói rằng chưa đủ bằng chứng.

---

## Cảnh 3.7.6: Chất lượng và giới hạn

Điểm mạnh của CATER là chất lượng văn bản.
Vì nó dùng thay thế từ đồng nghĩa có điều kiện và tối ưu rule, các metric như BLEU hoặc ROUGE-L có thể gần với model gốc.
Nhưng điểm yếu là khả năng phát hiện thường yếu hơn các watermark xác suất như GINSEW.
Vì watermark nằm trên bề mặt từ vựng, các tấn công thay thế từ đồng nghĩa hoặc paraphrase có thể làm tín hiệu yếu đi.

---

## Cảnh 3.7.7: Tổng kết CATER

Tóm lại, CATER bắt đầu từ một từ điển bí mật các cặp từ đồng nghĩa.
Sau đó, nó dùng linguistic features để kích hoạt rule thay thế trong những ngữ cảnh phù hợp.
Các rule được tối ưu để cân bằng giữa giữ chất lượng văn bản và tạo tín hiệu watermark đủ mạnh.
Khi kiểm tra model nghi ngờ, chủ sở hữu probing và đo hit ratio của các lựa chọn từ watermark.
CATER phù hợp khi API chỉ trả văn bản, không trả logits hay probability vector. Nhưng vì là surface-level watermark, nó thường kém bền hơn GINSEW trước các tấn công thay thế từ.