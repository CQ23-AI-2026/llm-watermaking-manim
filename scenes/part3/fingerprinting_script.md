## Cảnh 3.10: Phòng thủ chống Fine-tuning — Instruction Fingerprinting
Bây giờ, hãy chuyển sang mối đe dọa thứ hai: fine-tuning.
Giả sử một mô hình đã bị sao chép.
Kẻ tấn công không chỉ dùng nó ngay lập tức.
Họ tiếp tục fine-tune mô hình trên dữ liệu mới.
Sau quá trình này, mô hình có thể thay đổi đáng kể ở bề ngoài.
Câu hỏi là:
Làm sao chủ sở hữu vẫn có thể nhận ra mô hình của mình?
Một hướng tiếp cận là **Instruction Fingerprinting**, hay dấu vân tay chỉ dẫn.
Thay vì nhúng watermark vào mọi đầu ra, phương pháp này tạo ra một tập các cặp đặc biệt:
Một bên là prompt kỳ dị hoặc hiếm gặp.
Bên còn lại là phản hồi đặc trưng mà chỉ mô hình đã được cấy dấu vân tay mới có xu hướng tạo ra.
Có thể hình dung như một mật khẩu bí mật.
Với người dùng bình thường, mô hình hoạt động như mọi mô hình khác.
Nhưng khi chủ sở hữu nhập một số câu lệnh kiểm tra đặc biệt, mô hình sẽ phản hồi theo một mẫu đã định.
Nếu một mô hình tình nghi cũng phản hồi đúng những mẫu này, đó là dấu hiệu cho thấy nó có liên hệ với mô hình gốc.

---

## Cảnh 3.11: Ba giai đoạn của Instruction Fingerprinting
Instruction Fingerprinting thường có thể được hiểu qua ba giai đoạn.
### Giai đoạn một: Fingerprint Injection
Đầu tiên là cấy dấu vân tay.
Chủ mô hình tạo ra một tập prompt đặc biệt và phản hồi đặc trưng.
Sau đó, mô hình được huấn luyện để ghi nhớ hoặc phản ứng ổn định với các cặp này.
Điểm quan trọng là tập fingerprint phải hiếm.
Nó không nên xuất hiện tự nhiên trong dữ liệu thông thường.
Nếu không, một mô hình khác cũng có thể tình cờ phản hồi giống vậy.
### Giai đoạn hai: User Fine-tuning
Sau đó, mô hình có thể được người dùng hoặc bên thứ ba fine-tune trên dữ liệu riêng.
Trong kịch bản hợp pháp, đây là điều bình thường.
Nhưng trong kịch bản xâm phạm IP, fine-tuning có thể được dùng để che giấu nguồn gốc mô hình.
Một fingerprint tốt cần đủ bền để không biến mất hoàn toàn sau fine-tuning.
### Giai đoạn ba: Ownership Verification
Cuối cùng là xác minh quyền sở hữu.
Chủ mô hình gửi các prompt fingerprint vào mô hình tình nghi.
Nếu mô hình phản hồi đúng với tỷ lệ cao, ta có thể tính một chỉ số gọi là **Fingerprint Success Rate**, hay FSR.
FSR càng cao, dấu hiệu mô hình tình nghi có liên quan đến mô hình gốc càng mạnh.
Tuy nhiên, FSR không nên được xem là bằng chứng duy nhất.
Nó là một tín hiệu kỹ thuật quan trọng, cần được kết hợp với các phân tích khác.

---

## Cảnh 3.12: SFT và Adapter trong Instruction Fingerprinting
Có nhiều cách để cấy fingerprint vào mô hình.
Một cách trực tiếp là dùng **Supervised Fine-tuning**, hay SFT.
Trong cách này, ta đưa các cặp prompt — response fingerprint vào quá trình fine-tuning của mô hình.
Ưu điểm là đơn giản và dễ hiểu.
Mô hình học trực tiếp cách phản hồi với các prompt đặc biệt.
Nhưng nhược điểm là nếu làm không cẩn thận, việc cấy fingerprint có thể ảnh hưởng đến năng lực tổng quát của mô hình.
Một hướng khác là dùng **Adapter**.
Adapter là các module nhỏ được gắn thêm vào mô hình.
Thay vì thay đổi toàn bộ trọng số, ta có thể huấn luyện các adapter để mang dấu vân tay.
Cách này có thể giúp giảm ảnh hưởng đến năng lực cốt lõi của mô hình.
Khi đánh giá các phương pháp này, ta thường quan tâm đến hai câu hỏi:
Một là fingerprint có còn tồn tại sau fine-tuning hay không?
Hai là mô hình có bị giảm hiệu năng trên các benchmark thông thường hay không?
Một phương pháp tốt phải đạt được cả hai:
Dấu vân tay đủ bền để xác minh quyền sở hữu.
Nhưng mô hình vẫn giữ được năng lực thực hiện nhiệm vụ chính.
