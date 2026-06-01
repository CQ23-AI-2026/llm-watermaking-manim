# Script lồng tiếng: Part 1

## Scene 1.1: Lịch sử Watermark

Watermark không phải khái niệm mới. Từ hàng trăm năm trước, người ta đã dùng hình chìm trên giấy bạc để chống làm giả. Trên các con tem của Anh, bạn có thể thấy watermark hình vương miện CA. Trong thế giới số, invisible watermark được nhúng vào ảnh để bảo vệ bản quyền.

Nhưng watermark cho AI text thì khác. Và sự khác biệt cốt lõi nằm ở **cách tiếp cận**.

---

## Scene 1.2: Cũ vs. Mới

Watermark thập niên 1990 hoạt động theo kiểu **hậu xử lý** tức là tạo xong nội dung rồi mới gắn dấu vào. Còn watermark cho GenAI thì **can thiệp trực tiếp** vào quá trình sinh văn bản. Đây là một cách tiếp cận chủ động hơn rất nhiều.

---

## Scene 1.3: Hai thành phần cốt lõi (Watermark() và Detect())

Mọi hệ thống Watermark đều có hai thành phần. **Thứ nhất** là hàm Watermark nhận vào model gốc, trả ra model mới đã được gắn thủy vân cùng một chìa khóa phát hiện. **Thứ hai** là hàm Detect nhận chìa khóa và đoạn văn bản nghi vấn, rồi trả lời: văn bản này có phải do AI tạo ra hay không.

---

## Scene 1.4: Bốn tính chất lý tưởng

Một Watermark lý tưởng cần đạt 4 tính chất: **Quality** không làm giảm chất lượng văn bản. **Detection Accuracy** phát hiện chính xác. **Robustness** bền vững trước tấn công. Và **Security** không ai có thể giả mạo watermark nếu không có chìa khóa.
